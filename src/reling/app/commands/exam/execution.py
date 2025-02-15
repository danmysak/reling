from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from reling.app.exceptions import AlgorithmException
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.asr import ASRClient
from reling.config import MAX_SCORE
from reling.db.enums import ContentCategory
from reling.db.models import Dialogue, DialogueExam, Language, Text, TextExam
from reling.gpt import GPTClient
from reling.helpers.typer import typer_raise
from reling.helpers.voices import pick_voices
from reling.scanner import ScannerManager
from reling.tts import TTSClient
from reling.types import Promise
from reling.utils.timetracker import TimeTracker
from .explanation import build_dialogue_explainer, build_text_explainer
from .input import collect_dialogue_translations, collect_text_translations
from .presentation import present_dialogue_results, present_text_results
from .scoring import score_translations
from .storage import save_dialogue_exam, save_text_exam

__all__ = [
    'perform_dialogue_exam',
    'perform_text_exam',
]


def collect_perfect(content: Text | Dialogue, target_language: Language) -> list[set[str]]:
    """
    Collect the suggestions and correct answers from previous exams in the same target language, indexed by sentence.
    """
    suggestions = [set() for _ in range(content.size)]
    for exam in cast(list[TextExam] | list[DialogueExam], content.exams):
        if exam.target_language == target_language:
            for result in exam.results:
                if result.suggested_answer:
                    suggestions[result.index].add(result.suggested_answer)
                if result.score == MAX_SCORE:
                    suggestions[result.index].add(result.answer)
    return suggestions


def perform_text_exam(
        gpt: Promise[GPTClient],
        text: Text,
        skipped_indices: set[int],
        source_language: Language,
        target_language: Language,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
        asr: ASRClient | None,
        scanner_manager: ScannerManager,
        hide_prompts: bool,
        offline_scoring: bool,
) -> None:
    """
    Translate the text as needed, collect user translations, score them, save and present the results to the user,
    optionally reading the source and/or target language out loud.
    """
    with TemporaryDirectory() as file_storage:
        source_voice, target_voice = pick_voices(None, None)
        voice_source_tts = source_tts.with_voice(source_voice) if source_tts else None
        voice_target_tts = target_tts.with_voice(target_voice) if target_tts else None

        sentences = get_text_sentences(text, source_language, gpt)
        original_translations = get_text_sentences(text, target_language, gpt)

        with scanner_manager.get_scanner() as scanner:
            tracker = TimeTracker()
            translated = list(collect_text_translations(
                sentences=sentences,
                original_translations=original_translations,
                skipped_indices=skipped_indices,
                target_language=target_language,
                source_tts=voice_source_tts,
                asr=asr,
                scanner=scanner,
                hide_prompts=hide_prompts,
                storage=Path(file_storage),
                on_pause=tracker.pause,
                on_resume=tracker.resume,
            ))
            tracker.stop()

        try:
            results = list(score_translations(
                category=ContentCategory.TEXT,
                gpt=gpt,
                items=translated,
                original_translations=original_translations,
                previous_perfect=collect_perfect(text, target_language),
                source_language=source_language,
                target_language=target_language,
                offline=offline_scoring,
            ))
        except AlgorithmException as e:
            typer_raise(e.msg)

        text_exam = save_text_exam(
            text=text,
            source_language=source_language,
            target_language=target_language,
            read_source=source_tts is not None,
            read_target=target_tts is not None,
            listened=asr is not None,
            scanned=scanner is not None,
            started_at=tracker.started_at,
            finished_at=tracker.finished_at,
            total_pause_time=tracker.total_pause_time,
            sentences=translated,
            results=results,
        )

        present_text_results(
            sentences=translated,
            original_translations=original_translations,
            exam=text_exam,
            source_tts=voice_source_tts,
            target_tts=voice_target_tts,
            explain=build_text_explainer(
                gpt=gpt,
                sentences=translated,
                original_translations=original_translations,
                results=results,
                source_language=source_language,
                target_language=target_language,
            ),
        )


def perform_dialogue_exam(
        gpt: Promise[GPTClient],
        dialogue: Dialogue,
        skipped_indices: set[int],
        source_language: Language,
        target_language: Language,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
        asr: ASRClient | None,
        scanner_manager: ScannerManager,
        hide_prompts: bool,
        offline_scoring: bool,
) -> None:
    """
    Translate the dialogue as needed, collect user translations, score them, save and present the results to the user,
    optionally reading the source and/or target language out loud.
    """
    with TemporaryDirectory() as file_storage:
        speaker_voice, user_voice = pick_voices(dialogue.speaker_gender, dialogue.user_gender)
        source_user_tts = source_tts.with_voice(user_voice) if source_tts else None
        target_user_tts = target_tts.with_voice(user_voice) if target_tts else None
        target_speaker_tts = target_tts.with_voice(speaker_voice) if target_tts else None

        exchanges = get_dialogue_exchanges(dialogue, source_language, gpt)
        original_translations = get_dialogue_exchanges(dialogue, target_language, gpt)

        with scanner_manager.get_scanner() as scanner:
            tracker = TimeTracker()
            translated = list(collect_dialogue_translations(
                exchanges=exchanges,
                original_translations=original_translations,
                skipped_indices=skipped_indices,
                target_language=target_language,
                source_user_tts=source_user_tts,
                target_speaker_tts=target_speaker_tts,
                asr=asr,
                scanner=scanner,
                hide_prompts=hide_prompts,
                storage=Path(file_storage),
                on_pause=tracker.pause,
                on_resume=tracker.resume,
            ))
            tracker.stop()

        try:
            results = list(score_translations(
                category=ContentCategory.DIALOGUE,
                gpt=gpt,
                items=translated,
                original_translations=original_translations,
                previous_perfect=collect_perfect(dialogue, target_language),
                source_language=source_language,
                target_language=target_language,
                offline=offline_scoring,
            ))
        except AlgorithmException as e:
            typer_raise(e.msg)

        dialogue_exam = save_dialogue_exam(
            dialogue=dialogue,
            source_language=source_language,
            target_language=target_language,
            read_source=source_tts is not None,
            read_target=target_tts is not None,
            listened=asr is not None,
            scanned=scanner is not None,
            started_at=tracker.started_at,
            finished_at=tracker.finished_at,
            total_pause_time=tracker.total_pause_time,
            exchanges=translated,
            results=results,
        )

        present_dialogue_results(
            exchanges=translated,
            original_translations=original_translations,
            exam=dialogue_exam,
            source_user_tts=source_user_tts,
            target_speaker_tts=target_speaker_tts,
            target_user_tts=target_user_tts,
            explain=build_dialogue_explainer(
                gpt=gpt,
                exchanges=translated,
                original_translations=original_translations,
                results=results,
                source_language=source_language,
                target_language=target_language,
            ),
        )

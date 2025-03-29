from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from reling.app.exceptions import AlgorithmException
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.asr import ASRClient
from reling.config import MAX_SCORE
from reling.db.enums import ContentCategory, Gender
from reling.db.models import Dialogue, DialogueExam, Language, Text, TextExam
from reling.gpt import GPTClient
from reling.helpers.typer import typer_raise
from reling.helpers.voices import pick_voices
from reling.scanner import ScannerManager
from reling.tts import TTSClient, TTSVoiceClient
from reling.types import Promise
from reling.utils.timetracker import TimeTracker
from .explanation import build_explainer
from .input import collect_translations
from .presentation import present_results
from .scoring import score_translations
from .storage import save_exam

__all__ = [
    'perform_exam',
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


def get_voices(
        content: Text | Dialogue,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
) -> tuple[TTSVoiceClient | None, TTSVoiceClient | None, TTSVoiceClient | None]:
    """
    Pick TTS voices based on the content type (text or dialogue):
    - For a Text, return (source_voice, target_voice, None).
    - For a Dialogue, return (source_user_voice, target_user_voice, target_speaker_voice).
    """
    if isinstance(content, Text):
        source_voice, target_voice = pick_voices(None, None)
        return (
            source_tts.with_voice(source_voice) if source_tts else None,
            target_tts.with_voice(target_voice) if target_tts else None,
            None,
        )
    else:
        speaker_voice, user_voice = pick_voices(
            cast(Gender, content.speaker_gender),
            cast(Gender, content.user_gender),
        )
        return (
            source_tts.with_voice(user_voice) if source_tts else None,
            target_tts.with_voice(user_voice) if target_tts else None,
            target_tts.with_voice(speaker_voice) if target_tts else None,
        )


def perform_exam(
        gpt: Promise[GPTClient],
        content: Text | Dialogue,
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
    Collect user translations of the text or dialogue, score them, save and present the results to the user,
    optionally reading the source and/or target language out loud.
    """
    with TemporaryDirectory() as file_storage:
        is_text = isinstance(content, Text)
        category = ContentCategory.TEXT if is_text else ContentCategory.DIALOGUE

        voice_source_tts, voice_target_tts, voice_target_speaker_tts = get_voices(content, source_tts, target_tts)
        items, original_translations = (
            (get_text_sentences if is_text else get_dialogue_exchanges)(content, language, gpt)
            for language in (source_language, target_language)
        )

        with scanner_manager.get_scanner() as scanner:
            tracker = TimeTracker()
            translated = list(collect_translations(
                category=category,
                items=items,
                original_translations=original_translations,
                skipped_indices=skipped_indices,
                target_language=target_language,
                source_tts=voice_source_tts,
                target_speaker_tts=voice_target_speaker_tts,
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
                category=category,
                gpt=gpt,
                items=translated,
                original_translations=original_translations,
                previous_perfect=collect_perfect(content, target_language),
                source_language=source_language,
                target_language=target_language,
                offline=offline_scoring,
            ))
        except AlgorithmException as e:
            typer_raise(e.msg)

        exam = save_exam(
            content=content,
            source_language=source_language,
            target_language=target_language,
            read_source=source_tts is not None,
            read_target=target_tts is not None,
            listened=asr is not None,
            scanned=scanner is not None,
            started_at=tracker.started_at,
            finished_at=tracker.finished_at,
            total_pause_time=tracker.total_pause_time,
            items=translated,
            results=results,
        )

        present_results(
            items=translated,
            original_translations=original_translations,
            exam=exam,
            source_tts=voice_source_tts,
            target_tts=voice_target_tts,
            target_speaker_tts=voice_target_speaker_tts,
            explain=build_explainer(
                category=category,
                gpt=gpt,
                items=translated,
                original_translations=original_translations,
                results=results,
                source_language=source_language,
                target_language=target_language,
            ),
        )

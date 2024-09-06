from pathlib import Path
from tempfile import TemporaryDirectory

from tqdm import tqdm

from reling.app.app import app
from reling.app.exceptions import AlgorithmException
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.app.types import (
    API_KEY,
    ASR_MODEL,
    CONTENT_ARG,
    LANGUAGE_OPT,
    LANGUAGE_OPT_FROM,
    LISTEN_OPT,
    MODEL,
    READ_LANGUAGE_OPT,
    TTS_MODEL,
)
from reling.asr import ASRClient
from reling.db.models import Dialogue, Language, Text
from reling.gpt import GPTClient
from reling.helpers.voices import pick_voices
from reling.tts import TTSClient
from reling.utils.time import now
from reling.utils.typer import typer_raise
from .input import collect_dialogue_translations, collect_text_translations
from .presentation import present_dialogue_results, present_text_results
from .scoring import score_dialogue_translations, score_text_translations
from .storage import save_dialogue_exam, save_text_exam
from .types import ExchangeWithTranslation, SentenceWithTranslation

__all__ = [
    'exam',
]


@app.command()
def exam(
        api_key: API_KEY,
        model: MODEL,
        tts_model: TTS_MODEL,
        asr_model: ASR_MODEL,
        content: CONTENT_ARG,
        from_: LANGUAGE_OPT_FROM = None,
        to: LANGUAGE_OPT = None,
        read: READ_LANGUAGE_OPT = None,
        listen: LISTEN_OPT = False,
) -> None:
    """
    Test the user's ability to translate content from one language to another.
    If only one language is specified, the content's original language is assumed for the unspecified direction.
    """
    if from_ is None and to is None:
        typer_raise('You must specify at least one language.')
    from_ = from_ or content.language
    to = to or content.language
    if from_ == to:
        typer_raise('The source and target languages are the same.')

    read = read or []
    for language in read:
        if language not in [from_, to]:
            typer_raise(f'Cannot read in {language.name} as it is not the source or target language.')

    (perform_text_exam if isinstance(content, Text) else perform_dialogue_exam)(
        GPTClient(api_key=api_key, model=model),
        content,
        from_,
        to,
        source_tts=TTSClient(api_key=api_key, model=tts_model.get()) if from_ in read else None,
        target_tts=TTSClient(api_key=api_key, model=tts_model.get()) if to in read else None,
        asr=ASRClient(api_key=api_key, model=asr_model.get()) if listen else None,
    )


def perform_text_exam(
        gpt: GPTClient,
        text: Text,
        source_language: Language,
        target_language: Language,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
        asr: ASRClient | None,
) -> None:
    """
    Translate the text as needed, collect user translations, score them, save and present the results to the user,
    optionally reading the source and/or target language out loud.
    """
    with TemporaryDirectory() as file_storage:
        source_voice, target_voice = pick_voices(None, None)
        voice_source_tts = source_tts.with_voice(source_voice) if source_tts else None
        voice_target_tts = target_tts.with_voice(target_voice) if target_tts else None

        sentences = get_text_sentences(gpt, text, source_language)
        original_translations = get_text_sentences(gpt, text, target_language)

        started_at = now()
        translated = list(collect_text_translations(
            sentences=sentences,
            target_language=target_language,
            source_tts=voice_source_tts,
            asr=asr,
            storage=Path(file_storage),
        ))
        finished_at = now()

        try:
            results = list(tqdm(
                score_text_translations(
                    gpt=gpt,
                    sentences=translated,
                    source_language=source_language,
                    target_language=target_language,
                ),
                desc='Scoring translations',
                total=len(translated),
            ))
        except AlgorithmException as e:
            typer_raise(e.msg)

        save_text_exam(
            text=text,
            source_language=source_language,
            target_language=target_language,
            started_at=started_at,
            finished_at=finished_at,
            sentences=translated,
            results=results,
        )

        present_text_results(
            sentences=translated,
            original_translations=original_translations,
            results=results,
            duration=finished_at - started_at,
            source_tts=voice_source_tts,
            target_tts=voice_target_tts,
        )


def perform_dialogue_exam(
        gpt: GPTClient,
        dialogue: Dialogue,
        source_language: Language,
        target_language: Language,
        source_tts: TTSClient | None,
        target_tts: TTSClient | None,
        asr: ASRClient | None,
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

        exchanges = get_dialogue_exchanges(gpt, dialogue, source_language)
        original_translations = get_dialogue_exchanges(gpt, dialogue, target_language)

        started_at = now()
        translated = list(collect_dialogue_translations(
            exchanges=exchanges,
            original_translations=original_translations,
            target_language=target_language,
            source_user_tts=source_user_tts,
            target_speaker_tts=target_speaker_tts,
            asr=asr,
            storage=Path(file_storage),
        ))
        finished_at = now()

        try:
            results = list(tqdm(
                score_dialogue_translations(
                    gpt=gpt,
                    exchanges=translated,
                    original_translations=original_translations,
                    source_language=source_language,
                    target_language=target_language,
                ),
                desc='Scoring translations',
                total=len(translated),
            ))
        except AlgorithmException as e:
            typer_raise(e.msg)

        save_dialogue_exam(
            dialogue=dialogue,
            source_language=source_language,
            target_language=target_language,
            started_at=started_at,
            finished_at=finished_at,
            exchanges=translated,
            results=results,
        )

        present_dialogue_results(
            exchanges=translated,
            original_translations=original_translations,
            results=results,
            duration=finished_at - started_at,
            source_user_tts=source_user_tts,
            target_speaker_tts=target_speaker_tts,
            target_user_tts=target_user_tts,
        )

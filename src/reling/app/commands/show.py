from reling.app.app import app
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.app.types import (
    API_KEY,
    CONTENT_ARG,
    LANGUAGE_OPT_ARG,
    MODEL,
    READ_FAST_OPT,
    READ_OPT,
    READ_SLOWLY_OPT,
    TTS_MODEL,
)
from reling.db.models import Dialogue, Language, Text
from reling.gpt import GPTClient
from reling.helpers.output import output_text
from reling.helpers.voices import pick_voice, pick_voices
from reling.tts import InvalidTTSFlagCombination, TTSClient, TTSSpeed
from reling.utils.typer import typer_raise

__all__ = [
    'show',
]

SPEAKER_PREFIX = '> '
USER_PREFIX = '< '


@app.command()
def show(
        api_key: API_KEY,
        model: MODEL,
        tts_model: TTS_MODEL,
        content: CONTENT_ARG,
        language: LANGUAGE_OPT_ARG = None,
        read: READ_OPT = False,
        read_slowly: READ_SLOWLY_OPT = False,
        read_fast: READ_FAST_OPT = False,
) -> None:
    """Display a text or dialogue, or its translation if a language is specified."""
    try:
        tts_speed = TTSSpeed.from_flags(read_slowly, read, read_fast)
    except InvalidTTSFlagCombination:
        typer_raise('Only one reading speed can be specified at a time.')
    (show_text if isinstance(content, Text) else show_dialogue)(
        GPTClient(api_key=api_key, model=model),
        content,
        language or content.language,
        TTSClient(api_key=api_key, model=tts_model.get(), speed=tts_speed) if tts_speed else None,
    )


def show_text(gpt: GPTClient, text: Text, language: Language, tts: TTSClient | None) -> None:
    """Display the text in the specified language, optionally reading it out loud."""
    voice = pick_voice()
    for sentence in get_text_sentences(gpt, text, language):
        output_text(sentence, tts, voice)


def show_dialogue(gpt: GPTClient, dialogue: Dialogue, language: Language, tts: TTSClient | None) -> None:
    """Display the dialogue in the specified language, optionally reading it out loud."""
    exchanges = get_dialogue_exchanges(gpt, dialogue, language)
    speaker_voice, user_voice = pick_voices(dialogue.speaker_gender, dialogue.user_gender)
    for exchange in exchanges:
        output_text(exchange.speaker, tts, speaker_voice, print_prefix=SPEAKER_PREFIX)
        output_text(exchange.user, tts, user_voice, print_prefix=USER_PREFIX)

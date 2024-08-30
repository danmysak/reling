from reling.app.app import app
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.app.types import (
    API_KEY,
    CONTENT_ARG,
    LANGUAGE_OPT_ARG,
    MODEL,
    READ_OPT,
    TTS_MODEL,
)
from reling.db.models import Dialogue, Language, Text
from reling.gpt import GPTClient
from reling.helpers.output import output, SentenceData
from reling.helpers.voices import pick_voice, pick_voices
from reling.tts import TTSClient

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
) -> None:
    """Display a text or dialogue, or its translation if a language is specified."""
    (show_text if isinstance(content, Text) else show_dialogue)(
        GPTClient(api_key=api_key, model=model),
        content,
        language or content.language,
        TTSClient(api_key=api_key, model=tts_model.get()) if read else None,
    )


def show_text(gpt: GPTClient, text: Text, language: Language, tts: TTSClient | None) -> None:
    """Display the text in the specified language, optionally reading it out loud."""
    voice_tts = tts.with_voice(pick_voice()) if tts else None
    for sentence in get_text_sentences(gpt, text, language):
        output(SentenceData.from_tts(sentence, voice_tts))


def show_dialogue(gpt: GPTClient, dialogue: Dialogue, language: Language, tts: TTSClient | None) -> None:
    """Display the dialogue in the specified language, optionally reading it out loud."""
    exchanges = get_dialogue_exchanges(gpt, dialogue, language)
    speaker_tts, user_tts = map(tts.with_voice, pick_voices(
        dialogue.speaker_gender,
        dialogue.user_gender,
    )) if tts else (None, None)
    for exchange in exchanges:
        output(SentenceData.from_tts(exchange.speaker, speaker_tts, print_prefix=SPEAKER_PREFIX))
        output(SentenceData.from_tts(exchange.user, user_tts, print_prefix=USER_PREFIX))

from random import choice

from reling.app.app import app
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_OPT_ARG, MODEL, READ_OPT, TTS_MODEL
from reling.db.models import Dialogue, Language, Text
from reling.gpt import GPTClient
from reling.tts import TTSClient, Voice

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
    voice = choice(list(Voice))
    for sentence in get_text_sentences(gpt, text, language):
        print(sentence)
        if tts:
            tts.read(sentence, voice)  # type: ignore


def show_dialogue(gpt: GPTClient, dialogue: Dialogue, language: Language, tts: TTSClient | None) -> None:
    exchanges = get_dialogue_exchanges(gpt, dialogue, language)
    speaker_voice, user_voice = None, None
    if tts:
        speaker_voice = choice(list(Voice.get_voices(dialogue.speaker_gender)))
        user_voice = choice(sorted(set(Voice.get_voices(dialogue.user_gender)) - {speaker_voice}))
    for exchange in exchanges:
        print(SPEAKER_PREFIX + exchange.speaker)
        if tts:
            tts.read(exchange.speaker, speaker_voice)
        print(USER_PREFIX + exchange.user)
        if tts:
            tts.read(exchange.user, user_voice)

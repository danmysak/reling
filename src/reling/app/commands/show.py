from reling.app.app import app
from reling.app.translation import get_dialog_exchanges, get_text_sentences
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_OPT_ARG, MODEL
from reling.db.models import Dialog, Language, Text
from reling.gpt import GPTClient

__all__ = [
    'show',
]

SPEAKER_PREFIX = '> '
USER_PREFIX = '< '


@app.command()
def show(api_key: API_KEY, model: MODEL, content: CONTENT_ARG, language: LANGUAGE_OPT_ARG = None) -> None:
    """Display a text or dialog, or its translation if a language is specified."""
    gpt = GPTClient(api_key=api_key, model=model)
    (show_text if isinstance(content, Text) else show_dialog)(gpt, content, language or content.language)


def show_text(gpt: GPTClient, text: Text, language: Language) -> None:
    for sentence in get_text_sentences(gpt, text, language):
        print(sentence)


def show_dialog(gpt: GPTClient, dialog: Dialog, language: Language) -> None:
    exchanges = get_dialog_exchanges(gpt, dialog, language)
    for exchange in exchanges:
        print(SPEAKER_PREFIX + exchange.speaker)
        print(USER_PREFIX + exchange.user)

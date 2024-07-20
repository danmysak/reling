from ...gpt import GPTClient
from ..app import app
from ..types import API_KEY, CONTENT_ARG, LANGUAGE_ARG, MODEL

__all__ = [
    'translate',
]


@app.command()
def translate(api_key: API_KEY, model: MODEL, content: CONTENT_ARG, language: LANGUAGE_ARG) -> None:
    """Translate a text or dialog into another language."""
    gpt = GPTClient(api_key=api_key, model=model)
    pass

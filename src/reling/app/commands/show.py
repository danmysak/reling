from ..app import app
from ..types import CONTENT_ARG, LANGUAGE_OPT_ARG

__all__ = [
    'show',
]


@app.command()
def show(content: CONTENT_ARG, language: LANGUAGE_OPT_ARG = None) -> None:
    """Display a text or dialog, or its translation if a language is specified."""
    pass

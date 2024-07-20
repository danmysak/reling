from ..app import app
from ..types import CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM

__all__ = [
    'stats',
]


@app.command()
def stats(content: CONTENT_ARG, from_: LANGUAGE_OPT_FROM = None, to: LANGUAGE_OPT = None) -> None:
    """Display statistics about the translation exams, optionally filtered by source or target language."""
    pass

from ...db.enums import Level
from ...gpt import GPTClient
from ..app import app
from ..types import (
    API_KEY,
    CONTENT_CATEGORY_ARG,
    LANGUAGE_ARG,
    LEVEL_OPT,
    MODEL,
    STYLE_OPT,
    TOPIC_OPT,
)

__all__ = [
    'create',
]


@app.command()
def create(
        api_key: API_KEY,
        model: MODEL,
        category: CONTENT_CATEGORY_ARG,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.ADVANCED,
        topic: TOPIC_OPT = None,
        style: STYLE_OPT = None,
) -> None:
    """Create a text or a dialog and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    pass

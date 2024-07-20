import typer

from ...db.enums import Level
from ...gpt import GPTClient
from ..app import app
from ..types import API_KEY, LANGUAGE_ARG, LEVEL_OPT, MODEL, SPEAKER_OPT, STYLE_OPT, TOPIC_OPT

__all__ = [
    'create',
]

create = typer.Typer()
app.add_typer(
    create,
    name='create',
    help='Create a new text or dialog.',
)


@create.command()
def text(
        api_key: API_KEY,
        model: MODEL,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.ADVANCED,
        topic: TOPIC_OPT = None,
        style: STYLE_OPT = None,
) -> None:
    """Create a text and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    pass


@create.command()
def dialog(
        api_key: API_KEY,
        model: MODEL,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.ADVANCED,
        speaker: SPEAKER_OPT = None,
        topic: TOPIC_OPT = None,
) -> None:
    """Create a dialog and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    pass

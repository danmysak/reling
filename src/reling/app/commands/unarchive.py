from reling.app.app import app
from reling.app.types import CONTENT_ARG
from reling.db import single_session
from reling.utils.typer import typer_raise

__all__ = [
    'unarchive',
]


@app.command()
def unarchive(content: CONTENT_ARG) -> None:
    """Unarchive a text or dialogue."""
    if content.archived_at is None:
        typer_raise('The content is not archived.')

    with single_session() as session:
        content.archived_at = None
        session.commit()

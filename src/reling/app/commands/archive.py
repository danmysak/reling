from reling.app.app import app
from reling.app.types import CONTENT_ARG
from reling.db import single_session
from reling.utils.time import now
from reling.utils.typer import typer_raise

__all__ = [
    'archive',
]


@app.command()
def archive(content: CONTENT_ARG) -> None:
    """Archive a text or dialogue."""
    if content.archived_at is not None:
        typer_raise('The content is already archived.')

    with single_session() as session:
        content.archived_at = now()
        session.commit()

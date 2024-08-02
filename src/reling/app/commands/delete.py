from reling.app.app import app
from reling.app.types import CONTENT_ARG, FORCE_OPT
from reling.db import single_session
from reling.db.models import IdIndex
from reling.utils.typer import typer_raise

__all__ = [
    'delete',
]


@app.command()
def delete(content: CONTENT_ARG, force: FORCE_OPT = False) -> None:
    """Delete a text or dialog."""
    if not force and not input(f'Are you sure you want to delete "{content.id}"? (y/n): ').lower().startswith('y'):
        typer_raise('Operation canceled.')
    with single_session() as session:
        session.delete(content)
        session.query(IdIndex).filter_by(id=content.id).delete()
        session.commit()
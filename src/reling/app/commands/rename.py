from sqlalchemy.exc import IntegrityError, NoResultFound

from reling.app.app import app
from reling.app.types import CONTENT_ARG, NEW_NAME_ARG
from reling.db import single_session
from reling.db.models import IdIndex
from reling.utils.typer import typer_raise

__all__ = [
    'rename',
]


@app.command()
def rename(content: CONTENT_ARG, new_name: NEW_NAME_ARG) -> None:
    """Rename a text or dialogue."""
    with single_session() as session:
        try:
            id_index_item = session.query(IdIndex).filter_by(id=content.id).one()
        except NoResultFound:
            typer_raise(f'There is no content with the name "{content.id}".')  # Should never happen
        id_index_item.id = new_name
        content.id = new_name
        try:
            session.commit()
        except IntegrityError:
            typer_raise(f'The name "{new_name}" is already in use.')

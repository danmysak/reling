from ..app import app
from ..types import CONTENT_ARG, NEW_NAME_ARG

__all__ = [
    'rename',
]


@app.command()
def rename(content: CONTENT_ARG, new_name: NEW_NAME_ARG) -> None:
    """Rename a text or dialog."""
    pass

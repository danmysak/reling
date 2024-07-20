from ..app import app
from ..types import CONTENT_ARG

__all__ = [
    'unarchive',
]


@app.command()
def unarchive(content: CONTENT_ARG) -> None:
    """Unarchive a text or dialog."""
    pass

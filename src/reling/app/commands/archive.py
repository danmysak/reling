from ..app import app
from ..types import CONTENT_ARG

__all__ = [
    'archive',
]


@app.command()
def archive(content: CONTENT_ARG) -> None:
    """Archive a text or dialog."""
    pass

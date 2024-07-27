from reling.app.app import app
from reling.app.types import CONTENT_ARG

__all__ = [
    'archive',
]


@app.command()
def archive(content: CONTENT_ARG) -> None:
    """Archive a text or dialog."""
    pass

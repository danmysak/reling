from reling.app.app import app
from reling.app.types import CONTENT_ARG, FORCE_OPT

__all__ = [
    'delete',
]


@app.command()
def delete(content: CONTENT_ARG, force: FORCE_OPT = False) -> None:
    """Delete a text or dialog."""
    pass

from reling.db import single_session
from reling.db.models import Dialog, Text

__all__ = [
    'find_content',
]


def find_content(name: str) -> Text | Dialog | None:
    """Find a text or dialog by its name."""
    with single_session() as session:
        return session.get(Text, name) | session.get(Dialog, name)

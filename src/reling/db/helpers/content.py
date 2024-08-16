from reling.db import single_session
from reling.db.models import Dialogue, Text

__all__ = [
    'find_content',
]


def find_content(name: str) -> Text | Dialogue | None:
    """Find a text or dialogue by its name."""
    with single_session() as session:
        return session.get(Text, name) or session.get(Dialogue, name)

from datetime import datetime, UTC

__all__ = [
    'now',
]


def now() -> datetime:
    return datetime.now(UTC)

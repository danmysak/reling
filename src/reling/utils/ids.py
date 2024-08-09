import uuid

__all__ = [
    'generate_id',
]


def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())

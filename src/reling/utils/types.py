__all__ = [
    'ensure_not_none',
]


def ensure_not_none[T](value: T | None) -> T:
    """Raise a ValueError if the value is None."""
    if value is None:
        raise ValueError('Value cannot be None.')
    return value

__all__ = [
    'replace_prefix_casing',
]


def replace_prefix_casing(string: str, prefix: str) -> str:
    """Replace the prefix of a string with the casing of the given prefix."""
    return prefix + string[len(prefix):] if string.lower().startswith(prefix.lower()) else string

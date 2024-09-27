__all__ = [
    'capitalize_first_char',
    'replace_prefix_casing',
]


def capitalize_first_char(string: str) -> str:
    """Capitalize the first character of a string."""
    return string[:1].upper() + string[1:]


def replace_prefix_casing(string: str, prefix: str) -> str:
    """Replace the prefix of a string with the casing of the given prefix."""
    return prefix + string[len(prefix):] if string.lower().startswith(prefix.lower()) else string

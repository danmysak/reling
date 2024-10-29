from unicodedata import category

__all__ = [
    'capitalize_first_char',
    'is_punctuation',
    'is_whitespace',
    'replace_prefix_casing',
    'tokenize',
]


def capitalize_first_char(string: str) -> str:
    """Capitalize the first character of a string."""
    return string[:1].upper() + string[1:]


def replace_prefix_casing(string: str, prefix: str) -> str:
    """Replace the prefix of a string with the casing of the given prefix."""
    return prefix + string[len(prefix):] if string.lower().startswith(prefix.lower()) else string


def is_punctuation(char: str) -> bool:
    """Return whether the character is a punctuation symbol."""
    return category(char).startswith('P')


def is_whitespace(char: str) -> bool:
    """Return whether the character is a whitespace character."""
    return category(char).startswith('Z')


def tokenize(string: str, words_only: bool = False) -> list[str]:
    """Tokenize a string into words, punctuation, and whitespace."""
    tokens: list[str] = []
    current: list[str] = []
    for char in string:
        if is_punctuation(char) or is_whitespace(char):
            if current:
                tokens.append(''.join(current))
                current.clear()
            if not words_only:
                tokens.append(char)
        else:
            current.append(char)
    if current:
        tokens.append(''.join(current))
    return tokens

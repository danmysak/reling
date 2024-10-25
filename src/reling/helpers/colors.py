from rich.text import Text

__all__ = [
    'fade',
]

FADE = 'grey50'


def fade(text: str) -> Text:
    """Return the text in a faded color."""
    return Text(text, style=FADE)

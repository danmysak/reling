import re
from typing import Callable

__all__ = [
    'omit_empty',
    'remove_numbering',
    'slugify',
    'strip',
    'Transformer',
]

Transformer = Callable[[str], str | None]


def remove_numbering(text: str) -> str:
    return re.sub(r'^\s*\d+[.)]\s+', '', text)


def strip(text: str) -> str:
    return text.strip()


def omit_empty(text: str) -> str | None:
    return text or None


def slugify(text: str) -> str:
    return re.sub(r'[^\w-]', '', re.sub(r'\s+', '-', text.lower().strip()))

import re
from typing import Callable, Iterable, Generator

__all__ = [
    'add_numbering',
    'apply',
    'omit_empty',
    'remove_numbering',
    'slugify',
    'strip',
    'Transformer',
]

Transformer = Callable[[str, int], str | None]
# The second argument is the index of the item in the list.


def apply(transformer: Transformer, items: Iterable[str]) -> Generator[str, None, None]:
    for index, item in enumerate(items):
        yield transformer(item, index)


def add_numbering(text: str, index: int) -> str:
    return f'{index + 1}. {text}'


def remove_numbering(text: str, _: int) -> str:
    return re.sub(r'^\s*\d+[.)]\s+', '', text)


def strip(text: str, _: int) -> str:
    return text.strip()


def omit_empty(text: str, _: int) -> str | None:
    return text or None


def slugify(text: str, _: int) -> str:
    return re.sub(r'[^\w-]', '', re.sub(r'\s+', '-', text.lower().strip()))

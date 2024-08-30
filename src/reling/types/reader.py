from typing import Callable

from .speed import Speed

__all__ = [
    'Reader',
]


Reader = Callable[[Speed], None]

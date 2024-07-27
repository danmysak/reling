from typing import Generator, Iterable

__all__ = [
    'pair_items',
]


def pair_items[T](iterable: Iterable[T]) -> Generator[tuple[T, T], None, None]:
    """
    Return a generator that pairs items from the input iterable.
    If the input iterable has an odd number of items, the last item is ignored.
    """
    iterator = iter(iterable)
    return zip(iterator, iterator)

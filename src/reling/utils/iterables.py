from typing import Callable, Generator, Iterable

__all__ = [
    'map_asterisk',
    'pair_items',
]


def map_asterisk[T](f: Callable[..., T], items: Iterable[tuple]) -> Generator[T, None, None]:
    """Apply the function to each tuple in the iterable as positional arguments."""
    return (f(*args) for args in items)


def pair_items[T](iterable: Iterable[T]) -> Generator[tuple[T, T], None, None]:
    """
    Return a generator that pairs items from the input iterable.
    If the input iterable has an odd number of items, the last item is ignored.
    """
    iterator = iter(iterable)
    return zip(iterator, iterator)

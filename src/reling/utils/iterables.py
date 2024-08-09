from typing import Callable, cast, Generator, Iterable

__all__ = [
    'group_items',
    'map_asterisk',
    'pair_items',
]


def group_items[T](iterable: Iterable[T], group_size: int) -> Generator[tuple[T, ...], None, None]:
    """
    Group items from the iterable into tuples of the specified size.
    The last tuple is discarded if it is shorter than the specified size.
    """
    items = iter(iterable)
    return zip(*(items for _ in range(group_size)))


def pair_items[T](iterable: Iterable[T]) -> Generator[tuple[T, T], None, None]:
    """Pair items from the iterable into tuples. The last item is discarded if there is an odd number of items."""
    return cast(Generator[tuple[T, T], None, None], group_items(iterable, 2))


def map_asterisk[T](f: Callable[..., T], items: Iterable[tuple]) -> Generator[T, None, None]:
    """Apply the function to each tuple in the iterable as positional arguments."""
    return (f(*args) for args in items)

from typing import Callable

from reling.types import Promise

__all__ = [
    'name_function',
    'named_function',
    'promisify',
]


def name_function[T: Callable](function: T, name: str) -> T:
    """Set the name of a function."""
    function.__name__ = name
    return function


def named_function[T: Callable](name: str) -> Callable[[T], T]:
    """Decorator to set the name of a function."""
    return lambda function: name_function(function, name)


def promisify[T](value: T) -> Promise[T]:
    """Create a promise that returns a value."""
    return lambda: value

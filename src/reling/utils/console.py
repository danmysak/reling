from contextlib import contextmanager
from typing import Generator

__all__ = [
    'clear_current_line',
    'clear_previous',
    'erase_previous',
    'input_and_erase',
    'print_and_erase',
]


def clear_current_line() -> None:
    print('\033[2K', end='\r')


def clear_previous(lines: int = 1) -> None:
    print('\033[F\033[K' * lines, end='\r')


def erase_previous(text: str) -> None:
    clear_previous(text.count('\n') + 1)


def input_and_erase(prompt: str) -> str:
    data = input(prompt)
    erase_previous(prompt)
    return data


@contextmanager
def print_and_erase(text: str) -> Generator[None, None, None]:
    print(text)
    yield
    erase_previous(text)

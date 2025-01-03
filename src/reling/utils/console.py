from contextlib import contextmanager
from shutil import get_terminal_size
from typing import Generator, Iterable

from wcwidth import wcwidth

from .strings import universal_normalize

__all__ = [
    'clear_current_line',
    'clear_previous',
    'erase_previous',
    'input_and_erase',
    'interruptible_input',
    'print_and_erase',
    'stream_print',
]


def clear_current_line() -> None:
    print('\033[2K', end='\r')


def clear_previous(lines: int = 1) -> None:
    print('\033[F\033[K' * lines, end='\r')


def count_lines(text: str, num_columns: int) -> int:
    """Count the number of lines `text` takes up when printed with a maximum width of `num_columns`."""
    lines = 1
    taken = 0
    for char in text:
        if char == '\n':
            lines += 1
            taken = 0
        elif (char_width := wcwidth(char)) > 0:
            if taken + char_width <= num_columns:
                taken += char_width
            else:
                lines += 1
                taken = char_width
    return lines


def erase_previous(text: str, include_extra_line: bool = True) -> None:
    clear_current_line()
    clear_previous(count_lines(text, get_terminal_size().columns) + (0 if include_extra_line else -1))


def interruptible_input(prompt: str) -> str:
    try:
        return universal_normalize(input(prompt))
    except KeyboardInterrupt:
        erase_previous(prompt, include_extra_line=False)
        raise


def input_and_erase(prompt: str) -> str:
    data = interruptible_input(prompt)
    erase_previous(prompt + data + ' ')  # The space represents the rightmost position of the cursor
    return data


@contextmanager
def print_and_erase(text: str) -> Generator[None, None, None]:
    print(text)
    yield
    erase_previous(text)


def stream_print(stream: Iterable[str], start: str = '', end: str = '\n') -> None:
    print(start, end='', flush=True)
    for part in stream:
        print(part, end='', flush=True)
    print(end, end='', flush=True)

from contextlib import contextmanager
from itertools import chain
from shutil import get_terminal_size
from typing import Callable, Generator, Iterable

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from wcwidth import wcwidth

from .strings import universal_normalize

__all__ = [
    'clear_current_line',
    'input_and_erase',
    'interruptible_input',
    'print_and_erase',
    'print_and_maybe_erase',
    'stream_print_markdown',
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


@contextmanager
def print_and_maybe_erase(text: str) -> Generator[Callable[[], None], None, None]:
    print(text)
    yield lambda: erase_previous(text)


def stream_print_markdown(stream: Iterable[str], start: str = '', end: str = '\n') -> None:
    """Print a stream of Markdown-formatted text."""
    console = Console()
    buffer: list[str] = []
    with Live(console=console) as live:
        for chunk in chain([start], stream, [end]):
            buffer.append(chunk)
            live.update(Markdown(''.join(buffer)))

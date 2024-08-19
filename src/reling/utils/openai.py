from contextlib import contextmanager
from openai import APIError

from reling.utils.typer import typer_raise

__all__ = [
    'openai_handler',
]


@contextmanager
def openai_handler() -> None:
    try:
        yield
    except APIError as e:
        typer_raise(f'OpenAI API error:\n{e}')

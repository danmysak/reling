from enum import Enum
from typing import Callable, Never

import typer

from .strings import replace_prefix_casing

__all__ = [
    'typer_enum_autocompletion',
    'typer_enum_options',
    'typer_enum_parser',
    'typer_func_parser',
    'typer_raise',
]


def typer_raise(message: str) -> Never:
    typer.echo(message, err=True)
    raise typer.Exit(code=1)


def typer_func_parser[R](func: Callable[[str], R | None]) -> Callable[[str], R]:
    """Create a Typer argument parser from a function that returns a value or None."""

    def wrapper(arg: str) -> R:
        result = func(arg)
        if result is None:
            raise typer.BadParameter(arg)
        return result

    return wrapper


def typer_enum_options(enum: type[Enum]) -> str:
    """Return a string of the enum options for use in Typer help messages."""
    return ', '.join(f'"{member.lower()}"' for member in enum.__members__)


def typer_enum_parser(enum: type[Enum]) -> Callable[[str | Enum], Enum]:
    """Create a Typer argument parser from an Enum type."""

    def wrapper(arg: str | Enum) -> Enum:
        if isinstance(arg, Enum):  # Due to https://github.com/tiangolo/typer/discussions/720
            return arg
        try:
            return enum[arg.upper()]
        except KeyError:
            raise typer.BadParameter(
                f'{arg} (expected one of {typer_enum_options(enum)})',
            )

    return wrapper


def typer_enum_autocompletion(enum: type[Enum]) -> Callable[[str], list[str]]:
    """Create a Typer autocompletion function from an Enum type."""

    def wrapper(prefix: str) -> list[str]:
        lower = prefix.lower()
        return [
            replace_prefix_casing(member.lower(), prefix)
            for member in enum.__members__ if member.lower().startswith(lower)
        ]

    return wrapper

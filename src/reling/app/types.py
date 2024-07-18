from typing import Annotated, Optional

import typer

from ..db.enums import ContentCategory, Level
from ..db.helpers.content import find_content
from ..db.helpers.languages import find_language
from ..db.models import Dialog, Language, Text
from ..utils.typer import typer_enum_options, typer_enum_parser, typer_func_parser

__all__ = [
    'API_KEY',
    'CONTENT',
    'CONTENT_CATEGORY_ARG',
    'CONTENT_CATEGORY_OPT',
    'LANGUAGE_ARG',
    'LANGUAGE_OPT',
    'LEVEL_OPT',
    'MODEL',
    'SPEAKER_OPT',
    'STYLE_OPT',
    'TOPIC_OPT',
]

API_KEY = Annotated[str, typer.Option(
    envvar='RELING_API_KEY',
    help='OpenAI API key',
    prompt='OpenAI API key',
)]

MODEL = Annotated[str, typer.Option(
    envvar='RELING_MODEL',
    help='GPT model',
    prompt='GPT model',
)]

CONTENT = Annotated[Text | Dialog, typer.Argument(
    parser=typer_func_parser(find_content),
    help='Name of the text or dialog',
)]

LANGUAGE_ARG = Annotated[Language, typer.Argument(
    parser=typer_func_parser(find_language),
    help='Language code or name',
)]

LANGUAGE_OPT = Annotated[Language | None, typer.Option(
    parser=typer_func_parser(find_language),
    help='Language code or name',
)]

CONTENT_CATEGORY_ARG = Annotated[ContentCategory, typer.Argument(
    parser=typer_enum_parser(ContentCategory),
    help=f'Content category (one of {typer_enum_options(ContentCategory)})',
)]

CONTENT_CATEGORY_OPT = Annotated[ContentCategory | None, typer.Option(
    parser=typer_enum_parser(ContentCategory),
    help=f'Content category (one of {typer_enum_options(ContentCategory)})',
)]

LEVEL_OPT = Annotated[Level | None, typer.Option(
    parser=typer_enum_parser(Level),
    help=f'Level (one of {typer_enum_options(Level)})',
)]

# The `Optional` type is used instead of the union with `None` due to https://github.com/tiangolo/typer/issues/533

TOPIC_OPT = Annotated[Optional[str], typer.Option(
    help='Topic of the text (like "food" or "zoology")',
)]

STYLE_OPT = Annotated[Optional[str], typer.Option(
    help='Style of the text (like "mystery" or "news article")',
)]

SPEAKER_OPT = Annotated[Optional[str], typer.Option(
    help='Your interlocutor (like "waiter" or "friend")',
)]

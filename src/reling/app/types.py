import re
from typing import Annotated, Optional
# The `Optional` type is used instead of the union with `None` due to https://github.com/tiangolo/typer/issues/533

import typer

from reling.db.enums import ContentCategory, Level
from reling.db.helpers.content import find_content
from reling.db.helpers.ids import find_ids_by_prefix
from reling.db.helpers.languages import find_language, find_languages_by_prefix
from reling.db.models import Dialog, Language, Text
from reling.utils.typer import typer_enum_autocompletion, typer_enum_options, typer_enum_parser, typer_func_parser

__all__ = [
    'API_KEY',
    'ARCHIVE_OPT',
    'CONTENT_ARG',
    'CONTENT_CATEGORY_OPT',
    'FORCE_OPT',
    'LANGUAGE_ARG',
    'LANGUAGE_OPT',
    'LANGUAGE_OPT_ARG',
    'LANGUAGE_OPT_FROM',
    'LEVEL_OPT',
    'MODEL',
    'NEW_NAME_ARG',
    'REGEX_OPT',
    'SPEAKER_OPT',
    'STYLE_OPT',
    'TOPIC_OPT',
]

API_KEY = Annotated[str, typer.Option(
    envvar='RELING_API_KEY',
    help='Your OpenAI API key',
    prompt='Enter your OpenAI API key',
)]

MODEL = Annotated[str, typer.Option(
    envvar='RELING_MODEL',
    help='Identifier for the GPT model to be used',
    prompt='Enter the GPT model identifier',
)]

CONTENT_ARG = Annotated[Text | Dialog, typer.Argument(
    parser=typer_func_parser(find_content),
    help='Name of the text or dialog',
    autocompletion=find_ids_by_prefix,
)]

LANGUAGE_ARG = Annotated[Language, typer.Argument(
    parser=typer_func_parser(find_language),
    help='Language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT_ARG = Annotated[Language | None, typer.Argument(
    parser=typer_func_parser(find_language),
    help='Language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT = Annotated[Language | None, typer.Option(
    parser=typer_func_parser(find_language),
    help='Language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT_FROM = Annotated[Language | None, typer.Option(
    '--from',  # `from` is a reserved keyword
    parser=typer_func_parser(find_language),
    help='Language code or name',
    autocompletion=find_languages_by_prefix,
)]

CONTENT_CATEGORY_OPT = Annotated[ContentCategory | None, typer.Option(
    parser=typer_enum_parser(ContentCategory),
    help=f'Content category, one of: {typer_enum_options(ContentCategory)}',
    autocompletion=typer_enum_autocompletion(ContentCategory),
)]

LEVEL_OPT = Annotated[Level | None, typer.Option(
    parser=typer_enum_parser(Level),
    help=f'Level, one of: {typer_enum_options(Level)}',
    autocompletion=typer_enum_autocompletion(Level),
)]

TOPIC_OPT = Annotated[Optional[str], typer.Option(
    help='Topic of the content, e.g., "food" or "zoology"',
)]

STYLE_OPT = Annotated[Optional[str], typer.Option(
    help='Style of the text, e.g., "mystery" or "news article"',
)]

SPEAKER_OPT = Annotated[Optional[str], typer.Option(
    help='Interlocutor in the dialog, e.g., "waiter" or "friend"',
)]

NEW_NAME_ARG = Annotated[str, typer.Argument(
    help='New name for the text or dialog',
)]

REGEX_OPT = Annotated[re.Pattern | None, typer.Option(
    parser=re.compile,
    help='Regular expression to filter results',
)]

ARCHIVE_OPT = Annotated[Optional[bool], typer.Option(
    help='Search within archived items',
)]

FORCE_OPT = Annotated[Optional[bool], typer.Option(
    help='Force execution of the operation',
)]

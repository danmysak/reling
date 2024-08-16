import re
from typing import Annotated, Optional
# The `Optional` type is used instead of the union with `None` due to https://github.com/tiangolo/typer/issues/533

import typer

from reling.db.enums import ContentCategory, Level, Sex
from reling.db.helpers.content import find_content
from reling.db.helpers.ids import find_ids_by_prefix
from reling.db.helpers.languages import find_language, find_languages_by_prefix
from reling.db.models import Dialogue, Language, Text
from reling.types import WordWithSense
from reling.utils.typer import (
    typer_enum_autocompletion,
    typer_enum_options,
    typer_enum_parser,
    typer_func_parser,
    typer_regex_parser,
)

__all__ = [
    'API_KEY',
    'ARCHIVE_OPT',
    'CONTENT_ARG',
    'CONTENT_CATEGORY_OPT',
    'FORCE_OPT',
    'IDS_ONLY_OPT',
    'INCLUDE_OPT',
    'LANGUAGE_ARG',
    'LANGUAGE_OPT',
    'LANGUAGE_OPT_ARG',
    'LANGUAGE_OPT_FROM',
    'LEVEL_OPT',
    'MODEL',
    'NEW_NAME_ARG',
    'REGEX_CONTENT_OPT',
    'SIZE_DIALOGUE_OPT',
    'SIZE_TEXT_OPT',
    'SPEAKER_OPT',
    'SPEAKER_SEX_OPT',
    'STYLE_OPT',
    'TOPIC_OPT',
    'USER_SEX',
]

ENV_PREFIX = 'RELING_'

API_KEY = Annotated[str, typer.Option(
    envvar=f'{ENV_PREFIX}API_KEY',
    help='your OpenAI API key',
    prompt='Enter your OpenAI API key',
)]

MODEL = Annotated[str, typer.Option(
    envvar=f'{ENV_PREFIX}MODEL',
    help='identifier for the GPT model to be used',
    prompt='Enter the GPT model identifier',
)]

USER_SEX = Annotated[Sex, typer.Option(
    envvar=f'{ENV_PREFIX}USER_SEX',
    parser=typer_enum_parser(Sex),
    help=f'sex of the user, one of: {typer_enum_options(Sex)} (to customize the generated content)',
    prompt=f'Enter your sex ({typer_enum_options(Sex)})',
    autocompletion=typer_enum_autocompletion(Sex),
)]

CONTENT_ARG = Annotated[Text | Dialogue, typer.Argument(
    parser=typer_func_parser(find_content),
    help='name of the text or dialogue',
    autocompletion=find_ids_by_prefix,
)]

LANGUAGE_ARG = Annotated[Language, typer.Argument(
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT_ARG = Annotated[Language | None, typer.Argument(
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT = Annotated[Language | None, typer.Option(
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

LANGUAGE_OPT_FROM = Annotated[Language | None, typer.Option(
    '--from',  # `from` is a reserved keyword
    parser=typer_func_parser(find_language),
    help='language code or name',
    autocompletion=find_languages_by_prefix,
)]

CONTENT_CATEGORY_OPT = Annotated[ContentCategory | None, typer.Option(
    parser=typer_enum_parser(ContentCategory),
    help=f'content category, one of: {typer_enum_options(ContentCategory)}',
    autocompletion=typer_enum_autocompletion(ContentCategory),
)]

LEVEL_OPT = Annotated[Level | None, typer.Option(
    parser=typer_enum_parser(Level),
    help=f'level, one of: {typer_enum_options(Level)}',
    autocompletion=typer_enum_autocompletion(Level),
)]

TOPIC_OPT = Annotated[Optional[str], typer.Option(
    help='topic of the content, e.g., "food" or "zoology"',
)]

STYLE_OPT = Annotated[Optional[str], typer.Option(
    help='style of the text, e.g., "mystery" or "news article"',
)]

SPEAKER_OPT = Annotated[Optional[str], typer.Option(
    help='interlocutor in the dialogue, e.g., "waiter" or "friend"',
)]

SPEAKER_SEX_OPT = Annotated[Sex | None, typer.Option(
    parser=typer_enum_parser(Sex),
    help=f'sex of the interlocutor, one of: {typer_enum_options(Sex)}',
    autocompletion=typer_enum_autocompletion(Sex),
)]

SIZE_TEXT_OPT = Annotated[int, typer.Option(
    min=1,
    help='number of sentences in the text',
)]

SIZE_DIALOGUE_OPT = Annotated[int, typer.Option(
    min=1,
    help='number of exchanges in the dialogue',
)]

INCLUDE_OPT = Annotated[Optional[list[str]], typer.Option(
    help=f'word or phrase to be included in the content '
         f'(e.g., "bank" or "bank{WordWithSense.DIVIDER_WITH_WHITE_SPACE}financial institution" for disambiguation)',
)]

NEW_NAME_ARG = Annotated[str, typer.Argument(
    help='new name for the text or dialogue',
)]

REGEX_CONTENT_OPT = Annotated[re.Pattern | None, typer.Option(
    parser=typer_regex_parser,
    help='regular expression to filter results by content, topic, style, or speaker',
)]

ARCHIVE_OPT = Annotated[Optional[bool], typer.Option(
    help='Search within archived items.',
)]

IDS_ONLY_OPT = Annotated[Optional[bool], typer.Option(
    help='Display only the IDs of the items.',
)]

FORCE_OPT = Annotated[Optional[bool], typer.Option(
    help='Force execution of the operation.',
)]

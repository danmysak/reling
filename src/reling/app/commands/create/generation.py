from typing import Generator

from reling.db.enums import ContentCategory, Level
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogExchangeData, WordWithSense
from reling.utils.english import pluralize
from reling.utils.iterables import map_asterisk, pair_items
from reling.utils.transformers import omit_empty, remove_numbering, slugify, strip

__all__ = [
    'generate_dialog_exchanges',
    'generate_id',
    'generate_text_sentences',
]

# We ask the model to number each sentence/line of its response because this approach makes it more reliable in placing
# sentences on new lines and ensures that there are exactly the specified number of sentences in the response.


def build_level_prompt(level: Level, category: ContentCategory) -> str:
    """Return a prompt section describing the level of the content."""

    def get_sentences_description() -> str:
        match level:
            case Level.BASIC:
                return 'very simple'
            case Level.INTERMEDIATE:
                return 'rather simple'
            case Level.ADVANCED:
                return 'complex'

    def get_vocabulary_description() -> str:
        match level:
            case Level.BASIC:
                return 'very basic'
            case Level.INTERMEDIATE:
                return 'intermediate'
            case Level.ADVANCED:
                return 'advanced'

    return (f'The {category.value} should consist of {get_sentences_description()} sentences '
            f'and use {get_vocabulary_description()} vocabulary.')


def build_include_prompt(include: list[WordWithSense]) -> list[str]:
    """Return a prompt section describing the words or phrases to include in the content."""
    return [] if len(include) == 0 else [
        f'Include the following {pluralize('word', len(include))} or {pluralize('phrase', len(include))}:',
        *(item.format() for item in include),
    ]


def generate_text_sentences(
        gpt: GPTClient,
        num_sentences: int,
        language: Language,
        level: Level,
        topic: str,
        style: str,
        include: list[WordWithSense],
) -> Generator[str, None, None]:
    return gpt.ask(
        '\n'.join([
            f'Generate a text in {language.name} consisting of {num_sentences} {pluralize('sentence', num_sentences)}.',
            f'The text should be about {topic} and be written in the style of {style}.',
            f'Do not include any additional text; only generate the text as specified.',
            f'Number each sentence and put each sentence on a new line.',
            build_level_prompt(level, ContentCategory.TEXT),
            *build_include_prompt(include),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    )


def generate_dialog_exchanges(
        gpt: GPTClient,
        num_exchanges: int,
        language: Language,
        level: Level,
        speaker: str,
        topic: str | None,
        include: list[WordWithSense],
) -> Generator[DialogExchangeData, None, None]:
    return map_asterisk(DialogExchangeData, pair_items(gpt.ask(
        '\n'.join([
            f'Generate a dialog in {language.name} consisting of {num_exchanges * 2} sentences.',
            f'The dialog should be between two speakers, {speaker} and me.',
            *([f'The dialog should be about {topic}.'] if topic else []),
            f'Do not include any additional text; only generate the text as specified.',
            f'Number each sentence and put each sentence on a new line.',
            f'The first, third, etc. sentences should be spoken by {speaker}.'
            f'The second, fourth, etc. sentences should be spoken by me.'
            f'Do not prefix the sentences with the speakers’ names.',
            build_level_prompt(level, ContentCategory.DIALOG),
            *build_include_prompt(include),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    )))


def generate_id(
        gpt: GPTClient,
        sentences: list[str],
) -> str:
    return (list(gpt.ask(
        '\n'.join([
            'What should the following text be called in English?',
            '"""',
            *sentences,
            '"""',
            'The name should be a short, descriptive title.',
            'Do not include any additional text; only generate the English name as specified.',
        ]),
        transformers=[slugify],
    )) or [''])[0]

from typing import Generator

from reling.db.enums import ContentCategory
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogExchangeData
from reling.utils.iterables import map_asterisk, pair_items
from reling.utils.transformers import add_numbering, apply, omit_empty, remove_numbering, strip

__all__ = [
    'translate_dialog_exchanges',
    'translate_text_sentences',
]


def translate_sentences(
        gpt: GPTClient,
        sentences: list[str],
        category: ContentCategory,
        source_language: Language,
        target_language: Language,
) -> Generator[str, None, None]:
    return gpt.ask(
        '\n'.join([
            f'Translate the following {'sentences of a text' if category == ContentCategory.TEXT else 'dialog turns'}',
            f'from {source_language.name} into {target_language.name}.',

            f'Generate only the specified translations without any additional text.',
            f'Number each translated sentence and place each on a new line.'
            f'---',
            *apply(add_numbering, sentences),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    )


def translate_text_sentences(
        gpt: GPTClient,
        sentences: list[str],
        source_language: Language,
        target_language: Language,
) -> Generator[str, None, None]:
    return translate_sentences(
        gpt=gpt,
        sentences=sentences,
        category=ContentCategory.TEXT,
        source_language=source_language,
        target_language=target_language,
    )


def translate_dialog_exchanges(
        gpt: GPTClient,
        exchanges: list[DialogExchangeData],
        source_language: Language,
        target_language: Language,
) -> Generator[DialogExchangeData, None, None]:
    return map_asterisk(DialogExchangeData, pair_items(
        translate_sentences(
            gpt=gpt,
            sentences=[turn for exchange in exchanges for turn in exchange.all()],
            category=ContentCategory.DIALOG,
            source_language=source_language,
            target_language=target_language,
        )
    ))

import readline  # noqa: F401 (https://stackoverflow.com/a/14796424/430083)
from typing import Generator, Iterable

from reling.types import DialogExchangeData
from reling.utils.transformers import add_numbering
from .types import ExchangeWithTranslation, SentenceWithTranslation

__all__ = [
    'collect_dialog_translations',
    'collect_text_translations',
]


def collect_text_translations(
        sentences: Iterable[str],
) -> Generator[SentenceWithTranslation, None, None]:
    """Collect the translations of text sentences."""
    for index, sentence in enumerate(sentences):
        print(add_numbering(sentence, index))
        yield SentenceWithTranslation(
            sentence=sentence,
            translation=input(),
        )
        print()


def collect_dialog_translations(
        exchanges: Iterable[DialogExchangeData],
        original_translations: Iterable[DialogExchangeData],
) -> Generator[ExchangeWithTranslation, None, None]:
    """Collect the translations of user turns in a dialog."""
    for index, (exchange, original_translation) in enumerate(zip(exchanges, original_translations)):
        print(original_translation.speaker)
        print(add_numbering(exchange.user, index))
        yield ExchangeWithTranslation(
            exchange=exchange,
            user_translation=input(),
        )
        print()

from typing import Generator, Iterable

from reling.helpers.output import output_text
from reling.tts import TTSVoiceClient
from reling.types import DialogueExchangeData
from reling.utils.transformers import get_numbering_prefix
from .types import ExchangeWithTranslation, SentenceWithTranslation

__all__ = [
    'collect_dialogue_translations',
    'collect_text_translations',
]


def collect_text_translations(
        sentences: Iterable[str],
        source_tts: TTSVoiceClient | None,
) -> Generator[SentenceWithTranslation, None, None]:
    """Collect the translations of text sentences."""
    for index, sentence in enumerate(sentences):
        output_text(sentence, source_tts, print_prefix=get_numbering_prefix(index))
        yield SentenceWithTranslation(
            sentence=sentence,
            translation=input(),
        )
        print()


def collect_dialogue_translations(
        exchanges: Iterable[DialogueExchangeData],
        original_translations: Iterable[DialogueExchangeData],
        source_user_tts: TTSVoiceClient | None,
        target_speaker_tts: TTSVoiceClient | None,
) -> Generator[ExchangeWithTranslation, None, None]:
    """Collect the translations of user turns in a dialogue."""
    for index, (exchange, original_translation) in enumerate(zip(exchanges, original_translations)):
        output_text(original_translation.speaker, target_speaker_tts)
        output_text(exchange.user, source_user_tts, print_prefix=get_numbering_prefix(index))
        yield ExchangeWithTranslation(
            exchange=exchange,
            user_translation=input(),
        )
        print()

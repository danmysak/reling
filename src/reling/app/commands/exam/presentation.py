from dataclasses import dataclass
from typing import Iterable

from reling.helpers.output import output_text
from reling.tts import TTSVoiceClient
from reling.types import DialogueExchangeData
from reling.utils.scores import format_average_score
from reling.utils.transformers import get_numbering_prefix
from .scoring import MAX_SCORE
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'present_dialogue_results',
    'present_text_results',
]


@dataclass
class TitleData:
    text: str
    should_number: bool
    tts: TTSVoiceClient | None


def wait_for_key_press() -> None:
    input()


def present_results(
        titles: Iterable[list[TitleData]],
        provided_translations: Iterable[str],
        original_translations: Iterable[str],
        results: Iterable[ScoreWithSuggestion],
        target_tts: TTSVoiceClient | None,
) -> None:
    """Present the results of scoring translations."""
    scores: list[int] = []
    for index, (title_items, provided_translation, original_translation, result) in enumerate(zip(
            titles,
            provided_translations,
            original_translations,
            results,
    )):
        scores.append(result.score)
        for title in title_items:
            output_text(
                print_prefix=get_numbering_prefix(index) if title.should_number else '',
                text=title.text,
                tts=title.tts,
            )
        print(f'Your score: {result.score}/{MAX_SCORE}')
        print(f'Provided: {provided_translation}')
        if result.suggestion is not None:
            output_text(print_prefix='Improved: ', text=result.suggestion, tts=target_tts)
        output_text(print_prefix='Original: ', text=original_translation, tts=target_tts)
        wait_for_key_press()
    print('Your average score:', format_average_score(scores))


def present_text_results(
        sentences: Iterable[SentenceWithTranslation],
        original_translations: Iterable[str],
        results: Iterable[ScoreWithSuggestion],
        source_tts: TTSVoiceClient | None,
        target_tts: TTSVoiceClient | None,
) -> None:
    """Present the results of scoring text translations."""
    present_results(
        titles=([
            TitleData(
                text=sentence.sentence,
                should_number=True,
                tts=source_tts,
            ),
        ] for sentence in sentences),
        provided_translations=(sentence.translation for sentence in sentences),
        original_translations=original_translations,
        results=results,
        target_tts=target_tts,
    )


def present_dialogue_results(
        exchanges: Iterable[ExchangeWithTranslation],
        original_translations: Iterable[DialogueExchangeData],
        results: Iterable[ScoreWithSuggestion],
        source_user_tts: TTSVoiceClient | None,
        target_speaker_tts: TTSVoiceClient | None,
        target_user_tts: TTSVoiceClient | None,
) -> None:
    """Present the results of scoring dialogue translations."""
    present_results(
        titles=([
            TitleData(
                text=original_translation.speaker,
                should_number=False,
                tts=target_speaker_tts,
            ),
            TitleData(
                text=exchange.exchange.user,
                should_number=True,
                tts=source_user_tts,
            ),
        ] for original_translation, exchange in zip(
            original_translations,
            exchanges,
        )),
        provided_translations=(exchange.user_translation for exchange in exchanges),
        original_translations=(exchange.user for exchange in original_translations),
        results=results,
        target_tts=target_user_tts,
    )

from typing import Iterable

from reling.types import DialogueExchangeData
from reling.utils.scores import format_average_score
from reling.utils.transformers import add_numbering, apply
from .scoring import MAX_SCORE
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'present_dialogue_results',
    'present_text_results',
]


def wait_for_key_press() -> None:
    input()


def present_results(
        titles: Iterable[str],
        provided_translations: Iterable[str],
        original_translations: Iterable[str],
        results: Iterable[ScoreWithSuggestion],
) -> None:
    """Present the results of scoring translations."""
    scores: list[int] = []
    for title, provided_translation, original_translation, result in zip(
            titles,
            provided_translations,
            original_translations,
            results,
    ):
        scores.append(result.score)
        print(title)
        print(f'Your score: {result.score}/{MAX_SCORE}')
        print(f'Provided: {provided_translation}')
        if result.suggestion is not None:
            print(f'Improved: {result.suggestion}')
        print(f'Original: {original_translation}')
        wait_for_key_press()
    print('Your average score:', format_average_score(scores))


def present_text_results(
        sentences: Iterable[SentenceWithTranslation],
        original_translations: Iterable[str],
        results: Iterable[ScoreWithSuggestion],
) -> None:
    """Present the results of scoring text translations."""
    present_results(
        titles=apply(add_numbering, [sentence.sentence for sentence in sentences]),
        provided_translations=(sentence.translation for sentence in sentences),
        original_translations=original_translations,
        results=results,
    )


def present_dialogue_results(
        exchanges: Iterable[ExchangeWithTranslation],
        original_translations: Iterable[DialogueExchangeData],
        results: Iterable[ScoreWithSuggestion],
) -> None:
    """Present the results of scoring dialogue translations."""
    present_results(
        titles=('\n'.join(lines) for lines in zip(
            (exchange.speaker for exchange in original_translations),
            apply(add_numbering, (exchange.exchange.user for exchange in exchanges)),
        )),
        provided_translations=(exchange.user_translation for exchange in exchanges),
        original_translations=(exchange.user for exchange in original_translations),
        results=results,
    )

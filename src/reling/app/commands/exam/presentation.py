from dataclasses import dataclass
from datetime import timedelta
from functools import partial
from typing import Iterable

from reling.helpers.output import output, SentenceData
from reling.helpers.wave import play
from reling.tts import TTSVoiceClient
from reling.types import DialogueExchangeData, Input
from reling.utils.scores import format_average_score
from reling.utils.time import format_time_delta
from reling.utils.transformers import get_numbering_prefix
from .scoring import MAX_SCORE
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'present_dialogue_results',
    'present_text_results',
]

NA = 'N/A'


@dataclass
class TitleData:
    text: str
    should_number: bool
    tts: TTSVoiceClient | None


def present_results(
        titles: Iterable[list[TitleData]],
        provided_translations: Iterable[Input],
        original_translations: Iterable[str],
        results: Iterable[ScoreWithSuggestion],
        duration: timedelta,
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
            output(SentenceData.from_tts(
                title.text,
                title.tts,
                print_prefix=get_numbering_prefix(index) if title.should_number else '',
            ))
        print(f'Your score: {result.score}/{MAX_SCORE}')
        output(
            SentenceData(
                text=provided_translation.text.strip() or NA,
                print_prefix='Provided: ',
                reader=partial(play, provided_translation.audio) if provided_translation.audio and target_tts else None,
                reader_id='provided',
            ),
            SentenceData.from_tts(
                text=result.suggestion or NA,
                client=target_tts if result.suggestion else None,
                print_prefix='Improved: ',
                reader_id='improved',
            ),
            SentenceData.from_tts(
                text=original_translation,
                client=target_tts,
                print_prefix='Original: ',
                reader_id='original',
            ),
        )
        print()
    print(f'Average score: {format_average_score(scores)}')
    print(f'Exam duration: {format_time_delta(duration)}')


def present_text_results(
        sentences: Iterable[SentenceWithTranslation],
        original_translations: Iterable[str],
        results: Iterable[ScoreWithSuggestion],
        duration: timedelta,
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
        duration=duration,
        target_tts=target_tts,
    )


def present_dialogue_results(
        exchanges: Iterable[ExchangeWithTranslation],
        original_translations: Iterable[DialogueExchangeData],
        results: Iterable[ScoreWithSuggestion],
        duration: timedelta,
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
        duration=duration,
        target_tts=target_user_tts,
    )

from dataclasses import dataclass
from datetime import timedelta
from functools import partial
from itertools import repeat
from typing import Callable, Iterable

from rich.text import Text

from reling.config import MAX_SCORE
from reling.helpers.colors import fade
from reling.helpers.diff import highlight_diff
from reling.helpers.output import output, SentenceData
from reling.helpers.scoring import format_average_score
from reling.helpers.wave import play
from reling.tts import TTSVoiceClient
from reling.types import DialogueExchangeData, Input
from reling.utils.console import stream_print
from reling.utils.prompts import PROMPT_SEPARATOR, PromptOption
from reling.utils.time import format_time_delta
from reling.utils.transformers import get_numbering_prefix
from .types import ExchangeWithTranslation, ExplanationRequest, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'present_dialogue_results',
    'present_text_results',
]

NOTHING_TO_IMPROVE = fade('(no changes needed)')


@dataclass
class TitleData:
    text: str
    should_number: bool
    tts: TTSVoiceClient | None


def format_provided_and_suggestion(
        provided: str | None,
        perfect: str | None,
) -> tuple[str | Text | None, str | Text | None]:
    """Compute the representation of the provided answer and suggested improvement to be shown to the user."""
    if provided is not None and perfect is not None:
        if provided == perfect:
            return provided, NOTHING_TO_IMPROVE
        else:
            return highlight_diff(provided, perfect)
    else:
        return provided, perfect


def build_explanation_printer(
        explain: Callable[[ExplanationRequest], Iterable[str]],
        request: ExplanationRequest,
) -> Callable[[], None]:
    """Create a function to print an explanation."""
    return lambda: stream_print(explain(request), start=PROMPT_SEPARATOR + '\n')


def present_results(
        titles: list[list[TitleData]],
        provided_translations: list[Input],
        original_translations: list[str] | None,
        results: list[ScoreWithSuggestion],
        duration: timedelta,
        target_tts: TTSVoiceClient | None,
        explain: Callable[[ExplanationRequest], Iterable[str]],
) -> None:
    """Present the results of scoring translations."""
    scores: list[int] = []
    for index, (title_items, provided_translation, original_translation, result) in enumerate(zip(
            titles,
            provided_translations,
            original_translations if original_translations is not None else repeat(None),
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
        provided_text = provided_translation.text or None
        perfect_text = ((result.suggestion if result.suggestion != provided_text else None)
                        or (provided_text if result.score == MAX_SCORE else None)) if provided_text else None
        provided_print_text, improved_print_text = format_provided_and_suggestion(provided_text, perfect_text)
        output(*[
            SentenceData(
                print_text=provided_print_text,
                print_prefix='Provided: ',
                reader=partial(play, provided_translation.audio) if provided_translation.audio and target_tts else None,
                reader_id='provided',
            ),
            SentenceData.from_tts(
                text=perfect_text,
                client=target_tts,
                print_text=improved_print_text,
                print_prefix='Improved: ',
                reader_id='improved',
            ),
            *([SentenceData.from_tts(
                text=original_translation,
                client=target_tts,
                print_prefix='Original: ',
                reader_id='original',
            )] if original_translation is not None else []),
        ], extra_options=[
            PromptOption(
                'explain',
                build_explanation_printer(explain, ExplanationRequest(index, source=False)),
                {'source': build_explanation_printer(explain, ExplanationRequest(index, source=True))},
            ),
        ])
        print()
    print(f'Average score: {format_average_score(scores)}')
    print(f'Exam duration: {format_time_delta(duration)}')


def present_text_results(
        sentences: list[SentenceWithTranslation],
        original_translations: list[str],
        show_original: bool,
        results: list[ScoreWithSuggestion],
        duration: timedelta,
        source_tts: TTSVoiceClient | None,
        target_tts: TTSVoiceClient | None,
        explain: Callable[[ExplanationRequest], Iterable[str]],
) -> None:
    """Present the results of scoring text translations."""
    present_results(
        titles=[[
            TitleData(
                text=sentence.sentence,
                should_number=True,
                tts=source_tts,
            ),
        ] for sentence in sentences],
        provided_translations=[sentence.translation for sentence in sentences],
        original_translations=original_translations if show_original else None,
        results=results,
        duration=duration,
        target_tts=target_tts,
        explain=explain,
    )


def present_dialogue_results(
        exchanges: list[ExchangeWithTranslation],
        original_translations: list[DialogueExchangeData],
        show_original: bool,
        results: list[ScoreWithSuggestion],
        duration: timedelta,
        source_user_tts: TTSVoiceClient | None,
        target_speaker_tts: TTSVoiceClient | None,
        target_user_tts: TTSVoiceClient | None,
        explain: Callable[[ExplanationRequest], Iterable[str]],
) -> None:
    """Present the results of scoring dialogue translations."""
    present_results(
        titles=[[
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
        )],
        provided_translations=[exchange.user_translation for exchange in exchanges],
        original_translations=[exchange.user for exchange in original_translations] if show_original else None,
        results=results,
        duration=duration,
        target_tts=target_user_tts,
        explain=explain,
    )

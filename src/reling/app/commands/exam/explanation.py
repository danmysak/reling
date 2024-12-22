from typing import Callable, Generator

from reling.config import MAX_SCORE
from reling.db.enums import ContentCategory
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogueExchangeData, Promise
from reling.utils.feeders import CharFeeder
from reling.utils.values import coalesce
from .types import ExchangeWithTranslation, ExplanationRequest, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'build_dialogue_explainer',
    'build_text_explainer',
]

MISTAKE_THRESHOLD_RATIO = 0.5


def if_not(text: str | None, until_equals: str) -> str | None:
    """Return the text if it does not equal the specified value, otherwise return None."""
    return text if text != until_equals else None


def explain_structure(sentence: str, language: Language) -> list[str]:
    """Generate a prompt section for explaining the structure of a translation in the specified language."""
    return [
        f'The last line is translated into {language.name} as follows:',
        f'"""{sentence}"""',
        f'Explain the structure of this translation to a learner of {language.name}.',
    ]


def explain_mistakes(sentence: str, corrected: str, language: Language) -> list[str]:
    """Generate a prompt section for explaining why a corrected translation is preferred over the provided one."""
    return [
        f'A learner of {language.name} translated the last line as follows:',
        f'"""{sentence}"""',
        f'Explain why the following translation is more appropriate:'
        f'"""{corrected}"""',
    ]


def explain_difference(sentence: str, alternative: str, language: Language) -> list[str]:
    """Generate a prompt section for explaining differences between a provided and alternative translation."""
    return [
        f'A learner of {language.name} translated the last line as follows:',
        f'"""{sentence}"""',
        f'Explain whether there is any difference from the alternative translation below '
        f'and which option is more appropriate:',
        f'"""{alternative}"""',
    ]


def explain_source_structure(sentence: str) -> list[str]:
    """Generate a prompt section for explaining the structure of a sentence in the source language."""
    return [
        f'Explain the grammatical and structural elements of the last line ("""{sentence}""") to a language learner.',
    ]


def do_explain(
        gpt: Promise[GPTClient],
        category: ContentCategory,
        initial_sentences: list[str],
        provided: str,
        original: str,
        result: ScoreWithSuggestion,
        source_language: Language,
        target_language: Language,
        explain_source: bool,
) -> Generator[str, None, None]:
    """Generate an explanation for translations based on user-provided and corrected data."""
    return gpt().ask(
        prompt='\n'.join([
            f'Here is the beginning of a {category.value} in {source_language.name}:',
            f'',
            *initial_sentences,
            f'',
            *(
                explain_source_structure(initial_sentences[-1])
                if explain_source else
                explain_difference(
                    sentence=provided,
                    alternative=alternative,
                    language=target_language,
                )
                if result.score == MAX_SCORE and (alternative := coalesce(
                    if_not(result.suggestion, provided),
                    if_not(original, provided),
                )) else
                explain_mistakes(
                    sentence=provided,
                    corrected=result.suggestion or original,
                    language=target_language,
                )
                if MISTAKE_THRESHOLD_RATIO * MAX_SCORE < result.score < MAX_SCORE else
                explain_structure(
                    sentence=result.suggestion or original,
                    language=target_language,
                )
            ),
            f'',
            f'Be concise. Do not repeat the sentences; start directly with the answer.',
        ]),
        creative=False,
        feeder_type=CharFeeder,
        auto_normalize=False,
    )


def build_text_explainer(
        gpt: Promise[GPTClient],
        sentences: list[SentenceWithTranslation],
        original_translations: list[str],
        results: list[ScoreWithSuggestion],
        source_language: Language,
        target_language: Language,
) -> Callable[[ExplanationRequest], Generator[str, None, None]]:
    """Create a function to generate explanations for text translations."""
    def explain(request: ExplanationRequest) -> Generator[str, None, None]:
        index = request.sentence_index
        return do_explain(
            gpt=gpt,
            category=ContentCategory.TEXT,
            initial_sentences=[sentence.sentence for sentence in sentences[:index + 1]],
            provided=sentences[index].translation.text,
            original=original_translations[index],
            result=results[index],
            source_language=source_language,
            target_language=target_language,
            explain_source=request.source,
        )
    return explain


def build_dialogue_explainer(
        gpt: Promise[GPTClient],
        exchanges: list[ExchangeWithTranslation],
        original_translations: list[DialogueExchangeData],
        results: list[ScoreWithSuggestion],
        source_language: Language,
        target_language: Language,
) -> Callable[[ExplanationRequest], Generator[str, None, None]]:
    """Create a function to generate explanations for dialogue translations."""
    def explain(request: ExplanationRequest) -> Generator[str, None, None]:
        index = request.sentence_index
        return do_explain(
            gpt=gpt,
            category=ContentCategory.DIALOGUE,
            initial_sentences=[turn for exchange in exchanges[:index + 1] for turn in exchange.exchange.all()],
            provided=exchanges[index].user_translation.text,
            original=original_translations[index].user,
            result=results[index],
            source_language=source_language,
            target_language=target_language,
            explain_source=request.source,
        )
    return explain

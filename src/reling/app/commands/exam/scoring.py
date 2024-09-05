from itertools import islice
from typing import Generator

from reling.app.exceptions import AlgorithmException
from reling.db.enums import ContentCategory
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogueExchangeData
from reling.utils.english import pluralize
from reling.utils.iterables import group_items
from reling.utils.transformers import add_numbering, apply, omit_empty, remove_numbering, strip
from .types import ExchangeWithTranslation, ScoreWithSuggestion, SentenceWithTranslation

__all__ = [
    'MAX_SCORE',
    'score_dialogue_translations',
    'score_text_translations',
]

MAX_SCORE = 10
NA = 'N/A'
EMPTY_TRANSLATION = '<empty>'


def build_prompt(
        category: ContentCategory,
        source_language: Language,
        target_language: Language,
        blocks: list[str],
        translations: list[str],
) -> str:
    """Build a prompt for scoring translations."""
    # Speaker turns in dialogues are "graded" as well so that the model appreciates the context.
    n = len(blocks)
    return '\n'.join([
        f'Below {'is' if n == 1 else 'are'} {n} {pluralize('sentence', n)} from a {category.value} '
        f'in {source_language.name} along with {'its' if n == 1 else 'their'} {pluralize('translation', n)} '
        f'into {target_language.name} made by a language learner.',

        f'Score {'the' if n == 1 else 'each'} translation on a scale from 0 to {MAX_SCORE}. '
        f'If {'the' if n == 1 else 'a'} translation is empty, very short, or poor, assign a low score. ',
        f'If the translation is less than perfect, suggest a minimally modified version that would '
        f'deserve a {MAX_SCORE}.',

        f'{'Provide' if n == 1 else 'For each translation, provide'} your feedback on exactly four lines:',
        f'- original sentence on the first line;',  # The first two lines help improve the model's performance
        f'- learner\'s translation on the second line;',
        f'- score (just the number) on the third line;',
        f'- suggested modified translation (or "{NA}") on the fourth line.',

        *([f'Provide this feedback for each of the {n} translations.'] if n > 1 else []),
        f'Say nothing else.',
        f'',
        f'The original {category.value} is:',
        *apply(add_numbering, blocks),
        f'',
        f'The translations are:',
        *apply(add_numbering, [translation.strip() or EMPTY_TRANSLATION for translation in translations]),
    ])


def ask_and_parse(gpt: GPTClient, prompt: str) -> Generator[ScoreWithSuggestion, None, None]:
    """
    Ask the model to score translations and parse the output.
    :raises AlgorithmException: If there is an issue with the output of the model.
    """
    for _, _, string_score, suggestion in group_items(gpt.ask(
        prompt,
        creative=False,
        transformers=[strip, omit_empty, remove_numbering],
    ), 4):
        try:
            score = int(string_score)
        except ValueError:
            raise AlgorithmException(f'Could not parse the score as an integer from the model output: {string_score}.')
        if score < 0 or score > MAX_SCORE:
            raise AlgorithmException(f'The score {score} given by the model is not in the range from 0 to {MAX_SCORE}.')
        yield ScoreWithSuggestion(
            score=score,
            suggestion=suggestion if suggestion != NA and score < MAX_SCORE else None,
        )


def score_text_translations(
        gpt: GPTClient,
        sentences: list[SentenceWithTranslation],
        source_language: Language,
        target_language: Language,
) -> Generator[ScoreWithSuggestion, None, None]:
    """
    Score the translations of a text and provide suggestions for improvement.
    :raises AlgorithmException: If there is an issue with the scoring algorithm.
    """
    prompt = build_prompt(
        category=ContentCategory.TEXT,
        source_language=source_language,
        target_language=target_language,
        blocks=[sentence.sentence for sentence in sentences],
        translations=[sentence.translation.text for sentence in sentences],
    )
    return ask_and_parse(gpt, prompt)


def score_dialogue_translations(
        gpt: GPTClient,
        exchanges: list[ExchangeWithTranslation],
        original_translations: list[DialogueExchangeData],
        source_language: Language,
        target_language: Language,
) -> Generator[ScoreWithSuggestion, None, None]:
    """
    Score the translations of user turns in a dialogue and provide suggestions for improvement.
    :raises AlgorithmException: If there is an issue with the scoring algorithm.
    """
    prompt = build_prompt(
        category=ContentCategory.DIALOGUE,
        source_language=source_language,
        target_language=target_language,
        blocks=[turn for exchange in exchanges for turn in exchange.exchange.all()],
        translations=[turn
                      for exchange, original_translation in zip(exchanges, original_translations)
                      for turn in [original_translation.speaker, exchange.user_translation.text]],
    )
    yield from islice(ask_and_parse(gpt, prompt), 1, None, 2)

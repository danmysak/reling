from tqdm import tqdm

from reling.app.app import app
from reling.app.exceptions import AlgorithmException
from reling.app.translation import get_dialogue_exchanges, get_text_sentences
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM, MODEL
from reling.db.models import Dialogue, Language, Text
from reling.gpt import GPTClient
from reling.utils.time import now
from reling.utils.typer import typer_raise
from .input import collect_dialogue_translations, collect_text_translations
from .presentation import present_dialogue_results, present_text_results
from .scoring import score_dialogue_translations, score_text_translations
from .storage import save_dialogue_exam, save_text_exam
from .types import ExchangeWithTranslation, SentenceWithTranslation

__all__ = [
    'exam',
]


@app.command()
def exam(
        api_key: API_KEY,
        model: MODEL,
        content: CONTENT_ARG,
        from_: LANGUAGE_OPT_FROM = None,
        to: LANGUAGE_OPT = None,
) -> None:
    """
    Test the user's ability to translate content from one language to another.
    If only one language is specified, the content's original language is assumed for the unspecified direction.
    """
    if from_ is None and to is None:
        typer_raise('You must specify at least one language.')
    from_ = from_ or content.language
    to = to or content.language
    if from_ == to:
        typer_raise('The source and target languages are the same.')

    gpt = GPTClient(api_key=api_key, model=model)
    (perform_text_exam if isinstance(content, Text) else perform_dialogue_exam)(gpt, content, from_, to)


def perform_text_exam(
        gpt: GPTClient,
        text: Text,
        source_language: Language,
        target_language: Language,
) -> None:
    sentences = get_text_sentences(gpt, text, source_language)
    original_translations = get_text_sentences(gpt, text, target_language)
    started_at = now()
    translated = list(collect_text_translations(sentences))
    finished_at = now()
    try:
        results = list(tqdm(
            score_text_translations(gpt, translated, source_language, target_language),
            desc='Scoring translations',
            total=len(translated),
        ))
    except AlgorithmException as e:
        typer_raise(e.msg)
    save_text_exam(
        text=text,
        source_language=source_language,
        target_language=target_language,
        started_at=started_at,
        finished_at=finished_at,
        sentences=translated,
        results=results,
    )
    present_text_results(translated, original_translations, results)


def perform_dialogue_exam(
        gpt: GPTClient,
        dialogue: Dialogue,
        source_language: Language,
        target_language: Language,
) -> None:
    exchanges = get_dialogue_exchanges(gpt, dialogue, source_language)
    original_translations = get_dialogue_exchanges(gpt, dialogue, target_language)
    started_at = now()
    translated = list(collect_dialogue_translations(exchanges, original_translations))
    finished_at = now()
    try:
        results = list(tqdm(
            score_dialogue_translations(gpt, translated, original_translations, source_language, target_language),
            desc='Scoring translations',
            total=len(translated),
        ))
    except AlgorithmException as e:
        typer_raise(e.msg)
    save_dialogue_exam(
        dialogue=dialogue,
        source_language=source_language,
        target_language=target_language,
        started_at=started_at,
        finished_at=finished_at,
        exchanges=translated,
        results=results,
    )
    present_dialogue_results(translated, original_translations, results)

from tqdm import tqdm

from reling.app.app import app
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM, MODEL
from reling.db.models import Dialog, Language, Text
from reling.gpt import GPTClient
from reling.utils.time import now
from reling.utils.typer import typer_raise
from .input import collect_dialog_translations, collect_text_translations
from .presentation import present_dialog_results, present_text_results
from .scoring import score_dialog_translations, score_text_translations
from .storage import save_dialog_exam, save_text_exam
from .translation import get_dialog_exchanges, get_text_sentences
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
    (perform_text_exam if isinstance(content, Text) else perform_dialog_exam)(gpt, content, from_, to)


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
    results = list(tqdm(
        score_text_translations(gpt, translated, source_language, target_language),
        desc='Scoring translations',
        total=len(translated),
    ))
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


def perform_dialog_exam(
        gpt: GPTClient,
        dialog: Dialog,
        source_language: Language,
        target_language: Language,
) -> None:
    exchanges = get_dialog_exchanges(gpt, dialog, source_language)
    original_translations = get_dialog_exchanges(gpt, dialog, target_language)
    started_at = now()
    translated = list(collect_dialog_translations(exchanges, original_translations))
    finished_at = now()
    results = list(tqdm(
        score_dialog_translations(gpt, translated, original_translations, source_language, target_language),
        desc='Scoring translations',
        total=len(translated),
    ))
    save_dialog_exam(
        dialog=dialog,
        source_language=source_language,
        target_language=target_language,
        started_at=started_at,
        finished_at=finished_at,
        exchanges=translated,
        results=results,
    )
    present_dialog_results(translated, original_translations, results)

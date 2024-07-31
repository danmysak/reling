from sqlalchemy import exists
from tqdm import tqdm

from reling.app.app import app
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_ARG, MODEL
from reling.db import single_session
from reling.db.models import Dialog, DialogExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.gpt import GPTClient
from reling.types import DialogExchangeData
from reling.utils.typer import typer_raise
from .exceptions import TranslationExistsError
from .storage import save_dialog_translation, save_text_translation
from .translation import translate_dialog, translate_text

__all__ = [
    'translate',
]


@app.command()
def translate(api_key: API_KEY, model: MODEL, content: CONTENT_ARG, language: LANGUAGE_ARG) -> None:
    """Translate a text or dialog into another language."""
    if language.id == content.language_id:
        typer_raise(f'The content is already in {language.name}.')

    (process_text if isinstance(content, Text) else process_dialog)(
        content,
        gpt=GPTClient(api_key=api_key, model=model),
        target_language=language,
    )


def text_has_translation(text: Text, target_language: Language) -> bool:
    """Check if a text has already been translated into a target language."""
    with single_session() as session:
        return session.query(exists().where(
            TextSentenceTranslation.text_id == text.id,
            TextSentenceTranslation.language_id == target_language.id,
        )).scalar()


def dialog_has_translation(dialog: Dialog, target_language: Language) -> bool:
    """Check if a dialog has already been translated into a target language."""
    with single_session() as session:
        return session.query(exists().where(
            DialogExchangeTranslation.dialog_id == dialog.id,
            DialogExchangeTranslation.language_id == target_language.id,
        )).scalar()


def process_text(text: Text, gpt: GPTClient, target_language: Language) -> None:
    """Translate a text into another language."""
    try:
        if text_has_translation(text, target_language):
            raise TranslationExistsError
        sentences = list(tqdm(
            translate_text(
                gpt=gpt,
                sentences=[sentence.sentence for sentence in text.sentences],
                source_language=text.language,
                target_language=target_language,
            ),
            desc='Translating sentences',
            total=len(text.sentences),
        ))
        if len(sentences) != len(text.sentences):
            typer_raise('The number of translated sentences does not match the number of original sentences.')
        save_text_translation(text, target_language, sentences)
    except TranslationExistsError:
        typer_raise(f'The text has already been translated into {target_language.name}.')


def process_dialog(dialog: Dialog, gpt: GPTClient, target_language: Language) -> None:
    """Translate a dialog into another language."""
    try:
        if dialog_has_translation(dialog, target_language):
            raise TranslationExistsError
        exchanges = list(tqdm(
            translate_dialog(
                gpt=gpt,
                exchanges=[
                    DialogExchangeData(
                        speaker=exchange.speaker,
                        user=exchange.user,
                    )
                    for exchange in dialog.exchanges
                ],
                source_language=dialog.language,
                target_language=target_language,
            ),
            desc='Translating exchanges',
            total=len(dialog.exchanges),
        ))
        if len(exchanges) != len(dialog.exchanges):
            typer_raise('The number of translated exchanges does not match the number of original exchanges.')
        save_dialog_translation(dialog, target_language, exchanges)
    except TranslationExistsError:
        typer_raise(f'The dialog has already been translated into {target_language.name}.')

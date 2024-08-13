from typing import cast

from sqlalchemy import ColumnElement, exists
from tqdm import tqdm

from reling.app.exceptions import AlgorithmException
from reling.db import single_session
from reling.db.models import Dialog, DialogExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.gpt import GPTClient
from reling.types import DialogExchangeData
from .exceptions import TranslationExistsException
from .storage import save_dialog_translation, save_text_translation
from .translation import translate_dialog_exchanges, translate_text_sentences

__all__ = [
    'translate_dialog',
    'translate_text',
]


def is_text_translated(text: Text, language: Language) -> bool:
    """Check if a text has already been translated into a target language."""
    with single_session() as session:
        return session.query(exists().where(
            cast(ColumnElement[bool], TextSentenceTranslation.text_id == text.id),
            cast(ColumnElement[bool], TextSentenceTranslation.language_id == language.id),
        )).scalar()


def is_dialog_translated(dialog: Dialog, language: Language) -> bool:
    """Check if a dialog has already been translated into a target language."""
    with single_session() as session:
        return session.query(exists().where(
            cast(ColumnElement[bool], DialogExchangeTranslation.dialog_id == dialog.id),
            cast(ColumnElement[bool], DialogExchangeTranslation.language_id == language.id),
        )).scalar()


def translate_text(gpt: GPTClient, text: Text, language: Language) -> None:
    """
    Translate a text into another language.

    :raises ValueError: If the text is already in the target language.
    :raises TranslationExistsException: If the text has already been translated into the target language.
    :raises AlgorithmException: If there is an issue with the translation algorithm.
    """
    if language.id == text.language_id:
        raise ValueError(f'The text is already in {language.name}.')
    if is_text_translated(text, language):
        raise TranslationExistsException
    sentences = list(tqdm(
        translate_text_sentences(
            gpt=gpt,
            sentences=[sentence.sentence for sentence in text.sentences],
            source_language=text.language,
            target_language=language,
        ),
        desc=f'Translating sentences into {language.name}',
        total=len(text.sentences),
    ))
    if len(sentences) != len(text.sentences):
        raise AlgorithmException(
            'The number of translated sentences does not match the number of original sentences.',
        )
    save_text_translation(text, language, sentences)


def translate_dialog(gpt: GPTClient, dialog: Dialog, language: Language) -> None:
    """
    Translate a dialog into another language.

    :raises ValueError: If the dialog is already in the target language.
    :raises TranslationExistsException: If the dialog has already been translated into the target language.
    :raises AlgorithmException: If there is an issue with the translation algorithm.
    """
    if language.id == dialog.language_id:
        raise ValueError(f'The dialog is already in {language.name}.')
    if is_dialog_translated(dialog, language):
        raise TranslationExistsException
    exchanges = list(tqdm(
        translate_dialog_exchanges(
            gpt=gpt,
            exchanges=[
                DialogExchangeData(
                    speaker=exchange.speaker,
                    user=exchange.user,
                )
                for exchange in dialog.exchanges
            ],
            source_language=dialog.language,
            target_language=language,
        ),
        desc=f'Translating exchanges into {language.name}',
        total=len(dialog.exchanges),
    ))
    if len(exchanges) != len(dialog.exchanges):
        AlgorithmException(
            'The number of translated exchanges does not match the number of original exchanges.',
        )
    save_dialog_translation(dialog, language, exchanges)

from sqlalchemy.exc import IntegrityError

from reling.db import single_session
from reling.db.models import Dialog, DialogExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.types import DialogExchangeData
from .exceptions import TranslationExistsError


__all__ = [
    'save_dialog_translation',
    'save_text_translation',
]


def save_text_translation(
        source_text: Text,
        target_language: Language,
        translated_sentences: list[str],
) -> None:
    """
    Save the translation of a text.
    :raises TranslationExistsError: if the text has already been translated into the target language
    """
    try:
        with single_session() as session:
            session.add_all([
                TextSentenceTranslation(
                    text_id=source_text.id,
                    language_id=target_language.id,
                    text_sentence_index=index,
                    sentence=sentence,
                )
                for index, sentence in enumerate(translated_sentences)
            ])
            session.commit()
    except IntegrityError:
        raise TranslationExistsError


def save_dialog_translation(
        source_dialog: Dialog,
        target_language: Language,
        translated_exchanges: list[DialogExchangeData],
) -> None:
    """
    Save the translation of a dialog.
    :raises TranslationExistsError: if the dialog has already been translated into the target language
    """
    try:
        with single_session() as session:
            session.add_all([
                DialogExchangeTranslation(
                    dialog_id=source_dialog.id,
                    language_id=target_language.id,
                    dialog_exchange_index=index,
                    speaker=exchange.speaker,
                    user=exchange.user,
                )
                for index, exchange in enumerate(translated_exchanges)
            ])
            session.commit()
    except IntegrityError:
        raise TranslationExistsError

from reling.app.exceptions import AlgorithmException
from reling.app.translation import translate_dialog, translate_text, TranslationExistsException
from reling.db import single_session
from reling.db.models import Dialog, DialogExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.gpt import GPTClient
from reling.types import DialogExchangeData
from reling.utils.typer import typer_raise

__all__ = [
    'get_dialog_exchanges',
    'get_text_sentences',
]


def get_text_sentences(gpt: GPTClient, text: Text, language: Language) -> list[str]:
    """Get the sentences of a text in a specified language."""
    if language.id == text.language_id:
        return [sentence.sentence for sentence in text.sentences]
    try:
        translate_text(gpt, text, language)
    except TranslationExistsException:
        pass
    except AlgorithmException as e:
        typer_raise(e.msg)
    with single_session() as session:
        return [
            translation.sentence
            for translation in session.query(TextSentenceTranslation)
            .where(TextSentenceTranslation.text_id == text.id)
            .where(TextSentenceTranslation.language_id == language.id)
            .order_by(TextSentenceTranslation.text_sentence_index)
        ]


def get_dialog_exchanges(gpt: GPTClient, dialog: Dialog, language: Language) -> list[DialogExchangeData]:
    """Get the exchanges of a dialog in a specified language."""
    if language.id == dialog.language_id:
        return [
            DialogExchangeData(
                speaker=exchange.speaker,
                user=exchange.user,
            )
            for exchange in dialog.exchanges
        ]
    try:
        translate_dialog(gpt, dialog, language)
    except TranslationExistsException:
        pass
    except AlgorithmException as e:
        typer_raise(e.msg)
    with single_session() as session:
        return [
            DialogExchangeData(
                speaker=translation.speaker,
                user=translation.user,
            )
            for translation in session.query(DialogExchangeTranslation)
            .where(DialogExchangeTranslation.dialog_id == dialog.id)
            .where(DialogExchangeTranslation.language_id == language.id)
            .order_by(DialogExchangeTranslation.dialog_exchange_index)
        ]

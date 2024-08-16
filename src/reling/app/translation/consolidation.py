from reling.app.exceptions import AlgorithmException
from reling.db import single_session
from reling.db.models import Dialogue, DialogueExchangeTranslation, Language, Text, TextSentenceTranslation
from reling.gpt import GPTClient
from reling.types import DialogueExchangeData
from reling.utils.typer import typer_raise
from .exceptions import TranslationExistsException
from .operation import translate_dialogue, translate_text

__all__ = [
    'get_dialogue_exchanges',
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


def get_dialogue_exchanges(gpt: GPTClient, dialogue: Dialogue, language: Language) -> list[DialogueExchangeData]:
    """Get the exchanges of a dialogue in a specified language."""
    if language.id == dialogue.language_id:
        return [
            DialogueExchangeData(
                speaker=exchange.speaker,
                user=exchange.user,
            )
            for exchange in dialogue.exchanges
        ]
    try:
        translate_dialogue(gpt, dialogue, language)
    except TranslationExistsException:
        pass
    except AlgorithmException as e:
        typer_raise(e.msg)
    with single_session() as session:
        return [
            DialogueExchangeData(
                speaker=translation.speaker,
                user=translation.user,
            )
            for translation in session.query(DialogueExchangeTranslation)
            .where(DialogueExchangeTranslation.dialogue_id == dialogue.id)
            .where(DialogueExchangeTranslation.language_id == language.id)
            .order_by(DialogueExchangeTranslation.dialogue_exchange_index)
        ]
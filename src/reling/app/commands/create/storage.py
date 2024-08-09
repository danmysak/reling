from itertools import count

from reling.db import single_session
from reling.db.enums import ContentCategory, Level
from reling.db.helpers.ids import find_ids_by_prefix
from reling.db.models import Dialog, DialogExchange, IdIndex, Language, Text, TextSentence
from reling.types import DialogExchangeData
from reling.utils.time import now


__all__ = [
    'save_dialog',
    'save_text',
]


def generate_id(suggested_id: str) -> str:
    """Generate a unique ID based on the suggested ID."""
    taken_ids = set(find_ids_by_prefix(suggested_id))
    if suggested_id not in taken_ids:
        return suggested_id
    for suffix in count(2):
        if (suffixed_id := f'{suggested_id}-{suffix}') not in taken_ids:
            return suffixed_id


def save_text(
        suggested_id: str,
        sentences: list[str],
        language: Language,
        level: Level,
        topic: str,
        style: str,
) -> str:
    """Save a text with the given sentences and return its ID."""
    with single_session() as session:
        text_id = generate_id(suggested_id)
        text = Text(
            id=text_id,
            language_id=language.id,
            level=level,
            topic=topic,
            style=style,
            created_at=now(),
            archived_at=None,
        )
        session.add(text)
        session.add_all([
            TextSentence(
                text_id=text.id,
                index=index,
                sentence=sentence,
            )
            for index, sentence in enumerate(sentences)
        ])
        session.add(IdIndex(
            id=text_id,
            category=ContentCategory.TEXT,
        ))
        session.commit()
    return text_id


def save_dialog(
        suggested_id: str,
        exchanges: list[DialogExchangeData],
        language: Language,
        level: Level,
        speaker: str,
        topic: str | None,
) -> str:
    """Save a dialog with the given exchanges and return its ID."""
    with single_session() as session:
        dialog_id = generate_id(suggested_id)
        dialog = Dialog(
            id=dialog_id,
            language_id=language.id,
            level=level,
            topic=topic,
            speaker=speaker,
            created_at=now(),
            archived_at=None,
        )
        session.add(dialog)
        session.add_all([
            DialogExchange(
                dialog_id=dialog.id,
                index=index,
                speaker=exchange.speaker,
                user=exchange.user,
            )
            for index, exchange in enumerate(exchanges)
        ])
        session.add(IdIndex(
            id=dialog_id,
            category=ContentCategory.DIALOG,
        ))
        session.commit()
    return dialog_id

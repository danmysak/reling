from sqlalchemy import ColumnElement

from reling.db.models import DialogueExam, Language, TextExam
from .modalities import Modality

__all__ = [
    'get_filter',
]


def get_filter(language: Language, modality: Modality, model: type[TextExam | DialogueExam]) -> ColumnElement[bool]:
    """Get the filtering condition for the given language, modality, and model."""
    return (model.source_language_id if modality == Modality.COMPREHENSION else model.target_language_id) == language.id

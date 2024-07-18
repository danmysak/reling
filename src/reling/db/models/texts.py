from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..enums import Level
from .languages import Language

__all__ = [
    'Text',
    'TextExam',
    'TextExamResult',
    'TextSentence',
    'TextSentenceTranslation',
]


class Text(Base):
    __tablename__ = 'texts'

    id: Mapped[str] = mapped_column(primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    level: Mapped[Level]
    topic: Mapped[str]
    style: Mapped[str]
    created_at: Mapped[datetime]
    archived_at: Mapped[datetime | None] = mapped_column(index=True)


class TextSentence(Base):
    __tablename__ = 'text_sentences'

    text_id: Mapped[str] = mapped_column(ForeignKey(Text.id, ondelete='CASCADE'), primary_key=True)
    index: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]


class TextSentenceTranslation(Base):
    __tablename__ = 'text_sentence_translations'

    text_id: Mapped[str] = mapped_column(ForeignKey(Text.id, ondelete='CASCADE'), primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id), primary_key=True)
    text_sentence_index: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]


class TextExam(Base):
    __tablename__ = 'text_exams'

    id: Mapped[str] = mapped_column(primary_key=True)
    text_id: Mapped[str] = mapped_column(ForeignKey(Text.id, ondelete='CASCADE'))
    source_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    target_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime]


class TextExamResult(Base):
    __tablename__ = 'text_exam_results'

    text_exam_id: Mapped[str] = mapped_column(ForeignKey(TextExam.id, ondelete='CASCADE'), primary_key=True)
    text_sentence_index: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]
    suggested_answer: Mapped[str]
    score: Mapped[int]

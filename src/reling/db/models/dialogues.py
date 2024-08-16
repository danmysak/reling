from __future__ import annotations
from datetime import datetime

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from reling.db.base import Base
from reling.db.enums import Level, Sex
from .languages import Language

__all__ = [
    'Dialogue',
    'DialogueExam',
    'DialogueExamResult',
    'DialogueExchange',
    'DialogueExchangeTranslation',
]


class Dialogue(Base):
    __tablename__ = 'dialogues'

    id: Mapped[str] = mapped_column(primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    language: Mapped[Language] = relationship(Language)
    level: Mapped[Level]
    speaker: Mapped[str]
    topic: Mapped[str | None]
    speaker_sex: Mapped[Sex]
    user_sex: Mapped[Sex]
    created_at: Mapped[datetime]
    archived_at: Mapped[datetime | None]
    exchanges: Mapped[list[DialogueExchange]] = relationship(
        'DialogueExchange',
        order_by='DialogueExchange.index',
        passive_deletes=True,
    )
    exchange_translations: Mapped[list[DialogueExchangeTranslation]] = relationship(
        'DialogueExchangeTranslation',
        passive_deletes=True,
    )
    exams: Mapped[list[DialogueExam]] = relationship('DialogueExam', passive_deletes=True)

    __table_args__ = (
        Index('dialogue_chronological', 'archived_at', 'created_at'),
    )


class DialogueExchange(Base):
    __tablename__ = 'dialogue_exchanges'

    dialogue_id: Mapped[str] = mapped_column(
        ForeignKey(Dialogue.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    index: Mapped[int] = mapped_column(primary_key=True)
    speaker: Mapped[str]
    user: Mapped[str]


class DialogueExchangeTranslation(Base):
    __tablename__ = 'dialogue_exchange_translations'

    dialogue_id: Mapped[str] = mapped_column(
        ForeignKey(Dialogue.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id), primary_key=True)
    dialogue_exchange_index: Mapped[int] = mapped_column(primary_key=True)
    speaker: Mapped[str]
    user: Mapped[str]


class DialogueExam(Base):
    __tablename__ = 'dialogue_exams'

    id: Mapped[str] = mapped_column(primary_key=True)
    dialogue_id: Mapped[str] = mapped_column(ForeignKey(Dialogue.id, onupdate='CASCADE', ondelete='CASCADE'))
    source_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    source_language: Mapped[Language] = relationship(Language, foreign_keys=source_language_id)
    target_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    target_language: Mapped[Language] = relationship(Language, foreign_keys=target_language_id)
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime]
    results: Mapped[list[DialogueExamResult]] = relationship(
        'DialogueExamResult',
        order_by='DialogueExamResult.dialogue_exchange_index',
        passive_deletes=True,
    )


class DialogueExamResult(Base):
    __tablename__ = 'dialogue_exam_results'

    dialogue_exam_id: Mapped[str] = mapped_column(
        ForeignKey(DialogueExam.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    dialogue_exchange_index: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]
    suggested_answer: Mapped[str | None]
    score: Mapped[int]
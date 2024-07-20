from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..enums import Level
from .languages import Language

__all__ = [
    'Dialog',
    'DialogExam',
    'DialogExamResult',
    'DialogExchange',
    'DialogExchangeTranslation',
]


class Dialog(Base):
    __tablename__ = 'dialogs'

    id: Mapped[str] = mapped_column(primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    level: Mapped[Level]
    topic: Mapped[str | None]
    speaker: Mapped[str]
    created_at: Mapped[datetime]
    archived_at: Mapped[datetime | None] = mapped_column(index=True)


class DialogExchange(Base):
    __tablename__ = 'dialog_exchanges'

    dialog_id: Mapped[str] = mapped_column(ForeignKey(Dialog.id, ondelete='CASCADE'), primary_key=True)
    index: Mapped[int] = mapped_column(primary_key=True)
    speaker: Mapped[str]
    self: Mapped[str]


class DialogExchangeTranslation(Base):
    __tablename__ = 'dialog_exchange_translations'

    dialog_id: Mapped[str] = mapped_column(ForeignKey(Dialog.id, ondelete='CASCADE'), primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey(Language.id), primary_key=True)
    dialog_exchange_index: Mapped[int] = mapped_column(primary_key=True)
    speaker: Mapped[str]
    self: Mapped[str]


class DialogExam(Base):
    __tablename__ = 'dialog_exams'

    id: Mapped[str] = mapped_column(primary_key=True)
    dialog_id: Mapped[str] = mapped_column(ForeignKey(Dialog.id, ondelete='CASCADE'))
    source_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    target_language_id: Mapped[str] = mapped_column(ForeignKey(Language.id))
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime]


class DialogExamResult(Base):
    __tablename__ = 'dialog_exam_results'

    dialog_exam_id: Mapped[str] = mapped_column(ForeignKey(DialogExam.id, ondelete='CASCADE'), primary_key=True)
    dialog_exchange_index: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]
    suggested_answer: Mapped[str]
    score: Mapped[int]

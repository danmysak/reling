from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from . import models  # Register models with SQLAlchemy
from .base import Base

__all__ = [
    'init_db',
    'single_session',
]

SESSION: Session | None = None


def init_db(url: str) -> None:
    global SESSION
    if SESSION is None:
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        SESSION = Session(engine)


@contextmanager
def single_session() -> Generator[Session, None, None]:
    if SESSION is None:
        raise RuntimeError('Database is not initialized')
    try:
        yield SESSION
    except Exception:
        SESSION.rollback()
        raise

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from . import models  # Register models with SQLAlchemy
from .base import Base

__all__ = [
    'init_db',
    'single_session',
]

ENGINE: Engine | None = None
SESSION: Session | None = None


def init_db(url: str) -> None:
    global ENGINE
    if ENGINE is None:
        ENGINE = create_engine(url)
        Base.metadata.create_all(ENGINE)


@contextmanager
def single_session() -> Generator[Session, None, None]:
    global SESSION
    if SESSION is not None:
        yield SESSION
        return
    if ENGINE is None:
        raise RuntimeError('Database engine is not initialized')
    try:
        with Session(ENGINE) as session:
            SESSION = session
            yield session
    finally:
        SESSION = None

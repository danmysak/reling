from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from . import models  # Register models with SQLAlchemy
from .base import Base

__all__ = [
    'init_db',
    'start_session',
]

ENGINE: Engine | None = None


def init_db(url: str) -> None:
    global ENGINE
    if ENGINE is None:
        ENGINE = create_engine(url)
        Base.metadata.create_all(ENGINE)


@contextmanager
def start_session() -> Generator[Session, None, None]:
    if ENGINE is None:
        raise RuntimeError('Database engine is not initialized')
    with Session(ENGINE) as session:
        yield session

from pathlib import Path

from sqlalchemy.sql import exists, func

from ...utils.csv import read_csv
from .. import start_session
from ..models import Language

__all__ = [
    'find_language',
    'populate_languages',
]


def populate_languages(data: Path) -> None:
    """Populate the languages table with data from the CSV file, if it is empty."""
    with start_session() as session:
        if not session.query(exists().where(Language.id.isnot(None))).scalar():
            for language in read_csv(
                data,
                ['id', 'short_code', 'name', 'extra_name_a', 'extra_name_b'],
                empty_as_none=True,
            ):
                session.add(Language(**language))
            session.commit()


def find_language(language: str) -> Language | None:
    """Find a language, either by its id, short code, or name (case-insensitive), applying filters sequentially."""
    lower = func.lower(language)
    conditions = [
        Language.id == language,
        Language.short_code == language,
        func.lower(Language.name) == lower,
        func.lower(Language.extra_name_a) == lower,
        func.lower(Language.extra_name_b) == lower,
    ]

    with start_session() as session:
        for condition in conditions:
            if result := session.query(Language).filter(condition).first():
                return result

    return None

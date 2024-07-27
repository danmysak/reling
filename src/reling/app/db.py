from pathlib import Path

from reling.db import init_db as do_init_db

__all__ = [
    'get_db_path',
    'init_db',
]

DB_PATH: Path | None = None


def init_db(path: Path) -> None:
    global DB_PATH
    if DB_PATH is not None:
        raise RuntimeError('Database is already initialized')
    DB_PATH = path
    do_init_db(f'sqlite:///{DB_PATH}')


def get_db_path() -> Path:
    if DB_PATH is None:
        raise RuntimeError('Database is not initialized')
    return DB_PATH

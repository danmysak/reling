from pathlib import Path

from ..db import init_db
from ..db.helpers.languages import populate_languages
from ..utils.paths import get_app_data_parent
from . import commands  # Register commands with Typer
from .app import app

__all__ = [
    'app',
]

APP_NAME = 'ReLing'
DB_NAME = 'reling.db'

LANGUAGE_DATA_PATH = Path(__file__).parent / 'data' / 'languages.csv'


@app.callback()
def initialize() -> None:
    data_path = get_app_data_parent() / APP_NAME
    data_path.mkdir(parents=True, exist_ok=True)
    db_path = data_path / DB_NAME
    init_db(f'sqlite:///{db_path}')
    populate_languages(LANGUAGE_DATA_PATH)

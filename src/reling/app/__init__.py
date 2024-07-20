from ..db.helpers.languages import populate_languages
from ..utils.paths import get_app_data_parent
from . import commands  # Register commands with Typer
from .app import app
from .db import init_db

__all__ = [
    'app',
]

APP_NAME = 'ReLing'
DB_NAME = 'reling.db'


@app.callback()
def initialize() -> None:
    data_path = get_app_data_parent() / APP_NAME
    data_path.mkdir(parents=True, exist_ok=True)
    init_db(data_path / DB_NAME)
    populate_languages()

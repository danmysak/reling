from reling.data import LANGUAGES_PATH, SPEAKERS_PATH, STYLES_PATH, TOPICS_PATH
from reling.db.helpers.languages import populate_languages
from reling.db.helpers.modifiers import populate_modifiers
from reling.db.models import Speaker, Style, Topic
from reling.utils.paths import get_app_data_parent
from . import commands  # Register commands with Typer
from .app import app
from .db import init_db

__all__ = [
    'app',
]

APP_NAME = 'ReLing'
DB_NAME = 'reling.db'

# This code must run both during app execution and on auto-completion.
# Therefore, it should be placed at the top level of the module.
DATA_PATH = get_app_data_parent() / APP_NAME
DATA_PATH.mkdir(parents=True, exist_ok=True)
init_db(DATA_PATH / DB_NAME)
populate_languages(LANGUAGES_PATH)
populate_modifiers(Topic, TOPICS_PATH)
populate_modifiers(Style, STYLES_PATH)
populate_modifiers(Speaker, SPEAKERS_PATH)

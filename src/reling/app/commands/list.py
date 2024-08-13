from reling.app.app import app
from reling.app.types import (
    ARCHIVE_OPT,
    CONTENT_CATEGORY_OPT,
    LANGUAGE_OPT,
    LANGUAGE_OPT_FROM,
    LEVEL_OPT,
    NAMES_ONLY_OPT,
    REGEX_OPT,
)

__all__ = [
    'list_',
]


@app.command(name='list')
def list_(
        category: CONTENT_CATEGORY_OPT = None,
        archive: ARCHIVE_OPT = False,
        level: LEVEL_OPT = None,
        from_: LANGUAGE_OPT_FROM = None,
        to: LANGUAGE_OPT = None,
        search: REGEX_OPT = None,
        names_only: NAMES_ONLY_OPT = False,
) -> None:
    """List texts and/or dialogs, optionally filtered by name or other criteria."""
    pass

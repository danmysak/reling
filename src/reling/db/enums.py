from enum import StrEnum

__all__ = [
    'ContentCategory',
    'Level',
]


class ContentCategory(StrEnum):
    TEXT = 'text'
    DIALOG = 'dialog'


class Level(StrEnum):
    BASIC = 'basic'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

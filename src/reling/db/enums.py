from enum import Enum, StrEnum

__all__ = [
    'ContentCategory',
    'Level',
]


class ContentCategory(StrEnum):
    TEXT = 'text'
    DIALOG = 'dialog'


class Level(Enum):
    BASIC = 0
    INTERMEDIATE = 1
    ADVANCED = 2

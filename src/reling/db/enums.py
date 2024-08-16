from enum import StrEnum

__all__ = [
    'ContentCategory',
    'Level',
    'Sex',
]


class ContentCategory(StrEnum):
    TEXT = 'text'
    DIALOG = 'dialog'


class Level(StrEnum):
    BASIC = 'basic'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'


class Sex(StrEnum):
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'

    def describe(self) -> str:
        match self:
            case Sex.MALE:
                return 'a male'
            case Sex.FEMALE:
                return 'a female'
            case Sex.NONBINARY:
                return 'a nonbinary person'

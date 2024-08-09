from dataclasses import dataclass

from reling.types import DialogExchangeData

__all__ = [
    'ExchangeWithTranslation',
    'ScoreWithSuggestion',
    'SentenceWithTranslation',
]


@dataclass
class SentenceWithTranslation:
    sentence: str
    translation: str


@dataclass
class ExchangeWithTranslation:
    exchange: DialogExchangeData
    user_translation: str


@dataclass
class ScoreWithSuggestion:
    score: int
    suggestion: str | None

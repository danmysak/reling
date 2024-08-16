from dataclasses import dataclass

from reling.types import DialogueExchangeData

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
    exchange: DialogueExchangeData
    user_translation: str


@dataclass
class ScoreWithSuggestion:
    score: int
    suggestion: str | None

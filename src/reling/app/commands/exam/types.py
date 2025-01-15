from dataclasses import dataclass

from reling.types import DialogueExchangeData, Input

__all__ = [
    'ExchangeWithTranslation',
    'ExplanationRequest',
    'PreScoreWithSuggestion',
    'ScoreWithSuggestion',
    'SentenceWithTranslation',
]


@dataclass
class SentenceWithTranslation:
    sentence: str
    translation: Input | None


@dataclass
class ExchangeWithTranslation:
    exchange: DialogueExchangeData
    user_translation: Input | None


@dataclass
class PreScoreWithSuggestion:
    score: int
    suggestion: str | None


@dataclass
class ScoreWithSuggestion:
    score: int
    suggestion: str | None


@dataclass
class ExplanationRequest:
    sentence_index: int
    source: bool

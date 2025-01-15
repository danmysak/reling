from __future__ import annotations

from lcs2 import lcs_length

FUZZY_RATIO = 0.61


class FuzzyWord:
    """
    A class representing a word for fuzzy comparison.
    Two words are considered equal if they share at least FUZZY_RATIO of their characters, ignoring case.
    """
    _normalized: str

    def __init__(self, word: str) -> None:
        self._normalized = word.lower()

    def __eq__(self, other: FuzzyWord) -> bool:
        return (2 * lcs_length(self._normalized, other._normalized)
                >= (len(self._normalized) + len(other._normalized)) * FUZZY_RATIO)

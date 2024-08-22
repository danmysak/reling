from __future__ import annotations
from enum import Enum

__all__ = [
    'InvalidTTSFlagCombination',
    'TTSSpeed',
]


class InvalidTTSFlagCombination(ValueError):
    """Raised when multiple reading speeds are specified."""
    pass


class TTSSpeed(Enum):
    SLOW = 0.5
    NORMAL = 1.0
    FAST = 1.75

    @staticmethod
    def from_flags(slow: bool, normal: bool, fast: bool) -> TTSSpeed | None:
        """
        Get the TTS speed from the flags.
        :raises InvalidTTSFlagCombination: If multiple reading speeds are specified.
        """
        if sum([slow, normal, fast]) > 1:
            raise InvalidTTSFlagCombination()
        if slow:
            return TTSSpeed.SLOW
        if normal:
            return TTSSpeed.NORMAL
        if fast:
            return TTSSpeed.FAST
        return None

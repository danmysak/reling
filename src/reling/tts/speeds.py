from __future__ import annotations
from enum import Enum

from reling.utils.typer import typer_raise

__all__ = [
    'TTSSpeed',
]


class TTSSpeed(Enum):
    SLOW = 0.5
    NORMAL = 1.0
    FAST = 1.75

    @staticmethod
    def from_flags(slow: bool, normal: bool, fast: bool) -> TTSSpeed | None:
        """Get the TTS speed from the flags."""
        if sum([slow, normal, fast]) > 1:
            typer_raise('Only one reading speed can be specified at a time.')
        if slow:
            return TTSSpeed.SLOW
        if normal:
            return TTSSpeed.NORMAL
        if fast:
            return TTSSpeed.FAST
        return None

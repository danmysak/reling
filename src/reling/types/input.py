from dataclasses import dataclass
from pathlib import Path

__all__ = [
    'Input',
]


@dataclass
class Input:
    text: str
    audio: Path | None = None

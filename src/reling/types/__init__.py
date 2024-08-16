from dataclasses import dataclass
from typing import Self

__all__ = [
    'DialogExchangeData',
    'WordWithSense',
]


@dataclass
class DialogExchangeData:
    speaker: str
    user: str

    @staticmethod
    def assert_speaker_comes_first() -> None:
        pass

    def all(self) -> tuple[str, str]:
        return self.speaker, self.user


@dataclass
class WordWithSense:
    word: str
    sense: str | None

    DIVIDER_WITH_WHITE_SPACE = ': '

    @classmethod
    def parse(cls, text: str) -> Self:
        divider = cls.DIVIDER_WITH_WHITE_SPACE.strip()
        if divider in text:
            word, sense = text.split(divider, 1)
            return cls(word.strip(), sense.strip())
        else:
            return cls(text.strip(), None)

    def format(self) -> str:
        return f'"{self.word}"' + (f' ({self.sense})' if self.sense else '')

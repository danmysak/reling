from dataclasses import dataclass

__all__ = [
    'DialogExchangeData',
]


@dataclass
class DialogExchangeData:
    speaker: str
    user: str

    def all(self) -> tuple[str, str]:
        return self.speaker, self.user

from pathlib import Path
import re

from openai import OpenAI

from reling.db.models import Language
from reling.types import Transcriber
from reling.utils.openai import openai_handler

__all__ = [
    'ASRClient',
]


class ASRClient:
    _client: OpenAI
    _model: str

    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    @staticmethod
    def _normalize_transcription(text: str) -> str:
        return re.sub(
            r'^([a-z]+|[A-Z]+)[\'’]?(?=[A-Z][a-z]+([.?!,;:]|\s))',  # Remove extra prefixes that Whisper sometimes adds
            '',
            ''.join(char for char in text.strip()
                    if not (0xE000 <= ord(char) <= 0xF8FF))  # Strip private use area characters from the Whisper output
        ).capitalize()

    def transcribe(self, file: Path, language: Language | None = None, context: str | None = None) -> str:
        """Transcribe an audio file."""
        with openai_handler():
            return self._normalize_transcription(self._client.audio.transcriptions.create(
                file=file.open('rb'),
                model=self._model,
                language=language.short_code if language else None,
                prompt=context,
            ).text)

    def get_transcriber(self, language: Language | None = None, context: str | None = None) -> Transcriber:
        def transcribe(file: Path) -> str:
            return self.transcribe(file, language, context)
        return transcribe

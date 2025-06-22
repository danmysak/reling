from typing import Literal

from openai import OpenAI

from reling.db.models import Language
from reling.helpers.openai import openai_handler
from reling.helpers.pyaudio import get_audio, get_stream
from reling.types import Speed
from .tts_client import TTSClient
from .voices import Voice

__all__ = [
    'OpenAITTSClient',
]

CHANNELS = 1
RATE = 24000
CHUNK_SIZE = 1024
RESPONSE_FORMAT: Literal['pcm'] = 'pcm'


class OpenAITTSClient(TTSClient):
    _client: OpenAI
    _model: str
    _language: Language

    def __init__(self, *, api_key: str, model: str, language: Language) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._language = language

    def read(self, text: str, voice: Voice, speed: Speed) -> None:
        with (
            get_audio() as pyaudio,
            get_stream(
                pyaudio=pyaudio,
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                output=True,
            ) as stream,
            openai_handler(),
        ):
            response = self._client.audio.speech.create(
                model=self._model,
                voice=voice.value,  # type: ignore
                response_format=RESPONSE_FORMAT,
                input=text,
                speed=speed.value,
                instructions=f'Read in {self._language.name}.',
            )
            stream.write(response.content)

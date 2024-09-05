from __future__ import annotations

from openai import OpenAI

from reling.helpers.pyaudio import get_audio, get_stream
from reling.types import Reader, Speed
from reling.utils.openai import openai_handler
from .voices import Voice

__all__ = [
    'TTSClient',
    'TTSVoiceClient',
    'Voice',
]

CHANNELS = 1
RATE = 24000
CHUNK_SIZE = 1024
RESPONSE_FORMAT = 'pcm'


class TTSClient:
    _client: OpenAI
    _model: str

    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def read(self, text: str, voice: Voice, speed: Speed) -> None:
        """Read the text in real time using the specified voice."""
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
            self._client.audio.speech.with_streaming_response.create(
                model=self._model,
                voice=voice.value,
                response_format=RESPONSE_FORMAT,
                input=text,
                speed=speed.value,
            ) as response,
        ):
            for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                stream.write(chunk)

    def with_voice(self, voice: Voice) -> TTSVoiceClient:
        return TTSVoiceClient(self, voice)


class TTSVoiceClient:
    """A wrapper around TTSClient with a specific voice."""
    _tts: TTSClient
    _voice: Voice

    def __init__(self, tts: TTSClient, voice: Voice) -> None:
        self._tts = tts
        self._voice = voice

    def get_reader(self, text: str) -> Reader:
        def read(speed: Speed) -> None:
            self._tts.read(text, self._voice, speed)
        return read

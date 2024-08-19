from time import sleep

from openai import OpenAI

from reling.utils.openai import openai_handler
from .voices import Voice

__all__ = [
    'TTSClient',
    'Voice',
]

CHANNELS = 1
RATE = 24000

RESPONSE_FORMAT = 'pcm'
CHUNK_SIZE = 1024

SLEEP_BEFORE_CLOSE_SEC = 0.5  # This allows the last chunk to be played properly


class TTSClient:
    _client: OpenAI
    _model: str

    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def read(self, text: str, voice: Voice) -> None:
        import pyaudio
        player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, output=True)

        with openai_handler(), self._client.audio.speech.with_streaming_response.create(
                model=self._model,
                voice=voice.value,
                response_format=RESPONSE_FORMAT,
                input=text,
        ) as response:
            for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                player_stream.write(chunk)

        sleep(SLEEP_BEFORE_CLOSE_SEC)
        player_stream.stop_stream()
        player_stream.close()

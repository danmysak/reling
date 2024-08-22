from time import sleep

from openai import OpenAI

from reling.utils.openai import openai_handler
from .speeds import InvalidTTSFlagCombination, TTSSpeed
from .voices import Voice

__all__ = [
    'InvalidTTSFlagCombination',
    'TTSClient',
    'TTSSpeed',
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
    _speed: TTSSpeed

    def __init__(self, *, api_key: str, model: str, speed: TTSSpeed = TTSSpeed.NORMAL) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._speed = speed

    def read(self, text: str, voice: Voice) -> None:
        """Read the text in real time using the specified voice."""
        import pyaudio  # Only import this module if TTS is used
        player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, output=True)

        with openai_handler(), self._client.audio.speech.with_streaming_response.create(
            model=self._model,
            voice=voice.value,
            response_format=RESPONSE_FORMAT,
            input=text,
            speed=self._speed.value,
        ) as response:
            for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                player_stream.write(chunk)

        sleep(SLEEP_BEFORE_CLOSE_SEC)
        player_stream.stop_stream()
        player_stream.close()

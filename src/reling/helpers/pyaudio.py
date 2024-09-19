from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
from time import sleep
from typing import Callable, Generator, Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from pyaudio import PyAudio, Stream

from reling.utils.typer import typer_raise

__all__ = [
    'ensure_pyaudio',
    'get_audio',
    'get_stream',
    'PyAudioData'
]

OUTPUT_STOP_DELAY_SEC = 0.5  # This helps avoid audio glitches at the end of playback


@dataclass
class PyAudioData:
    audio: PyAudio
    paInt16: int
    paContinue: int
    paFramesPerBufferUnspecified: int


def ensure_pyaudio() -> None:
    """Ensure PyAudio is installed."""
    try:
        import pyaudio
    except ImportError:
        typer_raise('PyAudio could not be imported. See Readme for installation instructions.')


@contextmanager
def get_audio() -> Generator[PyAudioData, None, None]:
    """Dynamically import PyAudio and yield it, closing it afterward."""
    import pyaudio  # Only import this module if audio is used
    audio = pyaudio.PyAudio()
    try:
        yield PyAudioData(
            audio,
            paInt16=pyaudio.paInt16,
            paContinue=pyaudio.paContinue,
            paFramesPerBufferUnspecified=pyaudio.paFramesPerBufferUnspecified,
        )
    finally:
        audio.terminate()


@contextmanager
def get_stream(
        pyaudio: PyAudioData,
        format: int,  # noqa
        channels: int,
        rate: int,
        input: bool = False,  # noqa
        output: bool = False,
        frames_per_buffer: int | None = None,
        stream_callback: Callable[[bytes, int, Mapping[str, float], int], tuple[bytes | None, int]] | None = None,
) -> Generator[Stream, None, None]:
    """Create a PyAudio stream and yield it, closing it afterward."""
    stream = pyaudio.audio.open(
        format=format,
        channels=channels,
        rate=rate,
        input=input,
        output=output,
        frames_per_buffer=frames_per_buffer if frames_per_buffer is not None else pyaudio.paFramesPerBufferUnspecified,
        stream_callback=stream_callback,
    )
    try:
        yield stream
    finally:
        if output:
            sleep(OUTPUT_STOP_DELAY_SEC)
        stream.stop_stream()
        stream.close()
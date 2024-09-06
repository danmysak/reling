from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from tempfile import mkstemp

from reling.helpers.wave import FILE_EXTENSION, play, record
from reling.types import Input, Transcriber
from reling.utils.console import clear_previous, input_and_erase, print_and_erase
from reling.utils.prompts import ENTER, Prompt

__all__ = [
    'get_input',
    'TranscriberParams',
]

ENTER_TO_START_RECORDING = f'({ENTER} to start recording)'
RECORDING_UNTIL_ENTER = f'(recording... {ENTER} to stop)'
TRANSCRIBING = '(transcribing...)'


class Action(StrEnum):
    RE_RECORD = 're-record'
    LISTEN = 'listen'
    MANUAL_INPUT = 'manual input'


@dataclass
class TranscriberParams:
    transcribe: Transcriber
    storage: Path


def get_manual_input(prompt: str) -> Input:
    return Input(input(prompt))


def get_temp_file(storage: Path) -> Path:
    return Path(mkstemp(dir=storage, suffix=FILE_EXTENSION)[1])


def do_record(prompt: str, file: Path) -> None:
    with record(file):
        input_and_erase(prompt + RECORDING_UNTIL_ENTER)


def do_transcribe(prompt: str, transcribe: Transcriber, file: Path) -> str:
    with print_and_erase(prompt + TRANSCRIBING):
        return transcribe(file)


def get_audio_input(prompt: str, params: TranscriberParams) -> Input:
    """Get input from the user via audio recording, with optional re-recording, listening, and manual input."""
    input_and_erase(prompt + ENTER_TO_START_RECORDING)
    file = get_temp_file(params.storage)
    while True:
        do_record(prompt, file)
        transcription = do_transcribe(prompt, params.transcribe, file)
        print(prompt + transcription)
        while True:
            match Prompt.from_enum(Action).prompt():
                case Action.RE_RECORD:
                    clear_previous()
                    break
                case Action.LISTEN:
                    play(file)
                case Action.MANUAL_INPUT:
                    clear_previous()
                    return get_manual_input(prompt)
                case None:
                    return Input(transcription, audio=file)
                case _:
                    assert False


def get_input(prompt: str = '', transcriber_params: TranscriberParams | None = None) -> Input:
    """Get input from the user, optionally via audio recording."""
    return get_audio_input(prompt, transcriber_params) if transcriber_params else get_manual_input(prompt)

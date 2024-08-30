from __future__ import annotations
from dataclasses import dataclass

from reling.utils.prompts import enter_to_continue, Prompt, PromptOption
from reling.tts import TTSVoiceClient
from reling.types import Reader, Speed
from reling.utils.console import clear_current_line
from reling.utils.types import ensure_not_none

__all__ = [
    'output',
    'SentenceData',
]

PROMPT_TITLE = 'Play'
NORMAL_SPEED = 'normal speed'
SLOWLY = 'slowly'
REPLAY = 'replay'


@dataclass
class SentenceData:
    text: str
    print_prefix: str = ''
    reader: Reader | None = None
    reader_id: str | None = None

    @staticmethod
    def from_tts(
            text: str,
            client: TTSVoiceClient | None,
            *,
            print_prefix: str = '',
            reader_id: str | None = None,
    ) -> SentenceData:
        return SentenceData(
            text=text,
            print_prefix=print_prefix,
            reader=client.get_reader(text) if client else None,
            reader_id=reader_id,
        )


@dataclass
class ReaderWithSpeed:
    reader: Reader
    speed: Speed


@dataclass
class ReaderWithId:
    reader: Reader
    id: str


def add_single_sentence_options(prompt: Prompt[ReaderWithSpeed], reader: Reader) -> None:
    """Attach the options for a single sentence to the prompt: '[n]ormal speed | [s]lowly'."""
    prompt.add_option(PromptOption(
        description=NORMAL_SPEED,
        action=ReaderWithSpeed(reader, Speed.NORMAL),
    ))
    prompt.add_option(PromptOption(
        description=SLOWLY,
        action=ReaderWithSpeed(reader, Speed.SLOW),
    ))


def add_multi_sentence_options(prompt: Prompt[ReaderWithSpeed], readers: list[ReaderWithId]) -> None:
    """Attach the options for multiple sentences to the prompt: '[i]mproved | [is] | [o]riginal | [os]'."""
    for reader in readers:
        prompt.add_option(PromptOption(
            description=reader.id,
            action=ReaderWithSpeed(reader.reader, Speed.NORMAL),
            modifiers={
                SLOWLY: ReaderWithSpeed(reader.reader, Speed.SLOW),
            },
        ))


def construct_prompt(
        sentences_with_readers: list[SentenceData],
        current: ReaderWithSpeed | None,
        multi_sentence: bool,
) -> Prompt:
    """
    Construct a prompt for the user to choose the next sentence to read and the speed of the reading.
    :raises ValueError: If reader_id is not provided for a sentence with a reader in a multi-sentence output.
    """
    prompt = Prompt(PROMPT_TITLE)
    if multi_sentence:
        add_multi_sentence_options(prompt, [
            ReaderWithId(
                reader=ensure_not_none(sentence.reader),
                id=ensure_not_none(sentence.reader_id),
            )
            for sentence in sentences_with_readers
        ])
    else:
        add_single_sentence_options(prompt, sentences_with_readers[0].reader)
    if current:
        prompt.add_option(PromptOption(
            description=REPLAY,
            action=current,
        ))
    return prompt


def output(*sentences: SentenceData) -> None:
    """
    Output the sentences, reading them if a reader is provided.
    If multiple readers are provided, the user can choose which sentence to read next.
    The user can also choose the speed of the reading.

    :raises ValueError: If reader_id is not provided for a sentence with a reader in a multi-sentence output.
    """
    for sentence in sentences:
        print(sentence.print_prefix + sentence.text)
    multi_sentence = len(sentences) > 1
    if sentences_with_readers := [sentence for sentence in sentences if sentence.reader]:
        current = ReaderWithSpeed(sentences_with_readers[0].reader, Speed.NORMAL) if len(sentences) == 1 else None
        while True:
            if current:
                current.reader(current.speed)
                clear_current_line()  # Otherwise the input made during the reading will get displayed twice
            current = construct_prompt(sentences_with_readers, current, multi_sentence).prompt()
            if not current:
                break
    elif multi_sentence:
        enter_to_continue()

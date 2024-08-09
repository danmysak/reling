from tqdm import tqdm
import typer

from reling.app.app import app
from reling.app.types import (
    API_KEY,
    COUNT_DIALOG_OPT,
    COUNT_TEXT_OPT,
    INCLUDE_OPT,
    LANGUAGE_ARG,
    LEVEL_OPT,
    MODEL,
    SPEAKER_OPT,
    STYLE_OPT,
    TOPIC_OPT,
)
from reling.db.enums import Level
from reling.db.helpers.modifiers import get_random_modifier
from reling.db.models import Speaker, Style, Topic
from reling.gpt import GPTClient
from reling.types import WordWithSense
from reling.utils.typer import typer_raise
from .generation import generate_dialog_exchanges, generate_id, generate_text_sentences
from .storage import save_dialog, save_text

__all__ = [
    'create',
]

DEFAULT_COUNT_TEXT = 10
DEFAULT_COUNT_DIALOG = 10

MIN_COUNT_THRESHOLD = 0.9

create = typer.Typer()
app.add_typer(
    create,
    name='create',
    help='Create a new text or dialog.',
)


@create.command()
def text(
        api_key: API_KEY,
        model: MODEL,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.INTERMEDIATE,
        topic: TOPIC_OPT = None,
        style: STYLE_OPT = None,
        count: COUNT_TEXT_OPT = DEFAULT_COUNT_TEXT,
        include: INCLUDE_OPT = None,
) -> None:
    """Create a text and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    topic = topic or get_random_modifier(Topic).name
    style = style or get_random_modifier(Style).name

    sentences = list(tqdm(
        generate_text_sentences(
            gpt=gpt,
            num_sentences=count,
            language=language,
            level=level,
            topic=topic,
            style=style,
            include=list(map(WordWithSense.parse, include or [])),
        ),
        desc=f'Generating sentences in {language.name}',
        total=count,
    ))
    if len(sentences) < round(count * MIN_COUNT_THRESHOLD):
        typer_raise('Failed to generate the text.')

    text_id = save_text(
        suggested_id=generate_id(gpt, sentences),
        sentences=sentences,
        language=language,
        level=level,
        topic=topic,
        style=style,
    )
    print(f'Generated text with the following ID:\n{text_id}')


@create.command()
def dialog(
        api_key: API_KEY,
        model: MODEL,
        language: LANGUAGE_ARG,
        level: LEVEL_OPT = Level.INTERMEDIATE,
        speaker: SPEAKER_OPT = None,
        topic: TOPIC_OPT = None,
        count: COUNT_DIALOG_OPT = DEFAULT_COUNT_DIALOG,
        include: INCLUDE_OPT = None,
) -> None:
    """Create a dialog and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    speaker = speaker or get_random_modifier(Speaker).name

    exchanges = list(tqdm(
        generate_dialog_exchanges(
            gpt=gpt,
            num_exchanges=count,
            language=language,
            level=level,
            speaker=speaker,
            topic=topic,
            include=list(map(WordWithSense.parse, include or [])),
        ),
        desc=f'Generating exchanges in {language.name}',
        total=count,
    ))
    if len(exchanges) < round(count * MIN_COUNT_THRESHOLD):
        typer_raise('Failed to generate the dialog.')

    dialog_id = save_dialog(
        suggested_id=generate_id(gpt, [turn for exchange in exchanges for turn in exchange.all()]),
        exchanges=exchanges,
        language=language,
        level=level,
        speaker=speaker,
        topic=topic,
    )
    print(f'Generated dialog with the following ID:\n{dialog_id}')

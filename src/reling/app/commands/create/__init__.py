from tqdm import tqdm
import typer

from reling.app.app import app
from reling.app.types import API_KEY, LANGUAGE_ARG, LEVEL_OPT, MODEL, SPEAKER_OPT, STYLE_OPT, TOPIC_OPT
from reling.db.enums import Level
from reling.db.helpers.modifiers import get_random_modifier
from reling.db.models import Speaker, Style, Topic
from reling.gpt import GPTClient
from reling.utils.typer import typer_raise
from .generation import generate_dialog_exchanges, generate_id, generate_text_sentences
from .storage import save_dialog, save_text

__all__ = [
    'create',
]

NUM_TEXT_SENTENCES = 10
NUM_DIALOG_EXCHANGES = 10

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
) -> None:
    """Create a text and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    topic = topic or get_random_modifier(Topic).name
    style = style or get_random_modifier(Style).name

    sentences = list(tqdm(
        generate_text_sentences(
            gpt=gpt,
            num_sentences=NUM_TEXT_SENTENCES,
            language=language,
            level=level,
            topic=topic,
            style=style,
        ),
        desc='Generating sentences',
        total=NUM_TEXT_SENTENCES,
    ))
    if len(sentences) <= 1:
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
) -> None:
    """Create a dialog and save it to the database."""
    gpt = GPTClient(api_key=api_key, model=model)
    speaker = speaker or get_random_modifier(Speaker).name

    exchanges = list(tqdm(
        generate_dialog_exchanges(
            gpt=gpt,
            num_exchanges=NUM_DIALOG_EXCHANGES,
            language=language,
            level=level,
            speaker=speaker,
            topic=topic,
        ),
        desc='Generating exchanges',
        total=NUM_DIALOG_EXCHANGES,
    ))
    if len(exchanges) <= 1:
        typer_raise('Failed to generate the dialog.')

    dialog_id = save_dialog(
        suggested_id=generate_id(gpt, [sentence for exchange in exchanges for sentence in exchange.all()]),
        exchanges=exchanges,
        language=language,
        level=level,
        speaker=speaker,
        topic=topic,
    )
    print(f'Generated dialog with the following ID:\n{dialog_id}')

from reling.app.app import app
from reling.app.exceptions import AlgorithmException
from reling.app.translation import translate_dialog, translate_text, TranslationExistsException
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_ARG, MODEL
from reling.db.models import Text
from reling.gpt import GPTClient
from reling.utils.typer import typer_raise

__all__ = [
    'translate',
]


@app.command()
def translate(api_key: API_KEY, model: MODEL, content: CONTENT_ARG, language: LANGUAGE_ARG) -> None:
    """Translate a text or dialog into another language."""
    if language.id == content.language_id:
        typer_raise(f'The content is already in {language.name}.')

    gpt = GPTClient(api_key=api_key, model=model)
    try:
        (translate_text if isinstance(content, Text) else translate_dialog)(gpt, content, language)
    except TranslationExistsException:
        typer_raise(f'The content has already been translated into {language.name}.')
    except AlgorithmException as e:
        typer_raise(e.msg)

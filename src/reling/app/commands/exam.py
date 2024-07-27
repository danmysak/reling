from reling.app.app import app
from reling.app.types import API_KEY, CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM, MODEL
from reling.gpt import GPTClient

__all__ = [
    'exam',
]


@app.command()
def exam(
        api_key: API_KEY,
        model: MODEL,
        content: CONTENT_ARG,
        from_: LANGUAGE_OPT_FROM = None,
        to: LANGUAGE_OPT = None,
) -> None:
    """
    Test the user's ability to translate content from one language to another.
    If only one language is specified, the content's original language is assumed for the unspecified direction.
    """
    gpt = GPTClient(api_key=api_key, model=model)
    pass

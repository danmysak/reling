from typing import Generator

from openai import OpenAI

from ..utils.feeders import Feeder, LineFeeder

__all__ = [
    'GPTClient',
]


class GPTClient:
    _client: OpenAI
    _model: str

    def __init__(self, *, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def ask(self, request: str, feeder_type: type[Feeder] = LineFeeder) -> Generator[str, None, None]:
        """Ask the model a question and yield sections of the response as they become available."""
        feeder = feeder_type()
        stream = self._client.chat.completions.create(
            model=self._model,
            stream=True,
            messages=[{'role': 'user', 'content': request}],
        )

        for chunk in stream:
            feeder.put(chunk.choices[0].delta.content or '')
            while (line := feeder.get()) is not None:
                yield line

        feeder.end()
        while (line := feeder.get()) is not None:
            yield line

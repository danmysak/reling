from typing import Generator

from reling.db.enums import Sex
from reling.db.models import Language
from reling.gpt import GPTClient
from reling.types import DialogExchangeData
from reling.utils.iterables import map_asterisk, pair_items
from reling.utils.transformers import add_numbering, apply, omit_empty, remove_numbering, strip

__all__ = [
    'translate_dialog_exchanges',
    'translate_text_sentences',
]


def translate_text_sentences(
        gpt: GPTClient,
        sentences: list[str],
        source_language: Language,
        target_language: Language,
) -> Generator[str, None, None]:
    return gpt.ask(
        '\n'.join([
            f'Translate the following text from {source_language.name} into {target_language.name}.',
            f'Generate only the specified translations without any additional text.',
            f'Number each translated sentence and place each on a new line.',
            f'---',
            *apply(add_numbering, sentences),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    )


def translate_dialog_exchanges(
        gpt: GPTClient,
        exchanges: list[DialogExchangeData],
        speaker_sex: Sex,
        user_sex: Sex,
        source_language: Language,
        target_language: Language,
) -> Generator[DialogExchangeData, None, None]:
    DialogExchangeData.assert_speaker_comes_first()
    return map_asterisk(DialogExchangeData, pair_items(gpt.ask(
        '\n'.join([
            f'Translate the following dialogue between {speaker_sex.describe()} and {user_sex.describe()} '
            f'from {source_language.name} into {target_language.name}'
            f'{f' ({speaker_sex.describe()} speaks in the odd-numbered sentences,'
               f' and {user_sex.describe()} responds in the even-numbered sentences)'
               if speaker_sex != user_sex
               else ''}'
            f'.',

            f'Generate only the specified translations without any additional text.',
            f'Number each translated sentence and place each on a new line.',
            f'---',
            *apply(add_numbering, [turn for exchange in exchanges for turn in exchange.all()]),
        ]),
        transformers=[strip, omit_empty, remove_numbering],
    )))

from itertools import zip_longest
from pathlib import Path
from typing import Callable, Generator, Iterable

from reling.asr import ASRClient
from reling.db.enums import ContentCategory
from reling.db.models import Language
from reling.helpers.colors import fade
from reling.helpers.input import get_input, ScannerParams, TranscriberParams
from reling.helpers.output import output, SentenceData
from reling.scanner import Scanner
from reling.tts import TTSVoiceClient
from reling.types import DialogueExchangeData
from reling.utils.transformers import get_numbering_prefix
from .types import ExchangeWithTranslation, SentenceWithTranslation

__all__ = [
    'collect_translations',
]

HIDDEN_TEXT = '(...)'
TRANSLATION_PROMPT = 'Translation: '

SKIPPED = fade('(skipped)')


def collect_translations(
        category: ContentCategory,
        items: Iterable[str | DialogueExchangeData],
        original_translations: Iterable[str | DialogueExchangeData],
        skipped_indices: set[int],
        target_language: Language,
        source_tts: TTSVoiceClient | None,
        target_speaker_tts: TTSVoiceClient | None,
        asr: ASRClient | None,
        scanner: Scanner | None,
        hide_prompts: bool,
        storage: Path,
        on_pause: Callable[[], None],
        on_resume: Callable[[], None],
) -> Generator[SentenceWithTranslation | ExchangeWithTranslation, None, None]:
    """Collect the translations of text sentences or user turns in a dialogue."""
    is_dialogue = category == ContentCategory.DIALOGUE
    speaker_translations: list[str] = []
    collected: list[str] = []
    for index, (item, original_translation) in enumerate(zip(items, original_translations)):
        print_prefix = get_numbering_prefix(index)
        if is_dialogue:
            speaker_translations.append(original_translation.speaker)
        if index in skipped_indices:
            if is_dialogue:
                output(SentenceData(
                    print_text=original_translation.speaker,
                ))
            output(SentenceData(
                print_text=item.user if is_dialogue else item,
                print_prefix=print_prefix,
            ))
            output(SentenceData(SKIPPED))
            translation = None
            collected.append(original_translation.user if is_dialogue else original_translation)
        else:
            if is_dialogue:
                output(SentenceData.from_tts(
                    original_translation.speaker,
                    target_speaker_tts,
                ))
            output(SentenceData.from_tts(
                item.user if is_dialogue else item,
                source_tts,
                print_text=HIDDEN_TEXT if hide_prompts else None,
                print_prefix=print_prefix,
            ))
            translation = get_input(
                on_pause=on_pause,
                on_resume=on_resume,
                prompt=TRANSLATION_PROMPT,
                transcriber_params=TranscriberParams(
                    transcribe=asr.get_transcriber(target_language, '\n'.join(
                        (turn for exchange in zip_longest(speaker_translations, collected) for turn in exchange if turn)
                        if is_dialogue
                        else collected
                    )),
                    storage=storage,
                ) if asr else None,
                scanner_params=ScannerParams(
                    scanner=scanner,
                    language=target_language,
                ) if scanner else None,
            )
            collected.append(translation.text)
        yield (ExchangeWithTranslation(item, translation)
               if is_dialogue
               else SentenceWithTranslation(item, translation))
        print()

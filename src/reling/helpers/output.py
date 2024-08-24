from reling.tts import TTSVoiceClient
from reling.utils.console import clear_current_line

__all__ = [
    'output_text',
]


def output_text(text: str, tts: TTSVoiceClient | None, *, print_prefix: str = '') -> None:
    """Print the text with the specified prefix and optionally read it out loud."""
    print(print_prefix + text)
    if tts:
        tts.read(text)
        clear_current_line()  # Useful both when followed by another output and especially when followed by user input

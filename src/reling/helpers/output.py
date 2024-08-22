from reling.tts import TTSClient, Voice
from reling.utils.console import clear_current_line

__all__ = [
    'output_text',
]


def output_text(text: str, tts: TTSClient | None, voice: Voice, *, print_prefix: str = '') -> None:
    """Print the text with the specified prefix and optionally read it out loud."""
    print(print_prefix + text)
    if tts:
        tts.read(text, voice)
        clear_current_line()  # Useful both when followed by another output and especially when followed by user input

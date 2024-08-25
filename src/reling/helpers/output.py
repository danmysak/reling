from reling.tts import TTSVoiceClient
from reling.utils.console import clear_current_line, input_and_erase

__all__ = [
    'output_text',
]


def should_replay() -> bool:
    """Prompt the user to either replay the text or continue."""
    while True:
        response = input_and_erase('[r]eplay / continue (press Enter): ').strip().lower()
        if response == 'r':
            return True
        if response == '':
            return False


def output_text(text: str, tts: TTSVoiceClient | None, *, print_prefix: str = '') -> None:
    """Print the text with the specified prefix and optionally read it out loud."""
    print(print_prefix + text)
    if tts:
        while True:
            tts.read(text)
            clear_current_line()  # Otherwise the input made during the reading will get displayed twice
            if not should_replay():
                break

from reling.tts import TTSClient, Voice

__all__ = [
    'output_text',
]


def output_text(text: str, tts: TTSClient | None, voice: Voice, *, print_prefix: str = '') -> None:
    """Print the text with the specified prefix and optionally read it out loud."""
    print(print_prefix + text)
    if tts:
        tts.read(text, voice)

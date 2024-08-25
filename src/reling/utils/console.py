__all__ = [
    'clear_current_line',
    'clear_previous_line',
    'wait_for_key_press',
]

KEY_PRESS_PROMPT = '... Press Enter to continue ...'


def clear_current_line() -> None:
    print('\033[K', end='\r')


def clear_previous_line() -> None:
    print('\033[F\033[K', end='\r')


def wait_for_key_press() -> None:
    print('')
    input(KEY_PRESS_PROMPT)
    clear_previous_line()

__all__ = [
    'clear_current_line',
]


def clear_current_line() -> None:
    print('\033[K', end='\r')

__all__ = [
    'clear_current_line',
    'clear_previous',
    'input_and_erase',
]


def clear_current_line() -> None:
    print('\033[2K', end='\r')


def clear_previous(lines: int = 1) -> None:
    print('\033[F\033[K' * lines, end='\r')


def input_and_erase(prompt: str) -> str:
    data = input(prompt)
    clear_previous(prompt.count('\n') + 1)
    return data

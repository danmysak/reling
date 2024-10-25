from statistics import mean

__all__ = [
    'format_average_score',
]


def format_average_score(scores: list[int]) -> str:
    return f'{mean(scores):.1f}'

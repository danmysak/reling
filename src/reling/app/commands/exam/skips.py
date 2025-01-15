from reling.config import MAX_SCORE
from reling.db.models import Dialogue, Language, Text

__all__ = [
    'get_skipped_indices',
]


def get_skipped_indices(
        item: Text | Dialogue,
        source_language: Language,
        target_language: Language,
        skip_after: int,
) -> set[int]:
    """Get the indices of sentences that should be skipped for a specified language pair."""
    skipped_indices: set[int] = set()
    last_streaks: dict[int, int | None] = {index: 0 for index in range(item.size)}
    for exam in sorted(
            (exam for exam in item.exams
             if (exam.source_language, exam.target_language) == (source_language, target_language)),
            key=lambda e: e.started_at,
            reverse=True,
    ):
        for result in exam.results:
            if last_streaks[result.index] is not None:
                if result.score == MAX_SCORE:
                    last_streaks[result.index] += 1
                    if last_streaks[result.index] == skip_after:
                        skipped_indices.add(result.index)
                else:
                    last_streaks[result.index] = None
    return skipped_indices

import sys

from rich.console import Console
from rich.table import Table

from reling.app.app import app
from reling.app.types import CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM
from reling.db.models import DialogExam, Language, TextExam
from reling.utils.scores import format_average_score
from reling.utils.time import format_time, format_time_delta

__all__ = [
    'stats',
]


def does_exam_match(exam: TextExam | DialogExam, from_: Language | None, to: Language | None) -> bool:
    return (from_ is None or exam.source_language.id == from_.id) and (to is None or exam.target_language.id == to.id)


def get_exam_sort_key(exam: TextExam | DialogExam) -> tuple:
    return (
        exam.source_language.name,
        exam.target_language.name,
        exam.started_at,
    )


@app.command()
def stats(content: CONTENT_ARG, from_: LANGUAGE_OPT_FROM = None, to: LANGUAGE_OPT = None) -> None:
    """Display statistics about the translation exams, optionally filtered by source or target language."""
    table = Table()
    table.add_column('From', justify='left')
    table.add_column('To', justify='left')
    table.add_column('Taken at', justify='left')
    table.add_column('Duration', justify='right')
    table.add_column('Score', justify='right')

    last_languages: tuple[str, str] | None = None
    for exam in sorted(filter(lambda e: does_exam_match(e, from_, to), content.exams), key=get_exam_sort_key):
        languages = exam.source_language.id, exam.target_language.id
        if is_new_section := languages != last_languages:
            table.add_section()
            last_languages = languages
        table.add_row(
            exam.source_language.name if is_new_section else '',
            exam.target_language.name if is_new_section else '',
            format_time(exam.started_at),
            format_time_delta(exam.finished_at - exam.started_at),
            format_average_score([result.score for result in exam.results]),
        )

    if table.row_count == 0:
        print('No exams found.', file=sys.stderr)
    else:
        console = Console()
        console.print(table)

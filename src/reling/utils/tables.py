from typing import Iterable

from rich.console import Console, JustifyMethod
from rich.table import Table

__all__ = [
    'build_table',
    'DEFAULT_JUSTIFY_METHOD',
    'JustifyMethod',
    'Table',
    'print_table',
]

DEFAULT_JUSTIFY_METHOD: JustifyMethod = 'left'


def build_table(
        *,
        title: str | None = None,
        headers: list[str],
        data: Iterable[dict[str, str]],
        justify: dict[str, JustifyMethod] | None = None,
        group_by: list[str] | None = None,
) -> Table:
    """
    Build a Rich Table from headers and data.

    :param title: Table title.
    :param headers: List of column headers.
    :param data: Iterable of dictionaries with data. Keys must match headers.
    :param justify: Dictionary of column justifications. Keys must be in headers. Default is DEFAULT_JUSTIFY_METHOD.
    :param group_by: List of columns to group by: rows with the same values in these columns will be grouped together.
                     Only the first row of each group will have the group values displayed.
    :return: Rich Table.
    """
    justify = justify or {}
    if any(col not in headers for col in justify.keys()):
        raise ValueError('Justify columns must be in headers.')

    table = Table(title=title)
    for header in headers:
        table.add_column(header, justify=justify.get(header, DEFAULT_JUSTIFY_METHOD))

    group_by = group_by or []
    if any(col not in headers for col in group_by):
        raise ValueError('Group by columns must be in headers.')
    last_group: tuple[str, ...] | None = None

    for row in data:
        if sorted(row.keys()) != sorted(headers):
            raise ValueError('Data keys must match headers.')
        group = tuple(row[col] for col in group_by)
        if new_section := group != last_group:
            last_group = group
            table.add_section()
        table.add_row(*[row[col]
                        if new_section or col not in group_by
                        else ''
                        for col in headers])

    return table


def print_table(table: Table) -> None:
    Console().print(table)

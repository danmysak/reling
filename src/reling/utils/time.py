from datetime import datetime, timedelta, UTC

import pytz

__all__ = [
    'format_time',
    'format_time_delta',
    'now',
]

TIME_FORMAT = '%Y-%m-%d, %H:%M'


def format_time(time: datetime) -> str:
    return pytz.utc.localize(time).astimezone().strftime(TIME_FORMAT)


def format_time_delta(delta: timedelta) -> str:
    """Format timedelta as follows: '[X days, ][H:][M]M:SS'."""
    return str(delta).split('.')[0].removeprefix('0:').removeprefix('0')


def now() -> datetime:
    return datetime.now(UTC)

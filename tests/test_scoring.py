from pathlib import Path

from reling.config import MAX_SCORE
from reling.helpers.scoring import calculate_diff_score
from reling.utils.csv import read_csv

DATA = Path(__file__).parent / 'scoring.tsv'
DELIMITER = '\t'


def test_scoring() -> None:
    for case in read_csv(DATA, ['a', 'b', 'min', 'max'], empty_as_none=False, delimiter=DELIMITER):
        min_expected = round(float(case['min']) * MAX_SCORE)
        max_expected = round(float(case['max']) * MAX_SCORE)
        assert min_expected <= calculate_diff_score(case['a'], case['b']) <= max_expected
        assert min_expected <= calculate_diff_score(case['b'], case['a']) <= max_expected

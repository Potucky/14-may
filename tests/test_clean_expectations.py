"""The clean staging load must satisfy the published expectation contract."""

from __future__ import annotations

import pytest

from dq_runner.config import SUITE_PATH
from dq_runner.expectations import execute
from dq_runner.suite import load_expectations

CASES = load_expectations(SUITE_PATH)
CORE_TYPES = {
    "not_null",
    "not_blank",
    "unique",
    "between",
    "in_set",
    "foreign_key",
    "row_count",
    "max_age",
    "not_future",
    "column_gte_when_present",
    "parent_sum_matches",
    "product_equals",
}


def test_expectation_names_are_unique() -> None:
    names = [case.name for case in CASES]
    assert len(names) == len(set(names))


def test_suite_covers_the_core_check_types() -> None:
    present = {case.type for case in CASES}
    assert present == CORE_TYPES


@pytest.mark.clean
@pytest.mark.parametrize("case", CASES, ids=[case.name for case in CASES])
def test_clean_expectation(db, case) -> None:
    result = execute(db, case)
    assert result.success, result.message()

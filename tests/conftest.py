"""Session setup: reset the local demo database once per pytest run."""

from __future__ import annotations

import pytest

from dq_runner.config import assert_local_demo, load_settings
from dq_runner.db import connect
from dq_runner.load import reset_and_load


@pytest.fixture(scope="session")
def db():
    settings = load_settings()
    assert_local_demo(settings)
    conn = connect(settings)
    try:
        reset_and_load(conn)
        conn.autocommit = True
        yield conn
    finally:
        conn.close()


def pytest_html_report_title(report) -> None:
    report.title = "Harbor & Pine data quality expectations"


def pytest_metadata(metadata: dict) -> None:
    metadata["Project"] = "Harbor & Pine local PostgreSQL data quality demo"
    metadata["Schemas"] = "shop (clean), shop_defects (seeded defects)"
    for key in ("Packages", "JAVA_HOME", "CI"):
        metadata.pop(key, None)

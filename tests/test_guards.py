"""Guards around identifiers, the local-only reset, and unknown checks."""

from __future__ import annotations

import pytest

from typing import cast

from psycopg import Connection

from dq_runner.config import DbSettings, assert_local_demo
from dq_runner.expectations import Expectation, execute, ident


def test_rejects_unsafe_identifier() -> None:
    with pytest.raises(ValueError, match="Refusing identifier"):
        ident("customers; drop schema shop")


def test_refuses_non_local_host() -> None:
    settings = DbSettings(
        host="warehouse.internal",
        port=5432,
        dbname="shop",
        user="dq_demo",
        password="dq_demo_local_only",
    )
    with pytest.raises(RuntimeError, match="local PostgreSQL demo"):
        assert_local_demo(settings)


def test_refuses_unexpected_demo_password() -> None:
    settings = DbSettings(
        host="localhost",
        port=5432,
        dbname="shop",
        user="dq_demo",
        password="not-the-demo-password",
    )
    with pytest.raises(RuntimeError, match="documented local demo"):
        assert_local_demo(settings)


def test_unknown_expectation_type_is_rejected() -> None:
    case = Expectation(name="bad", type="drop_table", schema="shop", table="customers")
    with pytest.raises(ValueError, match="Unknown expectation type"):
        execute(cast(Connection, None), case)

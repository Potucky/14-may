"""SQL checks shaped like a Great Expectations suite.

The runner is intentionally small: each expectation is one query, and the
result records what was expected, what was observed, and a few sample values.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from psycopg import Connection, sql

_IDENT = re.compile(r"^[a-z_][a-z0-9_]*$")


@dataclass(frozen=True)
class Expectation:
    name: str
    type: str
    schema: str
    table: str | None = None
    column: str | None = None
    min: str | None = None
    max: str | None = None
    values: tuple[str, ...] = ()
    ref_table: str | None = None
    ref_column: str | None = None
    max_age_hours: int | None = None
    other_column: str | None = None
    parent_table: str | None = None
    parent_key: str | None = None
    parent_amount: str | None = None
    child_table: str | None = None
    child_key: str | None = None
    child_amount: str | None = None
    factors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExpectationResult:
    name: str
    expectation_type: str
    success: bool
    expected: str
    observed: str
    unexpected_count: int
    samples: tuple[str, ...]

    def message(self) -> str:
        samples = ", ".join(self.samples) if self.samples else "none"
        return (
            f"{self.name} [{self.expectation_type}] "
            f"expected {self.expected}; observed {self.observed}; "
            f"unexpected={self.unexpected_count}; samples: {samples}"
        )


def ident(name: str) -> sql.Identifier:
    if not _IDENT.fullmatch(name):
        raise ValueError(f"Refusing identifier {name!r}.")
    return sql.Identifier(name)


def execute(conn: Connection, case: Expectation) -> ExpectationResult:
    try:
        handler = _HANDLERS[case.type]
    except KeyError as exc:
        raise ValueError(f"Unknown expectation type {case.type!r}.") from exc
    return handler(conn, case)


def _require(case: Expectation, *fields: str) -> None:
    missing = []
    for field in fields:
        value = getattr(case, field)
        if value is None or value == ():
            missing.append(field)
    if missing:
        raise ValueError(
            f"Expectation {case.name!r} is missing {', '.join(missing)}."
        )


def _query(conn: Connection, statement: sql.SQL, params: tuple[Any, ...] = ()) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(statement, params)
        return cur.fetchall()


def _result(
    case: Expectation,
    *,
    success: bool,
    expected: str,
    observed: str,
    unexpected_count: int,
    samples: tuple[str, ...] = (),
) -> ExpectationResult:
    return ExpectationResult(
        name=case.name,
        expectation_type=case.type,
        success=success,
        expected=expected,
        observed=observed,
        unexpected_count=unexpected_count,
        samples=samples[:10],
    )


def _table(case: Expectation) -> sql.Composed:
    _require(case, "schema", "table")
    return sql.SQL("{schema}.{table}").format(
        schema=ident(case.schema),
        table=ident(case.table or ""),
    )


def _not_null(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column")
    rows = _query(
        conn,
        sql.SQL("select count(*) from {table} where {column} is null").format(
            table=_table(case),
            column=ident(case.column or ""),
        ),
    )
    count = int(rows[0][0])
    return _result(
        case,
        success=count == 0,
        expected="no nulls",
        observed=f"{count} null values",
        unexpected_count=count,
    )


def _not_blank(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column")
    rows = _query(
        conn,
        sql.SQL(
            "select count(*) from {table} "
            "where {column} is null or btrim({column}::text) = ''"
        ).format(
            table=_table(case),
            column=ident(case.column or ""),
        ),
    )
    count = int(rows[0][0])
    return _result(
        case,
        success=count == 0,
        expected="no nulls or blank strings",
        observed=f"{count} null or blank values",
        unexpected_count=count,
    )


def _unique(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column")
    column = ident(case.column or "")
    rows = _query(
        conn,
        sql.SQL(
            "select {column}::text, count(*) from {table} "
            "where {column} is not null and btrim({column}::text) <> '' "
            "group by {column} having count(*) > 1 "
            "order by {column}::text"
        ).format(table=_table(case), column=column),
    )
    samples = tuple(f"{value} ({count} rows)" for value, count in rows)
    return _result(
        case,
        success=not rows,
        expected="unique values",
        observed=f"{len(rows)} duplicated values",
        unexpected_count=len(rows),
        samples=samples,
    )


def _between(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column", "min", "max")
    rows = _query(
        conn,
        sql.SQL(
            "select {column}::text from {table} "
            "where {column} is not null "
            "and ({column} < %s::numeric or {column} > %s::numeric) "
            "order by {column}"
        ).format(table=_table(case), column=ident(case.column or "")),
        (case.min, case.max),
    )
    samples = tuple(str(row[0]) for row in rows)
    return _result(
        case,
        success=not rows,
        expected=f"between {case.min} and {case.max} inclusive",
        observed=f"{len(rows)} values outside the range",
        unexpected_count=len(rows),
        samples=samples,
    )


def _in_set(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column", "values")
    rows = _query(
        conn,
        sql.SQL(
            "select {column}::text from {table} "
            "where {column} is not null and not ({column} = any(%s)) "
            "order by {column}::text"
        ).format(table=_table(case), column=ident(case.column or "")),
        (list(case.values),),
    )
    samples = tuple(str(row[0]) for row in rows)
    allowed = ", ".join(case.values)
    return _result(
        case,
        success=not rows,
        expected=f"one of [{allowed}]",
        observed=f"{len(rows)} values outside the set",
        unexpected_count=len(rows),
        samples=samples,
    )


def _foreign_key(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column", "ref_table", "ref_column")
    rows = _query(
        conn,
        sql.SQL(
            "select child.{column}::text "
            "from {table} as child "
            "left join {schema}.{ref_table} as parent "
            "  on parent.{ref_column} = child.{column} "
            "where child.{column} is not null and parent.{ref_column} is null "
            "order by child.{column}"
        ).format(
            table=_table(case),
            schema=ident(case.schema),
            column=ident(case.column or ""),
            ref_table=ident(case.ref_table or ""),
            ref_column=ident(case.ref_column or ""),
        ),
    )
    samples = tuple(str(row[0]) for row in rows)
    return _result(
        case,
        success=not rows,
        expected=f"every {case.column} exists in {case.ref_table}.{case.ref_column}",
        observed=f"{len(rows)} orphan values",
        unexpected_count=len(rows),
        samples=samples,
    )


def _row_count(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "min", "max")
    lower = int(case.min or 0)
    upper = int(case.max or 0)
    rows = _query(conn, sql.SQL("select count(*) from {table}").format(table=_table(case)))
    count = int(rows[0][0])
    return _result(
        case,
        success=lower <= count <= upper,
        expected=f"{lower} to {upper} rows",
        observed=f"{count} rows",
        unexpected_count=0 if lower <= count <= upper else 1,
    )


def _max_age(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column", "max_age_hours")
    rows = _query(
        conn,
        sql.SQL(
            "select max({column}), "
            "extract(epoch from (now() - max({column}))) / 3600.0 "
            "from {table}"
        ).format(table=_table(case), column=ident(case.column or "")),
    )
    newest, age_hours = rows[0]
    limit = int(case.max_age_hours or 0)
    if newest is None or age_hours is None:
        return _result(
            case,
            success=False,
            expected=f"newest {case.column} within {limit} hours",
            observed="no timestamps",
            unexpected_count=1,
        )
    age = float(age_hours)
    success = 0 <= age <= limit
    return _result(
        case,
        success=success,
        expected=f"newest {case.column} within {limit} hours and not in the future",
        observed=f"{age:.1f} hours (max {newest.isoformat()})",
        unexpected_count=0 if success else 1,
    )


def _not_future(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column")
    rows = _query(
        conn,
        sql.SQL(
            "select {column}::text from {table} "
            "where {column} > now() order by {column}"
        ).format(table=_table(case), column=ident(case.column or "")),
    )
    samples = tuple(str(row[0]) for row in rows)
    return _result(
        case,
        success=not rows,
        expected=f"{case.column} at or before the database clock",
        observed=f"{len(rows)} future timestamps",
        unexpected_count=len(rows),
        samples=samples,
    )


def _column_gte(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column", "other_column")
    rows = _query(
        conn,
        sql.SQL(
            "select {column}::text, {other}::text from {table} "
            "where {column} is not null and {other} is not null "
            "and {column} < {other} "
            "order by {other}"
        ).format(
            table=_table(case),
            column=ident(case.column or ""),
            other=ident(case.other_column or ""),
        ),
    )
    samples = tuple(f"{left} < {right}" for left, right in rows)
    return _result(
        case,
        success=not rows,
        expected=f"{case.column} >= {case.other_column} when both are present",
        observed=f"{len(rows)} rows out of order",
        unexpected_count=len(rows),
        samples=samples,
    )


def _parent_sum(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(
        case,
        "parent_table",
        "parent_key",
        "parent_amount",
        "child_table",
        "child_key",
        "child_amount",
    )
    rows = _query(
        conn,
        sql.SQL(
            "select parent.{parent_key}::text, "
            "parent.{parent_amount}::text, "
            "coalesce(sum(child.{child_amount}), 0)::text "
            "from {schema}.{parent_table} as parent "
            "left join {schema}.{child_table} as child "
            "  on child.{child_key} = parent.{parent_key} "
            "group by parent.{parent_key}, parent.{parent_amount} "
            "having parent.{parent_amount} is distinct from "
            "coalesce(sum(child.{child_amount}), 0) "
            "order by parent.{parent_key}"
        ).format(
            schema=ident(case.schema),
            parent_table=ident(case.parent_table or ""),
            parent_key=ident(case.parent_key or ""),
            parent_amount=ident(case.parent_amount or ""),
            child_table=ident(case.child_table or ""),
            child_key=ident(case.child_key or ""),
            child_amount=ident(case.child_amount or ""),
        ),
    )
    samples = tuple(
        f"{case.parent_key}={key} {case.parent_amount}={amount} lines={total}"
        for key, amount, total in rows
    )
    return _result(
        case,
        success=not rows,
        expected=(
            f"{case.parent_table}.{case.parent_amount} equals "
            f"sum({case.child_table}.{case.child_amount})"
        ),
        observed=f"{len(rows)} parents out of balance",
        unexpected_count=len(rows),
        samples=samples,
    )


def _product_equals(conn: Connection, case: Expectation) -> ExpectationResult:
    _require(case, "column")
    if len(case.factors) != 2:
        raise ValueError(
            f"Expectation {case.name!r} needs exactly two factors."
        )
    left, right = case.factors
    rows = _query(
        conn,
        sql.SQL(
            "select {column}::text, {left}::text, {right}::text from {table} "
            "where {column} is distinct from ({left} * {right}) "
            "order by {column}"
        ).format(
            table=_table(case),
            column=ident(case.column or ""),
            left=ident(left),
            right=ident(right),
        ),
    )
    samples = tuple(
        f"{case.column}={total} but {left}*{right}={factor_a}*{factor_b}"
        for total, factor_a, factor_b in rows
    )
    return _result(
        case,
        success=not rows,
        expected=f"{case.column} = {left} * {right}",
        observed=f"{len(rows)} rows where the product does not match",
        unexpected_count=len(rows),
        samples=samples,
    )


_HANDLERS = {
    "not_null": _not_null,
    "not_blank": _not_blank,
    "unique": _unique,
    "between": _between,
    "in_set": _in_set,
    "foreign_key": _foreign_key,
    "row_count": _row_count,
    "max_age": _max_age,
    "not_future": _not_future,
    "column_gte_when_present": _column_gte,
    "parent_sum_matches": _parent_sum,
    "product_equals": _product_equals,
}

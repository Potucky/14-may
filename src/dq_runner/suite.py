"""Load the YAML expectation suite."""

from __future__ import annotations

from pathlib import Path

import yaml

from dq_runner.expectations import Expectation


def load_expectations(path: Path) -> list[Expectation]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema = document["schema"]
    cases: list[Expectation] = []
    for item in document["expectations"]:
        payload = dict(item)
        values = tuple(str(value) for value in payload.pop("values", []))
        factors = tuple(str(value) for value in payload.pop("factors", []))
        for field in ("min", "max"):
            if payload.get(field) is not None:
                payload[field] = str(payload[field])
        cases.append(
            Expectation(schema=schema, values=values, factors=factors, **payload)
        )
    return cases

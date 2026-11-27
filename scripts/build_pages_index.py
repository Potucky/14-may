"""Write the GitHub Pages index that links to the pytest HTML report."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _counts(junit_path: Path) -> tuple[int, int, int]:
    root = ET.parse(junit_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    tests = failures = errors = 0
    for suite in suites:
        tests += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
    return tests, failures, errors


def render(tests: int, failures: int, errors: int) -> str:
    passed = tests - failures - errors
    status = "passed" if failures == 0 and errors == 0 else "failed"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Harbor &amp; Pine data quality report</title>
  <style>
    body {{
      margin: 0;
      font-family: Georgia, "Iowan Old Style", serif;
      color: #1c1915;
      background: #f6f3ee;
    }}
    main {{
      max-width: 42rem;
      margin: 0 auto;
      padding: 3rem 1.5rem 4rem;
    }}
    h1 {{
      font-weight: 500;
      font-size: 2rem;
      margin-bottom: 0.25rem;
    }}
    p, li {{
      line-height: 1.5;
    }}
    a {{
      color: #0f4c3a;
    }}
    .status {{
      display: inline-block;
      margin: 1rem 0;
      padding: 0.35rem 0.7rem;
      border-radius: 999px;
      background: #e5f2eb;
      color: #0f4c3a;
      font-family: "Segoe UI", sans-serif;
      font-size: 0.95rem;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Harbor &amp; Pine data quality</h1>
    <p>Portfolio demo. Local PostgreSQL staging checks for a fictional retailer. Not employer code.</p>
    <p class="status">{status}: {passed} passed, {failures} failed, {errors} errors, {tests} total</p>
    <p><a href="report.html">Open the pytest HTML report</a></p>
    <p>The report is produced by the GitHub Actions run that deployed this site. Checks cover completeness, uniqueness, ranges, accepted values, referential integrity, row counts, freshness, and order-to-line reconciliation.</p>
  </main>
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_pages_index.py JUNIT_XML INDEX_HTML")
    junit_path = Path(sys.argv[1])
    index_path = Path(sys.argv[2])
    tests, failures, errors = _counts(junit_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(render(tests, failures, errors), encoding="utf-8")


if __name__ == "__main__":
    main()

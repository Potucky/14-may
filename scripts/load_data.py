"""Reload the local demo schemas.

pytest loads the same schemas before the suite. Use this script when you want
the tables available for a SQL client without running the tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dq_runner.load import main

if __name__ == "__main__":
    main()

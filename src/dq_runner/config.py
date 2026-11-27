"""Connection settings for the local demo database."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
SQL_DIR = REPO_ROOT / "sql"
SUITE_PATH = REPO_ROOT / "config" / "expectations.yml"

LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
DEMO_DB = "shop"
DEMO_USER = "dq_demo"
DEMO_PASSWORD = "dq_demo_local_only"


@dataclass(frozen=True)
class DbSettings:
    host: str
    port: int
    dbname: str
    user: str
    password: str


def load_settings() -> DbSettings:
    load_dotenv(REPO_ROOT / ".env")
    return DbSettings(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        dbname=os.environ.get("POSTGRES_DB", DEMO_DB),
        user=os.environ.get("POSTGRES_USER", DEMO_USER),
        password=os.environ.get("POSTGRES_PASSWORD", DEMO_PASSWORD),
    )


def assert_local_demo(settings: DbSettings) -> None:
    """Refuse to drop schemas on anything except the documented local demo.

    The loader rebuilds ``shop`` and ``shop_defects`` on every run. The host,
    database, user, and password all have to match the Docker Compose demo so
    a copied ``.env`` cannot wipe another database.
    """
    if settings.host not in LOCAL_HOSTS:
        raise RuntimeError(
            f"Refusing to reset a database on host {settings.host!r}. "
            "This project only targets a local PostgreSQL demo."
        )
    if (
        settings.dbname != DEMO_DB
        or settings.user != DEMO_USER
        or settings.password != DEMO_PASSWORD
    ):
        raise RuntimeError(
            "Refusing to reset a database whose settings do not match the "
            "documented local demo (database shop, user dq_demo, password "
            "dq_demo_local_only)."
        )

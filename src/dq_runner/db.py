"""Postgres connection helper for the local demo."""

from __future__ import annotations

import time

import psycopg
from psycopg import ClientCursor

from dq_runner.config import DbSettings

# Bounded readiness wait for container startup. Tests do not sleep.
_READY_ATTEMPTS = 20
_READY_PAUSE_SECONDS = 0.5


def connect(settings: DbSettings) -> psycopg.Connection:
    """Open a connection, retrying while Postgres is still starting.

    Each attempt uses a short connect timeout. The loop exists so ``pytest``
    can follow ``docker compose up`` without a fixed sleep in the tests.
    """
    last_error: Exception | None = None
    for attempt in range(1, _READY_ATTEMPTS + 1):
        try:
            return psycopg.connect(
                host=settings.host,
                port=settings.port,
                dbname=settings.dbname,
                user=settings.user,
                password=settings.password,
                connect_timeout=3,
                cursor_factory=ClientCursor,
            )
        except psycopg.OperationalError as exc:
            last_error = exc
            if attempt == _READY_ATTEMPTS:
                break
            time.sleep(_READY_PAUSE_SECONDS)
    raise RuntimeError(
        f"Postgres was not ready at {settings.host}:{settings.port}/{settings.dbname} "
        f"after {_READY_ATTEMPTS} attempts."
    ) from last_error

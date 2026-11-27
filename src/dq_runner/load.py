"""Drop and reload the demo schemas."""

from __future__ import annotations

from pathlib import Path

from psycopg import Connection

from dq_runner.config import SQL_DIR, assert_local_demo, load_settings
from dq_runner.db import connect


def reset_and_load(conn: Connection, sql_dir: Path = SQL_DIR) -> None:
    with conn.cursor() as cur:
        cur.execute("drop schema if exists shop_defects cascade")
        cur.execute("drop schema if exists shop cascade")
    conn.commit()
    for name in ("01_schema.sql", "02_seed.sql"):
        script = (sql_dir / name).read_text(encoding="utf-8")
        with conn.cursor() as cur:
            cur.execute(script)
        conn.commit()


def main() -> None:
    settings = load_settings()
    assert_local_demo(settings)
    conn = connect(settings)
    try:
        reset_and_load(conn)
    finally:
        conn.close()
    print(
        "Loaded schemas shop and shop_defects into "
        f"{settings.host}:{settings.port}/{settings.dbname}."
    )


if __name__ == "__main__":
    main()

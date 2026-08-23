import os
import threading
from datetime import datetime, timezone
from typing import Any, Optional

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgres://postgres:dev@localhost:5432/tasks"
)

SEED_TASKS = [
    ("Learn FastAPI", False),
    ("Build a CRUD API", True),
    ("Switch to SQLite", False),
]

_COLUMNS = "id, title, done, created_at, updated_at"


def _now():
    return datetime.now(timezone.utc)


def _serialize(row: Optional[tuple]) -> Optional[dict]:
    if row is None:
        return None
    data = dict(zip(("id", "title", "done", "created_at", "updated_at"), row))
    for key in ("created_at", "updated_at"):
        value = data.get(key)
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


class PostgresRepository:
    def __init__(self, database_url=DATABASE_URL):
        self.conn = psycopg.connect(database_url)
        self._lock = threading.Lock()
        self._create_table()
        self._migrate()
        self._seed_if_empty()

    def _create_table(self):
        with self._lock:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ
                )
                """
            )
            self.conn.commit()

    def _migrate(self):
        with self._lock:
            cols = [
                row[0]
                for row in self.conn.execute(
                    """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = 'tasks'
                    """
                ).fetchall()
            ]
            changed = False
            if "created_at" not in cols:
                self.conn.execute("ALTER TABLE tasks ADD COLUMN created_at TIMESTAMPTZ")
                changed = True
            if "updated_at" not in cols:
                self.conn.execute("ALTER TABLE tasks ADD COLUMN updated_at TIMESTAMPTZ")
                changed = True
            if changed:
                now = _now()
                self.conn.execute(
                    """
                    UPDATE tasks
                    SET created_at = %s, updated_at = %s
                    WHERE created_at IS NULL OR updated_at IS NULL
                    """,
                    (now, now),
                )
                self.conn.commit()

    def _seed_if_empty(self):
        with self._lock:
            row = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()
            count = row[0] if row else 0
            if count == 0:
                now = _now()
                for title, done in SEED_TASKS:
                    self.conn.execute(
                        f"""
                        INSERT INTO tasks ({_COLUMNS.replace("id, ", "")})
                        VALUES (%s, %s, %s, %s)
                        """,
                        (title, done, now, now),
                    )
                self.conn.commit()

    def add(self, item_dict):
        with self._lock:
            row: Any = self.conn.execute(
                f"""
                INSERT INTO tasks ({_COLUMNS.replace("id, ", "")})
                VALUES (%s, %s, %s, %s)
                RETURNING {_COLUMNS}
                """,
                (
                    item_dict["title"],
                    bool(item_dict.get("done", False)),
                    _now(),
                    _now(),
                ),
            ).fetchone()
            self.conn.commit()
            return _serialize(row)

    def get_all(self):
        with self._lock:
            rows = self.conn.execute(
                f"SELECT {_COLUMNS} FROM tasks ORDER BY id"
            ).fetchall()
            return [_serialize(row) for row in rows]

    def get_by_id(self, task_id):
        with self._lock:
            row = self.conn.execute(
                f"SELECT {_COLUMNS} FROM tasks WHERE id = %s", (task_id,)
            ).fetchone()
            return _serialize(row)

    def update(self, task_id, item_dict):
        with self._lock:
            row: Any = self.conn.execute(
                f"""
                UPDATE tasks
                SET title = %s, done = %s, updated_at = %s
                WHERE id = %s
                RETURNING {_COLUMNS}
                """,
                (
                    item_dict["title"],
                    bool(item_dict.get("done", False)),
                    _now(),
                    task_id,
                ),
            ).fetchone()
            self.conn.commit()
            return _serialize(row)

    def delete(self, task_id):
        with self._lock:
            row = self.conn.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,)
            ).fetchone()
            self.conn.commit()
            return row is not None

import sqlite3
import threading
from datetime import datetime

DB_PATH = "tasks.db"

SEED_TASKS = [
    ("Learn FastAPI", 0),
    ("Build a CRUD API", 1),
    ("Switch to SQLite", 0),
]


def _now():
    return datetime.now().isoformat(timespec="seconds")


class SQLiteRepository:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._create_table()
        self._migrate()
        self._seed_if_empty()

    def _create_table(self):
        with self._lock:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            self.conn.commit()

    def _migrate(self):
        with self._lock:
            cols = [
                row[1]
                for row in self.conn.execute("PRAGMA table_info(tasks)").fetchall()
            ]
            changed = False
            if "created_at" not in cols:
                self.conn.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT")
                changed = True
            if "updated_at" not in cols:
                self.conn.execute("ALTER TABLE tasks ADD COLUMN updated_at TEXT")
                changed = True
            if changed:
                now = _now()
                self.conn.execute(
                    """
                    UPDATE tasks
                    SET created_at = ?, updated_at = ?
                    WHERE created_at IS NULL OR updated_at IS NULL
                    """,
                    (now, now),
                )
                self.conn.commit()

    def _seed_if_empty(self):
        with self._lock:
            count = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            if count == 0:
                now = _now()
                self.conn.executemany(
                    """
                    INSERT INTO tasks (title, done, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    [(title, done, now, now) for title, done in SEED_TASKS],
                )
                self.conn.commit()

    def add(self, item_dict):
        with self._lock:
            now = _now()
            cursor = self.conn.execute(
                """
                INSERT INTO tasks (title, done, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (item_dict["title"], int(item_dict.get("done", False)), now, now),
            )
            self.conn.commit()
            row = self.conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return dict(row)

    def get_all(self):
        with self._lock:
            rows = self.conn.execute("SELECT * FROM tasks").fetchall()
            return [dict(row) for row in rows]

    def get_by_id(self, task_id):
        with self._lock:
            row = self.conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            return dict(row) if row else None

    def update(self, task_id, item_dict):
        with self._lock:
            row = self.conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            if row is None:
                return None
            self.conn.execute(
                """
                UPDATE tasks
                SET title = ?, done = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    item_dict["title"],
                    int(item_dict.get("done", False)),
                    _now(),
                    task_id,
                ),
            )
            self.conn.commit()
            updated = self.conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            return dict(updated)

    def delete(self, task_id):
        with self._lock:
            row = self.conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            if row is None:
                return False
            self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            return True

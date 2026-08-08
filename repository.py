import sqlite3
import threading

DB_PATH = "tasks.db"

SEED_TASKS = [
    ("Learn FastAPI", 0),
    ("Build a CRUD API", 1),
    ("Switch to SQLite", 0),
]

class SQLiteRepository:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._create_table()
        self._seed_if_empty()

    def _create_table(self):
        with self._lock:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            self.conn.commit()

    def _seed_if_empty(self):
        with self._lock:
            count = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            if count == 0:
                self.conn.executemany(
                    "INSERT INTO tasks (title, done) VALUES (?, ?)", SEED_TASKS
                )
                self.conn.commit()

    def add(self, item_dict):
        with self._lock:
            cursor = self.conn.execute(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                (item_dict["title"], int(item_dict.get("done", False))),
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

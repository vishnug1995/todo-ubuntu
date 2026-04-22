import os
import sqlite3

from db.repository import SqliteRepository, TodoRepository

_MIGRATIONS = [
    """
    CREATE TABLE IF NOT EXISTS todos (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        text         TEXT    NOT NULL,
        date         TEXT    NOT NULL,
        completed    INTEGER NOT NULL DEFAULT 0,
        created_at   TEXT    NOT NULL DEFAULT (datetime('now')),
        completed_at TEXT
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_todos_date ON todos(date);",
    """
    CREATE TABLE IF NOT EXISTS schema_version (
        version    INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """,
    "INSERT OR IGNORE INTO schema_version(version) VALUES (1);",
]


def get_data_dir() -> str:
    path = os.path.join(os.path.expanduser("~"), ".config", "todo-ubuntu")
    os.makedirs(path, exist_ok=True)
    return path


def _apply_migrations(conn: sqlite3.Connection) -> None:
    for sql in _MIGRATIONS:
        conn.execute(sql)
    conn.commit()


def create_repository() -> TodoRepository:
    # Future Supabase: if os.environ.get('SUPABASE_URL'): return SupabaseRepository(...)
    db_path = os.path.join(get_data_dir(), "todos.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    _apply_migrations(conn)
    return SqliteRepository(conn)

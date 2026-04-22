import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime


class TodoRepository(ABC):
    @abstractmethod
    def get_todos_for_date(self, date: str) -> list[dict]: ...

    @abstractmethod
    def add_todo(self, text: str, date: str) -> dict: ...

    @abstractmethod
    def complete_todo(self, todo_id: int) -> None: ...

    @abstractmethod
    def uncomplete_todo(self, todo_id: int) -> None: ...

    @abstractmethod
    def delete_todo(self, todo_id: int) -> None: ...


class SqliteRepository(TodoRepository):
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._conn.row_factory = sqlite3.Row

    def get_todos_for_date(self, date: str) -> list[dict]:
        cur = self._conn.execute(
            "SELECT * FROM todos WHERE date = ? ORDER BY completed ASC, created_at ASC",
            (date,),
        )
        return [dict(row) for row in cur.fetchall()]

    def add_todo(self, text: str, date: str) -> dict:
        cur = self._conn.execute(
            "INSERT INTO todos (text, date) VALUES (?, ?)",
            (text, date),
        )
        self._conn.commit()
        row = self._conn.execute(
            "SELECT * FROM todos WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
        return dict(row)

    def complete_todo(self, todo_id: int) -> None:
        self._conn.execute(
            "UPDATE todos SET completed = 1, completed_at = ? WHERE id = ?",
            (datetime.now().isoformat(), todo_id),
        )
        self._conn.commit()

    def uncomplete_todo(self, todo_id: int) -> None:
        self._conn.execute(
            "UPDATE todos SET completed = 0, completed_at = NULL WHERE id = ?",
            (todo_id,),
        )
        self._conn.commit()

    def delete_todo(self, todo_id: int) -> None:
        self._conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        self._conn.commit()

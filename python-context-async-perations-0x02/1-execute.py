#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager
A context manager that opens a connection, executes the provided query with params,
returns the fetched result on __enter__, and commits/rolls back and closes on __exit__.
"""

import sqlite3
from typing import Iterable, Optional, Any, List


class ExecuteQuery:
    """
    Context manager that:
      - opens a connection
      - executes the provided query with params
      - returns the fetched result on __enter__
      - commits/rolls back and closes on __exit__
    """
    def __init__(
        self,
        query: str,
        params: Optional[Iterable[Any]] = None,
        db_path: str = "users.db",
    ) -> None:
        self.db_path = db_path
        self.query = query
        self.params = tuple(params) if params is not None else tuple()
        self.conn: Optional[sqlite3.Connection] = None
        self._result: Optional[List[sqlite3.Row]] = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute(self.query, self.params)
        self._result = cur.fetchall()
        return self._result

    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            if self.conn:
                if exc_type:
                    self.conn.rollback()
                else:
                    self.conn.commit()
        finally:
            if self.conn:
                self.conn.close()
        return False


def main() -> None:
    print("=== Task 1: Reusable Query Context Manager ===")
    
    print("Users older than 25:")
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as rows:
        for row in rows:
            print(dict(row))
    
    print("\nUsers with 'Doe' in their name:")
    with ExecuteQuery("SELECT * FROM users WHERE name LIKE ?", ("%Doe%",)) as rows:
        for row in rows:
            print(dict(row))
    
    print("\nAll users (no parameters):")
    with ExecuteQuery("SELECT * FROM users") as rows:
        for row in rows:
            print(dict(row))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Task 0: Class-based context manager
A context manager that opens a connection on __enter__ and commits/rolls back + closes on __exit__ automatically.
"""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    Class-based context manager that opens a connection on __enter__
    and commits/rolls back + closes on __exit__ automatically.
    """
    def __init__(self, db_path: str = "users.db") -> None:
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # dict-like rows
        return self.conn

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
        # Return False to propagate exceptions if any
        return False


def main() -> None:
    print("=== Task 0: Class-based Context Manager ===")
    with DatabaseConnection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        print("All users in database:")
        for row in rows:
            print(dict(row))


if __name__ == "__main__":
    main()

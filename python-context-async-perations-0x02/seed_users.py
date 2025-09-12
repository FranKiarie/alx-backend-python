#!/usr/bin/env python3
"""
Seed script to create and populate the users database.
"""

import sqlite3

def main():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """)
    c.execute("DELETE FROM users")
    c.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        [
            ("John Doe", "john@example.com", 28),
            ("Jane Doe", "jane@example.com", 35),
            ("Grace Older", "grace@ex.com", 41),
            ("Paul Senior", "paul@ex.com", 52),
        ],
    )
    conn.commit()
    conn.close()
    print("Seeded users.db with sample users.")

if __name__ == "__main__":
    main()

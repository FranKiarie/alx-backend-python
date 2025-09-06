#!/usr/bin/env python3
"""
seed.py
- Connects to MySQL
- Creates database ALX_prodev (if not exists)
- Creates table user_data (if not exists)
- Inserts users from user_data.csv (idempotent)
- Exposes a generator to stream rows one-by-one from the DB

Prototypes required by 0-main.py:
    connect_db()
    create_database(connection)
    connect_to_prodev()
    create_table(connection)
    insert_data(connection, data)

Extra (for the assignment objective):
    stream_user_data(connection, batch_size=1000)  # generator
"""

import csv
import os
import uuid
from contextlib import closing

# Try mysql-connector-python first, then PyMySQL as a fallback
_DRIVERS = []
try:
    import mysql.connector  # type: ignore
    _DRIVERS.append("mysql.connector")
except Exception:
    pass

try:
    import pymysql  # type: ignore
    _DRIVERS.append("pymysql")
except Exception:
    pass

if not _DRIVERS:
    raise RuntimeError(
        "No MySQL driver found. Install one of:\n"
        "  pip install mysql-connector-python\n"
        "  or\n"
        "  pip install PyMySQL"
    )

# ---- Connection config (override via environment) ----
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
DB_NAME = "ALX_prodev"


def _connect_raw(database: str | None = None):
    """
    Low-level connector that works with either mysql-connector or PyMySQL.
    Returns a PEP-249 compliant connection object.
    """
    if "mysql.connector" in _DRIVERS:
        # mysql-connector-python
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            database=database if database else None,
            autocommit=True,  # convenient for DDL
        )
    # fallback: PyMySQL
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
        database=database if database else None,
        autocommit=True,  # convenient for DDL
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
    )


# ============ REQUIRED PROTOTYPES ============

def connect_db():
    """
    Connects to the MySQL server (no default database selected).
    Returns a connection or None on failure.
    """
    try:
        conn = _connect_raw(None)
        return conn
    except Exception as e:
        print(f"connect_db error: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    """
    try:
        with closing(connection.cursor()) as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    except Exception as e:
        print(f"create_database error: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    Returns a connection or None on failure.
    """
    try:
        conn = _connect_raw(DB_NAME)
        return conn
    except Exception as e:
        print(f"connect_to_prodev error: {e}")
        return None


def create_table(connection):
    """
    Creates the user_data table if it does not exist with required fields:
      - user_id (UUID text), PK, Indexed
      - name (VARCHAR, NOT NULL)
      - email (VARCHAR, NOT NULL)
      - age (DECIMAL, NOT NULL)
    """
    ddl = f"""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) NOT NULL,
        name    VARCHAR(255) NOT NULL,
        email   VARCHAR(255) NOT NULL,
        age     DECIMAL(5,0) NOT NULL,
        PRIMARY KEY (user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    # Explicit index on user_id (PK already creates it; kept for the spec)
    idx_user_id = "CREATE INDEX IF NOT EXISTS idx_user_data_user_id ON user_data (user_id);"

    try:
        with closing(connection.cursor()) as cur:
            cur.execute(ddl)
            # Some MySQLs don't support "IF NOT EXISTS" for CREATE INDEX.
            # So we wrap in try/except to be portable.
            try:
                cur.execute(idx_user_id)
            except Exception:
                # Fall back: check if index exists; if not, create without IF NOT EXISTS
                try:
                    cur.execute("SHOW INDEX FROM user_data WHERE Key_name = 'idx_user_data_user_id';")
                    exists = cur.fetchone()
                    if not exists:
                        cur.execute("CREATE INDEX idx_user_data_user_id ON user_data (user_id);")
                except Exception:
                    pass

        print("Table user_data created successfully")
    except Exception as e:
        print(f"create_table error: {e}")


def insert_data(connection, data):
    """
    Inserts CSV rows into user_data IF they do not already exist.
    'data' is a path to CSV (e.g., 'user_data.csv').

    CSV expected headers (order-insensitive):
        user_id, name, email, age
    If user_id is blank/missing, a UUID4 will be generated.
    A row is considered existing if a matching user_id OR email is found.
    """
    # Normalize CSV path (relative to current working dir)
    csv_path = os.path.abspath(data)

    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return

    try:
        with open(csv_path, newline="", encoding="utf-8") as f, closing(connection.cursor()) as cur:
            reader = csv.DictReader(f)
            # Make header names case-insensitive
            headers = [h.strip().lower() for h in reader.fieldnames] if reader.fieldnames else []
            # Map helper
            def _get(row, key):
                return row.get(key) or row.get(key.capitalize()) or row.get(key.upper())

            inserted = 0
            skipped = 0

            for row in reader:
                uid = (_get(row, "user_id") or "").strip()
                name = (_get(row, "name") or "").strip()
                email = (_get(row, "email") or "").strip()
                age_raw = (_get(row, "age") or "").strip()

                if not uid:
                    uid = str(uuid.uuid4())
                if not (name and email and age_raw):
                    # Skip incomplete rows
                    skipped += 1
                    continue

                try:
                    # Age may be integer-like; DECIMAL(5,0) expects numeric
                    age_val = int(str(age_raw).split(".")[0])
                except Exception:
                    skipped += 1
                    continue

                # Check existence by user_id OR email to prevent duplicates
                cur.execute(
                    "SELECT 1 FROM user_data WHERE user_id = %s OR email = %s LIMIT 1;",
                    (uid, email)
                )
                exists = cur.fetchone()

                if exists:
                    skipped += 1
                    continue

                cur.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                    (uid, name, email, age_val)
                )
                inserted += 1

            print(f"Inserted {inserted} rows; skipped {skipped} duplicates/invalid.")

    except Exception as e:
        print(f"insert_data error: {e}")


# ============ GENERATOR (streams rows one-by-one) ============

def stream_user_data(connection, batch_size: int = 1000):
    """
    Generator that streams rows from user_data one by one (memory-efficient).

    Usage:
        for row in seed.stream_user_data(conn, batch_size=500):
            print(row)

    Returns tuples (user_id, name, email, age) in user_id order.
    """
    try:
        # Use a non-buffered cursor where available to avoid loading all rows
        # mysql-connector: cursor(buffered=False)
        # PyMySQL: standard cursor is already server-side streaming for fetchmany
        if "mysql.connector" in _DRIVERS:
            cur = connection.cursor(buffered=False)
        else:
            cur = connection.cursor()

        with closing(cur) as cursor:
            cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id;")
            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                for row in rows:
                    yield row
    except Exception as e:
        # Turn DB errors into StopIteration-safe prints
        print(f"stream_user_data error: {e}")
        return

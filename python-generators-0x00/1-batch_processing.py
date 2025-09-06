#!/usr/bin/env python3
"""
1-batch_processing.py

Objective:
- Create a generator that fetches rows from MySQL in batches.
- Process each batch to filter users over age 25.

Prototypes required:
    def stream_users_in_batches(batch_size)
    def batch_processing(batch_size)

Constraints:
- Use yield (generator).
- Use no more than 3 loops in total across both functions.
"""

import os
import mysql.connector


def _connect():
    """Internal: connect to the ALX_prodev database using env vars or defaults."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database="ALX_prodev",
    )


def stream_users_in_batches(batch_size):
    """
    Generator that yields lists (batches) of user dict rows from user_data.

    Uses exactly ONE loop internally.
    """
    conn = _connect()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id;")

        batch = []
        # Loop #1
        for row in cur:
            batch.append(row)
            if len(batch) >= max(1, int(batch_size)):
                yield batch
                batch = []
        if batch:
            yield batch
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def batch_processing(batch_size):
    """
    Processes each batch and prints users with age > 25.

    This function uses TWO loops:
      - Loop #2 over batches
      - Loop #3 over rows in each batch
    Total loops across file: 3
    """
    # Loop #2
    for batch in stream_users_in_batches(batch_size):
        # Loop #3
        for user in batch:
            try:
                # age is stored as DECIMAL; mysql-connector returns int for DECIMAL(5,0)
                if int(user.get("age", 0)) > 25:
                    print(user)
            except Exception:
                # If age is malformed, skip the row silently
                continue

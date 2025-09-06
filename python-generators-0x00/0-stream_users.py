#!/usr/bin/env python3
"""
0-stream_users.py
Generator function to stream rows from user_data table one by one.
"""

import os
import mysql.connector


def stream_users():
    """
    Generator that yields rows from user_data table as dictionaries.
    Uses only one loop with yield.
    """
    # Read connection info from environment variables (fallback defaults)
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database="ALX_prodev",
    )

    cursor = conn.cursor(dictionary=True)  # returns rows as dicts
    cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY user_id;")

    # Single loop to stream rows
    for row in cursor:
        yield row

    cursor.close()
    conn.close()

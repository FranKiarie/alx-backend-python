#!/usr/bin/env python3
"""
2-lazy_paginate.py

Implements lazy pagination over user_data table.
- paginate_users(page_size, offset): fetches one page from DB
- lazy_pagination(page_size): generator yielding pages lazily

Constraints:
- Only ONE loop used in lazy_pagination
- Must use yield
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a page of rows from user_data with LIMIT + OFFSET.
    Returns a list of dict rows.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator: lazily yield one page of rows at a time.
    Uses only ONE loop.
    """
    offset = 0
    # Single loop
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

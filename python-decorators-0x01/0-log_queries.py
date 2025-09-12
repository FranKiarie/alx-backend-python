#!/usr/bin/env python3
"""
Task 0: Logging Database Queries
A decorator that logs SQL queries before execution.
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator that logs SQL queries before execution.
    
    Args:
        func: The function to be decorated
        
    Returns:
        The wrapped function that logs queries
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Fetch all users from the database with query logging.
    
    Args:
        query (str): SQL query to execute
        
    Returns:
        list: List of user records
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    print("=== Task 0: Logging Database Queries ===")
    print("Fetching all users with query logging...")
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users:")
    for user in users:
        print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

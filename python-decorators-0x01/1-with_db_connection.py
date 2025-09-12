#!/usr/bin/env python3
"""
Task 1: With DB Connection
A decorator that automatically manages database connections.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that automatically manages database connections.
    Opens a connection, passes it to the function, and closes it after execution.
    
    Args:
        func: The function to be decorated
        
    Returns:
        The wrapped function that manages database connections
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Get a user by their ID.
    
    Args:
        conn: Database connection
        user_id (int): The ID of the user to retrieve
        
    Returns:
        tuple: User record or None if not found
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


@with_db_connection
def get_all_users(conn):
    """
    Get all users from the database.
    
    Args:
        conn: Database connection
        
    Returns:
        list: List of all user records
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    print("=== Task 1: With DB Connection ===")
    
    print("Getting user with ID 1:")
    user = get_user_by_id(user_id=1)
    if user:
        print(f"  Found: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    else:
        print("  User not found")
    
    print("\nGetting user with ID 2:")
    user = get_user_by_id(user_id=2)
    if user:
        print(f"  Found: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    else:
        print("  User not found")
    
    print("\nGetting all users:")
    users = get_all_users()
    print(f"  Retrieved {len(users)} users:")
    for user in users:
        print(f"    ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

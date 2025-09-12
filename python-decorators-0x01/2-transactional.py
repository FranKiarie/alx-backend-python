#!/usr/bin/env python3
"""
Task 2: Transaction Management
A decorator that manages database transactions with automatic rollback on errors.
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


def transactional(func):
    """
    Decorator that manages database transactions.
    Commits on success, rolls back on any exception.
    
    Args:
        func: The function to be decorated
        
    Returns:
        The wrapped function that manages transactions
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[SUCCESS] Transaction committed successfully")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction failed: {e}")
            print("[ROLLBACK] Transaction rolled back")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email address.
    
    Args:
        conn: Database connection
        user_id (int): The ID of the user to update
        new_email (str): The new email address
        
    Returns:
        int: Number of rows affected
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    affected_rows = cursor.rowcount
    print(f"[UPDATE] Updated {affected_rows} user(s) with new email: {new_email}")
    return affected_rows


@with_db_connection
@transactional
def add_new_user(conn, name, email):
    """
    Add a new user to the database.
    
    Args:
        conn: Database connection
        name (str): User's name
        email (str): User's email
        
    Returns:
        int: ID of the newly created user
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    user_id = cursor.lastrowid
    print(f"[INSERT] Added new user with ID: {user_id}, Name: {name}, Email: {email}")
    return user_id


@with_db_connection
@transactional
def delete_user(conn, user_id):
    """
    Delete a user from the database.
    
    Args:
        conn: Database connection
        user_id (int): The ID of the user to delete
        
    Returns:
        int: Number of rows affected
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    affected_rows = cursor.rowcount
    print(f"[DELETE] Deleted {affected_rows} user(s) with ID: {user_id}")
    return affected_rows


if __name__ == "__main__":
    print("=== Task 2: Transaction Management ===")
    
    # Test successful transaction
    print("1. Testing successful email update:")
    try:
        update_user_email(user_id=1, new_email="john.updated@example.com")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n2. Testing successful user addition:")
    try:
        new_user_id = add_new_user(name="Test User", email="test@example.com")
        print(f"New user created with ID: {new_user_id}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n3. Testing transaction rollback (invalid operation):")
    try:
        # This will cause an error and rollback
        update_user_email(user_id=999, new_email="nonexistent@example.com")
    except Exception as e:
        print(f"Expected error occurred: {e}")
    
    print("\n4. Verifying current database state:")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    users = cursor.fetchall()
    conn.close()
    
    print(f"Current users in database ({len(users)} total):")
    for user in users:
        print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

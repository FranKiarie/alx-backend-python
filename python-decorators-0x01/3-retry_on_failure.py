#!/usr/bin/env python3
"""
Task 3: Retry on Failure
A decorator that retries database operations on failure with configurable retry count and delay.
"""

import time
import sqlite3
import functools
import random


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


def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function on failure.
    
    Args:
        retries (int): Number of retry attempts (default: 3)
        delay (float): Delay between retries in seconds (default: 2)
        
    Returns:
        The decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries - 1:  # Don't print on the last attempt
                        print(f"[Retry {attempt+1}/{retries}] Error: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print(f"[Final Attempt {attempt+1}/{retries}] Error: {e}")
            raise Exception(f"Operation failed after {retries} retries")
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetch all users with retry logic.
    Simulates occasional failures for demonstration.
    
    Args:
        conn: Database connection
        
    Returns:
        list: List of user records
    """
    # Simulate random failures for demonstration (30% chance)
    if random.random() < 0.3:
        raise Exception("Simulated database connection error")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


@with_db_connection
@retry_on_failure(retries=5, delay=0.5)
def get_user_by_id_with_retry(conn, user_id):
    """
    Get a user by ID with retry logic.
    
    Args:
        conn: Database connection
        user_id (int): The ID of the user to retrieve
        
    Returns:
        tuple: User record or None if not found
    """
    # Simulate occasional failures for demonstration (20% chance)
    if random.random() < 0.2:
        raise Exception("Simulated query timeout")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


@with_db_connection
@retry_on_failure(retries=2, delay=1)
def reliable_query(conn, query):
    """
    Execute a reliable query with retry logic.
    
    Args:
        conn: Database connection
        query (str): SQL query to execute
        
    Returns:
        list: Query results
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    print("=== Task 3: Retry on Failure ===")
    
    print("1. Testing fetch_users_with_retry (may fail and retry):")
    try:
        users = fetch_users_with_retry()
        print(f"[SUCCESS] Retrieved {len(users)} users:")
        for user in users[:3]:  # Show first 3 users
            print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        if len(users) > 3:
            print(f"  ... and {len(users) - 3} more users")
    except Exception as e:
        print(f"[FAILED] {e}")
    
    print("\n2. Testing get_user_by_id_with_retry (may fail and retry):")
    try:
        user = get_user_by_id_with_retry(user_id=1)
        if user:
            print(f"[SUCCESS] Found user: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        else:
            print("[SUCCESS] User not found")
    except Exception as e:
        print(f"[FAILED] {e}")
    
    print("\n3. Testing reliable_query with custom query:")
    try:
        results = reliable_query(query="SELECT COUNT(*) as user_count FROM users")
        print(f"[SUCCESS] Query result: {results[0][0]} users in database")
    except Exception as e:
        print(f"[FAILED] {e}")
    
    print("\n4. Testing with guaranteed failure (to show retry behavior):")
    
    @with_db_connection
    @retry_on_failure(retries=3, delay=0.5)
    def always_fail(conn):
        """Function that always fails for demonstration."""
        raise Exception("This operation always fails")
    
    try:
        always_fail()
    except Exception as e:
        print(f"[EXPECTED FAILURE] {e}")

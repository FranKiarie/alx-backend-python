#!/usr/bin/env python3
"""
Task 4: Cache Queries
A decorator that caches database query results to improve performance.
"""

import sqlite3
import functools
import hashlib
import json


# Global cache dictionary
query_cache = {}


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


def cache_query(func):
    """
    Decorator that caches database query results.
    Uses query string and parameters to create a cache key.
    
    Args:
        func: The function to be decorated
        
    Returns:
        The wrapped function that caches query results
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Create a cache key from the function name, query, and parameters
        query = kwargs.get("query", "")
        params = str(args[1:]) if len(args) > 1 else ""  # Skip conn parameter
        cache_key = f"{func.__name__}:{query}:{params}"
        
        # Check if result is in cache
        if cache_key in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {func.__name__}")
            return query_cache[cache_key]
        
        # Execute query and cache result
        print(f"[CACHE MISS] Executing query and caching result for: {func.__name__}")
        result = func(conn, *args, **kwargs)
        query_cache[cache_key] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users with caching enabled.
    
    Args:
        conn: Database connection
        query (str): SQL query to execute
        
    Returns:
        list: List of user records
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


@with_db_connection
@cache_query
def get_user_by_id_cached(conn, user_id):
    """
    Get a user by ID with caching.
    
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
@cache_query
def get_users_by_name_cached(conn, name_pattern):
    """
    Get users by name pattern with caching.
    
    Args:
        conn: Database connection
        name_pattern (str): Name pattern to search for
        
    Returns:
        list: List of matching user records
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name_pattern}%",))
    return cursor.fetchall()


def clear_cache():
    """Clear the query cache."""
    global query_cache
    query_cache.clear()
    print("[CACHE] Cache cleared")


def get_cache_stats():
    """Get cache statistics."""
    return {
        'cache_size': len(query_cache),
        'cached_queries': list(query_cache.keys())
    }


if __name__ == "__main__":
    print("=== Task 4: Cache Queries ===")
    
    print("1. Testing fetch_users_with_cache (first call - cache miss):")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users")
    
    print("\n2. Testing fetch_users_with_cache (second call - cache hit):")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users (from cache)")
    
    print("\n3. Testing get_user_by_id_cached (first call - cache miss):")
    user = get_user_by_id_cached(user_id=1)
    if user:
        print(f"Found user: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    
    print("\n4. Testing get_user_by_id_cached (second call - cache hit):")
    user = get_user_by_id_cached(user_id=1)
    if user:
        print(f"Found user: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    
    print("\n5. Testing get_user_by_id_cached with different ID (cache miss):")
    user = get_user_by_id_cached(user_id=2)
    if user:
        print(f"Found user: ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    
    print("\n6. Testing get_users_by_name_cached (first call - cache miss):")
    users = get_users_by_name_cached(name_pattern="Doe")
    print(f"Found {len(users)} users with 'Doe' in name:")
    for user in users:
        print(f"  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    
    print("\n7. Testing get_users_by_name_cached (second call - cache hit):")
    users = get_users_by_name_cached(name_pattern="Doe")
    print(f"Found {len(users)} users with 'Doe' in name (from cache)")
    
    print("\n8. Cache statistics:")
    stats = get_cache_stats()
    print(f"Cache size: {stats['cache_size']} entries")
    print("Cached queries:")
    for query in stats['cached_queries']:
        print(f"  - {query}")
    
    print("\n9. Testing cache clear:")
    clear_cache()
    stats = get_cache_stats()
    print(f"Cache size after clear: {stats['cache_size']} entries")
    
    print("\n10. Testing after cache clear (cache miss):")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Retrieved {len(users)} users (cache was cleared)")

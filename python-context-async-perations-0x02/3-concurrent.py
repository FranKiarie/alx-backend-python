#!/usr/bin/env python3
"""
Task 2: Concurrent async queries with aiosqlite + asyncio.gather
Demonstrates concurrent database operations using async/await patterns.
"""

import asyncio
from typing import List, Dict, Any
import aiosqlite

DB_PATH = "users.db"


async def async_fetch_users() -> List[Dict[str, Any]]:
    """Fetch all users from the database asynchronously."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def async_fetch_older_users() -> List[Dict[str, Any]]:
    """Fetch users older than 40 from the database asynchronously."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def async_fetch_young_users() -> List[Dict[str, Any]]:
    """Fetch users younger than 30 from the database asynchronously."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age < ?", (30,)) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]


async def fetch_concurrently() -> None:
    """Demonstrate concurrent database operations using asyncio.gather."""
    print("=== Task 2: Concurrent Async Queries ===")
    print("Fetching data concurrently...")
    
    # Execute multiple queries concurrently
    all_users, older_users, young_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
        async_fetch_young_users(),
    )

    print("\nAll users:")
    for row in all_users:
        print(f"  {row}")

    print(f"\nUsers older than 40 ({len(older_users)} found):")
    for row in older_users:
        print(f"  {row}")

    print(f"\nUsers younger than 30 ({len(young_users)} found):")
    for row in young_users:
        print(f"  {row}")


async def demonstrate_sequential_vs_concurrent() -> None:
    """Compare sequential vs concurrent execution times."""
    import time
    
    print("\n=== Performance Comparison ===")
    
    # Sequential execution
    start_time = time.time()
    all_users = await async_fetch_users()
    older_users = await async_fetch_older_users()
    young_users = await async_fetch_young_users()
    sequential_time = time.time() - start_time
    
    print(f"Sequential execution time: {sequential_time:.4f} seconds")
    
    # Concurrent execution
    start_time = time.time()
    all_users, older_users, young_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
        async_fetch_young_users(),
    )
    concurrent_time = time.time() - start_time
    
    print(f"Concurrent execution time: {concurrent_time:.4f} seconds")
    print(f"Speed improvement: {sequential_time/concurrent_time:.2f}x faster")


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
    asyncio.run(demonstrate_sequential_vs_concurrent())

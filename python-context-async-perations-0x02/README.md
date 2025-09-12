# Python Context Managers and Async Operations (0x02)

This project demonstrates Python context managers and asynchronous database operations using SQLite and aiosqlite.

## Project Structure

```
python-context-async-perations-0x02/
├── 0-databaseconnection.py    # Task 0: Class-based context manager
├── 1-execute.py              # Task 1: Reusable Query Context Manager
├── 3-concurrent.py           # Task 2: Concurrent async queries
├── seed_users.py             # Database seeding script
├── users.db                  # SQLite database with sample data
├── venv/                     # Virtual environment
└── README.md                 # This file
```

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install aiosqlite
   ```

3. **Seed the database:**
   ```bash
   python3 seed_users.py
   ```

## Database Schema

The `users` table contains:
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `email` (TEXT NOT NULL)
- `age` (INTEGER NOT NULL)

Sample data includes 4 users with different ages for testing various queries.

## Tasks Overview

### Task 0: Class-based Context Manager
- **File**: `0-databaseconnection.py`
- **Purpose**: Demonstrates a class-based context manager for database connections
- **Key Features**:
  - Implements `__enter__` and `__exit__` methods
  - Automatic connection management
  - Transaction handling (commit/rollback)
  - Exception propagation
  - Row factory for dict-like access

### Task 1: Reusable Query Context Manager
- **File**: `1-execute.py`
- **Purpose**: Shows a reusable context manager for executing queries
- **Key Features**:
  - Parameterized queries with type hints
  - Automatic result fetching
  - Connection lifecycle management
  - Support for parameterized queries
  - Multiple query examples

### Task 2: Concurrent Async Queries
- **File**: `3-concurrent.py`
- **Purpose**: Demonstrates concurrent database operations using async/await
- **Key Features**:
  - Uses `aiosqlite` for async SQLite operations
  - `asyncio.gather` for concurrent execution
  - Performance comparison (sequential vs concurrent)
  - Multiple async query functions
  - Proper async context management

## Running the Scripts

```bash
# Run individual tasks
python3 0-databaseconnection.py
python3 1-execute.py
python3 3-concurrent.py

# Seed database (run once)
python3 seed_users.py
```

## Key Concepts Demonstrated

1. **Context Managers**:
   - Class-based context managers with `__enter__` and `__exit__`
   - Automatic resource management
   - Exception handling and cleanup

2. **Async Programming**:
   - Async/await syntax
   - Concurrent execution with `asyncio.gather`
   - Async context managers
   - Performance benefits of concurrency

3. **Database Operations**:
   - SQLite with both sync and async libraries
   - Parameterized queries for security
   - Row factories for better data access
   - Transaction management

4. **Type Hints**:
   - Comprehensive type annotations
   - Optional types and generics
   - Return type specifications

## Dependencies

- Python 3.8+
- `aiosqlite` (for async SQLite operations)
- `sqlite3` (built into Python)

## Learning Objectives

After completing this project, you should understand:

- How to create custom context managers
- The benefits of using context managers for resource management
- Async/await patterns in Python
- Concurrent database operations
- Performance implications of sequential vs concurrent execution
- Type hints and modern Python practices
- SQLite operations with both sync and async libraries

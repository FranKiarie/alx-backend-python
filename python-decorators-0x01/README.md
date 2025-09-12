# Python Decorators Project (0x01)

This project demonstrates various Python decorators for database operations, showcasing different patterns and use cases.

## Project Structure

```
python-decorators-0x01/
├── 0-log_queries.py          # Task 0: Logging Database Queries
├── 1-with_db_connection.py   # Task 1: With DB Connection
├── 2-transactional.py        # Task 2: Transaction Management
├── 3-retry_on_failure.py     # Task 3: Retry on Failure
├── 4-cache_query.py          # Task 4: Cache Queries
├── users.db                  # SQLite database with sample data
└── README.md                 # This file
```

## Database Setup

The project uses SQLite with a `users` table containing sample data:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
```

## Tasks Overview

### Task 0: Logging Database Queries
- **File**: `0-log_queries.py`
- **Purpose**: Demonstrates a decorator that logs SQL queries before execution
- **Key Features**:
  - Logs query strings to console
  - Uses `functools.wraps` to preserve function metadata
  - Works with keyword arguments

### Task 1: With DB Connection
- **File**: `1-with_db_connection.py`
- **Purpose**: Shows automatic database connection management
- **Key Features**:
  - Opens database connection before function execution
  - Passes connection as first argument to decorated function
  - Automatically closes connection in `finally` block
  - Ensures connection cleanup even on exceptions

### Task 2: Transaction Management
- **File**: `2-transactional.py`
- **Purpose**: Implements transaction management with automatic rollback
- **Key Features**:
  - Commits transactions on success
  - Rolls back on any exception
  - Combines with `with_db_connection` decorator
  - Demonstrates decorator chaining

### Task 3: Retry on Failure
- **File**: `3-retry_on_failure.py`
- **Purpose**: Shows retry logic with configurable parameters
- **Key Features**:
  - Configurable retry count and delay
  - Simulates failures for demonstration
  - Exponential backoff support
  - Detailed logging of retry attempts

### Task 4: Cache Queries
- **File**: `4-cache_query.py`
- **Purpose**: Implements query result caching
- **Key Features**:
  - Caches query results based on function name and parameters
  - Cache hit/miss logging
  - Cache statistics and management
  - Memory-based caching with global dictionary

## Running the Scripts

Each script can be run independently:

```bash
# Run individual tasks
python3 0-log_queries.py
python3 1-with_db_connection.py
python3 2-transactional.py
python3 3-retry_on_failure.py
python3 4-cache_query.py
```

## Key Decorator Patterns Demonstrated

1. **Function Wrapping**: Using `functools.wraps` to preserve metadata
2. **Parameter Passing**: Handling both positional and keyword arguments
3. **Decorator Chaining**: Combining multiple decorators
4. **Exception Handling**: Proper error handling and cleanup
5. **State Management**: Managing global state (cache) across function calls
6. **Configuration**: Parameterized decorators with configurable behavior

## Dependencies

- Python 3.8+
- SQLite3 (built into Python)
- No external dependencies required

## Learning Objectives

After completing this project, you should understand:

- How to create custom decorators in Python
- Best practices for decorator implementation
- Database connection management patterns
- Transaction handling and error recovery
- Caching strategies for database operations
- Decorator composition and chaining
- Exception handling in decorators

## Notes

- The database file (`users.db`) is created automatically when running the scripts
- Some scripts include simulated failures for demonstration purposes
- All scripts include comprehensive error handling and logging
- The cache implementation is in-memory and will be lost when the program exits

# Unit Tests and Integration Tests

This directory contains unit tests and integration tests for the ALX Backend Python project.

## Files

- `test_utils.py` - Unit tests for the `utils` module
- `test_client.py` - Unit tests and integration tests for the `client` module

## Test Coverage

### test_utils.py

- **TestAccessNestedMap**: Tests for `access_nested_map` function
  - `test_access_nested_map`: Parameterized tests for valid inputs
  - `test_access_nested_map_exception`: Parameterized tests for KeyError exceptions

- **TestGetJson**: Tests for `get_json` function
  - `test_get_json`: Parameterized tests with mocked HTTP calls

- **TestMemoize**: Tests for `memoize` decorator
  - `test_memoize`: Tests caching functionality

### test_client.py

- **TestGithubOrgClient**: Unit tests for `GithubOrgClient` class
  - `test_org`: Tests organization data retrieval
  - `test_public_repos_url`: Tests public repos URL property
  - `test_public_repos`: Tests public repos method
  - `test_has_license`: Tests license checking

- **TestIntegrationGithubOrgClient**: Integration tests
  - `test_public_repos`: Integration test with fixtures

## Running Tests

```bash
# Run all tests
python3 -m unittest discover

# Run specific test file
python3 -m unittest test_utils.py
python3 -m unittest test_client.py

# Run with verbose output
python3 -m unittest -v test_utils.py
```

## Dependencies

- `unittest` - Python's built-in testing framework
- `parameterized` - For parameterized test cases
- `unittest.mock` - For mocking objects and functions

## Installation

```bash
pip install parameterized
```


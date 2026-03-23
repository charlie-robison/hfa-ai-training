# Testing Standards

## Running Tests
```bash
pytest                              # All tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests only
pytest -k "test_pricing"            # Tests matching a pattern
pytest --cov=src --cov-report=html  # With coverage report
```

## Conventions
- Test files: `test_<module>.py`
- Test functions: `test_<behavior>_<scenario>`
- Example: `test_calculate_price_returns_zero_for_invalid_sqft`
- One assertion per test when possible
- Use fixtures for shared setup, not setUp methods

## Unit vs Integration
- **Unit tests** (`tests/unit/`): no network, no database, no file I/O. Mock external dependencies.
- **Integration tests** (`tests/integration/`): hit real databases and APIs. Use test fixtures for known data.

## What to Test
- All public functions in `src/services/`
- All API endpoints in `src/api/`
- Edge cases: empty inputs, None values, boundary conditions
- Error paths: invalid data, API failures, timeouts

# Module 4: Assignment-Professional Calculator Command-Line Application with 100% Test Coverage

## Usage

Run the calculator:
```
python main.py
```

- Enter operations like `add 2 3` or `divide 10 2`.
- Use `history` to view past calculations.
- Use `help` for instructions.
- Type `exit` to quit.

Example:
```
Welcome to the calculator!

Enter operation (add, subtract, multiply, divide) followed by two numbers or exit to quit, history and help: add 5 3

The result is 8
```

## Testing

The project includes unit tests with 100% coverage using pytest and pytest-cov.

Run tests locally:
```
pytest --cov=app --cov-report=term --cov-fail-under=100
```

This will execute 26 tests and verify 100% coverage.

## CI/CD

GitHub Actions is configured to run tests on push/pull requests to main/master branches. It installs dependencies, runs pytest with coverage, and fails if coverage is below 100%.

## Author

Saketh Puramsetti
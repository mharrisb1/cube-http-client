# Contributing to cube-http-client

Thank you for your interest in contributing to cube-http-client! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Running Tests](#running-tests)
- [Running Examples](#running-examples)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Development Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- [uv](https://github.com/astral-sh/uv) for dependency management

### Initial Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/cube-http-client.git
   cd cube-http-client
   ```

2. Create and activate a virtual environment using uv:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:

   ```bash
   uv pip install -e ".[dev]"
   ```

4. Start the Docker environment for development:
   ```bash
   make setup
   ```

## Development Workflow

The project uses a `Makefile` to simplify common development tasks. Here are the available commands:

```bash
make setup           # Start Docker development environment
make teardown        # Stop Docker development environment
make format          # Format code with ruff
make static          # Static analysis with ty
make test            # Run all tests (auto-starts Docker)
make test-PATTERN    # Run tests matching PATTERN (auto-starts Docker)
make example-NAME    # Run example/NAME.py (auto-starts Docker)
make examples        # Run all examples (auto-starts Docker)
make check           # Run all checks (format, static, test)
make clean           # Clean up and stop Docker environment
make help            # Show this help message
```

## Running Tests

Tests require a running Docker environment with Cube.dev. The `make test` command will automatically start Docker if needed.

```bash
# Run all tests
make test

# Run specific tests matching a pattern
make test-meta
make test-load
```

## Running Examples

The project includes example scripts in the `examples/` directory. You can run them with the following commands:

```bash
# Run the quickstart example
make example-quickstart

# Run the async quickstart example
make example-async

# Run all examples
make examples
```

These commands will automatically start the Docker environment if it's not already running.

## Code Style

This project uses:

- [Ruff](https://github.com/astral-sh/ruff) for code formatting
- [Ty](https://github.com/astral-sh/ty) for static type checking

Before submitting a PR, make sure your code passes these checks:

```bash
make format     # Format code
make static     # Run static analysis
```

You can run all checks (including tests) with:

```bash
make check
```

### Code Style Guidelines

1. Use descriptive variable names and add docstrings to all public functions and classes.
2. Follow PEP 8 style guidelines.
3. Use type hints for all function parameters and return values.
4. Write unit tests for new features and ensure all tests pass.

## Pull Request Process

1. Fork the repository and create a new branch from `main`.
2. Make your changes and ensure they follow the code style guidelines.
3. Run tests and ensure all tests pass.
4. Update documentation if needed.
5. Submit a pull request.

### PR Guidelines

1. Keep PRs focused on a single feature or bug fix.
2. Include tests for new features or bug fixes.
3. Update or add documentation as needed.
4. Provide a clear description of the changes in the PR.

## Release Process

Releases are managed by the maintainers of the project. The general process is:

1. Update the version number in `pyproject.toml`.
2. Update the CHANGELOG.md file.
3. Create a new release on GitHub.
4. Publish the package to PyPI.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license (see LICENSE file).

## Questions or Need Help?

If you have questions or need help, please open an issue on GitHub or reach out to the maintainers.

# Development tasks for cube-http-client

.PHONY: format static test setup teardown examples clean help

# Start Docker development environment
setup:
	@echo "Starting Docker development environment..."
	cd docker && docker compose up -d
	@echo "Waiting for services to start..."
	@sleep 10
	@echo "Docker environment is ready!"

# Stop Docker development environment
teardown:
	@echo "Stopping Docker development environment..."
	cd docker && docker compose down
	@echo "Docker environment stopped."

# Format code with ruff
format:
	uv run ruff format src tests examples

# Static analysis with ty
static:
	uv run ty check src tests examples

# Run tests (requires Docker environment)
test: setup
	uv run pytest tests -v

# Run a specific test with optional pattern (requires Docker environment)
test-%: setup
	uv run pytest tests -v -k "$*"

# Run an example from the examples directory (requires Docker environment)
example-%: setup
	uv run python examples/$*.py

# Run all examples (requires Docker environment)
examples: setup
	@echo "Running all examples..."
	uv run python examples/quickstart.py
	uv run python examples/async_quickstart.py
	uv run python examples/custom_response_models.py
	uv run python examples/context_manager_examples.py
	uv run python examples/custom_client_examples.py
	@echo "Examples completed."

# Run all checks (format and static analysis don't require Docker)
check: format static test

build:
	rm -rf dist
	uv build

# Clean up
clean: teardown
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "Cleanup complete."

e2e: check examples clean

# Display help
help:
	@echo "Available targets:"
	@echo "  make setup           Start Docker development environment"
	@echo "  make teardown        Stop Docker development environment"
	@echo "  make format          Format code with ruff"
	@echo "  make static          Static analysis with ty"
	@echo "  make test            Run all tests (auto-starts Docker)"
	@echo "  make test-PATTERN    Run tests matching PATTERN (auto-starts Docker)"
	@echo "  make example-NAME    Run example/NAME.py (auto-starts Docker)"
	@echo "  make examples        Run all examples (auto-starts Docker)"
	@echo "  make check           Run all checks (format, static, test)"
	@echo "  make clean           Clean up and stop Docker environment"
	@echo "  make build			  Clean out previous builds and build the project"
	@echo "  make help            Show this help message"

# Default target
.DEFAULT_GOAL := help

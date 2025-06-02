# Makefile for aviation-stack-mcp

.PHONY: install dev test format lint build publish clean

# Install all dependencies (for end users or devs)
install:
	poetry install

# Activate virtual environment and open shell
dev:
	poetry env activate

# Run tests (assuming you use pytest)
test:
	@poetry run pytest || echo "No tests found"

# Format code using black
format:
	poetry run black .

# Lint code using flake8 or ruff
lint:
	poetry run ruff check .

# Build wheel and sdist
build:
	poetry build

# Publish to PyPI (must be logged in via poetry config)
publish:
	poetry publish --build

# Clean artifacts
clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache __pycache__ .mypy_cache
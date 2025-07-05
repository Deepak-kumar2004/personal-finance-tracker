# Personal Finance Tracker - Makefile
# Provides common development tasks

.PHONY: help install install-dev setup run clean test lint format check-format type-check all-checks pre-commit-install pre-commit-run

# Default target
help:
	@echo "Personal Finance Tracker - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup          - Run setup script (creates venv, installs deps)"
	@echo "  make install        - Install dependencies"
	@echo "  make install-dev    - Install with development dependencies"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo ""
	@echo "Development Commands:"
	@echo "  make run            - Run the application"
	@echo "  make test           - Run tests (when implemented)"
	@echo "  make lint           - Run linting checks"
	@echo "  make format         - Format code with black"
	@echo "  make check-format   - Check code formatting"
	@echo "  make type-check     - Run type checking with mypy"
	@echo "  make all-checks     - Run all code quality checks"
	@echo "  make pre-commit-run - Run pre-commit hooks manually"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean          - Clean up temporary files"
	@echo "  make help           - Show this help message"

# Setup and Installation
setup:
	@echo "Running setup script..."
	./setup.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .[dev]

# Pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install

pre-commit-run:
	@echo "Running pre-commit hooks..."
	pre-commit run --all-files

# Development
run:
	@echo "Starting Personal Finance Tracker..."
	python run.py

test:
	@echo "Running tests..."
	@echo "Note: Test framework not yet implemented"
	# pytest

lint:
	@echo "Running flake8..."
	flake8 app/ config/ run.py --max-line-length=88 --extend-ignore=E203,W503
	@echo "Running pylint..."
	pylint app/ config/ run.py --exit-zero --reports=no --score=no

format:
	@echo "Formatting code with black..."
	black app/ config/ run.py

check-format:
	@echo "Checking code formatting..."
	black --check app/ config/ run.py

type-check:
	@echo "Running type checks..."
	mypy app/ config/ run.py --ignore-missing-imports

all-checks: check-format lint type-check
	@echo "All code quality checks completed!"
	@echo "Consider running: make pre-commit-run"

# Utility
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Environment setup help
env-help:
	@echo "Environment Setup:"
	@echo "1. Create virtual environment: python -m venv .venv"
	@echo "2. Activate it: source .venv/bin/activate"
	@echo "3. Install dependencies: make install"
	@echo "4. Run application: make run"

# Contributing to Suno CLI

Thank you for your interest in contributing to Suno CLI!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/AceDataCloud/SunoCli.git
cd SunoCli

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install all development dependencies
pip install -e ".[dev,test]"

# Copy the example environment file
cp .env.example .env
```

## Code Quality

We use automated tools to maintain code quality:

```bash
# Lint with ruff
ruff check .

# Format with ruff
ruff format .

# Type check with mypy
mypy core commands
```

## Testing

```bash
# Run all unit tests
pytest

# Run with coverage
pytest --cov=core --cov=commands

# Run a specific test file
pytest tests/test_commands.py -v
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run the full test suite: `pytest`
5. Run linting: `ruff check . && ruff format --check .`
6. Commit changes with a clear message
7. Push and open a Pull Request

## Project Structure

```
SunoCli/
├── core/           # Core modules (client, config, output, exceptions)
├── commands/       # CLI command groups (one file per domain)
├── tests/          # Test suite (mirrors core/ and commands/)
├── main.py         # CLI entry point
└── pyproject.toml  # Project metadata and dependencies
```

## Adding a New Command

1. Add the click command in the appropriate `commands/*.py` file
2. Register it in `main.py` via `cli.add_command()`
3. Add tests in `tests/test_commands.py`
4. Update the README commands table

## Code Style

- Python 3.10+ type hints required
- Use `click` for CLI commands
- Use `rich` for formatted terminal output
- Use `httpx` for HTTP requests
- Follow ruff's default formatting rules

## Reporting Issues

Use [GitHub Issues](https://github.com/AceDataCloud/SunoCli/issues) to report bugs or request features. Include:

- Python version
- Suno CLI version (`suno --version`)
- Steps to reproduce
- Expected vs actual behavior

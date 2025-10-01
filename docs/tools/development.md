# Development Workflow

## Setup

### Initial Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-agent-config
```

2. Install dependencies:
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or install separately
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Development Environment

We use the following tools for code quality:

- **pytest**: Testing framework with coverage reporting
- **ruff**: Fast Python formatter and linter (line length: 100)
- **mypy**: Static type checking

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b issue-123-description
```

### 2. Write Code

Follow these standards:
- Use type hints for all function parameters and returns
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines
- Follow the existing code structure

### 3. Format and Lint

```bash
# Format code
ruff format .

# Check formatting without changes
ruff format --check .

# Check linting
ruff check .

# Fix auto-fixable issues
ruff check . --fix
```

### 4. Type Check

```bash
mypy tools/
mypy scripts/
```

### 5. Write Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Aim for >80% code coverage
- Test both success and error cases

Example test structure:
```python
import pytest
from tools.config.config_manager import ConfigManager

def test_config_manager_initialization():
    """Test ConfigManager initializes correctly."""
    manager = ConfigManager()
    assert manager is not None

def test_config_manager_load_config():
    """Test ConfigManager loads configuration."""
    manager = ConfigManager()
    config = manager.load_config("test-config.yaml")
    assert config["version"] == "1.0"
```

### 6. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tools --cov=scripts

# Run specific test file
pytest tests/test_config_manager.py

# Run with verbose output
pytest -v
```

### 7. Commit Changes

```bash
git add .
git commit -m "feat: add ConfigManager tool for centralized configuration"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 8. Push and Create PR

```bash
git push origin feature/your-feature-name
gh pr create --title "Add ConfigManager tool" --body "Description of changes"
```

## Testing Guidelines

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_config_manager.py
├── test_notes_processor.py
└── fixtures/
    ├── test-config.yaml
    └── test-note.md
```

### Fixtures

Use `conftest.py` for shared fixtures:

```python
import pytest
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_config(test_data_dir):
    """Load sample configuration."""
    return test_data_dir / "test-config.yaml"
```

### Coverage Requirements

- Minimum 80% overall coverage
- All new features must have tests
- Critical paths must have 100% coverage

## Code Quality Standards

### Type Hints

All functions must have type hints:

```python
from typing import Dict, List, Optional

def process_notes(
    note_path: str,
    config: Dict[str, Any],
    strict: bool = False
) -> List[Dict[str, str]]:
    """Process notes and extract metadata."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from note content.

    Args:
        content: The raw note content with frontmatter

    Returns:
        Dictionary containing parsed frontmatter metadata

    Raises:
        ValueError: If frontmatter is malformed
    """
    ...
```

### Error Handling

- Use specific exception types
- Provide clear error messages
- Include context in exceptions

```python
try:
    config = load_yaml(config_path)
except FileNotFoundError:
    raise ValueError(f"Configuration file not found: {config_path}")
except yaml.YAMLError as e:
    raise ValueError(f"Invalid YAML in {config_path}: {e}")
```

## Continuous Integration

All pull requests must pass:
- ✅ Ruff formatting check
- ✅ Ruff linting check
- ✅ Mypy type checking
- ✅ Pytest with >80% coverage

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create release branch
4. Tag release: `git tag v0.1.0`
5. Push tag: `git push origin v0.1.0`

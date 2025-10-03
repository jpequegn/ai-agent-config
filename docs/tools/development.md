# Development Guide

Guide for developing and contributing to the tools suite.

## Setup

```bash
# Clone repository
git clone https://github.com/jpequegn/ai-agent-config.git
cd ai-agent-config

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Development Workflow

### 1. Create Branch
```bash
git checkout -b issue-XXX-feature-name
```

### 2. Write Tests First (TDD)
```python
# tests/test_my_tool.py
def test_my_feature():
    tool = MyTool()
    result = tool.my_feature(input)
    assert result == expected
```

### 3. Implement Feature
```python
# tools/my_tool.py
class MyTool:
    def my_feature(self, input):
        """
        Brief description.
        
        Args:
            input: Description
        
        Returns:
            Description
        
        Example:
            >>> tool = MyTool()
            >>> tool.my_feature("test")
            'result'
        """
        return result
```

### 4. Run Tests
```bash
pytest tests/test_my_tool.py -v
pytest tests/ --cov=tools --cov-report=html
```

### 5. Update Documentation
- Add docstrings to all public methods
- Update tool documentation in docs/tools/
- Add usage examples

### 6. Create PR
```bash
git commit -m "Add my feature (#XXX)"
git push origin issue-XXX-feature-name
gh pr create
```

## Code Style

### Python Style
- Follow PEP 8
- Use type hints
- Write descriptive docstrings
- Keep functions focused (single responsibility)

### Naming Conventions
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### Documentation Style
```python
def function_name(param: str) -> Dict[str, Any]:
    """
    One-line summary.
    
    Longer description if needed.
    
    Args:
        param: Description with type
    
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception occurs
        
    Example:
        >>> function_name("test")
        {'result': 'value'}
    """
```

## Testing Guidelines

### Test Structure
```python
import pytest
from tools import MyTool

@pytest.fixture
def tool():
    return MyTool()

class TestMyFeature:
    def test_basic_case(self, tool):
        result = tool.my_feature("input")
        assert result == expected
    
    def test_edge_case(self, tool):
        result = tool.my_feature("")
        assert result is None
    
    def test_error_handling(self, tool):
        with pytest.raises(ValueError):
            tool.my_feature(None)
```

### Coverage Goals
- Core tools: >85%
- Specialized tools: >70%
- Focus on business logic, not boilerplate

## Performance Guidelines

### Targets
- Configuration reads (cached): <10ms
- NLP operations: <10ms
- Note parsing: <50ms
- Output formatting: <20ms

### Optimization
- Use caching for expensive operations
- Prefer O(n) algorithms
- Lazy load when possible
- Profile before optimizing

## Release Process

### Version Bump
Tools don't have separate versions - they follow repository releases.

### Changelog
Update CHANGELOG.md with:
- New features
- Bug fixes
- Breaking changes
- Performance improvements

## Contributing

### Good First Issues
Look for issues labeled "good first issue" or "documentation".

### Review Process
- All PRs require review
- CI must pass (tests, linting)
- Documentation must be updated
- Test coverage must not decrease

## Getting Help

- Check existing tool implementations
- Read tests for usage examples
- Ask in GitHub issues
- Review documentation

## See Also
- [Migration Guide](migration_guide.md)
- [Tool Documentation](README.md)
- [Testing Best Practices](https://docs.pytest.org/)

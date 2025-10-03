# Migration Guide: Commands to Tools

Step-by-step guide for migrating custom commands from long prompts to tools.

## Why Migrate?

**Before** (400-600 lines):
- Manual parsing logic in prompts
- Hard to test and maintain
- Inconsistent across commands
- Duplicate code everywhere

**After** (100-200 lines):
- Tested tools (85-93% coverage)
- Consistent behavior
- Easy to extend
- Reusable components

## Migration Process

### Step 1: Identify Parsing Logic

Find sections in your command that:
- Parse dates ("tomorrow", "next week")
- Extract entities (assignees, priorities)
- Parse natural language queries
- Look up configuration
- Format output

### Step 2: Replace with Tools

```python
# BEFORE: Manual date parsing
if date_text == "tomorrow":
    due_date = datetime.now() + timedelta(days=1)
elif date_text == "next week":
    due_date = datetime.now() + timedelta(weeks=1)

# AFTER: Use NLPProcessor
from tools import NLPProcessor
nlp = NLPProcessor()
date_expr = nlp.parse_date_expression(date_text)
due_date = date_expr.resolved_date
```

### Step 3: Test Integration

```bash
# Test the command
/your-command test-input

# Run unit tests if available
pytest tests/test_your_command.py
```

### Step 4: Update Documentation

Update command markdown to show tool usage.

## Common Patterns

### Pattern 1: Date Handling
```python
from tools import NLPProcessor
nlp = NLPProcessor()

# Single dates
date = nlp.parse_date_expression(user_input)

# Date ranges
date_range = nlp.parse_date_range(user_input)
```

### Pattern 2: Configuration Lookup
```python
from tools import ConfigManager
config = ConfigManager()

# Get project
project = config.get_project("mobile-app-v2")

# Get all projects
projects = config.get_all_projects(filters={"status": ["active"]})
```

### Pattern 3: Natural Language Queries
```python
from tools import NLPProcessor
nlp = NLPProcessor()

# Parse user query
intent = nlp.parse_command_intent(user_query)

# Extract filters
assignees = intent.filters.get("assignees", [])
priority = intent.filters.get("priority")
date_range = intent.filters.get("date_range")
```

### Pattern 4: Output Formatting
```python
from tools import OutputFormatter
formatter = OutputFormatter()

# Format with template
output = formatter.format(data, template="project_status")
```

## Example Migration

### Before: /todo command (300 lines)
```markdown
Parse date:
- if "tomorrow" → add 1 day
- if "next week" → add 7 days
- if "MM-DD-YYYY" → parse format
...150 lines of date parsing logic...
```

### After: /todo command (150 lines)
```python
from tools import NLPProcessor

nlp = NLPProcessor()
due_date = nlp.parse_date_expression(date_input).resolved_date
```

**Result**: 50% reduction, tested, supports 20+ date formats.

## Troubleshooting

### Tool Not Found
Ensure tools are installed:
```bash
pip install -r requirements.txt
```

### Import Error
Check tools/__init__.py for correct exports.

### Unexpected Behavior
Check tool tests for expected behavior:
```bash
pytest tests/test_nlp_processor.py -v
```

## See Also
- [Development Guide](development.md)
- [Tool Documentation](README.md)
- GitHub Issues: #179-184 for migration examples

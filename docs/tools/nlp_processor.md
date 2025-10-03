# NLPProcessor - Natural Language Processing

Natural language processing utilities for date parsing, entity extraction, command intent classification, and fuzzy matching.

## Quick Start

```python
from tools import NLPProcessor

nlp = NLPProcessor()

# Parse dates
date = nlp.parse_date_expression("tomorrow")
date_range = nlp.parse_date_range("last month")

# Extract entities
assignees = nlp.extract_assignees("@john,@sarah")
priority = nlp.extract_priorities("[high] urgent task")

# Parse command intent
intent = nlp.parse_command_intent("find notes about budget from last month")

# Fuzzy matching
matches = nlp.fuzzy_match("mobil", ["mobile-app-v2", "web-portal"], threshold=0.7)
```

## Features

### Date Parsing
- **Relative**: tomorrow, yesterday, next week, last month
- **Offsets**: in 3 days, 5 days ago, in 2 weeks
- **Absolute**: 2024-12-25, 12/25/2024
- **Ranges**: this week, last month, this year

### Entity Extraction
- **Assignees**: @mentions, "assign to john", comma-separated
- **Priorities**: [high], urgent, priority:high
- **Dates**: Any parseable date expression

### Command Intent
Parses natural language into structured CommandIntent with action, subject, and filters.

### Fuzzy Matching
Typo-tolerant string matching with configurable threshold (0.0-1.0).

## API Reference

See [tools/nlp_processor.py](../../tools/nlp_processor.py) for complete API.

Key methods:
- `parse_date_expression(text)` → DateExpression
- `parse_date_range(text)` → DateRange
- `extract_assignees(text)` → List[str]
- `extract_priorities(text)` → Priority
- `parse_command_intent(text)` → CommandIntent
- `fuzzy_match(query, candidates, threshold)` → List[FuzzyMatch]

## Performance

- All operations: <10ms
- Date parsing: ~1-2ms
- Intent parsing: ~3-5ms
- Fuzzy matching: ~5-8ms (depends on candidate count)

## Test Coverage: 93%

See [tests/test_nlp_processor.py](../../tests/test_nlp_processor.py) - 49 passing tests.

## See Also
- [Migration Guide](migration_guide.md) - Migrating commands to use NLP
- [Main README](README.md) - Tool suite overview

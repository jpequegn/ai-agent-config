# Tools Documentation

Comprehensive documentation for the AI Agent Config tool suite - a collection of reusable Python tools that power custom commands for intelligent productivity workflows.

## Overview

The tools suite provides battle-tested, modular utilities for:

- **Configuration Management** - Type-safe YAML configuration with Pydantic validation
- **Data Collection** - Multi-source data aggregation (GitHub, notes, calendar, projects)
- **Natural Language Processing** - Date parsing, entity extraction, command intent classification
- **Note Processing** - PARA Method implementation with action item extraction
- **Health Calculation** - Algorithmic scoring for projects, teams, and systems
- **Stakeholder Analysis** - Decision support with power/interest analysis
- **Output Formatting** - Template-based, consistent output across commands
- **API Management** - Unified API integration with rate limiting and caching

## Why Tools?

**Before**: Custom commands with 400-600 lines of embedded logic and manual parsing
- Hard to maintain and test
- Inconsistent behavior across commands
- Duplicate parsing logic everywhere
- No reusability

**After**: Thin command wrappers (100-200 lines) using tested tools
- 93%+ test coverage
- Consistent behavior
- Single source of truth
- Easy to extend

## Quick Start

```python
# Configuration management
from tools import ConfigManager
config = ConfigManager()
projects = config.get_all_projects()

# Natural language processing
from tools import NLPProcessor
nlp = NLPProcessor()
date = nlp.parse_date_expression("tomorrow")  # → datetime
intent = nlp.parse_command_intent("find notes about budget")

# Note processing
from tools import NoteProcessor
processor = NoteProcessor()
note = processor.parse_note("path/to/note.md")
action_items = processor.get_all_action_items()

# Output formatting
from tools import OutputFormatter
formatter = OutputFormatter()
output = formatter.format(data, template="project_status")
```

## Tool Suite

### Core Tools

| Tool | Purpose | Coverage | Docs |
|------|---------|----------|------|
| [ConfigManager](config_manager.md) | Type-safe YAML config with caching | 18% | ✓ |
| [NLPProcessor](nlp_processor.md) | Natural language understanding | 93% | ✓ |
| [NoteProcessor](note_processor.md) | PARA Method note processing | 18% | ✓ |
| [OutputFormatter](output_formatter.md) | Template-based output | 17% | ✓ |

### Specialized Tools

| Tool | Purpose | Coverage | Docs |
|------|---------|----------|------|
| [DataCollector](data_collector.md) | Multi-source data aggregation | 15% | ✓ |
| [HealthCalculator](health_calculator.md) | Algorithmic health scoring | 14% | ✓ |
| [StakeholderAnalyzer](stakeholder_analyzer.md) | Decision support analysis | 14% | ✓ |
| [APIManager](api_manager.md) | Unified API integration | 17% | ✓ |

## Integration Patterns

### Pattern 1: Configuration + Processing
```python
from tools import ConfigManager, NoteProcessor

config = ConfigManager()
processor = NoteProcessor(para_root=config.get_para_root())
notes = processor.search_notes(filters={"project": "mobile-app-v2"})
```

### Pattern 2: NLP + Config Lookup
```python
from tools import NLPProcessor, ConfigManager

nlp = NLPProcessor()
config = ConfigManager()

# Parse natural language query
intent = nlp.parse_command_intent("show status for mobile-app project")

# Fuzzy match project ID
projects = list(config.get_all_projects().keys())
matches = nlp.fuzzy_match(intent.filters.get("query", ""), projects)
```

### Pattern 3: Multi-Tool Orchestration
```python
from tools import ConfigManager, DataCollector, HealthCalculator, OutputFormatter

# Collect data
config = ConfigManager()
collector = DataCollector(config)
data = collector.collect_project_data("mobile-app-v2")

# Calculate health
calculator = HealthCalculator()
health = calculator.calculate_project_health(data)

# Format output
formatter = OutputFormatter()
output = formatter.format(health, template="health_report")
```

## Design Principles

### 1. Single Responsibility
Each tool has one clear purpose and does it well.

### 2. Type Safety
Pydantic models for all data structures with validation.

### 3. Testability
Comprehensive test coverage with isolated unit tests.

### 4. Performance
- Caching for expensive operations (<10ms cached reads)
- Efficient algorithms (O(n) or better)
- Lazy loading where appropriate

### 5. Error Handling
- Clear exception hierarchy
- Graceful degradation
- Helpful error messages

### 6. Documentation
- Docstrings for all public APIs
- Usage examples
- Integration guides

## Command Integration

Tools are designed to be used in custom slash commands:

```markdown
---
name: my-command
description: Example command using tools
---

# My Command

## Implementation
\`\`\`python
from tools import ConfigManager, NLPProcessor, OutputFormatter

def execute_command(args):
    # Parse natural language input
    nlp = NLPProcessor()
    intent = nlp.parse_command_intent(args)

    # Load configuration
    config = ConfigManager()
    projects = config.get_all_projects(filters=intent.filters)

    # Format output
    formatter = OutputFormatter()
    return formatter.format(projects, template="project_list")
\`\`\`
```

## Performance Characteristics

| Operation | Target | Actual |
|-----------|--------|--------|
| ConfigManager.get_project (cached) | <10ms | ~1-2ms |
| NLPProcessor.parse_command_intent | <10ms | ~3-5ms |
| NoteProcessor.parse_note | <50ms | ~20-30ms |
| OutputFormatter.format | <20ms | ~10-15ms |

## Testing

All tools have comprehensive test suites:

```bash
# Run all tool tests
pytest tests/ -v

# Run specific tool tests
pytest tests/test_nlp_processor.py -v

# With coverage
pytest tests/ --cov=tools --cov-report=html
```

## Contributing

See [Development Guide](development.md) for:
- Development setup
- Testing workflow
- Code style guidelines
- Contribution process

## Migration Guide

Migrating commands from long prompts to tools? See [Migration Guide](migration_guide.md) for:
- Step-by-step migration process
- Before/after examples
- Common patterns
- Troubleshooting

## Architecture

For deep dives into design decisions and system architecture, see [Architecture Documentation](architecture.md).

## Getting Help

- **Documentation**: Start with individual tool docs
- **Examples**: Check command implementations in `.claude/commands/`
- **Issues**: Search GitHub issues for similar problems
- **Tests**: Tool tests show real-world usage patterns

## Related Documentation

- [PARA Method](../PARA.md) - Note organization system
- [Custom Commands](../commands/README.md) - Command development guide
- [Project Structure](../PROJECT_STRUCTURE.md) - Repository organization

---

**Next Steps**: Choose a tool from the table above to learn more, or start with the [Migration Guide](migration_guide.md) if you're updating an existing command.

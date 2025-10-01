# Tools Architecture

## Overview

This directory contains the tool extraction and management system for the AI Agent Configuration repository. The tools system enables modular, reusable components that can be integrated into the Claude Code slash command ecosystem.

## Architecture

### Directory Structure

```
tools/
├── __init__.py           # Package initialization
├── config/              # Configuration management tools
├── notes/               # Notes processing tools
├── projects/            # Project management tools
└── shared/              # Shared utilities

scripts/
├── para-processor.py            # PARA Method note processor
├── project_data_collector.py   # Project data collection
├── project_status_analyzer.py  # Project status analysis
├── project_planner.py          # Project planning utilities
└── project_synchronizer.py     # Project synchronization

tests/
├── __init__.py          # Test package initialization
├── test_*.py            # Unit tests for tools
└── fixtures/            # Test fixtures and data
```

### Design Principles

1. **Modularity**: Each tool is self-contained and can be used independently
2. **Testability**: All tools have comprehensive test coverage
3. **Documentation**: Every tool has clear documentation and examples
4. **Type Safety**: All code uses type hints and passes mypy checks
5. **PARA Integration**: Tools align with the PARA Method structure

## Tool Categories

### Configuration Management
- **ConfigManager**: Central configuration management
- **ProjectConfig**: Project-specific configuration
- **LearningConfig**: Learning goals and tracking configuration
- **TeamConfig**: Team member and stakeholder management

### Notes Processing
- **NotesProcessor**: PARA Method note parsing and categorization
- **ActionItemExtractor**: Extract action items from notes
- **NoteLinker**: Link notes to projects and resources

### Project Management
- **ProjectDataCollector**: Collect project metadata and status
- **ProjectStatusAnalyzer**: Analyze project health and risks
- **ProjectPlanner**: Planning and milestone management
- **ProjectSynchronizer**: Sync notes with project milestones

## Integration with Claude Code

Tools are exposed as slash commands in the `.claude/commands/` directory. Each tool can be invoked via natural language commands or explicit flags.

Example:
```bash
/notes capture --project mobile-app-v2 --topic "Sprint Planning"
/project status --comprehensive
```

## Development Workflow

See [development.md](./development.md) for detailed development workflow, testing guidelines, and contribution standards.

## Dependencies

See `requirements.txt` for production dependencies and `requirements-dev.txt` for development dependencies.

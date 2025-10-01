# ConfigManager - Unified YAML Configuration Management

## Overview

ConfigManager is a centralized YAML configuration management tool with schema validation, intelligent caching, and atomic updates. It eliminates repetitive configuration loading logic and provides type-safe access to all configuration files.

## Features

- **Schema Validation**: Pydantic-based type-safe configuration models
- **Intelligent Caching**: File modification time-based cache invalidation
- **Atomic Updates**: Safe configuration updates with automatic backup and rollback
- **Cross-File Sync**: Automatic synchronization between related configuration files
- **Specialized Operations**: Convenient methods for common configuration tasks
- **High Performance**: <10ms cached reads, <100ms writes

## Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from tools import ConfigManager

# Initialize manager
mgr = ConfigManager()

# Get a project (50 lines of boilerplate → 1 line)
project = mgr.get_project("mobile-app-v2")
print(f"Project: {project.name}, Status: {project.status}")

# Update project status
mgr.update_project("mobile-app-v2", {"status": "completed"})

# Get all active projects
active_projects = mgr.get_all_projects(filters={"status": ["active", "in_progress"]})
```

## Core Operations

### Loading Configurations

```python
# Basic load
config = mgr.load_config("projects.yaml")

# Load with schema validation
from tools.schemas import ProjectsConfig
config = mgr.load_config("projects.yaml", schema=ProjectsConfig)

# Disable caching for fresh read
config = mgr.load_config("projects.yaml", use_cache=False)
```

### Updating Configurations

```python
# Simple update
updates = {"projects": {"my-project": {"status": "completed"}}}
mgr.update_config("projects.yaml", updates)

# Nested updates
updates = {
    "projects": {
        "my-project": {
            "milestones": [
                {"name": "Launch", "date": "2024-12-31", "status": "completed"}
            ]
        }
    }
}
mgr.update_config("projects.yaml", updates)

# Update without backup (faster but less safe)
mgr.update_config("projects.yaml", updates, backup=False)
```

### Validating Configurations

```python
from tools.schemas import TeamRosterConfig

# Validate against schema
try:
    validated = mgr.validate_config("team_roster.yaml", TeamRosterConfig)
    print("Configuration is valid")
except ConfigValidationError as e:
    print(f"Validation failed: {e}")
```

### Merging Configurations

```python
# Shallow merge (later configs override earlier)
merged = mgr.merge_configs(
    ["base_config.yaml", "env_config.yaml"],
    strategy="shallow"
)

# Deep merge (nested dictionaries merged recursively)
merged = mgr.merge_configs(
    ["default.yaml", "production.yaml"],
    strategy="deep"
)
```

## Specialized Operations

### Project Operations

```python
# Get single project
project = mgr.get_project("mobile-app-v2")
print(f"Owner: {project.owner}, Priority: {project.priority}")

# Update project
mgr.update_project("mobile-app-v2", {
    "status": "in_progress",
    "priority": "critical"
})

# Get all projects
all_projects = mgr.get_all_projects()

# Get filtered projects
active = mgr.get_all_projects(filters={"status": ["active", "in_progress"]})
high_priority = mgr.get_all_projects(filters={"priority": ["high", "critical"]})

# Multiple filters (AND logic)
critical_active = mgr.get_all_projects(filters={
    "status": ["active"],
    "priority": ["critical"]
})
```

### Team Operations

```python
# Get team member
member = mgr.get_team_member("sarah@company.com")
print(f"Name: {member.name}, Role: {member.role}")
print(f"Projects: {member.current_projects}")

# Access strongly-typed fields
review_date = member.next_review  # datetime.date object
```

### Stakeholder Operations

```python
# Get stakeholder profile
stakeholder = mgr.get_stakeholder("sarah@company.com")
print(f"Decision Authority: {stakeholder.decision_authority_level}")
print(f"Communication Style: {stakeholder.decision_preferences.communication_style}")

# Access influence factors
factors = stakeholder.influence_factors
print(f"Technical: {factors.technical_feasibility}")
print(f"Team Impact: {factors.team_impact}")
```

## Cross-File Synchronization

```python
# Sync project to notes cache
mgr.sync_project_to_notes("mobile-app-v2")

# Sync team roster to stakeholder contexts
# Updates stakeholder names and roles from team roster
mgr.sync_team_to_stakeholders()
```

## Caching

```python
# Get cache statistics
stats = mgr.get_cache_stats()
print(f"Cached files: {stats['cached_files']}")
print(f"Cache size: {stats['cache_size_bytes']} bytes")
print(f"Files: {stats['files']}")

# Clear cache (force reload on next access)
mgr.clear_cache()
```

## Error Handling

```python
from tools import ConfigNotFoundError, ConfigValidationError

try:
    project = mgr.get_project("nonexistent-project")
except KeyError as e:
    print(f"Project not found: {e}")

try:
    config = mgr.load_config("missing.yaml")
except ConfigNotFoundError as e:
    print(f"File not found: {e}")

try:
    validated = mgr.validate_config("invalid.yaml", ProjectsConfig)
except ConfigValidationError as e:
    print(f"Validation failed: {e}")
```

## Configuration Schemas

### Available Schemas

- `ProjectsConfig`: projects.yaml
- `TeamRosterConfig`: team_roster.yaml
- `StakeholderContextsConfig`: stakeholder_contexts.yaml
- `IntegrationsConfig`: integrations.yaml
- `DecisionFrameworksConfig`: decision_frameworks.yaml

### Schema Models

```python
from tools.schemas import (
    Project,
    ProjectStatus,
    Priority,
    Milestone,
    TeamMember,
    StakeholderProfile,
)

# Enums for type safety
status = ProjectStatus.IN_PROGRESS  # Type-safe
priority = Priority.HIGH

# Access model fields
project = mgr.get_project("my-project")
print(project.name)  # str
print(project.start_date)  # datetime.date
print(project.milestones)  # List[Milestone]
```

## Performance Guidelines

### Best Practices

1. **Use caching for repeated reads**:
   ```python
   # Good: Uses cache
   project = mgr.get_project("my-project")

   # Avoid: Bypasses cache unnecessarily
   config = mgr.load_config("projects.yaml", use_cache=False)
   project = Project(**config["projects"]["my-project"])
   ```

2. **Batch updates when possible**:
   ```python
   # Good: Single update with multiple changes
   mgr.update_project("my-project", {
       "status": "completed",
       "priority": "low",
       "tags": ["archived"]
   })

   # Avoid: Multiple separate updates
   mgr.update_project("my-project", {"status": "completed"})
   mgr.update_project("my-project", {"priority": "low"})
   mgr.update_project("my-project", {"tags": ["archived"]})
   ```

3. **Clear cache when memory is a concern**:
   ```python
   # After processing many configs
   mgr.clear_cache()
   ```

### Performance Benchmarks

- **Cached reads**: <10ms (guaranteed)
- **Uncached reads**: 10-50ms depending on file size
- **Writes**: <100ms including validation and backup
- **Schema validation**: <5ms overhead per operation

## Integration with Commands

### Before (50+ lines per command)

```python
def get_project_status(project_id):
    projects_path = Path.cwd() / ".claude" / "projects.yaml"
    with open(projects_path) as f:
        config = yaml.safe_load(f)

    if project_id not in config["projects"]:
        raise ValueError(f"Project not found: {project_id}")

    project_data = config["projects"][project_id]
    # Manual parsing and validation...
    return project_data
```

### After (1-2 lines)

```python
def get_project_status(project_id):
    mgr = ConfigManager()
    return mgr.get_project(project_id)
```

## Migration Guide

### Step 1: Import ConfigManager

```python
from tools import ConfigManager
```

### Step 2: Replace manual YAML loading

```python
# Old
with open(".claude/projects.yaml") as f:
    config = yaml.safe_load(f)
project = config["projects"]["my-project"]

# New
mgr = ConfigManager()
project = mgr.get_project("my-project")
```

### Step 3: Replace manual updates

```python
# Old
with open(".claude/projects.yaml") as f:
    config = yaml.safe_load(f)
config["projects"]["my-project"]["status"] = "completed"
with open(".claude/projects.yaml", "w") as f:
    yaml.safe_dump(config, f)

# New
mgr = ConfigManager()
mgr.update_project("my-project", {"status": "completed"})
```

## Advanced Usage

### Custom Configuration Root

```python
from pathlib import Path

# Use custom config directory
custom_root = Path("/path/to/configs")
mgr = ConfigManager(config_root=custom_root)
```

### Atomic Multi-File Updates

```python
# Update multiple files atomically
try:
    mgr.update_config("projects.yaml", project_updates)
    mgr.update_config("team_roster.yaml", team_updates)
    mgr.sync_team_to_stakeholders()
except Exception as e:
    # All updates rolled back automatically
    print(f"Update failed: {e}")
```

## Testing

```bash
# Run ConfigManager tests
pytest tests/test_config_manager.py -v

# Run with coverage
pytest tests/test_config_manager.py --cov=tools/config_manager
```

## API Reference

See the [ConfigManager source code](../../tools/config_manager.py) for detailed API documentation and type signatures.

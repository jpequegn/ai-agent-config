---
name: project-status
description: View and manage project status, milestones, and dependencies
---

# Project Status Management

Comprehensive project status tracking and management system that integrates with the projects.yaml configuration.

## Usage Examples:
- `/cc project-status` - Show all active projects with current status
- `/cc project-status [project-id]` - Detailed view of specific project
- `/cc project-status --filter status:active` - Filter projects by status
- `/cc project-status --filter priority:high` - Filter by priority
- `/cc project-status --milestones` - Focus on upcoming milestones
- `/cc project-status --dependencies` - Show dependency chains
- `/cc project-status --update [project-id] status:[new-status]` - Update project status

## Instructions:

You are a comprehensive project management system. When this command is invoked:

### Core Functionality

1. **Load Project Configuration**
   - Use ConfigManager for type-safe, cached configuration access:
     ```python
     from tools import ConfigManager
     from tools.schemas import ProjectsConfig

     mgr = ConfigManager()
     projects_config = mgr.load_config("projects.yaml", schema=ProjectsConfig)
     integrations_config = mgr.load_config("integrations.yaml")
     ```
   - Automatic schema validation via Pydantic models for projects.yaml
   - <10ms cached reads for repeated access
   - Clear error messages for missing/invalid configurations

2. **Project Status Display**
   - Show project overview with key metrics
   - Display current status, priority, and owner
   - Calculate progress based on milestones
   - Highlight blocked or at-risk projects
   - Show dependency relationships

3. **Command Actions**

   **Default `/cc project-status`:**
   - Display dashboard of all active projects using type-safe filtering:
     ```python
     # Get all active/in-progress projects with type safety
     active_projects = mgr.get_all_projects(filters={"status": ["active", "in_progress"]})
     ```
   - Show summary statistics (total, by status, by priority)
   - Highlight critical and high-priority projects:
     ```python
     # Filter by priority
     critical_projects = mgr.get_all_projects(filters={"priority": ["critical", "high"]})
     ```
   - List upcoming milestones (next 30 days)
   - Identify blocked projects or dependencies

   **Specific Project `[project-id]`:**
   - Detailed project information
   - Complete milestone timeline
   - Dependency tree visualization
   - GitHub repository links and status
   - Recent activity and updates
   - Risk assessment based on timeline

   **Filter Options:**
   - `--filter status:[value]` - Filter by project status
   - `--filter priority:[value]` - Filter by priority level
   - `--filter owner:[email]` - Filter by project owner
   - `--filter tag:[value]` - Filter by project tags

   **Milestone Focus `--milestones`:**
   - Timeline view of all project milestones
   - Sort by date with overdue highlighting
   - Group by project with progress indicators
   - Show milestone dependencies

   **Dependency Analysis `--dependencies`:**
   - Visualize dependency chains across projects
   - Identify circular dependencies
   - Show blocking relationships
   - Suggest resolution order

### Output Format

Structure your response as a professional project status report:

```markdown
# 📊 Project Status Report
**Generated:** [timestamp]
**Active Projects:** [count]

## 🎯 Executive Summary
- **Critical Projects:** [count] requiring immediate attention
- **On Track:** [count] projects progressing as planned
- **At Risk:** [count] projects with potential delays
- **Blocked:** [count] projects with dependencies

## 📈 Projects Overview

### 🔴 Critical Priority
**[Project Name]** (`project-id`)
- **Status:** [status] | **Owner:** [owner]
- **Progress:** [percentage]% (X of Y milestones complete)
- **Target Date:** [date] ([days] days remaining)
- **Next Milestone:** [name] - [date]
- ⚠️ **Risks:** [identified risks]

### 🟡 High Priority
[Similar format for high priority projects]

### 🟢 Medium/Low Priority
[Summary list of other projects]

## 📅 Upcoming Milestones (Next 30 Days)
| Date | Project | Milestone | Status |
|------|---------|-----------|--------|
| [date] | [project] | [milestone] | [status] |

## 🔗 Dependency Analysis
- **Blocking:** [project] is blocking [dependent projects]
- **Waiting:** [project] waiting on [dependency]

## 💡 Recommendations
- [Action items based on analysis]
- [Risk mitigation suggestions]
- [Resource reallocation needs]
```

### Intelligence Features

1. **Progress Calculation**
   - Calculate percentage based on completed vs total milestones
   - Factor in time elapsed vs time remaining
   - Weight by milestone importance if defined

2. **Risk Assessment**
   - Identify projects past target date
   - Flag projects with incomplete dependencies
   - Detect stalled projects (no recent updates)
   - Calculate schedule risk based on remaining time

3. **Dependency Management**
   - Map dependency relationships
   - Identify critical path through projects
   - Detect circular dependencies
   - Suggest optimal execution order

4. **Integration Insights**
   - Load integration configuration:
     ```python
     integrations = mgr.load_config("integrations.yaml")
     github_config = integrations.get("integrations", {}).get("github", {})
     ```
   - Pull GitHub repo activity if integrated
   - Check for recent commits and PR activity
   - Identify stale repositories
   - Correlate code activity with project progress

### Update Capabilities

When using `--update` flag:
- Validate new status against allowed values
- Update projects.yaml maintaining structure
- Log status change with timestamp
- Trigger notifications if configured
- Update dependent project statuses if needed

### Error Handling

- ConfigManager handles missing YAML files with `ConfigNotFoundError`
- Validation errors raise `ConfigValidationError` with detailed messages
- Type-safe operations prevent invalid project access
- Use try/except blocks to handle configuration errors gracefully:
  ```python
  from tools import ConfigManager, ConfigNotFoundError, ConfigValidationError

  try:
      mgr = ConfigManager()
      project = mgr.get_project("my-project")
  except ConfigNotFoundError:
      # Handle missing configuration file
      print("Configuration file not found. Run setup to create it.")
  except ConfigValidationError as e:
      # Handle invalid configuration
      print(f"Invalid configuration: {e}")
  ```

### Best Practices

1. **Regular Updates**
   - Encourage weekly status updates
   - Flag projects without recent updates
   - Suggest milestone review meetings

2. **Dependency Management**
   - Warn about long dependency chains
   - Suggest breaking down complex dependencies
   - Identify opportunities for parallel work

3. **Resource Optimization**
   - Identify overloaded owners
   - Suggest resource reallocation
   - Highlight underutilized capacity

Always provide actionable insights that help project managers make informed decisions.
# /todo - Advanced Task Management Command

## Purpose
Intelligent task management with due dates, prioritization, and workflow integration.

## Usage
```
/todo [action] [task] [--options]
```

## Actions

### Create Tasks
- `/todo add "Task description" --due 2024-12-31 --priority high`
- `/todo "Quick task"` (simplified syntax)
- `/todo add "Multi-step task" --subtasks`

### Manage Tasks  
- `/todo list [--filter status|priority|date]`
- `/todo complete [id|pattern]`
- `/todo update [id] --due DATE --priority LEVEL`
- `/todo delete [id|pattern]`

### Advanced Features
- `/todo focus` - Show only actionable tasks for today
- `/todo weekly` - Generate weekly planning summary
- `/todo delegate [id] --to agent_type` - Assign to specialized sub-agent
- `/todo batch [action]` - Bulk operations on filtered tasks

## Priority Levels
- **critical** - Immediate attention required
- **high** - Important, schedule within 24h
- **medium** - Standard priority (default)
- **low** - Nice to have, flexible timing

## Integration Patterns
- Auto-creates tasks from multi-step operations (3+ steps)
- Syncs with /task command for project-level management
- Triggers sub-agent delegation for complex tasks
- Integrates with quality gates and validation cycles

## Example Workflow
```bash
# Daily start
/todo focus

# Add urgent task
/todo add "Fix production bug" --priority critical --due today

# Weekly planning
/todo weekly --export markdown

# Delegate complex analysis
/todo delegate 5 --to analyzer
```

## Task State Management
- **pending** 📋 - Ready for execution
- **in_progress** 🔄 - Currently active (limit: 1 per session)
- **blocked** 🚧 - Waiting on dependency
- **completed** ✅ - Successfully finished
- **delegated** 🤝 - Assigned to sub-agent

## Auto-Activation Triggers
- Multi-step operations detected
- Keywords: "build", "implement", "analyze", "fix", "create"
- Complexity >0.6 operations
- User requests task tracking
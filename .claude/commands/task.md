# /task - Multi-Session Project Management Command

## Purpose  
Long-term project orchestration spanning multiple Claude Code sessions with persistent state management.

## Usage
```
/task [action] [project] [--options]
```

## Project Lifecycle Management

### Initialize Projects
- `/task init "Project Name" --type feature|bug|epic`
- `/task create "New Feature" --owner username --deadline 2024-12-31`
- `/task template webapp|api|analysis` - Use predefined templates

### Project Operations
- `/task list [--status active|completed|blocked]`
- `/task status "Project Name"` - Detailed progress report
- `/task update "Project Name" --progress 75 --notes "Current status"`
- `/task archive "Project Name"` - Move to completed projects

### Task Hierarchy (Epic → Story → Task)
- `/task breakdown "Epic Name" --stories 5` - Create story breakdown
- `/task assign story1 --to "Team Member"` 
- `/task dependency story1 --requires story2` - Set dependencies
- `/task milestone "Sprint 1" --date 2024-12-15`

### Cross-Session Continuity
- `/task resume "Project Name"` - Restore context from previous sessions
- `/task handoff "Project Name" --to colleague --notes "Status summary"`
- `/task sync` - Update project status across all active projects

## Project Templates

### Web Application
```yaml
phases:
  - planning: Requirements, architecture, design
  - development: Frontend, backend, integration  
  - testing: Unit, integration, E2E
  - deployment: CI/CD, monitoring, documentation
```

### API Development  
```yaml
phases:
  - design: OpenAPI spec, data models, endpoints
  - implementation: Routes, middleware, validation
  - testing: Unit tests, integration tests, load testing
  - deployment: Containerization, scaling, monitoring
```

### Data Analysis
```yaml
phases:
  - collection: Data sources, ETL pipelines
  - processing: Cleaning, transformation, validation
  - analysis: Statistical analysis, ML models
  - reporting: Visualizations, insights, recommendations
```

## State Persistence
- **Project Files**: `.claude/projects/{project-name}.json`
- **Session History**: Track progress across multiple interactions
- **Context Storage**: Remember decisions, blockers, and next steps
- **Team Handoffs**: Export/import project state for collaboration

## Integration Patterns
- **Sub-Agent Coordination**: Delegate specialized work to domain experts
- **Quality Gates**: Built-in validation checkpoints for each phase
- **Wave Orchestration**: Multi-stage execution for complex projects  
- **MCP Server Integration**: Leverage specialized servers for project needs

## Example Multi-Session Workflow

### Session 1: Project Initialization
```bash
/task init "User Authentication System" --type feature
/task breakdown "User Auth" --stories ["Login", "Registration", "Password Reset"]
/task assign "Login" --priority high --due 2024-12-20
```

### Session 2: Development Progress  
```bash
/task resume "User Authentication System"
/task update "Login" --progress 60 --notes "JWT implementation complete, testing needed"
/task delegate "Password Reset" --to security --validate
```

### Session 3: Project Completion
```bash
/task status "User Authentication System"
/task complete "Login" --evidence "All tests passing, deployed to staging"
/task milestone "MVP Complete" --achieved
```

## Reporting & Analytics
- `/task report weekly` - Progress summary across all active projects
- `/task metrics --project "Name"` - Velocity, completion rates, blockers
- `/task export --format json|markdown` - Share project status
- `/task timeline "Project Name"` - Visual project timeline

## Auto-Activation Triggers
- Feature implementation requests spanning multiple sessions
- Architecture or system design discussions  
- Long-term optimization or refactoring projects
- Cross-team collaboration requirements
- Keywords: "project", "feature", "epic", "milestone", "roadmap"
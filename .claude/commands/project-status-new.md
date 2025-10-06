---
name: project-status
description: Intelligent project status analysis with multi-source data synthesis
---

# /project status - Intelligent Project Status Command

Comprehensive project status analysis using the ProjectStatusGenerator tool for streamlined, consistent reporting.

## Usage Examples:
- `/project status` - Overview of all active projects
- `/project status <project-name>` - Detailed analysis of specific project
- `/project status --json` - JSON output for programmatic use
- `/project status --focus risks` - Focus on project risks and blockers
- `/project status --focus health` - Focus on project health metrics
- `/project status --focus trends` - Focus on trend analysis

## Instructions:

When this command is invoked, use the ProjectStatusGenerator tool for comprehensive project status analysis.

### Single Project Analysis

For `/project status <project-name>`:

```python
from tools import ProjectStatusGenerator

# Initialize generator
generator = ProjectStatusGenerator()

# Generate comprehensive status
status = generator.generate_status(
    project_id="<project-name>",
    focus=None,  # or "risks", "health", "trends"
    output_format="markdown",  # or "json"
)

# Display results
print(status.formatted_output)
print(f"\n<!-- Generated in {status.processing_time_ms:.2f}ms -->")
```

### All Projects Overview

For `/project status`:

```python
from tools import ProjectStatusGenerator

# Initialize generator
generator = ProjectStatusGenerator()

# Generate overview for all active projects
overview = generator.generate_overview(
    filters={"status": ["active", "in_progress"]},
    output_format="markdown",
)

# Display results for each project
for project_id, status in overview.items():
    print(f"\n## {project_id}")
    print(f"Health: {status.health_score.category.value} ({status.health_score.score:.1%})")
    print(f"Risks: {len(status.risks)}")
    print(f"Trend: {status.trends.direction.value if status.trends else 'N/A'}")

print(f"\n<!-- Analyzed {len(overview)} projects -->")
```

### JSON Output

For `--json` flag:

```python
from tools import ProjectStatusGenerator

generator = ProjectStatusGenerator()

# Generate with JSON output
status = generator.generate_status(
    project_id="<project-name>",
    output_format="json",
)

print(status.formatted_output)
```

## What the Tool Does

The **ProjectStatusGenerator** coordinates four underlying tools:

1. **DataCollector**: Aggregates data from multiple sources
   - GitHub (PRs, issues, commits, milestones)
   - Notes system (project notes and action items)
   - Calendar (meetings and deadlines)
   - Team data (members and availability)
   - 5-minute caching for performance

2. **HealthCalculator**: Comprehensive health analysis
   - Weighted scoring (Timeline 30%, Activity 25%, Blockers 25%, Dependencies 20%)
   - Trend analysis with statistical confidence
   - Risk assessment with mitigation strategies

3. **NoteProcessor**: Enhanced note operations
   - Type-safe note retrieval
   - Action item status tracking
   - Completion rate calculation

4. **OutputFormatter**: Template-based output generation
   - Professional markdown formatting
   - JSON output support
   - <50ms rendering with caching

## Key Features

**Automatic Data Collection:**
- Multi-source aggregation without manual setup
- Graceful degradation when sources unavailable
- Automatic retry with exponential backoff

**Intelligent Health Scoring:**
- Deterministic, tested algorithms
- Component breakdown (timeline, activity, blockers, dependencies)
- Health categories: Excellent (80-100%), Good (60-80%), At Risk (40-60%), Critical (0-40%)

**Trend Analysis:**
- Direction: improving, stable, declining
- Statistical confidence scores
- 30-day time window (configurable)

**Risk Assessment:**
- Automatically detected risks (schedule, resource, technical, dependency)
- Severity levels (critical, high, medium, low)
- Prioritized by impact score
- Mitigation suggestions included

## Output Format

### Markdown (Default)
Uses the `project_status.md.j2` template:
- Health score with emoji indicators (🟢 🟡 🟠 🔴)
- Milestone tables with progress tracking
- Blocker and risk sections
- Activity metrics and trends
- Automatic date formatting

### JSON
Structured data suitable for:
- Programmatic processing
- API integrations
- Dashboards and visualizations

## Error Handling

The tool handles errors automatically:
- Project not found → Clear error message with available projects
- Data source failures → Graceful degradation with partial data
- Network issues → Automatic retry (3 attempts)
- Missing integrations → Helpful setup guidance

## Performance

- **Initial Load**: ~100-200ms (first request)
- **Cached**: ~15-25ms (subsequent requests with 5-min cache)
- **Multi-Project**: ~50-100ms per project (parallel processing)

## Best Practices

1. **Use Focus Modes**: Specify `--focus` when you need specific insights
2. **JSON for Integration**: Use `--json` when feeding data to other tools
3. **Cache Awareness**: Understand 5-minute cache for recent data
4. **Error Messages**: Read error messages for setup guidance

## Example Output

```markdown
## 📊 Project Health: mobile-app

🟢 **75.0%** - Good

### Component Breakdown
- 🟢 80.0% Timeline
- 🟡 75.0% Activity
- 🟠 65.0% Blockers
- 🟢 70.0% Dependencies

## 📈 Trends
**Direction**: Improving ↗️
**Confidence**: 85%

## ⚠️ Risks (1)
### Timeline Delay Risk (medium)
Timeline may slip if budget approval delayed

**Mitigation**:
- Fast-track budget approval process

## 📝 Notes & Actions
- **Total Notes**: 15
- **Pending Actions**: 4
- **Overdue Actions**: 2
- **Completion Rate**: 60%

<!-- Generated in 23.45ms -->
```

## Implementation Notes

**Massive Simplification**:
- Command reduced from 421 lines → ~140 lines (67% reduction)
- Complex logic moved to reusable, tested tool
- Consistent behavior across all invocations

**Benefits**:
- **Testable**: Tool has comprehensive test suite
- **Reusable**: Other commands can use ProjectStatusGenerator
- **Maintainable**: Business logic separate from command interface
- **Consistent**: Shared output formatting
- **Faster**: Optimized caching and data collection

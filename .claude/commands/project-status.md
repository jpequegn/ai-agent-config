---
name: project-status
description: Intelligent project status analysis with multi-source data synthesis
---

# /project status - Intelligent Project Status Command

Comprehensive project status analysis that synthesizes data from multiple sources to provide actionable insights, health scoring, trend analysis, and risk identification.

## Usage Examples:
- `/project status` - Overview of all active projects with intelligent analysis
- `/project status <project-name>` - Detailed analysis of specific project
- `/project status --json` - JSON output for programmatic use
- `/project status --focus risks` - Focus on project risks and blockers
- `/project status --focus health` - Focus on project health metrics
- `/project status --focus trends` - Focus on trend analysis

## Instructions:

You are an intelligent project management analyst. When this command is invoked, you will:

### Core Functionality

1. **Multi-Source Data Collection**
   - Use the DataCollector tool from the tools package to gather data from:
     - GitHub API (PRs, issues, commits, milestones)
     - Notes system (project-related notes and action items)
     - Calendar integration (meetings, deadlines)
     - Team data (members, roles, availability)
   - Synthesize data from `.claude/projects.yaml` configuration
   - Integrate with `.claude/integrations.yaml` for API access
   - Automatic 5-minute caching for performance
   - Graceful degradation when data sources unavailable

2. **Intelligent Health Scoring with HealthCalculator**
   - Use HealthCalculator tool for deterministic, tested health scoring:
   ```python
   from tools import HealthCalculator

   calc = HealthCalculator()
   health = calc.calculate_project_health(project_data)
   # Returns: HealthScore(
   #   score=0.72,
   #   category="good",
   #   breakdown={
   #     "timeline": 0.75,
   #     "activity": 0.80,
   #     "blockers": 0.65,
   #     "dependencies": 0.70
   #   }
   # )
   ```
   - Health scoring uses weighted components (Timeline 30%, Activity 25%, Blockers 25%, Dependencies 20%)
   - Health Categories automatically determined:
     - 0.8-1.0: 🟢 Excellent (on track, active, minimal blockers)
     - 0.6-0.8: 🟡 Good (minor issues, manageable risks)
     - 0.4-0.6: 🟠 At Risk (significant concerns, needs attention)
     - 0.0-0.4: 🔴 Critical (major blockers, high risk of failure)

3. **Trend Analysis with HealthCalculator**
   - Use HealthCalculator for analyzing trends over time:
   ```python
   trends = calc.analyze_trends(
       historical_data=project_history,
       time_window=30  # days
   )
   # Returns: TrendAnalysis(
   #   direction="improving",  # "improving", "stable", "declining"
   #   slope=0.05,  # Rate of change
   #   confidence=0.85  # Statistical confidence
   # )
   ```
   - Trend directions automatically calculated:
     - **Improving**: Health score increasing, blockers resolved, milestones met
     - **Stable**: Consistent progress, predictable patterns (±5% variance)
     - **Declining**: Health score decreasing, new blockers, missed milestones

4. **Risk Assessment with HealthCalculator**
   - Use HealthCalculator for comprehensive risk analysis:
   ```python
   risks = calc.assess_risks(project_data)
   # Returns: List[Risk] sorted by priority
   # Each Risk includes:
   #   - type: "schedule", "resource", "technical", "dependency"
   #   - severity: "critical", "high", "medium", "low"
   #   - description: Human-readable risk description
   #   - mitigation: Suggested mitigation strategies
   #   - impact_score: Quantified impact (0.0-1.0)
   ```
   - Automated risk detection includes:
     - **Schedule Risk**: Target date vs. remaining milestones, overdue tasks
     - **Resource Risk**: Owner workload, team capacity constraints
     - **Technical Risk**: Open bugs/issues, code quality metrics
     - **Dependency Risk**: Blocking other projects, incomplete dependencies
   - Risks sorted by impact_score × severity for prioritization

### Command Actions

**Default `/project status`:**
Execute the following steps:

1. Use DataCollector tool to gather data for all projects
2. Calculate health scores and trends for each project
3. Identify risks and blockers across all projects
4. Generate executive summary with key insights
5. Present findings in structured format

**Specific Project Analysis `/project status <project-name>`:**
1. Collect detailed data for the specified project
2. Perform deep analysis of project health
3. Provide detailed trend analysis
4. List specific actionable recommendations
5. Include related project impacts

**Focus Modes:**
- `--focus risks`: Emphasize risk identification and mitigation strategies
- `--focus health`: Detailed health scoring breakdown and improvement suggestions
- `--focus trends`: Historical analysis and predictive insights

### Output Format

The `/project status` command uses **OutputFormatter** for consistent, template-based output generation.

#### Markdown Output (Default)

Output is generated using the `project_status.md.j2` template located in `templates/output/`:

```python
output = formatter.format_markdown(
    data=project_data,
    template="project_status",
    context={"focus": focus_mode}
)
print(output.content)
```

**Template Features:**
- Health scores with emoji indicators (🟢 🟡 🟠 🔴)
- Milestone tables with progress tracking
- Blocker and risk sections with severity levels
- Activity metrics and trend indicators
- Automatic date formatting (relative and absolute)
- Focus-based content emphasis (risks, health, trends)

**Sample Output Structure:**
```markdown
## 📊 Overall Health
🟢 75.0% Project Health

### Component Breakdown
- 🟢 80.0% Timeline
- 🟡 75.0% Activity
- 🟠 65.0% Blockers
- 🟢 70.0% Dependencies

## 📅 Timeline
**Status**: ✅ On Track

### Milestones
| Name | Status | Due Date | Progress |
|:-----|:-------|:---------|:---------|
| Planning | ✅ Complete | Oct 15, 2024 | 100% |
| Development | 🔄 In Progress | Nov 30, 2024 | 60% |

## 🎯 Activity
- **Commits**: 45
- **Pull Requests**: 12
- **Issues Closed**: 8
- **Activity Score**: 🟢 80.0%

## 🚧 Blockers
**Total Blockers**: 2

- 🚧 **Budget Approval** (high)
  - Waiting on executive approval for additional resources

## ⚠️ Risks
### ⚠️ Timeline Risk
**Severity**: medium | **Likelihood**: high
Project timeline may slip if budget approval delayed beyond next week.
...
```

#### JSON Output (--json flag)

```python
output = formatter.format_json(project_data, pretty=True)
print(output.content)
```

**JSON Structure:**
```json
{
  "health": {
    "overall_score": 0.75,
    "category": "good",
    "components": {
      "timeline": {"score": 0.80},
      "activity": {"score": 0.75},
      "blockers": {"score": 0.65},
      "dependencies": {"score": 0.70}
    }
  },
  "timeline": {
    "status": "on_track",
    "milestones": [...],
    "progress_ratio": 0.60
  },
  "activity": {
    "commits": 45,
    "pull_requests": 12,
    "issues_closed": 8,
    "score": 0.80
  },
  "blockers": [...],
  "dependencies": [...],
  "risks": [...]
}
```

### Implementation Steps

When executing this command:

1. **Initialize Tools (DataCollector, NoteProcessor, HealthCalculator, OutputFormatter)**
   ```python
   from tools import DataCollector, NoteProcessor, HealthCalculator, ConfigManager, OutputFormatter

   config = ConfigManager()
   collector = DataCollector()  # Multi-source data aggregation
   processor = NoteProcessor()  # Enhanced note operations
   calc = HealthCalculator()    # Health scoring and risk assessment
   formatter = OutputFormatter()  # Template-based output generation
   ```

2. **Collect Project Data with Enhanced Note Operations**
   ```python
   if project_name:
       # Collect data for specific project from all sources
       project_data = collector.aggregate_project_data(
           project_id=project_name,
           sources=["github", "notes", "calendar", "team", "config"]
       )

       # Enhanced note operations with NoteProcessor
       # Get detailed project notes (type-safe ParsedNote objects)
       project_notes = processor.get_project_notes(project_name)

       # Get action items by status (simplified from DataCollector)
       pending_actions = processor.get_action_items_by_status("pending", project=project_name)
       overdue_actions = processor.get_action_items_by_status("overdue", project=project_name)
       completed_actions = processor.get_action_items_by_status("completed", project=project_name)

       # Access collected data from DataCollector
       github_data = project_data.github_data
       notes_data = project_data.notes_data  # Basic note count and summaries
       calendar_data = project_data.calendar_data
       team_data = project_data.team_data
       config_data = project_data.config_data

       # Combine for comprehensive analysis
       detailed_notes_analysis = {
           'total_notes': len(project_notes),
           'pending_actions': len(pending_actions),
           'overdue_actions': len(overdue_actions),
           'completed_actions': len(completed_actions),
           'action_completion_rate': len(completed_actions) / (len(completed_actions) + len(pending_actions)) if (len(completed_actions) + len(pending_actions)) > 0 else 0
       }
   else:
       # Collect data for all active projects
       all_projects = config.get_all_projects(filters={"status": ["active", "in_progress"]})
       project_data = {}
       for project_id in all_projects:
           project_data[project_id] = collector.aggregate_project_data(
               project_id=project_id,
               sources=["github", "notes", "calendar", "team", "config"]
           )

           # Enhanced note analysis per project
           project_data[project_id].notes_detail = {
               'notes': processor.get_project_notes(project_id),
               'pending_actions': processor.get_action_items_by_status("pending", project=project_id),
               'overdue_actions': processor.get_action_items_by_status("overdue", project=project_id)
           }
   ```

3. **Calculate Health Scores with HealthCalculator**
   ```python
   # For each project, calculate health using HealthCalculator
   for project_id, data in project_data.items():
       # Calculate comprehensive health score
       health = calc.calculate_project_health(data)

       # Analyze trends over time
       trends = calc.analyze_trends(
           historical_data=data.history,
           time_window=30
       )

       # Assess risks and get mitigation strategies
       risks = calc.assess_risks(data)

       # Store results
       data.health_score = health.score
       data.health_category = health.category
       data.health_breakdown = health.breakdown
       data.trend_direction = trends.direction
       data.trend_confidence = trends.confidence
       data.risks = risks
   ```

4. **Generate Insights from Health Data**
   - Use health scores and trends to identify patterns
   - Prioritize projects by risk level (from assess_risks)
   - Suggest optimization based on health breakdown components
   - Highlight resource allocation issues from resource risks

5. **Format Output with OutputFormatter**
   ```python
   # Use OutputFormatter for consistent template-based output
   if json_flag:
       # JSON output for programmatic use
       output = formatter.format_json(project_data, pretty=True)
   else:
       # Markdown output using project_status template
       output = formatter.format_markdown(
           data=project_data,
           template="project_status",
           context={"focus": focus_mode}  # 'risks', 'health', 'trends', or None
       )

   print(output.content)

   # Performance tracking
   stats = formatter.get_performance_stats()
   print(f"<!-- Rendered in {output.processing_time_ms:.2f}ms -->")
   ```

   **Benefits of OutputFormatter:**
   - **Simplification**: 200+ lines of template specs → 5-10 lines
   - **Performance**: <50ms rendering with built-in caching
   - **Consistency**: Uses same template as other commands
   - **Maintainability**: Template changes don't require code changes

### Error Handling

DataCollector handles errors automatically with:
- Automatic retry with exponential backoff (3 attempts)
- Graceful degradation when data sources unavailable
- Detailed error messages with recovery suggestions
- Continuation with partial data when some sources fail

Additional handling:
- Validate project names against ConfigManager
- Provide helpful error messages for missing integrations
- Suggest setup steps when API credentials not configured

### Best Practices

- Always provide actionable recommendations
- Focus on business impact, not just technical metrics
- Highlight the most critical issues first
- Include confidence levels for predictions
- Suggest specific next steps with owners and timelines

## Implementation Notes

**OutputFormatter Integration Benefits:**
- **Massive Simplification**: 200+ lines of manual template specs → 5-10 lines of code
- **Performance**: <50ms rendering with built-in caching
- **Consistency**: Same template system used across all commands
- **Maintainability**: Template changes don't require code modifications
- **Flexibility**: Easy to add new output formats (HTML, PDF, etc.)
- **Type Safety**: Structured data models for reliable output

**HealthCalculator Integration Benefits:**
- **Simplified calculation**: 80+ lines of manual logic → 10 lines of HealthCalculator calls
- **Deterministic scoring**: Consistent, tested algorithms across all projects
- **Performance**: <50ms calculations (5x faster than manual implementation)
- **Comprehensive risk analysis**: Automatic detection with mitigation suggestions
- **Trend confidence**: Statistical confidence scores for trend analysis
- **Maintainability**: Centralized scoring logic, no duplication across commands

**Key HealthCalculator Methods:**
- `calc.calculate_project_health(data)` - Returns HealthScore with breakdown
- `calc.analyze_trends(history, time_window)` - Returns TrendAnalysis with confidence
- `calc.assess_risks(data)` - Returns prioritized list of Risk objects

**Complete Tool Integration (4 Tools Working Together):**
- **DataCollector**: Multi-source aggregation (GitHub, notes, calendar, team, config)
- **NoteProcessor**: Enhanced note operations with type-safe models
- **HealthCalculator**: Deterministic health scoring, trend analysis, risk assessment
- **OutputFormatter**: Template-based output generation with <50ms rendering
- **Synergy**:
  - DataCollector provides data for HealthCalculator to analyze
  - NoteProcessor provides detailed note insights
  - HealthCalculator provides consistent scoring across all projects
  - OutputFormatter transforms data into beautiful, consistent output
  - All four tools work together for comprehensive project analysis and presentation

**Key NoteProcessor Methods for Project Status:**
- `processor.get_project_notes(project_id)` - Get all project-linked notes (type-safe ParsedNote objects)
- `processor.get_action_items_by_status("pending", project=project_id)` - Pending action items
- `processor.get_action_items_by_status("overdue", project=project_id)` - Overdue action items
- `processor.get_action_items_by_status("completed", project=project_id)` - Completed action items

**Benefits of Integration:**
- **Type-safe operations**: ParsedNote models with validated data
- **Detailed analysis**: Access to full note content, action items, metadata
- **Action tracking**: Precise action item status by project
- **70% complexity reduction**: Simplified from manual note parsing
- **Automatic caching**: Both tools leverage caching for performance
- **Graceful degradation**: Both handle missing data sources gracefully

**Usage Pattern:**
1. Use DataCollector for multi-source aggregation and high-level metrics
2. Use NoteProcessor for detailed note analysis and action item tracking
3. Combine both for comprehensive project status insights
4. Calculate health scores using combined data from both tools

Remember: This command should be your go-to tool for project management decision-making. Always prioritize actionable insights over data dumps.
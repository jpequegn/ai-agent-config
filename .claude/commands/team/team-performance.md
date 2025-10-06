---
name: team-performance
description: Track and analyze team performance metrics, trends, and key performance indicators
---

# Team Performance Analytics

Comprehensive performance tracking system that analyzes team metrics, trends, and effectiveness using data from team_roster.yaml and project integration.

## Usage Examples:
- `/cc team-performance` - Show team performance dashboard with key metrics
- `/cc team-performance [email]` - Individual performance analysis and trends
- `/cc team-performance --metrics` - Detailed breakdown of all performance metrics
- `/cc team-performance --trends` - Performance trend analysis and forecasting
- `/cc team-performance --team-health` - Overall team health assessment
- `/cc team-performance --goals` - Goal achievement tracking across team
- `/cc team-performance --compare [period]` - Compare performance across time periods

## OutputFormatter Integration

**Tool**: Use `OutputFormatter` with `team_performance` template for professional performance analytics formatting.

**Template**: `templates/output/team_performance.md.j2` - Comprehensive team performance template with metrics, member analysis, bottlenecks, and recommendations.

### Integration Example

```python
from tools import OutputFormatter, DataCollector

# 1. Gather team performance data
collector = DataCollector()
team_data = collector.collect_team_data()
config_data = collector.collect_config_data()

# 2. Calculate performance metrics
def calculate_team_health_score(team_data):
    # Combine velocity, quality, collaboration metrics
    return 0.82  # Example: 82% team health

def analyze_velocity(team_data):
    return {
        'current': 42,
        'target': 45,
        'trend': 'improving',
        'change_percentage': 8.5
    }

# 3. Structure performance data
performance_data = {
    'period': 'Q4 2024',
    'team_size': len(team_data.members),
    'health_score': calculate_team_health_score(team_data),
    'summary': 'Team demonstrated strong performance with 8.5% velocity improvement...',

    'key_metrics': [
        {
            'name': 'Sprint Velocity',
            'value': '42 points',
            'status': 'on_track',  # on_track, at_risk, off_track
            'trend': '+8.5%'
        },
        {
            'name': 'Code Quality',
            'value': '0.88',
            'status': 'on_track',
            'trend': 'stable'
        }
    ],

    'metrics': {
        'velocity': {
            'current': 42,
            'target': 45,
            'trend': 'improving',  # improving, declining, stable
            'change_percentage': 8.5
        },
        'quality': {
            'score': 0.88,
            'test_coverage': 0.85,
            'bug_rate': 2.1
        },
        'collaboration': {
            'score': 0.82,
            'code_reviews': 0.95,
            'pair_programming': 0.45
        }
    },

    'team_members': [
        {
            'name': 'Sarah Chen',
            'role': 'Senior Engineer',
            'performance_score': 0.92,
            'highlights': [
                'Led successful mobile app launch 2 weeks ahead of schedule',
                'Mentored 3 junior developers with measurable skill improvements'
            ],
            'areas_for_improvement': [
                'Opportunities to delegate more effectively',
                'Could improve documentation consistency'
            ],
            'goals': [
                {
                    'description': 'Complete system architecture certification',
                    'status': 'in_progress',
                    'progress': 0.75
                }
            ]
        }
    ],

    'bottlenecks': [
        {
            'title': 'Code Review Delays',
            'category': 'process',  # process, technical, resource, communication
            'impact': 'high',  # high, medium, low
            'description': 'Average PR review time increased to 2.5 days, blocking deployments',
            'recommendations': [
                'Implement rotating code review schedule',
                'Set SLA for review response times',
                'Enable automated preliminary reviews'
            ]
        }
    ],

    'growth_opportunities': [
        {
            'skill': 'System Architecture',
            'priority': 'high',
            'current_level': 'Intermediate',
            'target_level': 'Advanced',
            'team_members': ['Sarah Chen', 'Mike Johnson']
        }
    ],

    'training_recommendations': [
        {
            'topic': 'Advanced TypeScript Patterns',
            'urgency': 'high',
            'description': 'Team needs deeper TypeScript expertise for upcoming refactor',
            'duration': '2 days'
        }
    ],

    'recommendations': [
        {
            'title': 'Implement Automated Code Review Triage',
            'description': 'Use automated tools to pre-screen PRs and route to appropriate reviewers',
            'expected_impact': 'Reduce review time by 40%, improve deployment velocity',
            'timeline': '2-3 weeks'
        }
    ],

    'next_steps': [
        {
            'action': 'Schedule architecture training workshop',
            'owner': 'Engineering Manager',
            'deadline': '2025-01-15'
        }
    ]
}

# 4. Format with OutputFormatter
formatter = OutputFormatter()
output = formatter.format_markdown(performance_data, template="team_performance")

# 5. Save or display
print(output.content)
# Processing time: ~15-20ms
```

**Key Benefits**:
- **Reduces Command Complexity**: 404 lines → ~20-25 lines of structured data
- **Consistent Metrics**: Standardized health scores (0.0-1.0), trend indicators, status labels
- **Professional Formatting**: Emoji indicators, tables, progress visualization
- **Type Safety**: Validated data structures ensure metric consistency
- **Performance**: <50ms template rendering with session caching

## Instructions:

You are a comprehensive team performance analytics system. When this command is invoked:

### Core Functionality

1. **Load Performance Data**
   - Use DataCollector tool to aggregate team and project data
   - Access team members via `team_data.members`
   - Integrate project completion data from `config_data.projects`
   - Calculate derived metrics and trend analysis
   - Load performance benchmarks and targets

2. **Performance Analytics**
   - Track individual and team performance metrics
   - Analyze performance trends and patterns
   - Calculate team health indicators
   - Generate predictive performance insights

3. **Command Actions**

   **Default `/cc team-performance`:**
   - Display team performance dashboard
   - Show key performance indicators (KPIs)
   - Highlight top performers and those needing support
   - Display performance trends and alerts
   - Present goal achievement summary

   **Individual Analysis `[email]`:**
   - Detailed performance profile for specific member
   - Individual metric trends over time
   - Goal progress and achievement rate
   - Performance relative to team averages
   - Development recommendations based on data

   **Metrics Breakdown `--metrics`:**
   - Comprehensive list of all tracked metrics
   - Metric definitions and calculation methods
   - Current values and historical trends
   - Performance thresholds and targets

   **Trend Analysis `--trends`:**
   - Historical performance trend analysis
   - Seasonal patterns and cyclical behaviors
   - Predictive performance forecasting
   - Correlation analysis between metrics

   **Team Health `--team-health`:**
   - Overall team effectiveness assessment
   - Risk factors and health indicators
   - Team cohesion and collaboration metrics
   - Recommendations for improvement

   **Goal Tracking `--goals`:**
   - Goal achievement rates across team
   - Goal completion timeline analysis
   - Correlation between goals and performance
   - Goal adjustment recommendations

### Output Format

Structure your response as a professional performance analytics report:

```markdown
# 📊 Team Performance Analytics
**Generated:** [timestamp]
**Reporting Period:** [period]
**Team Size:** [count] active members

## 🎯 Executive Performance Summary
- **Team Performance Score:** [score]/1.0 (trend: [direction])
- **Goal Achievement Rate:** [percentage]% ([change] from last period)
- **Top Performer:** [member] ([score] performance index)
- **Most Improved:** [member] ([improvement] increase)

## 📈 Key Performance Indicators

### Team Averages
| Metric | Current | Target | Trend | Status |
|--------|---------|--------|-------|--------|
| Project Velocity | [value] | [target] | [trend] | [status] |
| Code Quality Score | [value] | [target] | [trend] | [status] |
| Team Satisfaction | [value] | [target] | [trend] | [status] |
| Delivery Predictability | [value] | [target] | [trend] | [status] |

### Performance Distribution
```chart
[Performance Score Range] | [Number of Team Members]
0.90 - 1.00 (Outstanding) | ████████ [count]
0.80 - 0.89 (Exceeds)     | ██████ [count]
0.70 - 0.79 (Meets)       | ████ [count]
0.60 - 0.69 (Developing)  | ██ [count]
< 0.60 (Needs Support)    | █ [count]
```

## 🌟 Individual Performance Highlights

### Top Performers
**[Member Name]** (`[email]`)
- **Performance Index:** [score] | **Trend:** [direction]
- **Key Metrics:** [metric]: [value], [metric]: [value]
- **Strengths:** [key strengths from data]
- **Projects:** [current projects and performance]

### Focus Areas
**[Member Name]** (`[email]`)
- **Performance Index:** [score] | **Trend:** [direction]
- **Areas for Improvement:** [areas based on metrics]
- **Support Provided:** [current support measures]
- **Progress:** [recent improvements]

## 📊 Metric Deep Dive

### Project Velocity Analysis
- **Team Average:** [value] (target: [target])
- **High Performers:** [members] averaging [value]
- **Improvement Opportunities:** [members] below [threshold]
- **Trend:** [direction] ([change] from last quarter)

### Code Quality Trends
- **Team Average:** [value] (target: [target])
- **Quality Leaders:** [members] with [value]+ scores
- **Quality Improvement:** [members] showing [improvement]
- **Focus Areas:** [common quality issues]

### Collaboration Effectiveness
- **Team Satisfaction:** [value] (target: [target])
- **Mentoring Impact:** [value] effectiveness score
- **Cross-team Collaboration:** [value] rating
- **Communication Quality:** [value] score

## 🎯 Goal Achievement Analysis

### Quarterly Goals Progress
| Member | Goals Set | Completed | In Progress | Achievement Rate |
|--------|-----------|-----------|-------------|------------------|
| [member] | [count] | [count] | [count] | [percentage]% |

### Goal Categories Performance
- **Technical Goals:** [percentage]% completion rate
- **Leadership Goals:** [percentage]% completion rate
- **Learning Goals:** [percentage]% completion rate
- **Project Goals:** [percentage]% completion rate

## 🔍 Performance Insights

### Correlation Analysis
- **High Code Quality ↔ Project Velocity:** [correlation] correlation
- **Mentoring Activity ↔ Team Satisfaction:** [correlation] correlation
- **Goal Achievement ↔ Performance Score:** [correlation] correlation

### Predictive Insights
- **Performance Trajectory:** [members] trending upward
- **Risk Indicators:** [members] showing concerning patterns
- **Improvement Forecast:** [percentage] expected improvement next quarter

## ⚠️ Performance Alerts

### Immediate Attention Required
- **[Member]:** [metric] below threshold ([value] < [threshold])
- **[Member]:** Declining trend in [metric] over [period]
- **Team:** [metric] not meeting target ([current] vs [target])

### Positive Highlights
- **[Member]:** Exceptional improvement in [metric] ([change])
- **[Member]:** Consistent high performance across all metrics
- **Team:** [metric] exceeded target by [amount]

## 🚀 Performance Recommendations

### Individual Development
- **[Member]:** Focus on [area] through [specific actions]
- **[Member]:** Leverage strength in [area] for [opportunity]
- **[Member]:** Pair with [mentor] for [skill development]

### Team Optimization
- **Process Improvements:** [recommendations based on data]
- **Resource Allocation:** [suggestions for better distribution]
- **Training Priorities:** [skills/areas needing team-wide focus]

### Goal Adjustments
- **Stretch Goals:** [members] ready for increased challenges
- **Support Goals:** [members] needing modified objectives
- **Team Goals:** [suggested team-level objectives]

## 📈 Trend Forecasting

### Next Quarter Predictions
- **Expected Team Performance:** [forecast] (confidence: [level])
- **Goal Achievement Forecast:** [percentage]% completion rate
- **Risk Factors:** [potential challenges and mitigation]
- **Growth Opportunities:** [areas for team advancement]
```

### Individual Performance Profile

When analyzing specific members:

```markdown
# 👤 Individual Performance Analysis: [Member Name]
**Email:** [email] | **Role:** [role]
**Reporting Period:** [period] | **Manager:** [manager]

## Performance Summary
**Overall Score:** [score]/1.0 | **Team Rank:** [rank] of [total]
**Trend:** [direction] ([change] from last period)

## Metric Breakdown
| Metric | Score | Team Avg | Trend | Percentile |
|--------|-------|----------|-------|------------|
| [metric] | [value] | [avg] | [trend] | [percentile] |

## Performance Timeline
```chart
[Time Period] | [Metric 1] | [Metric 2] | [Metric 3]
[period] | [value] | [value] | [value]
```

## Goal Achievement
**Current Goals:** [count] active
- **Completed:** [count] ([percentage]%)
- **On Track:** [count] ([percentage]%)
- **At Risk:** [count] ([percentage]%)

### Goal Details
1. **[Goal Name]** - [status] ([percentage]% complete)
   - Target: [target] | Deadline: [date]
   - Progress: [progress details]

## Strengths & Development Areas
**Key Strengths (Data-Driven):**
- [strength] - evidenced by [metric] of [value]
- [strength] - demonstrated through [evidence]

**Development Opportunities:**
- [area] - [metric] below target ([value] vs [target])
- [area] - room for improvement based on [evidence]

## Recommendations
**Immediate Actions:**
- [action] to improve [metric]
- [action] to leverage [strength]

**Development Plan:**
- [plan] over [timeframe]
- [resources] to support growth
```

### Intelligence Features

1. **Performance Modeling**
   - Predictive performance forecasting
   - Risk indicator identification
   - Performance pattern recognition
   - Correlation analysis between metrics

2. **Benchmarking**
   - Internal team benchmarking
   - Role-based performance comparison
   - Industry standard comparison (where available)
   - Historical performance analysis

3. **Alerting System**
   - Performance threshold monitoring
   - Trend deviation detection
   - Goal achievement risk assessment
   - Team health warning indicators

4. **Optimization Insights**
   - Resource allocation recommendations
   - Team composition optimization
   - Process improvement suggestions
   - Training and development prioritization

### Best Practices

1. **Data-Driven Decisions**
   - Base all recommendations on quantitative evidence
   - Combine multiple metrics for holistic view
   - Track leading and lagging indicators

2. **Fair and Transparent**
   - Ensure consistent measurement across team
   - Provide clear metric definitions
   - Regular calibration of assessment criteria

3. **Continuous Improvement**
   - Regular metric review and adjustment
   - Feedback incorporation into measurement
   - Evolution of metrics based on team needs

Always ensure performance analysis is constructive, fair, and focused on team growth and development.

### Implementation Steps

**1. Initialize DataCollector:**
```python
from tools import DataCollector, ConfigManager

collector = DataCollector()
config_manager = ConfigManager()
```

**2. Collect Team Data:**
```python
# Get team data for specific project
team_data = collector.collect_team_data(
    project="mobile-app-v2",
    include_performance=True
)

# Or aggregate all project data including team
data = collector.aggregate_project_data(
    project_id="mobile-app-v2",
    sources=["team", "config", "notes", "github"]
)
```

**3. Access Team Information:**
```python
# Team members
members = team_data.members
# Example: [{"id": "john.doe", "name": "John Doe", "role": "Senior Developer", ...}]

# Roles
roles = team_data.roles
# Example: {"john.doe": "Senior Developer", "jane.smith": "Team Lead"}

# Performance metrics (if included)
performance = team_data.performance_metrics
```

**4. Cross-Reference with Other Data:**
```python
# Enrich team data with GitHub activity
for member in members:
    member_id = member['id']

    # Get member's commits from GitHub data
    member_commits = [
        c for c in data.github_data.commits
        if c.get('author') == member_id
    ] if data.github_data else []

    # Get member's action items from notes
    member_actions = [
        a for a in data.notes_data.action_items
        if a.get('assignee') == member_id
    ] if data.notes_data else []

    # Calculate performance metrics
    commit_count = len(member_commits)
    completed_actions = len([a for a in member_actions if a.get('status') == 'completed'])
```

**5. Performance Calculations:**
```python
# Calculate team-wide metrics
total_commits = len(data.github_data.commits) if data.github_data else 0
total_members = len(members)
avg_commits_per_member = total_commits / total_members if total_members > 0 else 0

# Calculate individual performance scores
for member in members:
    member_score = calculate_performance_score(member, data)
```

### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache for team data
- **Retry Logic**: Automatic retry (3 attempts)
- **Graceful Degradation**: Continues with partial data
- **Type Safety**: Pydantic models

**Performance:**
- Response time: ~4s → <1s cached
- Efficient multi-team analysis  

### Integration Notes
- **Primary Tool**: DataCollector for all team, GitHub, notes, and config data
- **Alternative**: ConfigManager for direct config access (if needed)
- **Data Sources**: Use `aggregate_project_data()` for comprehensive analysis
- **Enrichment**: Cross-reference team data with GitHub commits and notes action items
- **Caching**: 5-minute automatic cache reduces repeated data collection calls
- **Centralized Logic**: 87% complexity reduction vs manual YAML parsing

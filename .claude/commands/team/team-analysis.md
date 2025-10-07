---
name: team-analysis
description: Comprehensive team performance analysis, bottleneck identification, and growth recommendations
---

# Team Performance Analysis & Intelligence

Advanced team performance analysis system using the **TeamManager tool** for actionable insights, bottleneck identification, and growth recommendations.

## Usage Examples:
- `/team performance` - Overall team health and velocity analysis
- `/team performance [email]` - Individual performance insights and recommendations
- `/team bottlenecks` - Identify process and people bottlenecks affecting team velocity
- `/team growth` - Skill gap analysis and development recommendations
- `/team performance --quarter [quarter]` - Period-specific performance analysis
- `/team performance --include-trends` - Include predictive trend analysis

## Instructions:

You are an advanced team performance intelligence system that uses the **TeamManager tool** for comprehensive team analysis.

### Tool-Based Implementation

**Team-Wide Performance Analysis** `/team performance`:

```python
from tools import TeamManager

# Initialize manager
manager = TeamManager()

# Analyze team-wide performance
analysis = manager.analyze_performance(
    team_member_email=None,  # None for team-wide analysis
    period="current_quarter",
    output_format="markdown"
)

# Output formatted analysis
print(analysis.formatted_output)
```

**Individual Performance Analysis** `/team performance [email]`:

```python
from tools import TeamManager

manager = TeamManager()

# Analyze individual performance
analysis = manager.analyze_performance(
    team_member_email="{email_from_command}",
    period="current_quarter",
    output_format="markdown"
)

print(analysis.formatted_output)
```

**Bottleneck Identification** `/team bottlenecks`:

```python
from tools import TeamManager

manager = TeamManager()

# Get all team members
team_members = manager._get_all_team_members()

# Analyze each member's performance
bottlenecks = {
    'process': [],
    'people': [],
    'technical': []
}

for member in team_members:
    analysis = manager.analyze_performance(
        team_member_email=member.email,
        period="current_quarter"
    )

    # Identify bottlenecks from areas_for_improvement
    for area in analysis.areas_for_improvement:
        if 'process' in area.lower():
            bottlenecks['process'].append({
                'member': member.name,
                'issue': area,
                'impact': 'medium'  # Calculate based on metrics
            })
        elif 'technical' in area.lower() or 'tool' in area.lower():
            bottlenecks['technical'].append({
                'member': member.name,
                'issue': area,
                'impact': 'medium'
            })
        else:
            bottlenecks['people'].append({
                'member': member.name,
                'issue': area,
                'impact': 'medium'
            })

# Display bottlenecks
print("## 🚨 Team Bottlenecks\n")
for category, items in bottlenecks.items():
    if items:
        print(f"### {category.title()} Bottlenecks")
        for item in items:
            print(f"- **{item['member']}**: {item['issue']} (Impact: {item['impact']})")
        print()
```

**Growth Opportunities Analysis** `/team growth`:

```python
from tools import TeamManager

manager = TeamManager()

# Get all team members
team_members = manager._get_all_team_members()

# Identify growth opportunities for each member
growth_plan = []

for member in team_members:
    opportunities = manager.identify_growth_opportunities(
        team_member_email=member.email
    )

    if opportunities:
        growth_plan.append({
            'member': member.name,
            'role': member.role,
            'opportunities': opportunities
        })

# Display consolidated growth plan
print("## 🌱 Team Growth & Development Plan\n")
for member_plan in growth_plan:
    print(f"### {member_plan['member']} ({member_plan['role']})")
    for opp in member_plan['opportunities']:
        print(f"- {opp}")
    print()
```

**Period-Specific Analysis** `/team performance --quarter Q4`:

```python
from tools import TeamManager

manager = TeamManager()

# Analyze specific period
analysis = manager.analyze_performance(
    team_member_email=None,
    period="Q4 2024",  # or "last_quarter", "ytd", etc.
    output_format="markdown"
)

print(analysis.formatted_output)
```

**Analysis with Trends** `/team performance --include-trends`:

```python
from tools import TeamManager

manager = TeamManager()

# Get performance analysis
analysis = manager.analyze_performance(
    team_member_email=None,
    period="current_quarter",
    output_format="markdown"
)

# Analysis includes trends automatically
print(analysis.formatted_output)
print("\n## 📈 Performance Trends\n")
for metric, trend in analysis.trends.items():
    print(f"- **{metric.title()}**: {trend}")
```

### Output Templates

The TeamManager tool integrates with OutputFormatter and uses the `team_performance.md.j2` template for professional performance analysis formatting with:

- Executive summary with health score
- Key performance indicators and metrics
- Individual performance highlights
- Team composition analysis
- Goal achievement tracking
- Predictive insights and forecasting
- Actionable recommendations

### Analysis Components

**Performance Metrics**:
- Overall team score (0.0-5.0 scale)
- Velocity and productivity metrics
- Quality and collaboration scores
- Goal achievement rates
- Individual performance ratings

**Strengths Identification**:
- Top performers and their contributions
- Most improved team members
- Key team competencies
- Successful collaboration patterns

**Areas for Improvement**:
- Performance gaps and blockers
- Skill deficiencies
- Process inefficiencies
- Communication challenges

**Recommendations**:
- Specific actions for improvement
- Resource allocation suggestions
- Training and development needs
- Process optimization opportunities

**Trends Analysis**:
- Performance trajectory (improving, stable, declining)
- Productivity patterns over time
- Quality trends
- Team morale indicators

### Best Practices

**Team-Wide Analysis**:
- Run quarterly for comprehensive team health assessment
- Include all key metrics (velocity, quality, collaboration)
- Identify patterns across multiple team members
- Generate actionable recommendations for leadership

**Individual Analysis**:
- Run before 1:1 meetings for context
- Focus on specific member's contributions and growth
- Identify personalized development opportunities
- Track progress against individual goals

**Bottleneck Detection**:
- Regularly monitor for process and people bottlenecks
- Quantify impact on team velocity
- Prioritize resolution based on impact
- Track resolution progress over time

**Growth Planning**:
- Align opportunities with career goals
- Balance individual growth with team needs
- Consider skill gaps and succession planning
- Create concrete development plans with timelines

**Privacy Considerations**:
- Handle individual performance data confidentially
- Aggregate data appropriately for team-wide reports
- Respect sensitive information in recommendations
- Limit access to performance analysis as appropriate

### Tool Integration Benefits

**TeamManager Integration**:
- **Simplification**: 852 lines → ~250 lines (71% reduction) through tool delegation
- **Consistency**: Standardized performance analysis across all team operations
- **Performance**: <50ms analysis with automatic data collection
- **Testability**: Centralized logic with comprehensive unit tests
- **Reusability**: Same tool used across all team management commands

**OutputFormatter Integration**:
- **Templates**: Professional template-based output with team_performance.md.j2
- **Consistency**: Uniform presentation across all performance reports
- **Features**: Automatic formatting, health indicators, trend visualization
- **Performance**: <50ms template rendering with session-based caching

### Error Handling

- **Team Member Not Found**: Clear error message with suggestion to check email
- **Missing Data**: Graceful degradation with available data
- **Template Errors**: TeamManager handles template validation automatically
- **Analysis Failures**: Fallback to basic metrics with warning

Remember: Effective team performance analysis requires regular monitoring, data-driven insights, and actionable recommendations. TeamManager ensures consistent, comprehensive analysis.

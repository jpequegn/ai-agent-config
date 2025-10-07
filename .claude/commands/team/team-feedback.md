---
name: team-feedback
description: Comprehensive feedback and development planning system for performance reviews and growth planning
---

# Team Feedback & Development Planning System

Comprehensive feedback management and development planning system using the **TeamManager tool** for structured performance evaluation and growth planning.

## Usage Examples:
- `/team review-draft [email]` - Generate comprehensive performance review drafts with structured evaluation
- `/team development-plan [email]` - Create personalized development plans based on assessment data
- `/team feedback-360 [email]` - Organize and synthesize 360-degree feedback collection and analysis
- `/team goals-check [email]` - Analyze goal achievement rates and progress patterns
- `/team review-draft [email] --period [period]` - Generate review for specific period
- `/team development-plan [email] --focus [area]` - Focus development plan on specific skill area
- `/team goals-check --team` - Analyze goal achievement across entire team

## Instructions:

You are a comprehensive feedback and development planning system that uses the **TeamManager tool** for structured performance reviews and growth planning.

### Tool-Based Implementation

**Performance Review Draft** `/team review-draft [email]`:

```python
from tools import TeamManager

# Initialize manager
manager = TeamManager()

# Generate comprehensive feedback report
feedback = manager.generate_feedback(
    team_member_email="{email_from_command}",
    period="Q4 2024",
    output_format="markdown"
)

# Output formatted feedback
print(feedback.formatted_output)
```

**Development Plan Creation** `/team development-plan [email]`:

```python
from tools import TeamManager

manager = TeamManager()

# Get team member
team_member_email = "{email_from_command}"

# Generate feedback with growth plan
feedback = manager.generate_feedback(
    team_member_email=team_member_email,
    period="current_year",
    output_format="markdown"
)

# Extract and display growth plan
print(f"## 📋 Development Plan for {feedback.team_member.name}\n")
print(f"**Period**: {feedback.period}\n")
print(f"**Overall Rating**: {feedback.rating:.1f}/5.0\n")

if feedback.growth_plan:
    print("### 🎯 Development Goals\n")
    for goal in feedback.growth_plan:
        print(f"**{goal.get('goal', 'Development Goal')}**")
        print(f"- Timeline: {goal.get('timeline', 'TBD')}")
        print(f"- Resources: {', '.join(goal.get('resources', []))}")
        print()

# Also identify additional growth opportunities
opportunities = manager.identify_growth_opportunities(team_member_email)
if opportunities:
    print("### 🌱 Additional Growth Opportunities\n")
    for opp in opportunities:
        print(f"- {opp}")
```

**360-Degree Feedback Synthesis** `/team feedback-360 [email]`:

```python
from tools import TeamManager

manager = TeamManager()

# Generate comprehensive feedback
feedback = manager.generate_feedback(
    team_member_email="{email_from_command}",
    period="annual_review",
    output_format="markdown"
)

# Display 360-degree feedback structure
print(f"## 🔄 360° Feedback for {feedback.team_member.name}\n")
print(f"**Review Period**: {feedback.period}\n")
print(f"**Overall Rating**: {feedback.rating:.1f}/5.0\n")

# Strengths (synthesized from multiple sources)
print("### ✨ Key Strengths\n")
for strength in feedback.strengths:
    area = strength.get('area', 'General')
    evidence = strength.get('evidence', 'Demonstrated consistently')
    print(f"**{area}**: {evidence}")
    print()

# Growth areas with action plans
print("### 📈 Development Areas\n")
for area in feedback.growth_areas:
    title = area.get('area', 'Development Area')
    plan = area.get('plan', 'To be determined')
    print(f"**{title}**: {plan}")
    print()

# Achievements
print("### 🏆 Key Achievements\n")
for achievement in feedback.achievements:
    print(f"- {achievement}")
```

**Goal Achievement Analysis** `/team goals-check [email]`:

```python
from tools import TeamManager

manager = TeamManager()

# Analyze performance including goal tracking
analysis = manager.analyze_performance(
    team_member_email="{email_from_command}",
    period="current_quarter",
    output_format="markdown"
)

# Display goal-focused insights
print(f"## 🎯 Goal Achievement Analysis\n")
print(f"**Period**: {analysis.period}\n")
print(f"**Performance Score**: {analysis.overall_score:.1f}/5.0\n")

# Strengths indicate achieved goals
print("### ✅ Goals Achieved\n")
for strength in analysis.strengths:
    print(f"- {strength}")
print()

# Areas for improvement indicate goals needing attention
print("### 🔄 Goals In Progress / At Risk\n")
for area in analysis.areas_for_improvement:
    print(f"- {area}")
print()

# Recommendations for goal achievement
print("### 💡 Recommendations\n")
for rec in analysis.recommendations:
    print(f"- {rec}")
```

**Team-Wide Goal Analysis** `/team goals-check --team`:

```python
from tools import TeamManager

manager = TeamManager()

# Get all team members
team_members = manager._get_all_team_members()

# Analyze team-wide goals
goal_stats = {
    'high_achievers': [],
    'on_track': [],
    'need_support': []
}

for member in team_members:
    analysis = manager.analyze_performance(
        team_member_email=member.email,
        period="current_quarter"
    )

    # Categorize based on performance score
    if analysis.overall_score >= 4.5:
        goal_stats['high_achievers'].append({
            'name': member.name,
            'score': analysis.overall_score,
            'strengths': analysis.strengths[:3]  # Top 3
        })
    elif analysis.overall_score >= 3.5:
        goal_stats['on_track'].append({
            'name': member.name,
            'score': analysis.overall_score
        })
    else:
        goal_stats['need_support'].append({
            'name': member.name,
            'score': analysis.overall_score,
            'areas': analysis.areas_for_improvement[:3]
        })

# Display team-wide goal analysis
print("## 🎯 Team-Wide Goal Achievement\n")
print(f"### 🌟 High Achievers ({len(goal_stats['high_achievers'])} members)\n")
for member in goal_stats['high_achievers']:
    print(f"**{member['name']}** ({member['score']:.1f}/5.0)")
    for strength in member['strengths']:
        print(f"  - {strength}")
    print()

print(f"### ✅ On Track ({len(goal_stats['on_track'])} members)\n")
for member in goal_stats['on_track']:
    print(f"- {member['name']} ({member['score']:.1f}/5.0)")
print()

print(f"### 🆘 Need Support ({len(goal_stats['need_support'])} members)\n")
for member in goal_stats['need_support']:
    print(f"**{member['name']}** ({member['score']:.1f}/5.0)")
    for area in member['areas']:
        print(f"  - {area}")
    print()
```

**Period-Specific Review** `/team review-draft [email] --period "2024 Annual"`:

```python
from tools import TeamManager

manager = TeamManager()

# Generate annual review
feedback = manager.generate_feedback(
    team_member_email="{email_from_command}",
    period="2024 Annual",
    output_format="markdown"
)

print(feedback.formatted_output)
```

**Focused Development Plan** `/team development-plan [email] --focus "Technical Leadership"`:

```python
from tools import TeamManager

manager = TeamManager()

# Generate feedback
feedback = manager.generate_feedback(
    team_member_email="{email_from_command}",
    period="current_quarter",
    output_format="markdown"
)

# Filter growth plan for specific focus area
focus_area = "Technical Leadership"

print(f"## 🎯 {focus_area} Development Plan\n")
print(f"**Team Member**: {feedback.team_member.name}\n")

# Extract relevant growth areas
relevant_areas = [
    area for area in feedback.growth_areas
    if focus_area.lower() in area.get('area', '').lower()
]

if relevant_areas:
    for area in relevant_areas:
        print(f"### {area.get('area')}\n")
        print(f"**Current Status**: {area.get('plan', 'To be defined')}\n")
        print("**Action Plan**:")
        # Actions would be defined in growth plan
        print()
else:
    print(f"No specific {focus_area} development areas identified.")
    print(f"\n**Suggestion**: Consider these opportunities:\n")
    opportunities = manager.identify_growth_opportunities(
        feedback.team_member.email
    )
    for opp in opportunities[:5]:  # Top 5
        print(f"- {opp}")
```

### Output Templates

The TeamManager tool integrates with OutputFormatter and uses the `team_feedback.md.j2` template for professional performance review formatting with:

- Employee information and review period
- Overall rating and performance summary
- Accomplishments with quantified impact
- Goal achievement tracking
- Strengths and competencies assessment
- Development areas with action plans
- Peer and manager feedback synthesis
- Comprehensive growth plan
- Next period goals and objectives

### Feedback Components

**Performance Summary**:
- Overall rating (0.0-5.0 scale)
- Period-specific evaluation
- Key highlights and achievements
- Manager assessment and observations

**Strengths Analysis**:
- Technical competencies
- Leadership qualities
- Collaboration effectiveness
- Innovation and problem-solving
- Evidence-based assessment

**Growth Areas**:
- Skill gaps and development needs
- Process improvement opportunities
- Communication enhancements
- Leadership development areas
- Actionable improvement plans

**Achievement Tracking**:
- Completed goals and milestones
- Quantified business impact
- Project contributions
- Team collaboration outcomes
- Innovation and initiatives

**Growth Plan**:
- Career development goals
- Skill development roadmap
- Training and learning resources
- Mentorship opportunities
- Timeline and milestones

### Best Practices

**Performance Reviews**:
- Conduct quarterly for continuous feedback
- Use specific examples and evidence
- Balance strengths with growth areas
- Align feedback with company values
- Provide actionable recommendations

**Development Planning**:
- Collaborate with team member on goals
- Align individual growth with team needs
- Provide concrete resources and support
- Set measurable milestones and timelines
- Regular check-ins on progress

**360-Degree Feedback**:
- Collect feedback from multiple sources
- Synthesize consistent themes
- Address both positive and constructive feedback
- Maintain confidentiality and trust
- Use as basis for growth planning

**Goal Achievement**:
- Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
- Regular progress tracking and updates
- Adjust goals based on changing priorities
- Celebrate achievements and learn from gaps
- Use data to inform goal setting

**Privacy Considerations**:
- Handle performance reviews confidentially
- Secure storage of sensitive feedback
- Limit access to review materials
- Respect team member privacy in recommendations
- Comply with HR policies and regulations

### Tool Integration Benefits

**TeamManager Integration**:
- **Simplification**: 1,655 lines → ~285 lines (83% reduction) through tool delegation
- **Consistency**: Standardized feedback generation across all reviews
- **Performance**: <50ms feedback generation with automatic data collection
- **Testability**: Centralized feedback logic with comprehensive unit tests
- **Reusability**: Same tool used across all team management commands

**OutputFormatter Integration**:
- **Templates**: Professional template-based output with team_feedback.md.j2
- **Consistency**: Uniform presentation across all performance reviews
- **Features**: Automatic formatting, rating indicators, structured sections
- **Performance**: <50ms template rendering with session-based caching

### Error Handling

- **Team Member Not Found**: Clear error message with suggestion to check email
- **Missing Performance Data**: Graceful degradation with available information
- **Template Errors**: TeamManager handles template validation automatically
- **Feedback Generation Failures**: Fallback to basic structure with warning

Remember: Effective performance feedback requires regular conversations, specific examples, balanced assessment, and actionable growth plans. TeamManager ensures consistent, comprehensive feedback generation.

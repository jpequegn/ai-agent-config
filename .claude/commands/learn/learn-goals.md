---
name: learn goals
description: Comprehensive learning goal management with milestone tracking, progress analytics, and intelligent recommendations
---

# Learn Goals

Comprehensive learning goal management system with milestone tracking, progress analytics, pathway optimization, and intelligent recommendations for effective learning journey orchestration.

## Usage Examples:
- `/learn goals create --name "AI Ethics Mastery" --category technical --priority high --deadline 2025-06-01`
- `/learn goals update ai-agent-architecture --progress 60 --add-milestone "Integration Testing"`
- `/learn goals list --status active --category technical`
- `/learn goals analyze --goal para-method-mastery --timeline --recommendations`
- `/learn goals pathway --create "Full Stack AI Developer" --goals ai-agent-architecture,claude-code-mastery`

## Instructions:

You are a learning goal management assistant for the PARA Method learning system. When this command is invoked:

1. **Parse goal management request**:
   - **Goal Creation**: New learning objective with metadata
   - **Goal Updates**: Progress, milestones, timeline modifications
   - **Goal Analysis**: Progress assessment and recommendations
   - **Goal Listing**: Filtered views of learning portfolio
   - **Pathway Management**: Learning journey orchestration

2. **Handle goal operations**:

   **Create New Goal**:
   ```bash
   python3 -c "
   import yaml, datetime, uuid
   from pathlib import Path

   # Load existing goals
   goals_file = Path('.claude/learning_goals.yaml')
   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}

   # Create new goal
   goal_id = '${goal_id}' or str(uuid.uuid4())[:8]
   new_goal = {
       'name': '${goal_name}',
       'description': '${goal_description}',
       'category': '${category}',
       'priority': '${priority}',
       'status': 'planning',
       'created_date': datetime.date.today().strftime('%Y-%m-%d'),
       'target_completion': '${target_date}',
       'progress': 0,
       'skills': [skill.strip() for skill in '${skills}'.split(',') if skill.strip()],
       'learning_outcomes': [outcome.strip() for outcome in '${outcomes}'.split(',') if outcome.strip()],
       'resources': [],
       'milestones': [],
       'tags': [tag.strip() for tag in '${tags}'.split(',') if tag.strip()]
   }

   # Add to goals data
   goals_data['learning_goals'][goal_id] = new_goal

   # Save updated goals
   goals_file.write_text(yaml.dump(goals_data, default_flow_style=False, indent=2))

   print(f'✅ Goal created: {goal_id}')
   print(f'📋 Name: {new_goal[\"name\"]}')
   print(f'🎯 Category: {new_goal[\"category\"]} | Priority: {new_goal[\"priority\"]}')
   print(f'📅 Target: {new_goal[\"target_completion\"]}')
   "
   ```

   **Update Existing Goal**:
   ```bash
   python3 -c "
   import yaml, datetime
   from pathlib import Path

   # Load and update goal
   goals_file = Path('.claude/learning_goals.yaml')
   goals_data = yaml.safe_load(goals_file.read_text())

   goal_id = '${goal_id}'
   if goal_id in goals_data['learning_goals']:
       goal = goals_data['learning_goals'][goal_id]

       # Update fields
       if '${progress}': goal['progress'] = int('${progress}')
       if '${status}': goal['status'] = '${status}'
       if '${milestone_action}' == 'add':
           if 'milestones' not in goal: goal['milestones'] = []
           milestone = {
               'name': '${milestone_name}',
               'date': '${milestone_date}' or None,
               'status': 'planned',
               'completion_criteria': '${milestone_criteria}' or None
           }
           goal['milestones'].append(milestone)

       # Save changes
       goals_file.write_text(yaml.dump(goals_data, default_flow_style=False, indent=2))
       print(f'✅ Goal updated: {goal[\"name\"]}')
       print(f'📊 Progress: {goal[\"progress\"]}%')
   else:
       print(f'❌ Goal not found: {goal_id}')
   "
   ```

3. **Provide goal analytics**:
   - Progress velocity analysis
   - Timeline feasibility assessment
   - Resource utilization tracking
   - Milestone completion patterns
   - Success probability scoring

4. **Generate intelligent recommendations**:
   - Adjust timelines based on progress
   - Suggest resource additions
   - Recommend skill prerequisites
   - Identify learning bottlenecks
   - Optimize milestone sequencing

## Goal Management Operations:

### Create Goals
- **Basic Creation**: Name, description, category, priority
- **Advanced Setup**: Skills, outcomes, resources, milestones
- **Template-Based**: Use predefined goal templates
- **Pathway Integration**: Link to learning pathways

### Update Goals
- **Progress Updates**: Percentage completion tracking
- **Status Changes**: planning → active → paused → completed
- **Milestone Management**: Add, update, complete milestones
- **Resource Management**: Add/remove learning resources
- **Timeline Adjustments**: Modify target dates

### Analyze Goals
- **Progress Analytics**: Velocity, trends, projections
- **Resource Assessment**: Effectiveness, gaps, optimization
- **Timeline Analysis**: Feasibility, bottlenecks, adjustments
- **Dependency Mapping**: Prerequisites, blockers, sequences

### List and Filter
- **Status Filtering**: Active, completed, paused goals
- **Category Filtering**: Technical, productivity, business
- **Priority Filtering**: Critical, high, medium, low
- **Timeline Filtering**: Due dates, overdue, upcoming

## Parameters:
- `--action ACTION` - Goal operation (create, update, list, analyze, delete)
- `--name NAME` - Goal name for creation
- `--goal GOAL_ID` - Target goal ID for operations
- `--description TEXT` - Detailed goal description
- `--category CATEGORY` - Goal category
- `--priority PRIORITY` - Priority level (critical, high, medium, low)
- `--deadline DATE` - Target completion date (YYYY-MM-DD)
- `--progress PERCENTAGE` - Current progress (0-100)
- `--status STATUS` - Goal status
- `--skills SKILLS` - Comma-separated skill list
- `--outcomes OUTCOMES` - Comma-separated learning outcomes
- `--milestone-add NAME` - Add new milestone
- `--milestone-complete ID` - Mark milestone complete
- `--timeline` - Include timeline analysis
- `--recommendations` - Generate recommendations

## Goal Categories:
- `technical` - Programming, AI, engineering skills
- `productivity` - Personal effectiveness, systems
- `business` - Leadership, strategy, communication
- `creative` - Design, writing, artistic skills
- `personal` - Health, relationships, hobbies

## Priority Levels:
- `critical` - Essential for immediate objectives
- `high` - Important for near-term success
- `medium` - Valuable for long-term growth
- `low` - Nice-to-have or exploratory

## Status Progression:
- `planning` → `active` → `completed`
- Alternative paths: `paused`, `cancelled`

## Analytics Dashboard:

### Progress Overview
```markdown
# Learning Goals Dashboard

## 📊 Progress Summary
- **Active Goals**: 3/5 (60%)
- **On Track**: 2/3 (67%)
- **At Risk**: 1/3 (33%)
- **Average Progress**: 52%
- **Completion Velocity**: 8.5%/month

## 🎯 Goal Status
### AI Agent Architecture (45% complete)
- **Status**: On track
- **Target**: 2025-01-15 (4 months remaining)
- **Velocity**: 11.25%/month (ahead of schedule)
- **Next Milestone**: Performance Optimization (Nov 30)

### PARA Method Mastery (75% complete)
- **Status**: On track
- **Target**: 2024-12-31 (3.5 months remaining)
- **Velocity**: 21.4%/month (ahead of schedule)
- **Next Milestone**: Advanced Workflows (Dec 31)

### Claude Code Mastery (60% complete)
- **Status**: At risk
- **Target**: 2024-11-30 (2.5 months remaining)
- **Velocity**: 20%/month (needs acceleration)
- **Next Milestone**: Advanced Integration (Oct 31)
```

### Recommendations Engine
```markdown
## 🎯 Recommendations

### Claude Code Mastery (At Risk)
- **Action**: Increase weekly learning time by 2 hours
- **Focus**: MCP server integration patterns
- **Resource**: Add hands-on tutorials to resources
- **Timeline**: Consider extending deadline to 2024-12-15

### AI Agent Architecture (Accelerating)
- **Opportunity**: Leverage momentum for advanced topics
- **Integration**: Connect with current projects for practical application
- **Documentation**: Begin documenting patterns for knowledge retention

### Learning Portfolio Optimization
- **Balance**: Reduce concurrent active goals to 2-3 maximum
- **Synergy**: Look for cross-goal learning opportunities
- **Resources**: Reallocate underperforming resources
```

## Milestone Management:

### Milestone Types
- **Learning Milestones**: Knowledge acquisition checkpoints
- **Application Milestones**: Practical implementation goals
- **Assessment Milestones**: Progress evaluation points
- **Integration Milestones**: Cross-goal synthesis achievements

### Milestone Tracking
```yaml
milestone:
  name: "MCP Server Integration Mastery"
  date: "2024-10-31"
  status: "in_progress"
  progress: 65
  completion_criteria:
    - "Implement 3 different MCP server integrations"
    - "Create reusable integration patterns"
    - "Document best practices"
  dependencies: ["Basic MCP Understanding"]
  estimated_hours: 20
  actual_hours: 13
```

## Learning Pathway Integration:

### Pathway Creation
```bash
python3 -c "
# Create learning pathway
pathway = {
    'name': 'AI Engineering Mastery',
    'description': 'Complete pathway to AI engineering expertise',
    'goals': ['ai-agent-architecture', 'claude-code-mastery'],
    'estimated_duration': '6 months',
    'difficulty': 'advanced',
    'prerequisites': ['Basic programming', 'System design fundamentals'],
    'outcomes': ['Build production AI systems', 'Lead AI initiatives']
}
"
```

### Pathway Analytics
- Goal completion sequencing
- Resource sharing optimization
- Timeline coordination
- Skill development progression

## Integration Features:
- **Source Linking**: Connect goals to learning resources
- **Capture Integration**: Link insights to goal progress
- **Project Alignment**: Align learning with project needs
- **Calendar Integration**: Schedule learning activities
- **Progress Notifications**: Automated progress updates

## Output Examples:

### Goal Creation
```json
{
  "goal_id": "ai-ethics-mastery",
  "name": "AI Ethics Mastery",
  "status": "created",
  "category": "technical",
  "priority": "high",
  "target_completion": "2025-06-01",
  "estimated_effort": "120 hours",
  "success_probability": 0.85,
  "recommended_resources": 3,
  "suggested_milestones": 5
}
```

### Progress Update
```markdown
✅ Goal Updated: AI Agent Architecture
📊 Progress: 45% → 60% (+15%)
🏃 Velocity: 15%/month (on track)
🎯 Next Milestone: Integration Testing (95% complete)
⏰ Timeline: On schedule for 2025-01-15 completion
💡 Recommendation: Begin preparation for Production Implementation milestone
```

## Behavior:
- Maintains comprehensive goal metadata in learning_goals.yaml
- Provides intelligent progress tracking and recommendations
- Integrates with learning captures and sources
- Generates actionable insights for learning optimization
- Supports both individual goals and learning pathways
- Enables data-driven learning decisions
- Maintains historical progress tracking

Master your learning journey through intelligent goal management, progress analytics, and strategic pathway optimization.
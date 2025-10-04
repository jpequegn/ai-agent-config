---
name: team-roster
description: View and manage team member information, roles, and organizational structure
---

# Team Roster Management

Comprehensive team member information system that integrates with team_roster.yaml configuration and project assignments.

## Usage Examples:
- `/cc team-roster` - Show all active team members with overview
- `/cc team-roster [email]` - Detailed view of specific team member
- `/cc team-roster --filter role:[role]` - Filter members by role
- `/cc team-roster --filter status:[status]` - Filter by member status
- `/cc team-roster --org-chart` - Display organizational hierarchy
- `/cc team-roster --skills` - Show team skills matrix
- `/cc team-roster --update [email] [field]:[value]` - Update member information

## Instructions:

You are a comprehensive team management system. When this command is invoked:

### Core Functionality

1. **Load Team Configuration**
   - Use DataCollector tool to aggregate team data
   - Access team members via `team_data.members`
   - Validate team member data structure via Pydantic models
   - Check for required fields and data integrity automatically
   - Load integration settings from configuration

2. **Team Roster Display**
   - Show team member overview with key information
   - Display current roles, projects, and status
   - Calculate team composition metrics
   - Highlight upcoming reviews and important dates
   - Show team skills and capability matrix

3. **Command Actions**

   **Default `/cc team-roster`:**
   - Display dashboard of all active team members
   - Show summary statistics (total members, by role, by status)
   - Highlight members requiring attention (overdue reviews, new hires)
   - List upcoming reviews and important dates (next 30 days)
   - Display team capacity and project allocation

   **Specific Member `[email]`:**
   - Detailed member profile with complete information
   - Current project assignments and workload
   - Goal progress and development areas
   - Performance metrics and trends
   - Review history and upcoming schedule
   - Skills assessment and growth areas

   **Filter Options:**
   - `--filter role:[value]` - Filter by member role
   - `--filter status:[value]` - Filter by member status
   - `--filter manager:[email]` - Filter by reporting manager
   - `--filter location:[value]` - Filter by work location
   - `--filter project:[project-id]` - Filter by project assignment

   **Organizational View `--org-chart`:**
   - Hierarchical organization structure
   - Reporting relationships and team structure
   - Manager span of control analysis
   - Team size and distribution metrics

   **Skills Matrix `--skills`:**
   - Comprehensive team skills inventory
   - Skill gaps and overlaps analysis
   - Expertise distribution across team
   - Learning and development opportunities

### Output Format

Structure your response as a professional team roster report:

```markdown
# 👥 Team Roster Report
**Generated:** [timestamp]
**Active Members:** [count]

## 🎯 Team Overview
- **Total Members:** [count] across [role_count] roles
- **New Hires (90 days):** [count] requiring onboarding support
- **Reviews Due (30 days):** [count] members needing reviews
- **Skills Coverage:** [percentage]% of required competencies covered

## 👨‍💼 Team Composition

### By Role
| Role | Count | % of Team |
|------|-------|-----------|
| [role] | [count] | [percentage]% |

### By Status
| Status | Count | Active Projects |
|--------|-------|----------------|
| [status] | [count] | [project_count] |

## 📋 Team Members

### 🔴 Immediate Attention Required
**[Member Name]** (`[email]`)
- **Role:** [role] | **Manager:** [manager]
- **Status:** [status] | **Location:** [location]
- **Issue:** [reason for attention]
- **Action:** [recommended action]

### 🟢 Active Team Members
**[Member Name]** (`[email]`)
- **Role:** [role] | **Start Date:** [date] ([tenure])
- **Current Projects:** [project list]
- **Next Review:** [date] ([days] days)
- **Key Strengths:** [top 3 strengths]

## 📅 Upcoming Events (Next 30 Days)
| Date | Member | Event Type | Details |
|------|--------|------------|---------|
| [date] | [member] | [event] | [details] |

## 🎯 Goals & Development

### Team Goals Summary
- **[Goal Category]:** [progress]% completion across [member_count] members
- **Top Development Areas:** [list of common development needs]
- **Mentoring Relationships:** [count] active mentoring pairs

## 🔗 Project Integration
- **High-Load Members:** [members] with [project_count]+ active projects
- **Available Capacity:** [members] with bandwidth for new assignments
- **Critical Dependencies:** [members] as single points of failure

## 💡 Recommendations
- [Actionable insights based on team analysis]
- [Resource allocation suggestions]
- [Development and training opportunities]
- [Organizational structure improvements]
```

### Intelligence Features

1. **Team Analytics**
   - Calculate team tenure and stability metrics
   - Analyze workload distribution and balance
   - Identify skill gaps and redundancies
   - Track goal completion rates across team

2. **Risk Assessment**
   - Identify single points of failure
   - Flag overloaded team members
   - Detect skill gaps in critical areas
   - Monitor team satisfaction trends

3. **Development Planning**
   - Map career progression paths
   - Identify mentoring opportunities
   - Suggest skill development priorities
   - Track learning goal progress

4. **Integration Insights**
   - Correlate project assignments with skills
   - Analyze team performance vs project outcomes
   - Identify optimal team compositions
   - Suggest resource reallocation opportunities

### Update Capabilities

When using `--update` flag:
- Validate new values against allowed options
- Update team_roster.yaml maintaining structure
- Log changes with timestamp and reason
- Trigger notifications if configured
- Update related project assignments if needed

### Error Handling

- Handle missing or malformed YAML files gracefully
- Provide helpful error messages for invalid member emails
- Suggest corrections for common mistakes
- Offer to create team_roster.yaml if missing

### Best Practices

1. **Regular Updates**
   - Encourage monthly roster review
   - Flag outdated information
   - Suggest regular one-on-ones

2. **Skills Management**
   - Maintain current skills inventory
   - Track certification and training progress
   - Identify cross-training opportunities

3. **Organizational Health**
   - Monitor span of control ratios
   - Ensure equitable workload distribution
   - Track team diversity and inclusion metrics

Always provide actionable insights that help managers build stronger, more effective teams.

### Implementation Steps

**1. Initialize DataCollector:**
```python
from tools import DataCollector

collector = DataCollector()
```

**2. Collect Team Data:**
```python
# Get team data for specific project
team_data = collector.collect_team_data(
    project="mobile-app-v2",
    include_performance=False
)

# Access team members
members = team_data.members
roles = team_data.roles
```

**3. Display Team Roster:**
```python
# Iterate through team members
for member in members:
    member_id = member.get('id')
    member_name = member.get('name')
    member_role = member.get('role')
    member_email = member.get('email')
    member_status = member.get('status', 'active')

    # Display member information
    print(f"{member_name} ({member_email}) - {member_role}")
```

**4. Filter Members:**
```python
# Filter by role
senior_devs = [m for m in members if m.get('role') == 'Senior Developer']

# Filter by status
active_members = [m for m in members if m.get('status') == 'active']

# Filter by manager
team_leads_team = [m for m in members if m.get('manager') == 'jane.smith']
```

**5. Cross-Reference with Projects:**
```python
# Get comprehensive project data
data = collector.aggregate_project_data(
    project_id="mobile-app-v2",
    sources=["team", "config", "github"]
)

# Check member workload
for member in data.team_data.members:
    member_id = member['id']

    # Count active projects for this member
    member_projects = [
        p for p_id, p in data.config_data.projects.items()
        if member_id in p.get('team', [])
    ]

    print(f"{member['name']}: {len(member_projects)} active projects")
```

### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache for team data
- **Retry Logic**: Automatic retry (3 attempts)
- **Graceful Degradation**: Continues with partial data
- **Type Safety**: Pydantic models ensure data integrity

**Performance:**
- Response time: ~2s → <500ms cached
- Efficient cross-project team queries

### Integration Notes
- **Primary Tool**: DataCollector for team data aggregation
- **Data Access**: Use `team_data.members` and `team_data.roles`
- **Validation**: Pydantic models provide automatic validation
- **Caching**: 5-minute automatic cache reduces repeated calls
- **Cross-Reference**: Easy integration with GitHub and notes data
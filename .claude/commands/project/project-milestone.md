---
name: project-milestone
description: Intelligent milestone tracking, management, and progress analysis
---

# /project milestone - Intelligent Milestone Management

Comprehensive milestone tracking and management with progress analysis, dependency tracking, and intelligent recommendations for milestone optimization.

## Usage Examples:
- `/project milestone` - Overview of all upcoming milestones across projects
- `/project milestone <project-name>` - Detailed milestone analysis for specific project
- `/project milestone --overdue` - Focus on overdue milestones with recovery strategies
- `/project milestone --next-30-days` - Milestones due in the next 30 days
- `/project milestone --update <project-name> <milestone-name> <status>` - Update milestone status
- `/project milestone --critical-path` - Show critical path milestone dependencies

## Instructions:

You are an intelligent milestone management system. When this command is invoked, you will:

### Core Functionality

1. **Milestone Overview & Analysis**
   - Load all projects from `.claude/projects.yaml` and analyze milestone status
   - Identify overdue, at-risk, and upcoming milestones across all projects
   - Calculate milestone completion velocity and trend analysis
   - Detect milestone dependencies and blocking relationships

2. **Intelligent Progress Tracking**
   - Analyze milestone completion patterns and predict timeline risks
   - Integrate with ProjectDataCollector for activity-based milestone validation
   - Use ProjectStatusAnalyzer for health scoring and trend analysis
   - Provide milestone-specific recommendations and action items

3. **Dependency Management**
   - Map milestone dependencies within and across projects
   - Identify critical path milestones that impact multiple projects
   - Detect milestone conflicts and resource allocation issues
   - Suggest optimal milestone sequencing and timing

4. **Smart Notifications & Alerts**
   - Identify milestones approaching deadline without activity
   - Detect milestone slippage patterns and cascade risks
   - Recommend proactive interventions and timeline adjustments

### Command Actions

**Default Milestone Overview `/project milestone`:**

Execute the following analysis:

1. **Load All Project Milestones**
   ```python
   from project_status_analyzer import ProjectStatusAnalyzer
   from project_planner import ProjectPlanner

   analyzer = ProjectStatusAnalyzer()
   planner = ProjectPlanner()

   # Get all projects and their milestones
   projects_config = analyzer.projects_config.get('projects', {})
   ```

2. **Milestone Status Analysis**
   ```python
   # Categorize milestones by status and urgency
   overdue_milestones = []
   upcoming_milestones = []
   at_risk_milestones = []
   completed_milestones = []

   for project_id, project_config in projects_config.items():
       milestones = project_config.get('milestones', [])
       # Analyze each milestone for status, risk, and dependencies
   ```

3. **Generate Intelligent Overview**

**Specific Project Analysis `/project milestone <project-name>`:**

1. **Deep Milestone Analysis**
   - Detailed timeline analysis for project milestones
   - Activity correlation with milestone progress
   - Resource allocation impact on milestone delivery
   - Dependency chain analysis

2. **Milestone Health Scoring**
   - Calculate milestone health based on activity, timeline, resources
   - Identify at-risk milestones before they become overdue
   - Provide specific recommendations for milestone recovery

**Milestone Updates `/project milestone --update <project-name> <milestone-name> <status>`:**

1. **Update Milestone Status**
   - Update milestone status in projects.yaml
   - Validate status transitions (planned → in_progress → completed)
   - Trigger dependency updates for dependent milestones
   - Log milestone change with timestamp

2. **Cascade Analysis**
   - Analyze impact on dependent milestones
   - Update project health scores
   - Recommend timeline adjustments for affected projects

### Output Format

#### Comprehensive Milestone Dashboard (Default)

```markdown
# 📅 Intelligent Milestone Dashboard
**Generated:** {timestamp}
**Total Active Milestones:** {total_count}
**Projects Analyzed:** {project_count}

## 🎯 Executive Summary
- **Overdue:** {overdue_count} milestones requiring immediate attention
- **At Risk:** {at_risk_count} milestones likely to slip without intervention
- **Upcoming (30 days):** {upcoming_count} milestones requiring preparation
- **On Track:** {on_track_count} milestones progressing well

## 🚨 Critical Actions Required

### Overdue Milestones (Immediate Action)
**{Milestone Name}** - {Project Name}
- **Due:** {due_date} ({days_overdue} days overdue)
- **Status:** {current_status}
- **Impact:** Blocking {dependent_count} other milestones
- **Owner:** {owner_email}
- **🔥 Priority Actions:**
  - {action_1}
  - {action_2}
- **Recovery Timeline:** {estimated_recovery_time}

**{Milestone Name 2}** - {Project Name 2}
[Similar format for other overdue milestones]

### At-Risk Milestones (Preventive Action)
**{Milestone Name}** - {Project Name}
- **Due:** {due_date} ({days_until_due} days remaining)
- **Risk Score:** {risk_score}/1.0 ({risk_category})
- **Risk Factors:**
  - {risk_factor_1}
  - {risk_factor_2}
- **Recommended Actions:**
  - {recommendation_1}
  - {recommendation_2}

## 📈 Upcoming Milestones (Next 30 Days)

### High Priority
| Date | Project | Milestone | Status | Owner | Dependencies |
|------|---------|-----------|--------|--------|--------------|
| {date} | {project} | {milestone} | {status} | {owner} | {dep_count} |
| {date} | {project} | {milestone} | {status} | {owner} | {dep_count} |

### Medium Priority
| Date | Project | Milestone | Status | Owner | Dependencies |
|------|---------|-----------|--------|--------|--------------|
| {date} | {project} | {milestone} | {status} | {owner} | {dep_count} |

## 🔗 Critical Path Analysis

### Cross-Project Dependencies
**{Milestone A}** ({Project 1}) → **{Milestone B}** ({Project 2}) → **{Milestone C}** ({Project 3})

**Critical Path Risks:**
- ⚠️ **{Risk}**: {description}
  - **Impact:** {impact_description}
  - **Mitigation:** {mitigation_strategy}

### Resource Conflicts
- **{Person}** assigned to {conflict_count} overlapping milestones
  - {milestone_1} ({project_1}) - Due: {date}
  - {milestone_2} ({project_2}) - Due: {date}
  - **Recommendation:** {resolution_strategy}

## 📊 Milestone Analytics

### Completion Velocity
- **This Month:** {completed_this_month}/{planned_this_month} milestones completed
- **Trend:** {trend_analysis} (vs. last month)
- **Average Delivery Time:** {avg_delivery_days} days per milestone

### Project Health by Milestones
- **{Project Name}**: {milestone_health_score}/1.0 ({completed}/{total} milestones)
- **{Project Name}**: {milestone_health_score}/1.0 ({completed}/{total} milestones)

## 💡 Strategic Recommendations

### Portfolio Optimization
1. **Milestone Sequencing**: {sequencing_recommendation}
2. **Resource Reallocation**: {resource_recommendation}
3. **Timeline Adjustment**: {timeline_recommendation}

### Process Improvements
1. **Early Warning System**: {early_warning_recommendation}
2. **Dependency Management**: {dependency_recommendation}
3. **Communication Protocol**: {communication_recommendation}
```

#### Project-Specific Milestone Analysis

```markdown
# 📅 Project Milestone Analysis: {Project Name}
**Generated:** {timestamp}
**Project Status:** {project_status} | **Health Score:** {health_score}/1.0

## 🎯 Milestone Overview
- **Total Milestones:** {total_count}
- **Completed:** {completed_count} | **In Progress:** {in_progress_count} | **Planned:** {planned_count}
- **Overdue:** {overdue_count} | **At Risk:** {at_risk_count}

## 📈 Milestone Timeline

### Completed Milestones ✅
**{Milestone Name}** - Completed {completion_date}
- **Original Due:** {original_due} ({variance} days {early/late})
- **Deliverables:** {deliverable_1}, {deliverable_2}
- **Impact on Project:** {impact_analysis}

### In Progress Milestones 🔄
**{Milestone Name}** - Due {due_date} ({days_remaining} days remaining)
- **Progress Indicators:**
  - GitHub Activity: {commits_count} commits, {pr_count} PRs in last week
  - Notes Activity: {notes_count} project notes, {action_items_count} action items
- **Risk Assessment:** {risk_level} risk of delay
- **Blocking Dependencies:** {dependency_count} activities waiting
- **Next Actions:**
  - {next_action_1}
  - {next_action_2}

### Planned Milestones 📋
**{Milestone Name}** - Planned for {due_date}
- **Prerequisites:** {prerequisite_1}, {prerequisite_2}
- **Resource Requirements:** {resource_requirements}
- **Preparation Status:** {preparation_percentage}% ready

## 🔗 Dependency Analysis

### Internal Dependencies (Within Project)
```
{Milestone A} → {Milestone B} → {Milestone C}
```

**Dependency Health:**
- ✅ {Milestone A}: Completed on time
- 🟡 {Milestone B}: Minor delay risk
- ⚪ {Milestone C}: Dependent on B completion

### External Dependencies (Cross-Project)
- **Waiting On:** {External Milestone} from {External Project}
  - **Status:** {external_status}
  - **Expected:** {external_expected_date}
  - **Risk:** {external_risk_assessment}

- **Blocking:** {Dependent Project} waiting on {Our Milestone}
  - **Their Dependency:** {their_milestone_name}
  - **Our Commitment:** {our_due_date}
  - **Impact if Delayed:** {delay_impact}

## ⚠️ Risk Analysis

### Milestone-Specific Risks
1. **{Milestone Name}**
   - **Risk:** {risk_description}
   - **Probability:** {probability} | **Impact:** {impact}
   - **Early Warning Signals:** {warning_signals}
   - **Mitigation Plan:** {mitigation_actions}

### Critical Path Risks
- **Bottleneck:** {bottleneck_milestone} could delay {affected_milestone_count} subsequent milestones
- **Resource Risk:** {resource_person} critical for {critical_milestone_count} milestones
- **Dependency Risk:** External dependency on {external_project} has {risk_level} risk

## 📊 Performance Metrics

### Milestone Delivery Performance
- **On-Time Delivery Rate:** {on_time_percentage}%
- **Average Delay:** {average_delay_days} days
- **Milestone Velocity:** {milestones_per_month} milestones/month

### Predictive Analysis
- **Projected Completion:** {projected_completion_date} (±{confidence_interval} days)
- **Risk-Adjusted Timeline:** {risk_adjusted_date}
- **Success Probability:** {success_probability}%

## 💡 Optimization Recommendations

### Immediate Actions (This Week)
1. **{High Priority Action}**: {action_description}
   - **Owner:** {action_owner}
   - **Deadline:** {action_deadline}
   - **Success Metric:** {success_metric}

### Process Improvements
1. **Milestone Granularity**: {granularity_recommendation}
2. **Checkpoint Frequency**: {checkpoint_recommendation}
3. **Dependency Communication**: {communication_recommendation}

### Resource Optimization
1. **Skill Gap:** {skill_gap_analysis}
2. **Capacity Planning:** {capacity_recommendation}
3. **Cross-Training:** {training_recommendation}
```

#### JSON Output Format (--json flag)

```json
{
  "dashboard_type": "milestone_overview",
  "generated_at": "2024-09-14T11:30:00Z",
  "summary": {
    "total_milestones": 15,
    "overdue": 3,
    "at_risk": 2,
    "upcoming_30_days": 5,
    "on_track": 5
  },
  "milestones": [
    {
      "name": "Content Creation",
      "project_name": "Q4 Marketing Campaign",
      "project_id": "q4-marketing-campaign",
      "due_date": "2024-10-31",
      "status": "in_progress",
      "days_until_due": 47,
      "days_overdue": 0,
      "owner": "sarah@company.com",
      "risk_score": 0.3,
      "risk_category": "low",
      "dependencies": [],
      "blocking": ["Launch Campaign"],
      "recent_activity": {
        "github_commits": 8,
        "notes_count": 2,
        "action_items": 3
      },
      "recommendations": [
        "Schedule design review meeting",
        "Coordinate with external design consultant"
      ]
    }
  ],
  "critical_path": [
    {
      "milestone": "Content Creation",
      "project": "Q4 Marketing Campaign",
      "dependent_milestones": 2
    }
  ],
  "resource_conflicts": [
    {
      "person": "sarah@company.com",
      "conflicting_milestones": 2,
      "severity": "medium",
      "recommendation": "Prioritize Q4 campaign milestone"
    }
  ],
  "analytics": {
    "completion_velocity": {
      "this_month": 4,
      "last_month": 3,
      "trend": "improving"
    },
    "average_delivery_time": 12.5
  }
}
```

### Implementation Steps

When executing this command:

1. **Initialize Analysis Systems**
   ```python
   from project_status_analyzer import ProjectStatusAnalyzer
   from project_planner import ProjectPlanner
   from project_data_collector import ProjectDataCollector

   analyzer = ProjectStatusAnalyzer()
   planner = ProjectPlanner()
   collector = ProjectDataCollector()
   ```

2. **Comprehensive Milestone Analysis**
   ```python
   # Load all project milestones
   all_milestones = []
   for project_id, project_config in projects_config.items():
       project_milestones = analyze_project_milestones(project_id, project_config)
       all_milestones.extend(project_milestones)

   # Categorize and analyze
   milestone_categories = categorize_milestones(all_milestones)
   dependency_analysis = analyze_milestone_dependencies(all_milestones)
   ```

3. **Smart Risk Assessment**
   ```python
   # Calculate risk scores for each milestone
   for milestone in all_milestones:
       milestone.risk_score = calculate_milestone_risk(milestone, project_data)
       milestone.recommendations = generate_milestone_recommendations(milestone)
   ```

4. **Generate Actionable Output**
   - Prioritize milestones by urgency and impact
   - Provide specific, actionable recommendations
   - Include timeline predictions and risk assessments
   - Suggest process improvements and optimizations

### Best Practices

1. **Milestone Granularity**:
   - Milestones should be 1-4 weeks apart for effective tracking
   - Each milestone should have clear, measurable deliverables
   - Avoid milestones that are too broad or too granular

2. **Dependency Management**:
   - Map all milestone dependencies explicitly
   - Communicate dependency changes promptly
   - Build buffer time for critical dependencies

3. **Progress Tracking**:
   - Update milestone status weekly minimum
   - Use multiple indicators (activity, deliverables, stakeholder feedback)
   - Identify early warning signals for milestone slippage

4. **Cross-Project Coordination**:
   - Maintain visibility into dependent projects
   - Coordinate milestone timing across project boundaries
   - Establish clear communication protocols for changes

Remember: Effective milestone management is about early detection and proactive intervention, not just status reporting.
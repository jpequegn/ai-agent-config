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
   - Use DataCollector tool for multi-source activity data (GitHub, notes, team)
   - Automatic 5-minute caching for performance optimization
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

1. **Load All Project Milestones with HealthCalculator**
   ```python
   from tools import ConfigManager, DataCollector, HealthCalculator

   config = ConfigManager()
   collector = DataCollector(config)
   calc = HealthCalculator()

   # Get all active projects and their milestones
   all_projects = config.get_all_projects(filters={"status": ["active", "in_progress"]})
   ```

2. **Milestone Status Analysis with HealthCalculator**
   ```python
   # Categorize milestones by status and urgency
   overdue_milestones = []
   upcoming_milestones = []
   at_risk_milestones = []
   completed_milestones = []

   for project_id, project_config in all_projects.items():
       # Collect activity data for milestone validation
       project_data = collector.aggregate_project_data(
           project_id=project_id,
           sources=["github", "notes", "config"]
       )

       milestones = project_config.get('milestones', [])

       # Calculate timeline progress using HealthCalculator
       timeline_progress = calc.calculate_timeline_progress(
           milestones=milestones,
           start_date=project_config.get('start_date'),
           target_date=project_config.get('target_date')
       )

       # Calculate project health with timeline component
       project_health_data = {
           "milestones": milestones,
           "github_data": project_data.github_data.__dict__ if project_data.github_data else {},
           "blockers": project_config.get('blockers', []),
           "dependencies": project_config.get('dependencies', []),
           "start_date": project_config.get('start_date'),
           "target_date": project_config.get('target_date'),
       }
       health = calc.calculate_project_health(project_health_data)

       # Assess timeline-specific risks
       risks = calc.assess_risks(project_health_data)
       timeline_risks = [r for r in risks if r.category == "timeline"]

       # Predict milestone completion
       if timeline_progress["total_count"] > timeline_progress["completed_count"]:
           prediction = calc.predict_completion(
               current_progress=timeline_progress["percent_complete"] / 100,
               velocity=project_config.get("velocity", 1.0),
               remaining_work=timeline_progress["total_count"] - timeline_progress["completed_count"]
           )
       else:
           prediction = None

       # Enrich each milestone with HealthCalculator metrics
       for milestone in milestones:
           milestone['timeline_progress'] = timeline_progress
           milestone['health_score'] = health
           milestone['timeline_component'] = health.components.get('timeline')
           milestone['risks'] = timeline_risks
           milestone['completion_prediction'] = prediction
   ```

3. **Generate Intelligent Overview with HealthCalculator Insights**

**Specific Project Analysis `/project milestone <project-name>`:**

1. **Deep Milestone Analysis with HealthCalculator**
   ```python
   # Get specific project
   project = config.get_project(project_name)

   # Collect comprehensive data
   project_data = collector.aggregate_project_data(
       project_id=project_name,
       sources=["github", "notes", "config"]
   )

   # Calculate detailed timeline progress
   timeline_progress = calc.calculate_timeline_progress(
       milestones=project.get('milestones', []),
       start_date=project.get('start_date'),
       target_date=project.get('target_date')
   )

   # Get comprehensive health score
   health_data = {
       "milestones": project.get('milestones', []),
       "github_data": project_data.github_data.__dict__ if project_data.github_data else {},
       "blockers": project.get('blockers', []),
       "dependencies": project.get('dependencies', []),
       "start_date": project.get('start_date'),
       "target_date": project.get('target_date'),
   }
   health = calc.calculate_project_health(health_data)

   # Assess all risks with mitigation suggestions
   risks = calc.assess_risks(health_data)
   timeline_risks = [r for r in risks if r.category == "timeline"]

   # Predict completion for each remaining milestone
   for milestone in project.get('milestones', []):
       if milestone.get('status') != 'completed':
           milestone_prediction = calc.predict_completion(
               current_progress=timeline_progress["percent_complete"] / 100,
               velocity=project.get("velocity", 1.0),
               remaining_work=1  # Each milestone as unit of work
           )
           milestone['prediction'] = milestone_prediction
   ```

2. **Milestone Health Scoring with Timeline Component**
   ```python
   # Extract timeline component details
   timeline_component = health.components.get('timeline')

   # Display timeline health metrics
   print(f"Timeline Health Score: {timeline_component.score:.2f}")
   print(f"Weight in Overall Health: {timeline_component.weight}")
   print(f"Weighted Contribution: {timeline_component.weighted_score:.2f}")
   print(f"Progress Ratio: {timeline_progress['progress_ratio']:.2f}")
   print(f"On Track: {timeline_progress['on_track']}")

   # Identify at-risk milestones using risk assessment
   for risk in timeline_risks:
       print(f"Risk: {risk.title}")
       print(f"Severity: {risk.severity.value}")
       print(f"Mitigation: {', '.join(risk.mitigation_suggestions)}")
   ```

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

**Portfolio Timeline Metrics (HealthCalculator):**
- **Overall Progress:** {portfolio_percent_complete}% ({completed_milestones}/{total_milestones} milestones)
- **Progress Ratio:** {portfolio_progress_ratio:.2f} (1.0 = on schedule)
- **Average Timeline Health:** {avg_timeline_score:.2f}/1.0
- **Projects On Track:** {on_track_projects}/{total_projects}

## 🚨 Critical Actions Required

### Overdue Milestones (Immediate Action)
**{Milestone Name}** - {Project Name}
- **Due:** {due_date} ({days_overdue} days overdue)
- **Status:** {current_status}
- **Timeline Health:** {timeline_score:.2f}/1.0 (Progress Ratio: {progress_ratio:.2f})
- **Impact:** Blocking {dependent_count} other milestones
- **Owner:** {owner_email}
- **Risk Level:** {risk_severity} ({risk_likelihood} likelihood)
- **🔥 Priority Actions:**
  - {action_1}
  - {action_2}
- **Recovery Timeline:** {estimated_recovery_time}
- **Predicted Completion:** {prediction_eta} (Confidence: {prediction_confidence:.0%})

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

**Timeline Metrics (HealthCalculator):**
- **Progress:** {percent_complete:.0f}% ({completed_count}/{total_count} milestones)
- **Progress Ratio:** {progress_ratio:.2f} (1.0 = on schedule, <0.95 = behind)
- **On Track Status:** {on_track_status}
- **Timeline Health Score:** {timeline_score:.2f}/1.0 (Weight: {timeline_weight})
- **Predicted Completion:** {predicted_completion_date} (Risk: {completion_risk})

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

## ⚠️ Risk Analysis (HealthCalculator)

### Timeline-Specific Risks
**Identified by HealthCalculator.assess_risks():**

1. **{Risk Title}** - {Risk Category}
   - **Severity:** {severity.value} | **Likelihood:** {likelihood.value}
   - **Priority Score:** {priority_score:.2f}
   - **Impact Areas:** {affected_areas}
   - **Description:** {risk_description}
   - **Mitigation Suggestions:**
     - {mitigation_1}
     - {mitigation_2}
     - {mitigation_3}

### Milestone-Specific Risks
1. **{Milestone Name}**
   - **Timeline Risk Score:** {timeline_risk_score:.2f}
   - **Progress Ratio:** {progress_ratio:.2f} (Behind schedule if <0.95)
   - **Days Until Due:** {days_until_due}
   - **Early Warning Signals:**
     - Low activity score: {activity_score:.2f}
     - High blocker count: {blocker_count}
   - **Recommended Actions:**
     - {action_from_healthcalculator_1}
     - {action_from_healthcalculator_2}

### Critical Path Risks
- **Bottleneck:** {bottleneck_milestone} could delay {affected_milestone_count} subsequent milestones
- **Resource Risk:** {resource_person} critical for {critical_milestone_count} milestones
- **Dependency Risk:** External dependency on {external_project} has {risk_level} risk

## 📊 Performance Metrics

### Milestone Delivery Performance
- **On-Time Delivery Rate:** {on_time_percentage}%
- **Average Delay:** {average_delay_days} days
- **Milestone Velocity:** {milestones_per_month} milestones/month

### HealthCalculator Predictions
**Using HealthCalculator.predict_completion():**

- **Estimated Completion:** {estimated_completion_date}
- **Estimated Days Remaining:** {estimated_days:.0f} days
- **Confidence Level:** {confidence:.0%}
- **Risk Level:** {risk_level} (low/medium/high)
- **Current Velocity:** {current_velocity:.2f} milestones/week
- **Remaining Work:** {remaining_work} milestones

### Timeline Health Analysis
- **Timeline Component Score:** {timeline_score:.2f}/1.0
- **Progress Ratio:** {progress_ratio:.2f} (1.0 = perfect pace)
- **On Track Status:** {"✅ Yes" if on_track else "⚠️ No"}
- **Completion Percentage:** {percent_complete:.0f}%

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

1. **Initialize Data Collection with HealthCalculator**
   ```python
   from tools import DataCollector, ConfigManager, HealthCalculator

   config = ConfigManager()
   collector = DataCollector(config)
   calc = HealthCalculator()
   ```

2. **Collect Project Data and Analyze Milestones with HealthCalculator**
   ```python
   # Get all active projects
   all_projects = config.get_all_projects(filters={"status": ["active", "in_progress"]})

   # Collect data for milestone analysis
   all_milestones = []
   for project_id, project_config in all_projects.items():
       # Collect multi-source data for activity validation
       project_data = collector.aggregate_project_data(
           project_id=project_id,
           sources=["github", "notes", "config"]
       )

       # Calculate timeline progress using HealthCalculator
       timeline_progress = calc.calculate_timeline_progress(
           milestones=project_config.get('milestones', []),
           start_date=project_config.get('start_date'),
           target_date=project_config.get('target_date')
       )

       # Calculate project health with timeline component
       health_data = {
           "milestones": project_config.get('milestones', []),
           "github_data": project_data.github_data.__dict__ if project_data.github_data else {},
           "blockers": project_config.get('blockers', []),
           "dependencies": project_config.get('dependencies', []),
           "start_date": project_config.get('start_date'),
           "target_date": project_config.get('target_date'),
       }
       health = calc.calculate_project_health(health_data)

       # Assess timeline risks
       risks = calc.assess_risks(health_data)
       timeline_risks = [r for r in risks if r.category == "timeline"]

       # Predict completion for remaining milestones
       if timeline_progress["total_count"] > timeline_progress["completed_count"]:
           prediction = calc.predict_completion(
               current_progress=timeline_progress["percent_complete"] / 100,
               velocity=project_config.get("velocity", 1.0),
               remaining_work=timeline_progress["total_count"] - timeline_progress["completed_count"]
           )
       else:
           prediction = None

       # Extract and enrich milestone information
       milestones = project_config.get('milestones', [])
       for milestone in milestones:
           # Enrich with activity data
           milestone['github_activity'] = {
               'commits': len(project_data.github_data.commits or []),
               'prs': len(project_data.github_data.pull_requests or []),
               'issues': len(project_data.github_data.issues or [])
           }
           milestone['notes_activity'] = {
               'count': len(project_data.notes_data.project_notes or []),
               'action_items': len(project_data.notes_data.action_items or [])
           }
           # Add HealthCalculator metrics
           milestone['timeline_progress'] = timeline_progress
           milestone['timeline_health'] = health.components.get('timeline')
           milestone['project_health'] = health
           milestone['timeline_risks'] = timeline_risks
           milestone['completion_prediction'] = prediction
           milestone['project_id'] = project_id
           milestone['project_name'] = project_config.get('name', project_id)

       all_milestones.extend(milestones)

   # Categorize and analyze
   milestone_categories = categorize_milestones(all_milestones)
   dependency_analysis = analyze_milestone_dependencies(all_milestones)
   ```

3. **Smart Risk Assessment with HealthCalculator**
   ```python
   # HealthCalculator provides automatic risk scoring and mitigation
   for milestone in all_milestones:
       # Timeline risks already calculated per project
       timeline_risks = milestone.get('timeline_risks', [])

       # Extract risk details
       for risk in timeline_risks:
           print(f"Risk: {risk.title}")
           print(f"Severity: {risk.severity.value}")
           print(f"Priority: {risk.priority_score:.2f}")
           print(f"Mitigation: {risk.mitigation_suggestions}")

       # Use timeline health for risk categorization
       timeline_health = milestone.get('timeline_health')
       if timeline_health and timeline_health.score < 0.6:
           milestone['risk_category'] = 'high'
       elif timeline_health and timeline_health.score < 0.8:
           milestone['risk_category'] = 'medium'
       else:
           milestone['risk_category'] = 'low'
   ```

4. **Generate Actionable Output**
   - Prioritize milestones by urgency and impact
   - Provide specific, actionable recommendations
   - Include timeline predictions and risk assessments
   - Suggest process improvements and optimizations

### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache reduces repeated API/CLI calls (2-5s improvement)
- **Retry Logic**: Automatic retry with exponential backoff (3 attempts)
- **Graceful Degradation**: Continues with partial data when sources unavailable
- **Type Safety**: Pydantic models ensure data consistency

**HealthCalculator Benefits:**
- **Timeline Progress**: Precise progress ratio and on-track calculations (<10ms)
- **Predictive**: Completion ETAs with confidence and risk levels
- **Risk Assessment**: Automatic timeline risk detection with mitigation suggestions
- **Health Scoring**: Timeline component scoring (0.0-1.0 scale)
- **Performance**: <50ms for all calculations
- **Type Safety**: Pydantic models for all data structures

**Error Scenarios:**
- If GitHub data unavailable → Use notes and config data only
- If notes CLI fails → Use GitHub and config data only
- If no activity data available → Base analysis on milestone dates and status
- If milestone dates missing → HealthCalculator uses defaults for calculations
- Always provide milestone overview even with partial data

### Benefits of HealthCalculator Integration

✅ **Accurate Progress Tracking**: Precise progress ratio calculations
- Progress ratio: actual vs. expected completion
- On-track determination (within 5% threshold)
- Percentage complete with date-based projections

✅ **Predictive Intelligence**: Forward-looking completion estimates
- Estimated completion dates with confidence intervals
- Risk level assessment (low/medium/high)
- Velocity-based predictions for remaining work

✅ **Risk Awareness**: Automatic timeline risk detection
- Timeline delay risks with severity levels
- Impact scoring and priority calculation
- Built-in mitigation suggestions for each risk

✅ **Consistency**: Same calculation logic across commands
- Timeline scoring methodology standardized
- Health component weights configurable
- Reproducible, deterministic results

✅ **Simplified Implementation**: Replace manual calculations
- Timeline progress: 1 method call vs 20+ lines
- Risk assessment: Automatic vs manual logic
- Consistent API across all project commands

### Integration Notes

- **Performance**: Caching improves response time from ~5s to <1s for cached queries
- **HealthCalculator**: <50ms for timeline calculations, <100ms for comprehensive health
- **Reliability**: Built-in error handling eliminates manual subprocess error management
- **Consistency**: Same data models used across all project commands
- **Maintainability**: Centralized data collection and health scoring in tested tools (87% coverage)

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
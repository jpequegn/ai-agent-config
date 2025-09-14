---
name: project-sync
description: Multi-project synchronization with cross-project conflict detection and resolution
---

# /project sync - Multi-Project Synchronization

Automatically sync project data across tools and identify cross-project impacts, resource conflicts, and dependency issues.

## Usage Examples:
- `/project sync` - Sync all projects and analyze conflicts
- `/project sync <project-name>` - Sync specific project and check cross-project impacts
- `/project sync --analyze-conflicts` - Full sync with detailed conflict analysis
- `/project sync mobile-app-v2 --conflicts` - Sync specific project with impact analysis

## Instructions:

You are an intelligent multi-project synchronization system. When this command is invoked, you will:

### Core Functionality

1. **Data Source Integration**
   - Integrate with ProjectDataCollector for GitHub, calendar, and notes data
   - Leverage ProjectStatusAnalyzer for health scoring and trend analysis
   - Coordinate with ProjectPlanner for resource conflict detection
   - Maintain data freshness across all project sources

2. **Cross-Project Analysis**
   - Detect resource allocation conflicts across multiple projects
   - Identify dependency chains and blocking relationships
   - Analyze timeline overlaps and resource bottlenecks
   - Track milestone dependencies and impacts

3. **Intelligent Conflict Detection**
   - Resource over-allocation (same person on multiple projects)
   - Timeline conflicts and scheduling overlaps
   - Dependency chain issues (blocked projects blocking others)
   - Critical path conflicts affecting multiple projects

4. **Automated Status Updates**
   - Update project status based on activity data from sources
   - Sync milestone completion from GitHub milestones
   - Detect project health changes and suggest status updates
   - Maintain consistency across project configuration

### Command Actions

**Full Project Sync `/project sync`:**

Execute comprehensive synchronization:

1. **Initialize Synchronization System**
   ```python
   from project_synchronizer import ProjectSynchronizer

   synchronizer = ProjectSynchronizer()
   ```

2. **Execute Full Sync with Analysis**
   ```python
   # Sync all projects with conflict analysis
   result = synchronizer.sync_all_projects(analyze_conflicts=True)

   # Generate human-readable report
   report = synchronizer.generate_sync_report(result)
   ```

3. **Present Comprehensive Sync Results**

**Specific Project Sync `/project sync <project-name>`:**

Execute targeted synchronization with cross-project impact analysis:

1. **Target-Specific Sync**
   ```python
   # Sync specific project with cross-project impact analysis
   result = synchronizer.sync_project(project_name, analyze_conflicts=True)
   ```

2. **Cross-Project Impact Assessment**
   - Analyze how changes to target project affect other projects
   - Identify resource conflicts caused by target project updates
   - Check dependency impacts on downstream projects
   - Generate targeted recommendations

### Output Format

#### Comprehensive Sync Report (Default)

```markdown
# 🔄 Project Synchronization Report
**Generated:** {timestamp}
**Projects Synced:** {project_count}

## 📊 Executive Summary
- **Projects Updated:** {updated_count}
- **Resource Conflicts:** {conflicts_count}
- **Dependency Issues:** {dependency_count}
- **Status Changes:** {status_updates_count}

## 📥 Data Updates
- ✅ GitHub data refreshed
- ✅ Calendar data refreshed
- ✅ Notes data refreshed

## 🔄 Status Updates

**{Project Name}:**
- milestone_{milestone_name}: marked as completed from GitHub
- status_suggestion: active (Health metrics show recovery)

**{Project Name 2}:**
- milestone_{milestone_name}: updated based on calendar events
- activity_level: increased (Recent commits detected)

## ⚠️ Resource Conflicts

🔴 **{person@company.com}** - time_overlap
  - **Projects:** Q4 Marketing Campaign, Mobile App V2
  - **Period:** 2024-11
  - **Issue:** sarah@company.com is allocated to 2 projects in 2024-11
  - **Suggestions:**
    - Stagger project timelines to reduce workload
    - Consider reassigning ownership of one project

🟡 **{person@company.com}** - over_allocation
  - **Projects:** Infrastructure Upgrade, Security Audit
  - **Period:** 2024-10
  - **Issue:** john@company.com at 120% capacity in October
  - **Suggestions:**
    - Bring in additional DevOps resources
    - Extend infrastructure timeline by 2 weeks

## 🔗 Dependency Issues

🚨 **Mobile App V2** ← **Design System Update**
  - **Issue:** Mobile App V2 depends on Design System Update which is blocked
  - **Type:** blocked
  - **Suggestions:**
    - Unblock Design System Update to enable Mobile App V2 progress
    - Find alternative solution that doesn't depend on Design System

⚠️ **Q4 Marketing** ← **Budget Approval**
  - **Issue:** Q4 Marketing depends on Budget Approval which is delayed
  - **Type:** delayed
  - **Suggestions:**
    - Fast-track budget approval process
    - Prepare contingency plan with reduced budget scope

## 💡 Recommendations

🔴 **2 high-priority resource conflicts detected**
  Multiple projects are competing for the same resources
  **Action Items:**
  - Review project timelines and consider staggering overlapping projects
  - Identify opportunities to bring in additional resources
  - Reassign project ownership where feasible
  **Affected Projects:** Q4 Marketing Campaign, Mobile App V2, Infrastructure Upgrade

🟡 **3 projects have status updates**
  Project status has changed based on recent activity
  **Action Items:**
  - Review updated project statuses
  - Update stakeholder communications
  - Adjust resource allocation based on status changes
  **Affected Projects:** Mobile App V2, Q4 Marketing, Infrastructure Upgrade

## 📈 Next Steps
1. **Immediate Actions (This Week)**
   - Resolve critical resource conflict for {person} between {project1} and {project2}
   - Unblock {dependency} to enable {dependent_project} progress
   - Update stakeholders on {project} status changes

2. **Strategic Planning (Next 2 Weeks)**
   - Review overall resource allocation strategy
   - Consider bringing in contractor support for {skill_area}
   - Reassess project timeline dependencies

3. **Process Improvements**
   - Set up automated sync schedule (daily/weekly)
   - Implement early warning system for resource conflicts
   - Establish clearer dependency communication protocols
```

#### Targeted Project Sync Report

```markdown
# 🔄 Project Sync: {Project Name}
**Generated:** {timestamp}
**Target Project:** {project_name}
**Cross-Project Impacts:** {impact_count}

## 🎯 Project Updates
- **Status:** Updated from {old_status} to {new_status}
- **Milestones:** {completed_count} completed, {at_risk_count} at risk
- **Activity Level:** {activity_trend} (based on GitHub activity)
- **Health Score:** {health_score}/1.0 ({health_category})

## 📊 Data Synchronization
- **GitHub:** {commits_count} new commits, {issues_count} issues updated
- **Calendar:** {events_count} project events, {meetings_count} meetings
- **Notes:** {notes_count} project notes analyzed

## 🌊 Cross-Project Impact Analysis

### Resource Impact
- **{Owner}**: Now allocated to {allocation}% across {project_count} projects
- **Timeline Conflict**: Overlaps with {conflicting_project} in {time_period}
- **Capacity Assessment**: {capacity_status} for {time_period}

### Dependency Impact
- **Blocking Projects:** {project} waiting on {milestone}
- **Dependent On:** {dependency_project} milestone {dependency_name}
- **Critical Path:** Changes affect {affected_project_count} downstream projects

### Resource Recommendations
- **Immediate:** {immediate_action}
- **Strategic:** {strategic_recommendation}
- **Timeline:** {timeline_adjustment_recommendation}
```

#### JSON Output Format (--json flag)

```json
{
  "timestamp": "2024-09-14T12:00:00Z",
  "projects_synced": ["q4-marketing-campaign", "mobile-app-v2"],
  "data_sources_updated": ["github", "calendar", "notes"],
  "conflicts_detected": [
    {
      "resource": "sarah@company.com",
      "conflict_type": "time_overlap",
      "projects": ["q4-marketing-campaign", "mobile-app-v2"],
      "time_period": "2024-11",
      "severity": "high",
      "description": "sarah@company.com is allocated to 2 projects in 2024-11",
      "resolution_suggestions": [
        "Stagger project timelines to reduce workload",
        "Consider reassigning ownership of one project"
      ]
    }
  ],
  "dependency_issues": [
    {
      "dependent_project": "mobile-app-v2",
      "blocking_project": "design-system-update",
      "dependency_name": "design-system-update",
      "issue_type": "blocked",
      "impact": "high",
      "description": "mobile-app-v2 depends on design-system-update which is blocked",
      "resolution_suggestions": [
        "Unblock design-system-update to enable mobile-app-v2 progress"
      ]
    }
  ],
  "status_updates": [
    {
      "project": "mobile-app-v2",
      "updates": {
        "milestone_User Research Complete": "marked as completed from GitHub",
        "status_suggestion": "active",
        "reason": "Health metrics show recovery"
      },
      "timestamp": "2024-09-14T12:00:00Z"
    }
  ],
  "recommendations": [
    {
      "type": "resource_conflict",
      "priority": "high",
      "title": "2 high-priority resource conflicts detected",
      "description": "Multiple projects are competing for the same resources",
      "action_items": [
        "Review project timelines and consider staggering overlapping projects",
        "Identify opportunities to bring in additional resources"
      ],
      "affected_projects": ["q4-marketing-campaign", "mobile-app-v2"]
    }
  ],
  "summary": {
    "projects_count": 2,
    "conflicts_count": 1,
    "dependency_issues_count": 1,
    "status_updates_count": 1,
    "data_freshness": "2024-09-14T12:00:00Z"
  }
}
```

### Implementation Steps

When executing this command:

1. **Initialize Multi-Project Synchronization**
   ```python
   from project_synchronizer import ProjectSynchronizer

   synchronizer = ProjectSynchronizer()
   ```

2. **Execute Appropriate Sync Strategy**
   ```python
   if specific_project:
       result = synchronizer.sync_project(project_name, analyze_conflicts=True)
   else:
       result = synchronizer.sync_all_projects(analyze_conflicts=True)
   ```

3. **Generate Comprehensive Analysis**
   ```python
   # Cross-project conflict detection
   conflicts = synchronizer._detect_resource_conflicts(project_data)

   # Dependency analysis
   dependency_issues = synchronizer._analyze_cross_project_dependencies(project_data)

   # Status updates based on fresh data
   status_updates = synchronizer._update_project_status(...)
   ```

4. **Present Actionable Intelligence**
   - Prioritize conflicts by severity and impact
   - Provide specific resolution suggestions
   - Include timeline and resource recommendations
   - Generate next steps with clear ownership

### Integration with Existing Systems

**ProjectDataCollector Integration:**
- Leverage existing GitHub, calendar, and notes connectors
- Use cached data for performance optimization
- Maintain data freshness timestamps

**ProjectStatusAnalyzer Integration:**
- Use health scoring for status update recommendations
- Leverage trend analysis for conflict prediction
- Integrate risk assessment into recommendations

**ProjectPlanner Integration:**
- Cross-reference resource requirements with allocations
- Use dependency analysis for conflict detection
- Leverage timeline planning for overlap detection

### Error Handling

- **Data Source Unavailable**: Use cached data with staleness warnings
- **Project Not Found**: Provide clear error message with available projects
- **Configuration Errors**: Validate project configuration and suggest fixes
- **API Failures**: Graceful degradation with partial sync results

### Best Practices

1. **Regular Sync Cadence**:
   - Daily sync for active projects
   - Weekly comprehensive analysis
   - On-demand sync for critical changes

2. **Conflict Resolution Priority**:
   - Address critical resource conflicts first
   - Resolve blocking dependencies before timeline issues
   - Focus on high-impact, low-effort solutions

3. **Communication Integration**:
   - Generate stakeholder-ready status updates
   - Include actionable recommendations in reports
   - Provide clear next steps with ownership

4. **Data Quality**:
   - Validate data consistency across sources
   - Flag stale or missing data
   - Maintain audit trail of sync operations

Remember: Effective project synchronization enables proactive conflict resolution and strategic resource optimization across your entire project portfolio.
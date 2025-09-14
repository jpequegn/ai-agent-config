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
   - Use the ProjectDataCollector system (`./project_data_collector.py`) to gather data from:
     - GitHub API (PRs, issues, commits, milestones)
     - Notes system (project-related notes and action items)
     - Calendar integration (meetings, deadlines)
   - Synthesize data from `.claude/projects.yaml` configuration
   - Integrate with `.claude/integrations.yaml` for API access

2. **Intelligent Health Scoring**
   - Calculate project health score (0.0-1.0) based on:
     - **Timeline Progress** (0.3 weight): Milestone completion vs. elapsed time
     - **Activity Level** (0.25 weight): Recent GitHub commits, PRs, issue updates
     - **Blocker Status** (0.25 weight): Number and severity of blockers
     - **Dependency Health** (0.2 weight): Status of dependent projects
   - Health Categories:
     - 0.8-1.0: 🟢 Excellent (on track, active, minimal blockers)
     - 0.6-0.8: 🟡 Good (minor issues, manageable risks)
     - 0.4-0.6: 🟠 At Risk (significant concerns, needs attention)
     - 0.0-0.4: 🔴 Critical (major blockers, high risk of failure)

3. **Trend Analysis**
   - **Velocity Trends**: Compare recent activity vs. historical average
     - Increasing: Recent commits/PRs > 120% of average
     - Stable: Recent activity within 80-120% of average
     - Decreasing: Recent activity < 80% of average
   - **Risk Trends**: Track risk factors over time
     - Improving: Blockers resolved, milestones met
     - Stable: Consistent progress, predictable patterns
     - Declining: New blockers, missed milestones, reduced activity

4. **Blocker and Risk Identification**
   - **Automated Blocker Detection**:
     - Dependencies on incomplete projects
     - Overdue milestones
     - Stale GitHub repositories (no commits > 7 days)
     - Open high-priority issues
     - Missing environment variables for integrations
   - **Risk Assessment**:
     - Schedule Risk: Target date vs. remaining milestones
     - Resource Risk: Owner workload across projects
     - Technical Risk: High number of open bugs/issues
     - Dependency Risk: Blocking other projects

### Command Actions

**Default `/project status`:**
Execute the following steps:

1. Use ProjectDataCollector to gather data for all projects
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

#### Human-Readable Format (Default)

```markdown
# 📊 Intelligent Project Status Analysis
**Generated:** {timestamp}
**Data Sources:** GitHub ✅ | Notes ✅ | Calendar ⚠️

## 🎯 Executive Summary
- **Total Projects:** {count}
- **Health Distribution:** {excellent_count}🟢 {good_count}🟡 {risk_count}🟠 {critical_count}🔴
- **Critical Actions Needed:** {critical_count}
- **Overall Portfolio Health:** {portfolio_score}/1.0

## 📈 Project Analysis

### 🔴 Critical Projects (Immediate Action Required)
**{Project Name}** (Health: {score}/1.0)
- **Status:** {status} | **Owner:** {owner} | **Priority:** {priority}
- **Progress:** {completion}% ({completed_milestones}/{total_milestones} milestones)
- **Target Date:** {target_date} ({days_remaining} days remaining)
- **🚨 Critical Issues:**
  - {blocker_1}
  - {blocker_2}
- **💡 Immediate Actions:**
  - {action_1}
  - {action_2}
- **📊 Recent Activity:** {github_summary}
- **📈 Trend:** {trend_analysis}

### 🟡 Projects Needing Attention
[Similar format for at-risk projects]

### 🟢 Projects On Track
**{Project Name}** | Health: {score}/1.0 | Progress: {completion}%
**{Project Name}** | Health: {score}/1.0 | Progress: {completion}%

## 🎯 Key Insights & Recommendations

### 📊 Portfolio Health Trends
- **Velocity Trend:** {increasing/stable/decreasing}
- **Risk Trend:** {improving/stable/declining}
- **Resource Utilization:** {owner_workload_analysis}

### 💡 Strategic Recommendations
1. **Immediate (This Week):**
   - {high_priority_action_1}
   - {high_priority_action_2}

2. **Short-term (Next 2 Weeks):**
   - {medium_priority_action_1}
   - {medium_priority_action_2}

3. **Long-term (Next Month):**
   - {strategic_action_1}
   - {strategic_action_2}

### 🔍 Detected Patterns
- {insight_1}
- {insight_2}
- {insight_3}
```

#### JSON Output Format (--json flag)

```json
{
  "status": "success",
  "command": "/project status",
  "generated_at": "2024-09-14T10:30:00Z",
  "data_sources": {
    "github": {"status": "connected", "last_updated": "2024-09-14T10:29:45Z"},
    "notes": {"status": "available", "last_updated": "2024-09-14T10:29:50Z"},
    "calendar": {"status": "disconnected", "message": "API key not configured"}
  },
  "summary": {
    "total_projects": 3,
    "health_distribution": {
      "excellent": 1,
      "good": 1,
      "at_risk": 1,
      "critical": 0
    },
    "portfolio_health_score": 0.73,
    "critical_actions_needed": 2
  },
  "projects": [
    {
      "name": "Q4 Marketing Campaign",
      "id": "q4-marketing-campaign",
      "health_score": 0.65,
      "health_category": "good",
      "completion_percentage": 60,
      "status": "in_progress",
      "priority": "high",
      "owner": "sarah@company.com",
      "target_date": "2024-12-31",
      "days_remaining": 108,
      "milestones": {
        "completed": 1,
        "total": 4,
        "next": {
          "name": "Content Creation",
          "date": "2024-10-31",
          "days_until": 47
        }
      },
      "blockers": [
        {
          "type": "dependency",
          "description": "Waiting on budget-approval decision",
          "severity": "medium",
          "days_blocked": 5
        }
      ],
      "recent_activity": {
        "github": {
          "commits_last_week": 8,
          "prs_last_week": 3,
          "open_issues": 2
        },
        "notes": {
          "recent_notes": 2,
          "action_items_open": 3
        }
      },
      "trends": {
        "velocity": "stable",
        "risk_level": "medium",
        "activity_trend": "increasing"
      },
      "recommendations": [
        {
          "priority": "high",
          "action": "Follow up on budget approval decision",
          "impact": "Unblocks content creation milestone"
        }
      ]
    }
  ],
  "insights": {
    "portfolio_trends": {
      "velocity_trend": "stable",
      "risk_trend": "stable",
      "resource_utilization": "balanced"
    },
    "recommendations": {
      "immediate": [
        "Follow up on budget approval for Q4 Marketing Campaign",
        "Review user research completion for Mobile App V2"
      ],
      "short_term": [
        "Schedule architecture review for Mobile App V2",
        "Plan infrastructure upgrade rollout"
      ],
      "long_term": [
        "Consider resource reallocation based on project priorities",
        "Implement automated project health monitoring"
      ]
    },
    "patterns": [
      "Projects with external dependencies have higher risk scores",
      "GitHub activity correlates strongly with milestone completion",
      "Projects without recent notes activity tend to stall"
    ]
  }
}
```

### Implementation Steps

When executing this command:

1. **Initialize Data Collection**
   ```python
   from project_data_collector import ProjectDataCollector
   collector = ProjectDataCollector()
   ```

2. **Collect Project Data**
   ```python
   if project_name:
       project_data = collector.collect_project_data(project_name)
   else:
       project_data = collector.collect_all_projects_data()
   ```

3. **Calculate Health Scores**
   - Timeline Progress: (completed_milestones / total_milestones) * (days_elapsed / total_days)
   - Activity Level: Normalize recent GitHub activity (commits, PRs, issues)
   - Blocker Impact: Penalize based on number and severity of blockers
   - Dependency Health: Factor in dependency project health scores

4. **Perform Trend Analysis**
   - Compare recent activity vs. 30-day rolling average
   - Analyze milestone completion velocity
   - Track blocker resolution rate

5. **Generate Insights**
   - Identify common patterns across projects
   - Suggest optimization opportunities
   - Highlight resource allocation issues

6. **Format Output**
   - Default: Human-readable markdown with actionable insights
   - --json flag: Structured JSON for programmatic use
   - Focus modes: Emphasized analysis on specific areas

### Error Handling

- Handle missing project configurations gracefully
- Provide meaningful errors for API connection failures
- Suggest setup steps for missing integrations
- Offer degraded functionality when data sources are unavailable

### Best Practices

- Always provide actionable recommendations
- Focus on business impact, not just technical metrics
- Highlight the most critical issues first
- Include confidence levels for predictions
- Suggest specific next steps with owners and timelines

Remember: This command should be your go-to tool for project management decision-making. Always prioritize actionable insights over data dumps.
---
name: team-sync
description: Synchronize team data with projects, meetings, and organizational systems
---

# Team Data Synchronization

Comprehensive integration system that synchronizes team member information with project assignments, meeting schedules, and organizational data for unified team management.

## Usage Examples:
- `/cc team-sync` - Full synchronization of all team data sources
- `/cc team-sync --projects` - Sync team assignments with project data
- `/cc team-sync --meetings` - Integrate team data with meeting schedules
- `/cc team-sync --validate` - Validate data consistency across systems
- `/cc team-sync --report` - Generate synchronization status report
- `/cc team-sync --conflicts` - Identify and resolve data conflicts
- `/cc team-sync [email]` - Sync specific team member's data

## Instructions:

You are a comprehensive team data synchronization system. When this command is invoked:

### Core Functionality

1. **Load Integration Sources**
   - Read team data from `.claude/team_roster.yaml`
   - Load project assignments from `.claude/projects.yaml`
   - Access meeting data and schedules
   - Check integration settings from `.claude/integrations.yaml`

2. **Data Synchronization**
   - Synchronize team member project assignments
   - Update workload and capacity information
   - Integrate meeting participation and schedules
   - Validate data consistency across sources

3. **Command Actions**

   **Default `/cc team-sync`:**
   - Perform comprehensive data synchronization
   - Update all team member project assignments
   - Refresh meeting schedules and participation
   - Generate synchronization summary report
   - Identify and flag data inconsistencies

   **Project Sync `--projects`:**
   - Synchronize team assignments with project data
   - Update project ownership and participation
   - Calculate team workload and capacity
   - Identify unassigned projects or team members
   - Generate project-team alignment report

   **Meeting Sync `--meetings`:**
   - Integrate team member meeting schedules
   - Update recurring meeting participation
   - Calculate meeting load and availability
   - Identify scheduling conflicts or gaps
   - Generate meeting participation analysis

   **Data Validation `--validate`:**
   - Check data consistency across all sources
   - Identify missing or conflicting information
   - Validate email addresses and references
   - Flag potential data quality issues
   - Generate data health report

   **Sync Report `--report`:**
   - Comprehensive synchronization status
   - Data source freshness and last update times
   - Integration health and error rates
   - Recommendations for data improvements

   **Conflict Resolution `--conflicts`:**
   - Identify data conflicts between sources
   - Suggest resolution strategies
   - Show conflict impact analysis
   - Provide manual override options

### Output Format

Structure your response as a professional synchronization report:

```markdown
# 🔄 Team Data Synchronization Report
**Generated:** [timestamp]
**Sync Status:** [status]
**Sources:** [count] integrated systems

## 🎯 Synchronization Summary
- **Team Members Synced:** [count] of [total] ([percentage]%)
- **Project Assignments:** [count] assignments updated
- **Meeting Schedules:** [count] schedules synchronized
- **Data Conflicts:** [count] requiring attention
- **Last Full Sync:** [timestamp] ([time] ago)

## 📊 Integration Health

### Data Source Status
| Source | Status | Last Updated | Records | Sync Rate |
|--------|--------|--------------|---------|-----------|
| Team Roster | [status] | [timestamp] | [count] | [percentage]% |
| Projects | [status] | [timestamp] | [count] | [percentage]% |
| Meetings | [status] | [timestamp] | [count] | [percentage]% |

### Sync Quality Metrics
- **Data Completeness:** [percentage]% (target: 95%+)
- **Reference Integrity:** [percentage]% (target: 100%)
- **Update Frequency:** [frequency] (target: daily)
- **Error Rate:** [percentage]% (target: <1%)

## 🔗 Project Assignment Sync

### Successfully Synchronized
**[Member Name]** (`[email]`)
- **Current Projects:** [count] active assignments
- **Workload:** [percentage]% capacity utilized
- **Recent Changes:** [changes made]
- **Status:** ✅ All assignments validated

### Assignment Updates
| Member | Project Added | Project Removed | Workload Change |
|--------|---------------|-----------------|-----------------|
| [member] | [project] | [project] | [change] |

### Unresolved Issues
**[Member Name]** - Project Assignment Conflict
- **Issue:** Listed in [project] but not in team roster
- **Impact:** Project ownership unclear
- **Resolution:** [suggested action]

## 📅 Meeting Integration

### Meeting Participation Summary
- **Regular Meetings:** [count] team members in recurring meetings
- **Meeting Load:** [average] hours/week per team member
- **Availability:** [percentage]% team available for new meetings
- **Conflicts:** [count] scheduling conflicts identified

### Meeting Assignment Updates
**[Meeting Name]** - [frequency]
- **Participants Updated:** [changes]
- **New Attendees:** [members added]
- **Removed:** [members removed]
- **Reason:** [reason for changes]

## ⚠️ Data Conflicts & Issues

### Critical Issues Requiring Attention
**Email Mismatch**
- **Team Roster:** [email] for [name]
- **Projects:** [email] for [name]
- **Impact:** Project assignments unclear
- **Resolution:** [recommended action]

**Project Ownership Conflict**
- **Project:** [project_id]
- **Team Roster Owner:** [email]
- **Project Config Owner:** [email]
- **Resolution:** [recommended action]

### Minor Issues
- **[Issue Type]:** [count] instances
- **Impact:** [impact description]
- **Auto-Resolution:** [action taken]

## 📈 Workload Analysis

### Team Capacity Overview
| Member | Active Projects | Workload % | Availability | Status |
|--------|----------------|------------|--------------|--------|
| [member] | [count] | [percentage]% | [hours] | [status] |

### Capacity Insights
- **Overallocated:** [count] members above 100% capacity
- **Available Capacity:** [count] members with <80% utilization
- **Balanced Load:** [count] members at optimal 80-100% capacity
- **New Assignment Capacity:** [hours] available across team

## 🎯 Goal & Performance Sync

### Goal Alignment
- **Project Goals ↔ Individual Goals:** [percentage]% alignment
- **Misaligned Goals:** [count] requiring review
- **Goal Coverage:** [percentage]% of projects have team goal alignment

### Performance Integration
- **Performance Data Currency:** [percentage]% up-to-date
- **Missing Performance Data:** [count] members
- **Performance-Project Correlation:** Available for [count] members

## 💡 Sync Recommendations

### Immediate Actions
1. **[Action]** - [description] ([priority])
2. **[Action]** - [description] ([priority])
3. **[Action]** - [description] ([priority])

### Process Improvements
- **Automation Opportunities:** [suggestions]
- **Data Quality Enhancements:** [recommendations]
- **Integration Optimizations:** [improvements]

### Team Management
- **Workload Rebalancing:** [suggestions]
- **Project Assignments:** [recommendations]
- **Meeting Optimization:** [improvements]

## 🔄 Next Sync Schedule
- **Automatic Sync:** [frequency] at [time]
- **Manual Sync Triggers:** [conditions]
- **Full Validation:** [frequency]
- **Conflict Review:** [frequency]
```

### Individual Member Sync

When syncing specific member data:

```markdown
# 👤 Member Synchronization: [Member Name]
**Email:** [email] | **Status:** [sync_status]
**Last Synced:** [timestamp]

## Sync Status Summary
- **Team Roster:** ✅ Current and validated
- **Project Assignments:** [status] - [details]
- **Meeting Schedules:** [status] - [details]
- **Performance Data:** [status] - [details]

## Project Assignment Validation
**Current Projects from Team Roster:**
- [project]: [role] ([percentage]% allocation)
- [project]: [role] ([percentage]% allocation)

**Projects from Project System:**
- [project]: Owner ([status])
- [project]: Contributor ([status])

**Sync Actions:**
- ✅ [action completed]
- ⚠️ [action needed]
- ❌ [conflict requiring resolution]

## Data Completeness
| Field | Team Roster | Projects | Meetings | Status |
|-------|-------------|----------|----------|--------|
| Name | [value] | [value] | [value] | [status] |
| Role | [value] | [value] | [value] | [status] |
| Manager | [value] | [value] | [value] | [status] |

## Recommendations
- [Specific recommendations for this member]
- [Data quality improvements needed]
- [Integration enhancements]
```

### Integration Features

1. **Real-time Sync**
   - Automatic data synchronization triggers
   - Change detection and propagation
   - Conflict resolution workflows
   - Data validation and integrity checks

2. **Cross-System Validation**
   - Reference integrity verification
   - Data consistency enforcement
   - Duplicate detection and resolution
   - Missing data identification

3. **Workload Optimization**
   - Capacity calculation and monitoring
   - Project allocation optimization
   - Resource utilization analysis
   - Availability forecasting

4. **Meeting Integration**
   - Calendar synchronization
   - Meeting participation tracking
   - Availability calculation
   - Scheduling conflict detection

### Error Handling

- **Data Source Unavailability:** Graceful degradation with cached data
- **Validation Failures:** Clear error reporting with resolution guidance
- **Sync Conflicts:** Intelligent conflict resolution with user oversight
- **Performance Issues:** Incremental sync and optimization strategies

### Best Practices

1. **Data Governance**
   - Establish single source of truth for each data element
   - Implement data quality standards and validation rules
   - Regular data audits and cleanup processes

2. **Sync Management**
   - Schedule regular synchronization cycles
   - Monitor sync performance and success rates
   - Maintain sync logs for troubleshooting

3. **Conflict Resolution**
   - Establish clear precedence rules for conflicting data
   - Implement approval workflows for significant changes
   - Maintain audit trails for all data modifications

Always ensure data synchronization maintains integrity while providing actionable insights for team management optimization.
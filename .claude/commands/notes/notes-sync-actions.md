---
name: notes-sync-actions
description: Synchronize action items between notes system and project milestones
---

# /notes sync-actions - Action Item Synchronization

Intelligent synchronization of action items between the PARA notes system and project management, ensuring alignment between note-based tasks and project milestones.

## Usage Examples:
- `/notes sync-actions` - Sync action items across all projects
- `/notes sync-actions --project mobile-app-v2` - Sync specific project action items
- `/notes sync-actions --overdue-alert` - Focus on overdue action items requiring attention
- `/notes sync-actions --milestone-align` - Align action items with project milestones
- `/notes sync-actions --dry-run` - Preview sync changes without applying

## Instructions:

You are an intelligent action item synchronization system that maintains alignment between notes-based tasks and project milestone tracking. When this command is invoked, you will:

### Core Synchronization Functions

1. **Action Item Discovery and Extraction**
   - Scan all project-linked notes for action items (meetings, decisions, research notes)
   - Parse action item format: assignee, due date, task description, source note
   - Identify action items that reference specific project milestones
   - Extract completion status and progress indicators from note content

2. **Project Milestone Mapping**
   - Load project configuration and milestone definitions from `.claude/projects.yaml`
   - Match action items to relevant project milestones based on content analysis
   - Identify milestone dependencies that are tracked through action items
   - Map action item completion to milestone progress assessment

3. **Bidirectional Synchronization**
   - Update project cache with action item status from notes
   - Generate milestone progress updates based on action item completion
   - Flag inconsistencies between note status and project tracking
   - Maintain audit trail of synchronization activities

4. **Intelligent Alerting and Recommendations**
   - Identify overdue action items that could impact project timelines
   - Generate milestone risk assessments based on action item status
   - Recommend resource reallocation based on action item workload
   - Suggest follow-up actions for blocked or delayed items

### Command Actions

**Full Portfolio Synchronization `/notes sync-actions`:**

Execute comprehensive action item synchronization:

1. **Discovery Phase** (using NoteProcessor)
   ```python
   from tools import NoteProcessor
   from tools.note_models import ActionItemFilters

   processor = NoteProcessor()

   # Get all action items across all projects (simplified from manual cache reading)
   all_action_items = processor.extract_action_items(scope="all")
   pending = processor.get_action_items_by_status("pending")
   overdue = processor.get_action_items_by_status("overdue")
   completed = processor.get_action_items_by_status("completed")
   ```

2. **Synchronization Analysis**
   ```python
   # Analyze action items for synchronization needs
   sync_analysis = {
       'total_items': len(all_action_items),
       'overdue_items': find_overdue_items(all_action_items),
       'milestone_mapped': map_items_to_milestones(all_action_items, projects),
       'completion_updates': detect_completion_status_changes(all_action_items),
       'conflict_detection': identify_sync_conflicts(all_action_items, projects),
       'new_items': find_new_action_items(all_action_items)
   }
   ```

3. **Execute Synchronization**
   ```python
   # Update project caches with synchronized data
   for project_id, project_data in projects['projects'].items():
       project_actions = filter_actions_for_project(all_action_items, project_id)

       # Update milestone progress based on action item completion
       milestone_updates = calculate_milestone_progress(project_actions, project_data)

       # Update project cache with synchronized action items
       update_project_cache(project_id, {
           'action_items': project_actions,
           'milestone_progress_updates': milestone_updates,
           'sync_timestamp': datetime.now().isoformat()
       })
   ```

**Project-Specific Synchronization `/notes sync-actions --project {project-name}`:**

Execute targeted synchronization:

1. **Project-Focused Analysis** (using NoteProcessor)
   ```python
   # Get project-specific notes and action items
   project_notes = processor.get_project_notes(project_id)
   project_actions = processor.extract_action_items(
       scope=f"project:{project_id}"
   )

   # Sync project notes cache
   sync_result = processor.sync_project_notes(project_id)
   ```

2. **Milestone Impact Assessment**
   - Calculate milestone completion percentage based on linked action items
   - Identify at-risk milestones based on overdue action items
   - Generate timeline impact analysis for project leadership

### Output Formats

#### Comprehensive Synchronization Report (Default)

```markdown
# 🔄 Action Item Synchronization Report
**Sync Timestamp:** {timestamp}
**Projects Analyzed:** {project_count} | **Action Items Processed:** {total_action_items}

## 📊 Synchronization Summary

**Action Item Status:**
- **Total Active:** {active_count} items across {project_count} projects
- **Completed This Cycle:** {completed_count} items
- **Newly Discovered:** {new_count} items from recent notes
- **Status Updates:** {updated_count} items with status changes

**Milestone Impact:**
- **Milestones Updated:** {milestone_count} with new progress data
- **At Risk:** {at_risk_count} milestones due to overdue action items
- **Completed:** {completed_milestone_count} milestones marked complete

## 🚨 Critical Action Items Requiring Attention

### Overdue Items Impacting Project Timelines ({overdue_count})

**{project_name} - {milestone_name} at Risk**
- 🔴 **{action_item}** - Owner: {owner} - Due: {due_date} ({days_overdue} days overdue)
  - **Impact**: {milestone_impact_description}
  - **Source**: {source_note} ({note_date})
  - **Recommendation**: {recommended_action}

**{project_name} - Resource Conflict Detected**
- 🟡 **{action_item}** - Owner: {owner} - Due: {due_date}
  - **Conflict**: {owner} has {conflict_count} concurrent action items due this week
  - **Projects Affected**: {affected_project_list}
  - **Recommendation**: {resource_reallocation_suggestion}

### High-Impact Items Due This Week ({due_this_week_count})

| Action Item | Owner | Due Date | Project | Milestone Impact | Status |
|-------------|--------|----------|---------|------------------|---------|
| {action_item} | {owner} | {due_date} | {project} | {milestone_impact} | 🟡 In Progress |
| {action_item} | {owner} | {due_date} | {project} | {milestone_impact} | 🔴 Blocked |

## 📈 Project Milestone Updates

### Progress Updates Applied

**{project_name}:**
- **{milestone_name}**: Updated to {new_percentage}% complete (was {old_percentage}%)
  - Driving Factor: {completion_reason}
  - Action Items: {completed_count}/{total_count} completed
  - Timeline Impact: {timeline_assessment}

- **{milestone_name}**: Status changed to {new_status}
  - Reason: {status_change_reason}
  - Next Actions: {required_next_actions}
  - Risk Level: {risk_assessment}

### Milestones Requiring Attention

**At Risk Milestones ({at_risk_count}):**
1. **{project_name} - {milestone_name}** (Due: {due_date})
   - **Risk**: {overdue_action_count} overdue action items
   - **Impact**: Potential {delay_estimate} delay
   - **Actions**: {recommended_interventions}

2. **{project_name} - {milestone_name}** (Due: {due_date})
   - **Risk**: Resource over-allocation affecting {owner_name}
   - **Impact**: Quality and timeline risk
   - **Actions**: {resource_reallocation_options}

## 🎯 Action Item Performance Analysis

### Completion Trends
- **Portfolio Completion Rate**: {portfolio_completion_rate}% (target: 85%)
- **Average Completion Time**: {avg_completion_days} days
- **On-Time Completion**: {on_time_percentage}% of items completed by due date

### Owner Performance
| Owner | Active Items | Completion Rate | Avg. Days to Complete | Workload Risk |
|-------|--------------|-----------------|---------------------|---------------|
| {owner_name} | {active_count} | {completion_rate}% | {avg_days} | {workload_risk} |
| {owner_name} | {active_count} | {completion_rate}% | {avg_days} | {workload_risk} |

### Project Performance
| Project | Active Actions | Completion Rate | Milestone Alignment | Health Score |
|---------|----------------|-----------------|-------------------|--------------|
| {project_name} | {active_count} | {completion_rate}% | {alignment_score}% | {health_score}/10 |

## 🔗 Cross-Project Action Item Dependencies

### Blocking Relationships Detected
- **{project_a}** waiting on **{project_b}**: {action_item_description}
  - Owner: {owner} | Due: {due_date}
  - Impact: {impact_on_dependent_project}

- **{dependency_description}**: {action_count} action items form dependency chain
  - Critical Path Impact: {critical_path_assessment}
  - Recommended Action: {dependency_resolution_strategy}

### Resource Allocation Conflicts
- **{owner_name}**: {project_count} projects, {total_action_items} active items
  - Capacity Risk: {over_allocation_percentage}% over recommended capacity
  - Affected Projects: {project_list}
  - Recommendation: {capacity_management_suggestion}

## 💡 Synchronization Insights and Recommendations

### Process Improvements
1. **Action Item Documentation**: {improvement_suggestion_1}
2. **Milestone Alignment**: {improvement_suggestion_2}
3. **Ownership Clarity**: {improvement_suggestion_3}

### Strategic Recommendations
1. **Resource Planning**: {resource_recommendation}
2. **Timeline Management**: {timeline_recommendation}
3. **Cross-Project Coordination**: {coordination_recommendation}

### Automation Opportunities
- **Status Updates**: {automation_suggestion_1}
- **Overdue Alerts**: {automation_suggestion_2}
- **Progress Tracking**: {automation_suggestion_3}

## 📅 Next Sync Actions

### Immediate (Next 24 Hours)
- [ ] Address {critical_overdue_count} critically overdue action items
- [ ] Resolve {resource_conflict_count} resource allocation conflicts
- [ ] Update stakeholders on {at_risk_milestone_count} at-risk milestones

### This Week
- [ ] Review {pending_review_count} action items pending status updates
- [ ] Implement {process_improvement_count} identified process improvements
- [ ] Schedule follow-up for {follow_up_count} blocked action items

### Strategic (Next 2 Weeks)
- [ ] Analyze action item patterns for process optimization
- [ ] Implement automated synchronization for routine updates
- [ ] Review and update action item assignment strategies

---
**Next Automatic Sync**: {next_sync_time} | **Manual Sync Available**: Use `/notes sync-actions` anytime
```

#### Project-Specific Synchronization Report

```markdown
# 🔄 Action Sync: {Project Name}
**Sync Date:** {timestamp} | **Action Items:** {total_items} | **Milestone Impact:** {impact_count}

## 📊 Project Action Item Status

### Current State
- **Active Items**: {active_count} | **Overdue**: {overdue_count} | **Completed This Month**: {monthly_completed}
- **Milestone Completion**: {milestone_progress}% based on action item tracking
- **Team Workload**: {team_workload_assessment}

### Recent Synchronization Changes
- **Status Updates**: {status_update_count} items updated from note content
- **New Items**: {new_item_count} action items discovered from recent notes
- **Completed Items**: {completed_count} items marked complete and archived

## 🎯 Milestone Alignment Analysis

### {Milestone Name} ({due_date})
**Progress**: {progress_percentage}% complete based on {linked_action_count} linked action items

**Action Items Status:**
- ✅ **Completed** ({completed_count}):
  - {completed_action_1} (Completed {date} by {owner})
  - {completed_action_2} (Completed {date} by {owner})

- 🔄 **In Progress** ({in_progress_count}):
  - {in_progress_action_1} - Owner: {owner} - Due: {due_date}
  - {in_progress_action_2} - Owner: {owner} - Due: {due_date}

- 🚨 **Overdue** ({overdue_count}):
  - {overdue_action_1} - Owner: {owner} - Due: {past_date} ({days_overdue} days)

**Milestone Risk Assessment**: {risk_level}
**Expected Completion**: {projected_completion_date}
**Recommendation**: {milestone_recommendation}

## 📋 Action Item Details

### High Priority Items
| Action Item | Owner | Due Date | Source Note | Milestone Link | Status | Days Remaining |
|-------------|--------|----------|-------------|----------------|---------|----------------|
| {action_item} | {owner} | {due_date} | {source_note} | {milestone} | {status} | {days_remaining} |

### Recently Updated
- **{action_item}**: Status changed from {old_status} to {new_status}
  - Source: {source_note_update}
  - Impact: {impact_on_milestone}

### Blocked Items Requiring Attention
- **{blocked_action}**: Blocked by {blocking_factor}
  - Owner: {owner} | Originally Due: {original_due_date}
  - Resolution Strategy: {resolution_approach}
  - Escalation Needed: {escalation_recommendation}

## 💬 Communication and Follow-up

### Owner Notifications Required
- **{owner_name}**: {action_count} items needing attention
  - Overdue: {overdue_count} | Due This Week: {due_soon_count}
  - Recommended: Schedule check-in to review status and blockers

### Stakeholder Updates
- **Project Status**: {milestone_progress}% complete based on action item tracking
- **Timeline Impact**: {timeline_assessment}
- **Key Message**: {stakeholder_communication_summary}

### Next Review Date
**Scheduled**: {next_review_date}
**Focus**: {next_review_focus_areas}
```

#### Dry Run Preview

```markdown
# 🔍 Action Item Sync Preview (Dry Run)
**Would be applied if executed without --dry-run flag**

## 📊 Proposed Changes

### Status Updates ({update_count})
- **{action_item}** → Status: {old_status} → {new_status}
  - Reason: {change_reason}
  - Source: {source_evidence}

### New Action Items ({new_count})
- **{new_action_item}**
  - Source: {source_note}
  - Owner: {proposed_owner}
  - Due: {proposed_due_date}
  - Milestone: {linked_milestone}

### Milestone Progress Updates ({milestone_count})
- **{project_name} - {milestone_name}**: {old_percentage}% → {new_percentage}%
  - Driver: {progress_driver}
  - Timeline Impact: {timeline_change}

## ⚠️ Potential Issues Detected
- **{issue_description}**: {issue_details}
  - Recommendation: {resolution_suggestion}

## 🎯 Execute Full Sync
To apply these changes, run: `/notes sync-actions` (without --dry-run flag)
```

### Implementation Steps

When executing this command:

1. **Action Item Discovery** (simplified with NoteProcessor)
   ```python
   from tools import NoteProcessor
   from tools.note_models import ActionItemFilters

   processor = NoteProcessor()

   # Simple method calls replace 15+ lines of manual cache reading
   all_items = processor.extract_action_items(scope="all")

   # Filter by project if needed
   project_items = processor.extract_action_items(scope=f"project:{project_id}")

   # Get by status
   pending = processor.get_action_items_by_status("pending", project=project_id)
   overdue = processor.get_action_items_by_status("overdue", project=project_id)
   ```

2. **Milestone Mapping and Progress Calculation**
   ```python
   def calculate_milestone_progress(action_items, project_data):
       """Calculate milestone completion based on action item status"""
       milestone_progress = {}

       for milestone in project_data.get('milestones', []):
           linked_items = find_linked_action_items(action_items, milestone)

           if linked_items:
               completed_count = sum(1 for item in linked_items if item['status'] == 'completed')
               total_count = len(linked_items)
               progress_percentage = (completed_count / total_count) * 100

               milestone_progress[milestone['name']] = {
                   'progress_percentage': progress_percentage,
                   'completed_items': completed_count,
                   'total_items': total_count,
                   'last_update': datetime.now().isoformat()
               }

       return milestone_progress
   ```

3. **Conflict Detection and Resolution**
   ```python
   def detect_synchronization_conflicts(action_items, projects):
       """Identify conflicts between notes and project data"""
       conflicts = []

       # Check for overdue items affecting milestones
       overdue_items = [item for item in action_items
                       if is_overdue(item) and item.get('linked_milestone')]

       # Check for resource over-allocation
       owner_workload = analyze_owner_workload(action_items)
       over_allocated = [owner for owner, load in owner_workload.items()
                        if load > CAPACITY_THRESHOLD]

       # Check for milestone dependency conflicts
       dependency_conflicts = check_dependency_chains(action_items, projects)

       return {
           'overdue_milestone_impact': overdue_items,
           'resource_over_allocation': over_allocated,
           'dependency_conflicts': dependency_conflicts
       }
   ```

4. **Generate Comprehensive Report**
   - Combine all analysis into actionable insights
   - Provide specific recommendations for each identified issue
   - Generate follow-up actions with clear ownership and timelines

### Integration Features

**Automatic Triggers:**
- Daily synchronization for active projects with recent note activity
- Immediate sync when meeting notes are created with action items
- Weekly comprehensive sync with conflict detection and resolution

**Alert Systems:**
- Overdue action items affecting critical milestones
- Resource allocation conflicts across multiple projects
- Milestone risk assessments based on action item completion patterns

**Reporting Integration:**
- Feed synchronized data into project review reports
- Provide action item insights for decision support analysis
- Generate portfolio-level action item performance metrics

### Error Handling

**Data Integrity:**
- Validate action item format and required fields
- Handle missing project references gracefully
- Detect and repair corrupted cache data

**Conflict Resolution:**
- Provide clear options for resolving synchronization conflicts
- Maintain audit trail of all synchronization decisions
- Allow manual override of automatic synchronization rules

### Best Practices

1. **Regular Synchronization:**
   - Run daily sync during active project periods
   - Schedule weekly comprehensive analysis and conflict resolution
   - Perform immediate sync after important meetings or decisions

2. **Quality Assurance:**
   - Validate action item assignments against project team membership
   - Check due date feasibility against project timelines
   - Ensure milestone linking accuracy and completeness

3. **Communication Integration:**
   - Generate owner-specific action item summaries
   - Provide project managers with milestone risk assessments
   - Create executive summaries of action item portfolio health

## Implementation Notes

**NoteProcessor Integration Benefits:**
- **90+ lines → 10 lines** for action item discovery
- Type-safe operations with ActionItemFilters
- Automatic error handling and validation
- `get_project_notes()` replaces manual cache reading
- `sync_project_notes()` handles cache updates automatically
- `extract_action_items()` with scope filtering (all, project:id, inbox)
- `get_action_items_by_status()` for pending, completed, overdue filtering

**Key Methods:**
- `processor.extract_action_items(scope="all")` - Get all action items
- `processor.get_action_items_by_status("overdue", project=id)` - Filter by status
- `processor.get_project_notes(project_id)` - Get project-linked notes
- `processor.sync_project_notes(project_id)` - Update cache system

Remember: Effective action item synchronization bridges the gap between detailed note-taking and strategic project management, ensuring nothing falls through the cracks.
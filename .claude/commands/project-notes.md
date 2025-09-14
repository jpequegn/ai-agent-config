---
name: project-notes
description: Display and manage notes linked to specific projects with action item synchronization
---

# /project notes - Project-Linked Notes Overview

Comprehensive view of all notes linked to a specific project, including meeting notes, decisions, action items, and cross-references with other projects.

## Usage Examples:
- `/project notes mobile-app-v2` - Show all notes for Mobile App V2 project
- `/project notes q4-marketing --recent 30` - Last 30 days of marketing project notes
- `/project notes infrastructure-upgrade --type meeting` - Only meeting notes for infrastructure project
- `/project notes mobile-app-v2 --actions-only` - Focus on action items and their status
- `/project notes --all --summary` - Summary view of notes across all projects

## Instructions:

You are a project-notes integration system that provides comprehensive views of notes linked to projects. When this command is invoked, you will:

### Core Functionality

1. **Load Project Data and Notes**
   - Load project configuration from `.claude/projects.yaml`
   - Load project notes cache from `.claude/cache/notes_{project_name}.json`
   - Cross-reference with actual note files in inbox for complete data
   - Validate and sync cache data with current note status

2. **Comprehensive Notes Analysis**
   - Categorize notes by type: meetings, decisions, research, quick notes
   - Extract key themes and recurring topics from note content
   - Analyze action item completion patterns and milestone alignment
   - Identify project decision history and impact assessment

3. **Cross-Project Intelligence**
   - Detect references to other projects in notes
   - Map project dependencies mentioned in meetings and decisions
   - Identify resource conflicts and collaboration opportunities
   - Track stakeholder involvement across multiple projects

4. **Action Item Synchronization**
   - Sync action item status between notes and project milestones
   - Generate alerts for overdue action items from notes
   - Map note action items to project deliverables and deadlines
   - Provide completion tracking and accountability metrics

### Command Actions

**Single Project Notes Overview `/project notes {project-name}`:**

Execute comprehensive project notes analysis:

1. **Load Project Context**
   ```python
   import yaml
   import json
   from pathlib import Path
   from datetime import datetime, timedelta

   # Load project configuration
   with open('.claude/projects.yaml', 'r') as f:
       projects = yaml.safe_load(f)

   project_data = projects['projects'].get(project_name)
   if not project_data:
       return {"error": f"Project {project_name} not found"}

   # Load project notes cache
   cache_file = f'.claude/cache/notes_{project_name.replace("-", "_")}.json'
   notes_cache = load_or_create_cache(cache_file)
   ```

2. **Generate Comprehensive Analysis**
   ```python
   # Analyze notes content and extract insights
   notes_analysis = {
       'total_notes': len(notes_cache['project_notes']),
       'note_categories': categorize_notes(notes_cache['project_notes']),
       'action_items': analyze_action_items(notes_cache['action_items']),
       'decisions': track_decisions(notes_cache['decisions']),
       'themes': extract_themes(notes_cache['project_notes']),
       'milestone_alignment': check_milestone_alignment(notes_cache, project_data),
       'stakeholder_involvement': analyze_stakeholders(notes_cache),
       'cross_references': find_cross_references(notes_cache)
   }
   ```

3. **Present Integrated Overview**

**All Projects Summary `/project notes --all`:**

Execute portfolio-wide notes analysis:

1. **Cross-Project Notes Analysis**
   - Load notes caches for all active projects
   - Identify cross-project themes and collaboration patterns
   - Generate portfolio-wide action item status
   - Create strategic insights from project note patterns

### Output Formats

#### Single Project Notes Overview (Default)

```markdown
# 📝 Project Notes: {Project Name}
**Status:** {project_status} | **Notes:** {total_count} | **Last Activity:** {last_note_date}
**Action Items:** {active_count} active, {completed_count} completed, {overdue_count} overdue

## 📊 Notes Overview

### Recent Activity (Last 30 Days)
- **{date}**: **{note_title}** ({note_type})
  - Key Outcome: {summary}
  - Action Items: {action_count} ({completed_count} completed)
  - Attendees: {attendee_list}

- **{date}**: **{note_title}** ({note_type})
  - Key Decision: {decision_summary}
  - Impact: {impact_on_project}
  - Status: {implementation_status}

### Note Categories
| Type | Count | Recent | Key Themes |
|------|-------|--------|------------|
| **Meetings** | {meeting_count} | {last_meeting_date} | {meeting_themes} |
| **Decisions** | {decision_count} | {last_decision_date} | {decision_themes} |
| **Research** | {research_count} | {last_research_date} | {research_themes} |
| **Quick Notes** | {quick_count} | {last_quick_date} | {quick_themes} |

## 🎯 Action Items Analysis

### Active Action Items ({active_count})
| Action Item | Owner | Due Date | Source Note | Milestone Link | Status |
|-------------|--------|----------|-------------|----------------|---------|
| {action_item} | {owner} | {due_date} | {source_note} | {milestone} | 🟡 In Progress |
| {action_item} | {owner} | {due_date} | {source_note} | {milestone} | 🔴 At Risk |

### Recently Completed ({completed_count})
- ✅ **{action_item}** - Completed {date} by {owner} (Source: {note_title})
- ✅ **{action_item}** - Completed {date} by {owner} (Source: {note_title})

### Overdue Items Requiring Attention ({overdue_count})
- 🚨 **{overdue_action}** - Due {past_date} - Owner: {owner}
  - Source: {source_note} ({note_date})
  - Days Overdue: {days_overdue}
  - **Recommendation**: {suggested_action}

## 🔑 Key Decisions Tracked

### Recent Decisions ({recent_decision_count})
1. **{decision_title}** ({date})
   - **Decision**: {decision_details}
   - **Rationale**: {reasoning}
   - **Impact**: {impact_on_milestones}
   - **Status**: {implementation_status}
   - **Source**: {meeting_or_note}

2. **{decision_title}** ({date})
   - **Decision**: {decision_details}
   - **Stakeholders**: {affected_stakeholders}
   - **Timeline Impact**: {timeline_changes}
   - **Follow-up**: {next_actions}

### Implementation Status
- **Implemented**: {implemented_count} decisions
- **In Progress**: {in_progress_count} decisions
- **Pending**: {pending_count} decisions
- **Blocked**: {blocked_count} decisions

## 📈 Project-Notes Alignment

### Milestone Coverage
| Milestone | Due Date | Notes References | Action Items | Completion Risk |
|-----------|----------|------------------|--------------|-----------------|
| {milestone_name} | {due_date} | {reference_count} notes | {action_count} items | 🟢 On Track |
| {milestone_name} | {due_date} | {reference_count} notes | {action_count} items | 🟡 At Risk |

### Progress Insights
- **Well-Documented Milestones**: {covered_milestones} have comprehensive note coverage
- **Under-Documented Areas**: {uncovered_areas} need more discussion and documentation
- **Action Item Alignment**: {alignment_percentage}% of action items link to project milestones

## 🔗 Cross-References and Dependencies

### Related Projects Referenced
- **{related_project}**: {reference_count} mentions
  - Key Dependency: {dependency_description}
  - Last Discussed: {last_mention_date}
- **{related_project}**: {reference_count} mentions
  - Collaboration Area: {collaboration_type}
  - Status: {collaboration_status}

### External System References
- **GitHub Repositories**: {repo_references} references to code/issues
- **Design Tools**: {design_references} references to Figma/design assets
- **Documentation**: {doc_references} references to external docs

### Stakeholder Involvement
| Stakeholder | Notes Involvement | Action Items Assigned | Last Active |
|-------------|-------------------|----------------------|-------------|
| {stakeholder_name} | {note_count} meetings | {action_count} items | {last_active_date} |
| {stakeholder_name} | {note_count} meetings | {action_count} items | {last_active_date} |

## 💡 Insights and Recommendations

### Content Analysis
**Most Discussed Topics:**
1. **{topic_1}**: Mentioned in {count} notes - {trend_analysis}
2. **{topic_2}**: Discussed in {count} notes - {trend_analysis}
3. **{topic_3}**: Tracked across {count} notes - {trend_analysis}

**Recurring Concerns:**
- **{concern_1}**: Raised in {count} meetings, needs strategic attention
- **{concern_2}**: Ongoing issue affecting {affected_milestones}

### Process Recommendations
**Note-Taking Effectiveness:**
- {recommendation_1_based_on_analysis}
- {recommendation_2_for_better_tracking}
- {recommendation_3_for_action_items}

**Project Alignment:**
- {alignment_recommendation_1}
- {milestone_tracking_suggestion}
- {communication_improvement_suggestion}

## 📅 Next Actions

### Immediate (This Week)
- Review {overdue_count} overdue action items
- Follow up on {pending_decision_count} pending decisions
- Schedule follow-up for {at_risk_milestone_count} at-risk milestones

### Short-term (Next 2 Weeks)
- Document {undocumented_area_count} under-documented project areas
- Sync action item status with project milestone progress
- Address {blocked_decision_count} blocked decisions

### Strategic (Next Month)
- Review note-taking process effectiveness
- Improve cross-project collaboration documentation
- Implement action item automation for recurring tasks

---
**Last Updated**: {timestamp} | **Next Review**: {next_review_date}
```

#### Action Items Focus View

```markdown
# ✅ Action Items: {Project Name}
**Total Active**: {active_count} | **Completed This Month**: {monthly_completed}

## 🚨 Urgent Attention Required

### Overdue Items ({overdue_count})
| Action Item | Owner | Originally Due | Days Overdue | Source | Impact |
|-------------|--------|---------------|--------------|---------|--------|
| {action_item} | {owner} | {due_date} | {days_late} | {source_note} | {milestone_impact} |

### Due This Week ({due_this_week_count})
| Action Item | Owner | Due Date | Progress | Milestone Link |
|-------------|--------|----------|----------|----------------|
| {action_item} | {owner} | {due_date} | {progress_status} | {linked_milestone} |

## 📊 Action Item Performance

### Completion Trends
- **This Month**: {monthly_completion_rate}% completion rate
- **Last Month**: {last_month_rate}% (trend: {trend_direction})
- **Average Days to Complete**: {avg_completion_days}

### Owner Performance
| Owner | Active Items | Completion Rate | Avg. Completion Time |
|-------|--------------|-----------------|---------------------|
| {owner} | {active_count} | {completion_rate}% | {avg_days} days |

## 🎯 Milestone Alignment

### Action Items by Milestone
- **{milestone_name}** ({milestone_due}): {action_count} items
  - Completed: {completed_count} | Remaining: {remaining_count}
  - Risk Assessment: {risk_level}
- **{milestone_name}** ({milestone_due}): {action_count} items
  - Progress: {progress_percentage}%
  - Expected Completion: {expected_date}
```

#### Cross-Project Summary

```markdown
# 📝 Portfolio Notes Summary
**Active Projects**: {active_project_count} | **Total Notes**: {total_note_count}

## 📊 Cross-Project Activity

### Most Active Projects (by Notes)
1. **{project_name}**: {note_count} notes, {action_count} action items
2. **{project_name}**: {note_count} notes, {action_count} action items
3. **{project_name}**: {note_count} notes, {action_count} action items

### Cross-Project Themes
- **{theme_1}**: Discussed in {project_count} projects
- **{theme_2}**: Affecting {project_count} projects
- **{theme_3}**: Coordinated across {project_count} projects

### Resource Conflicts from Notes
- **{person}**: Mentioned as owner/participant in {project_count} projects
  - Action Items: {total_action_items} across projects
  - Risk: {over_allocation_risk}

## 🔗 Project Interconnections

### Dependencies Documented in Notes
- **{project_a}** → **{project_b}**: {dependency_description}
- **{project_c}** ← **{project_d}**: {blocking_relationship}

### Collaboration Patterns
- **{project_group}**: Regular joint meetings and shared action items
- **{stakeholder}**: Key participant across {project_count} projects
```

### Implementation Steps

When executing this command:

1. **Load Project and Notes Data**
   ```python
   # Load project configuration
   with open('.claude/projects.yaml', 'r') as f:
       projects = yaml.safe_load(f)

   # Load specific project cache
   cache_file = f'.claude/cache/notes_{project_name.replace("-", "_")}.json'
   try:
       with open(cache_file, 'r') as f:
           notes_cache = json.load(f)
   except FileNotFoundError:
       notes_cache = {
           "project_notes": [],
           "action_items": [],
           "decisions": [],
           "collected_at": datetime.now().isoformat()
       }
   ```

2. **Analyze Notes Content**
   ```python
   # Categorize notes by type and date
   notes_by_type = categorize_notes(notes_cache['project_notes'])

   # Extract themes and topics
   themes = extract_themes(notes_cache['project_notes'])

   # Analyze action item patterns
   action_analysis = analyze_action_items(notes_cache['action_items'])

   # Cross-reference with project milestones
   milestone_alignment = check_milestone_references(notes_cache, project_data)
   ```

3. **Generate Cross-References**
   ```python
   # Find references to other projects
   cross_references = find_cross_project_references(notes_cache)

   # Map stakeholder involvement
   stakeholder_analysis = analyze_stakeholder_participation(notes_cache)

   # Identify external system references
   external_refs = extract_external_references(notes_cache)
   ```

4. **Create Comprehensive Report**
   - Combine all analysis into structured output
   - Provide actionable recommendations
   - Include next steps and follow-up actions
   - Generate alerts for items requiring immediate attention

### Integration with Existing Systems

**Project Data Sources:**
- `.claude/projects.yaml` for project configuration and milestones
- `.claude/cache/notes_*.json` for project-specific notes data
- Actual note files in inbox for complete content analysis
- Cross-project references and dependencies

**Action Item Synchronization:**
- Extract action items from all note types
- Map to project milestones and deliverables
- Track completion status and update project progress
- Generate alerts for overdue or at-risk items

**Decision Tracking:**
- Document all project decisions from meeting notes
- Track implementation status and impact
- Link decisions to milestone changes and resource allocation
- Provide decision history for context and learning

### Error Handling

**Missing Data:**
- Handle projects without notes gracefully
- Provide clear messaging for empty or missing cache files
- Suggest actions to improve note-project linking

**Data Inconsistencies:**
- Detect and report orphaned notes references
- Validate action item assignments against project team
- Check for timeline inconsistencies between notes and project data

### Best Practices

1. **Comprehensive Coverage:**
   - Analyze all note types for complete project picture
   - Include both explicit and implicit project references
   - Consider historical patterns and trends in analysis

2. **Actionable Insights:**
   - Focus on items requiring immediate attention
   - Provide specific recommendations with clear next steps
   - Connect insights to project success and risk factors

3. **Cross-Project Intelligence:**
   - Identify collaboration opportunities and resource sharing
   - Highlight conflicts and dependencies that need attention
   - Generate portfolio-level insights from project note patterns

Remember: Effective project-notes integration transforms scattered information into strategic intelligence that drives project success and organizational learning.
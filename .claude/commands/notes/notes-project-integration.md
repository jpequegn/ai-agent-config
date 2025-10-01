---
name: notes-project-integration
description: Seamless integration between PARA notes system and project orchestration
---

# Notes-Project Integration

Create seamless integration between project orchestration and the PARA notes system with automatic linking, cross-referencing, and action item synchronization.

## Usage Examples:
- `/notes meeting --project mobile-app-v2 --topic "Sprint Planning"`
- `/notes capture --project q4-marketing --template quick-note "Budget approval update"`
- `/project notes mobile-app-v2` - Show all notes linked to project
- `/notes search --project-context mobile-app-v2 "timeline"`
- `/notes sync-actions --project mobile-app-v2` - Sync action items with project milestones

## Instructions:

You are an intelligent notes-project integration system that creates seamless connections between the PARA notes system and project management. When integration commands are invoked, you will:

### Core Integration Functions

1. **Automatic Project Context Detection**
   - Analyze note content, titles, and topics to identify relevant projects
   - Match against project names, tags, and keywords from `.claude/projects.yaml`
   - Auto-suggest project associations based on content analysis
   - Support explicit project specification via `--project` flag

2. **Cross-Reference Management**
   - Link notes to projects in cache files (`.claude/cache/notes_*.json`)
   - Update project cache with note references and summaries
   - Maintain bidirectional references between notes and projects
   - Track note-project relationship history and relevance

3. **Action Item Synchronization**
   - Extract action items from meeting notes and project discussions
   - Map note action items to project milestones and tasks
   - Sync action item status between notes and project tracking
   - Generate project status updates from note action item completion

4. **Enhanced Search and Context**
   - Provide project context in note search results
   - Search notes within specific project scope
   - Include related project information in note displays
   - Generate project-specific note summaries and insights

### Command Implementations

**Project-Aware Note Creation:**

When notes commands include project context:

1. **Enhanced Notes Meeting with Project Context**
   ```bash
   # User: /notes meeting --project mobile-app-v2 --topic "Sprint Planning"

   # Execute note creation with project integration
   ./notes capture --template meeting --topic "Meeting: Sprint Planning" --project mobile-app-v2

   # Auto-populate meeting context from project data
   # - Load project status, milestones, team members from .claude/projects.yaml
   # - Include recent project activity and decisions in meeting template
   # - Pre-populate attendees from project owner and team
   # - Add project milestone context to agenda
   ```

2. **Auto-Linked Project Notes with ConfigManager**
   ```python
   from tools import ConfigManager

   # Initialize ConfigManager
   mgr = ConfigManager()

   # Create note with automatic project synchronization
   def create_project_note(project_name, note_data):
       # Automatic project-to-notes sync via ConfigManager
       mgr.sync_project_to_notes(project_name)

       # Notes cache automatically updated at:
       # .claude/cache/notes_{project_name}.json

       # Cache contains validated project data:
       # - Project metadata (name, description, status)
       # - Milestones and deadlines
       # - Team members and ownership
       # - Dependencies and relationships

       return f"Project '{project_name}' synced to notes cache"
   ```

**Project Notes Overview:**

```bash
# User: /project notes mobile-app-v2
```

Execute project notes analysis using ConfigManager:

1. **Load Project Context and Notes with ConfigManager**
   ```python
   from tools import ConfigManager
   import json

   mgr = ConfigManager()

   # Sync project to notes cache first (ensures fresh data)
   mgr.sync_project_to_notes('mobile-app-v2')

   # Load synced project data with type safety
   project = mgr.get_project('mobile-app-v2')

   # Load notes cache (automatically updated by sync)
   cache_file = mgr.config_root / "cache" / "notes_mobile-app-v2.json"
   with open(cache_file, 'r') as f:
       notes_cache = json.load(f)

   # Generate comprehensive project notes overview
   # Project data is type-safe and validated via Pydantic
   overview = {
       'project_name': project.name,
       'project_status': project.status,
       'milestones': [m.model_dump() for m in project.milestones],
       'team': [project.owner] + project.team_members,
       'notes_cache': notes_cache
   }
   ```

2. **Present Integrated Overview**

**Action Item Synchronization with ConfigManager:**

```bash
# User: /notes sync-actions --project mobile-app-v2
```

Execute automatic synchronization using ConfigManager:

1. **Automatic Project-to-Notes Sync**
   ```python
   from tools import ConfigManager

   mgr = ConfigManager()

   # Sync project data to notes cache (automatic and atomic)
   mgr.sync_project_to_notes('mobile-app-v2')

   # Notes cache automatically updated with:
   # - Latest project milestones and tasks
   # - Team member assignments
   # - Project status and deadlines
   # - Dependencies and relationships

   # Type-safe access to synced project data
   project = mgr.get_project('mobile-app-v2')

   # Access project milestones with type safety
   for milestone in project.milestones:
       print(f"Milestone: {milestone.title}")
       print(f"  Due: {milestone.target_date}")
       print(f"  Status: {milestone.status}")
   ```

### Output Formats

#### Project Notes Overview

```markdown
# 📝 Project Notes: Mobile App V2 Redesign
**Project Status:** {status} | **Notes Count:** {note_count} | **Last Updated:** {last_update}

## 📊 Notes Summary

**Recent Activity:**
- **{date}**: {note_title} ({note_type}) - {key_outcome}
- **{date}**: {note_title} ({note_type}) - {key_outcome}
- **{date}**: {note_title} ({note_type}) - {key_outcome}

**Note Categories:**
- **Meeting Notes:** {meeting_count} notes
  - Sprint Planning: {count} notes
  - Stakeholder Reviews: {count} notes
  - Team Standups: {count} notes
- **Research Notes:** {research_count} notes
- **Decision Records:** {decision_count} notes
- **Action Items:** {action_count} items ({completed_count} completed)

## 🎯 Key Insights from Notes

**Recurring Themes:**
- **{theme_1}**: Mentioned in {count} notes, key concern: {summary}
- **{theme_2}**: Discussed in {count} notes, opportunity: {summary}
- **{theme_3}**: Tracked across {count} notes, status: {summary}

**Critical Decisions Documented:**
- **{decision_title}** ({date}): {decision_summary}
  - Impact: {impact_assessment}
  - Status: {implementation_status}
- **{decision_title}** ({date}): {decision_summary}
  - Impact: {impact_assessment}
  - Status: {implementation_status}

## ✅ Action Items Status

### Active Actions
- **{action_item}** - Owner: {owner} - Due: {due_date} - Source: {note_title}
- **{action_item}** - Owner: {owner} - Due: {due_date} - Source: {note_title}

### Recently Completed
- **{completed_action}** - Completed: {date} - Source: {note_title}
- **{completed_action}** - Completed: {date} - Source: {note_title}

### Overdue (Needs Attention)
- **{overdue_action}** - Due: {past_date} - Owner: {owner} - Source: {note_title}

## 📈 Notes-Project Alignment

**Project Milestones Referenced in Notes:**
- **{milestone_name}** ({milestone_date}): Referenced in {count} notes
  - Latest Update: {latest_reference} - {status}
- **{milestone_name}** ({milestone_date}): Discussed in {count} notes
  - Progress: {progress_summary}

**Action Items Linked to Milestones:**
- **{milestone_name}**: {action_count} action items from notes
  - {completed_count} completed, {pending_count} pending
- **{milestone_name}**: {action_count} action items mapped
  - Risk: {risk_assessment} based on action item status

## 🔗 Cross-References

**Related Projects:** {related_project_count} projects referenced in notes
- **{related_project}**: {reference_count} cross-references
- **{related_project}**: {reference_count} mentions

**External References:** {external_count} external documents/systems mentioned
- **{system_name}**: {reference_count} references
- **{document_type}**: {reference_count} references

## 💡 Recommendations

**Note Organization:**
- {recommendation_1_based_on_note_analysis}
- {recommendation_2_for_better_tracking}

**Project Alignment:**
- {project_recommendation_1}
- {action_item_organization_suggestion}

**Next Actions:**
- Review overdue action items from notes
- Update project milestones based on recent meeting outcomes
- Archive completed decisions and action items
```

#### Smart Meeting Note Template with Project Context

```markdown
# 📝 Meeting: {topic}
**Project:** {project_name} | **Date:** {date} | **Duration:** {duration}

## 🎯 Project Context
**Current Status:** {project_status}
**Active Milestones:**
- **{milestone_name}** (Due: {date}) - {progress}% complete
- **{milestone_name}** (Due: {date}) - {progress}% complete

**Recent Project Activity:**
- {recent_activity_from_project_cache}
- {recent_decisions_affecting_this_meeting}

## 👥 Attendees
{auto_populated_from_project_team}
- {project_owner} (Project Owner)
- {team_member_1} (Role)
- {team_member_2} (Role)

## 📋 Agenda
{template_agenda_with_project_context}

### Project Status Review
- Review progress on current milestones
- Address blockers identified in previous notes
- Update on dependencies and external factors

### Discussion Topics
- {topic_1_relevant_to_project}
- {topic_2_based_on_recent_project_notes}
- {topic_3_aligned_with_project_goals}

## 📝 Discussion Notes

### {Topic 1}
**Discussion:**
**Key Points:**
-
**Concerns Raised:**
-

### {Topic 2}
**Discussion:**
**Decisions Made:**
-

## ✅ Action Items
{linked_to_project_milestones}
- [ ] **{action_item}** - Assigned: {owner} - Due: {date} - Links to: {milestone}
- [ ] **{action_item}** - Assigned: {owner} - Due: {date} - Links to: {milestone}

## 🎯 Decisions Made
{tracked_for_project_context}
- **{decision}**: {rationale} - Impact on: {affected_milestones}
- **{decision}**: {outcome} - Timeline impact: {impact}

## 📊 Project Impact
**Milestones Affected:**
- {milestone}: {impact_description}
- {milestone}: {schedule_change}

**Next Project Actions:**
- Update project timeline based on decisions
- Communicate changes to stakeholders
- Review resource allocation

## 🔄 Follow-up
- **Next Meeting:** {date} - {agenda_preview}
- **Dependencies:** {what_needs_to_happen_before_next_meeting}
- **Stakeholder Communication:** {who_needs_updates}

---
*Auto-linked to Project: {project_name} | Notes will sync with project cache*
```

### Implementation Integration Points

**Enhanced Notes Commands:**

1. **notes-meeting.md Enhancement**
   - Add `--project PROJECT_NAME` parameter
   - Auto-populate meeting context from project data
   - Link meeting notes to project cache automatically
   - Include project milestones and team in meeting template

2. **notes-capture.md Enhancement**
   - Add project context detection from note content
   - Auto-suggest project links based on keywords
   - Update project cache with new note references
   - Extract and link action items to project milestones

**New Project Commands:**

3. **project-notes.md** - Project Notes Overview
   - Display all notes linked to a specific project
   - Show action item status and milestone connections
   - Provide project-specific note insights and summaries
   - Generate project communication based on note content

4. **project-sync.md Enhancement**
   - Include notes data in project synchronization
   - Update project status based on note content and action items
   - Sync action item completion between notes and project tracking
   - Generate alerts for overdue note action items

### Technical Implementation

**Cache File Structure Enhancement:**
```json
{
  "project_notes": [
    {
      "note_id": "meeting_2024-09-14_sprint-planning",
      "title": "Sprint Planning - Mobile App V2",
      "created_at": "2024-09-14T10:00:00Z",
      "type": "meeting",
      "file_path": "inbox/meeting_2024-09-14_sprint-planning.md",
      "summary": "Sprint planning session covering user story prioritization",
      "attendees": ["john@company.com", "sarah@company.com"],
      "action_items": [
        {
          "item": "Complete user research analysis",
          "owner": "sarah@company.com",
          "due_date": "2024-09-20",
          "linked_milestone": "User Research Complete",
          "status": "pending"
        }
      ],
      "decisions": [
        {
          "decision": "Prioritize iOS development over Android",
          "impact": "Affects development timeline and resource allocation",
          "linked_milestones": ["Development Sprint 1", "Beta Release"]
        }
      ],
      "tags": ["sprint-planning", "development", "priorities"],
      "project_references": ["mobile-app-v2"],
      "external_references": []
    }
  ],
  "action_items": [
    {
      "id": "action_001",
      "item": "Complete user research analysis",
      "source": "meeting_2024-09-14_sprint-planning",
      "owner": "sarah@company.com",
      "due_date": "2024-09-20",
      "linked_milestone": "User Research Complete",
      "status": "pending",
      "created_at": "2024-09-14T10:30:00Z"
    }
  ],
  "decisions": [
    {
      "id": "decision_001",
      "decision": "Prioritize iOS development over Android",
      "source": "meeting_2024-09-14_sprint-planning",
      "rationale": "Resource constraints and market timing",
      "impact": "Timeline acceleration, resource reallocation",
      "linked_milestones": ["Development Sprint 1", "Beta Release"],
      "created_at": "2024-09-14T10:45:00Z"
    }
  ],
  "cross_references": {
    "related_projects": ["q4-marketing-campaign"],
    "blocking_dependencies": ["design-system-update"],
    "external_systems": ["github", "figma"]
  },
  "collected_at": "2024-09-14T11:00:00Z",
  "last_sync": "2024-09-14T11:00:00Z"
}
```

**Project Context Detection Algorithm:**
```python
def detect_project_context(note_content, note_title, note_metadata):
    """Automatically detect relevant projects from note content"""

    # Load project configuration
    projects = load_projects()

    # Score projects based on relevance
    project_scores = {}

    for project_id, project_data in projects.items():
        score = 0

        # Check for explicit project name mentions
        if project_data['name'].lower() in (note_title + ' ' + note_content).lower():
            score += 50

        # Check for project tag matches
        for tag in project_data.get('tags', []):
            if tag in note_content.lower():
                score += 20

        # Check for team member mentions
        if 'owner' in project_data:
            if project_data['owner'] in note_content:
                score += 30

        # Check for milestone/deliverable mentions
        for milestone in project_data.get('milestones', []):
            if milestone['name'].lower() in note_content.lower():
                score += 25

        if score > 0:
            project_scores[project_id] = score

    # Return projects above relevance threshold
    relevant_projects = {
        project: score for project, score in project_scores.items()
        if score >= 30
    }

    return relevant_projects
```

### Error Handling & Validation

**Missing Project References:**
- Gracefully handle notes that don't match any projects
- Provide suggestions for project linking based on content analysis
- Allow manual project association through command flags

**Cache Synchronization:**
- Handle concurrent updates to project cache files
- Validate cache file structure and repair if corrupted
- Backup and restore mechanisms for cache data

**Cross-System Consistency:**
- Validate that referenced projects exist in configuration
- Check for orphaned notes references in project caches
- Maintain referential integrity between notes and projects

### Error Handling

ConfigManager provides automatic error handling for project-to-notes synchronization:

```python
from tools import ConfigManager, ConfigNotFoundError, ConfigValidationError

try:
    mgr = ConfigManager()

    # Sync project to notes cache
    mgr.sync_project_to_notes('mobile-app-v2')

    # Load synced project data
    project = mgr.get_project('mobile-app-v2')

    # Access project milestones
    for milestone in project.milestones:
        print(f"Milestone: {milestone.title}")

except KeyError as e:
    # Handle missing project
    print(f"Project not found: {e}")
    print("Check project ID and ensure it exists in projects.yaml")

except ConfigNotFoundError:
    # Handle missing configuration file
    print("Projects configuration not found. Please create projects.yaml")

except ConfigValidationError as e:
    # Handle invalid project structure
    print(f"Invalid project configuration: {e}")
    print("Check that all required fields are present and properly formatted")

except Exception as e:
    # Handle sync failures
    print(f"Synchronization failed: {e}")
    print("Notes cache may be inconsistent. Please retry sync operation")
```

**Error Scenarios:**
- **Missing Project**: KeyError with clear message about which project was not found
- **Missing Config File**: ConfigNotFoundError with guidance to create projects.yaml
- **Invalid Project**: ConfigValidationError with details about which fields are missing or malformed
- **Sync Failures**: Exception with error details and recovery guidance
- **Type Safety**: Pydantic models prevent attribute access errors at runtime

**Sync Rollback:**
- ConfigManager sync operations are atomic
- If sync fails, notes cache remains in previous valid state
- No partial updates to ensure data consistency

### Best Practices

1. **Seamless User Experience:**
   - Auto-detect project context whenever possible
   - Provide intelligent defaults and suggestions
   - Make explicit project association optional but easy
   - Maintain backward compatibility with existing notes workflow
   - Use ConfigManager's automatic sync for consistency

2. **Data Integrity:**
   - Use ConfigManager's atomic sync operations
   - Sync project data before accessing notes cache
   - Rely on Pydantic validation for data consistency
   - Archive old references while maintaining historical context

3. **Performance Optimization:**
   - Leverage ConfigManager's caching (<10ms cached reads)
   - Use incremental updates via sync_project_to_notes()
   - Implement lazy loading for large project note histories
   - Cache relationship data is automatically maintained

4. **Extensibility:**
   - Design integration points for future note types and project features
   - Support plugin architecture for custom project-note workflows
   - Enable API access for external integrations
   - Use type-safe ConfigManager methods for reliability

5. **Configuration Management:**
   - Always use ConfigManager for project access
   - Rely on automatic synchronization for consistency
   - Use type-safe field access to prevent runtime errors
   - Handle missing configurations gracefully with proper error messages

Remember: Effective notes-project integration creates a unified knowledge system where project context enhances note-taking and notes provide rich context for project management. ConfigManager ensures this integration is automatic, type-safe, and consistent.
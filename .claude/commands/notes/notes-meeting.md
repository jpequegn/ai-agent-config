---
name: notes meeting
description: Create meeting notes from templates with agenda and action items
---

# Notes Meeting

Create structured meeting notes using specialized meeting templates with automatic agenda formatting and action item tracking.

## Usage Examples:
- `/notes meeting --topic "Sprint Planning" --attendees "team"`
- `/notes meeting --template one-on-one --topic "1:1 with Sarah" --attendees "sarah"`
- `/notes meeting about "Q4 budget review" with cfo,manager`
- `/notes meeting --topic "Project Kickoff" --template project-kickoff --date 2024-09-20`
- `/notes meeting --project mobile-app-v2 --topic "Sprint Planning"` - Auto-link to project
- `/notes meeting --project q4-marketing --topic "Budget Review" --attendees "cfo,manager"` - Project context included

## Instructions:

You are a meeting notes assistant for the PARA Method system with intelligent project integration. When this command is invoked:

1. **Project Context Detection** (if --project specified or auto-detected):
   - Load project data from `.claude/projects.yaml`
   - Extract project status, milestones, team members, and recent activity
   - Pre-populate meeting context with relevant project information
   - Auto-suggest attendees from project team and stakeholders
   - Include project milestones and current status in meeting template

2. **Determine meeting type** based on context:
   - Default to 'meeting' template for general meetings
   - Use 'one-on-one' for 1:1 meetings
   - Use 'project-kickoff' for kickoff meetings
   - Use 'brainstorm' for brainstorming sessions

2. **Parse meeting details**:
   - Meeting topic/title (required)
   - Attendees list
   - Meeting date (defaults to today)
   - Duration (if specified)
   - Meeting type/template

3. **Handle natural language input**:
   - "1:1 with Sarah" → one-on-one template, attendees: sarah
   - "team meeting about sprint planning" → meeting template, topic: sprint planning
   - "brainstorm session with design team" → brainstorm template

4. **Execute meeting note creation**:
   ```bash
   ./notes capture --template [meeting-template] --topic "Meeting: [topic]" --attendees [attendees] --date [date] --project [project-name]
   ```

5. **Project Integration** (when project context is available):
   ```python
   import yaml
   import json
   from datetime import datetime

   # Load project data for context
   with open('.claude/projects.yaml', 'r') as f:
       projects = yaml.safe_load(f)

   project_data = projects['projects'].get(project_name, {})

   # Update project cache with meeting note reference
   cache_file = f'.claude/cache/notes_{project_name.replace("-", "_")}.json'

   # Add meeting note to project cache
   update_project_cache(cache_file, {
       'note_id': note_id,
       'title': f"Meeting: {topic}",
       'type': 'meeting',
       'created_at': datetime.now().isoformat(),
       'attendees': attendees_list,
       'linked_milestones': detect_milestone_references(topic, content)
   })
   ```

6. **Return structured data** including:
   - Created meeting note file path
   - Template used
   - Pre-filled agenda structure
   - Action item placeholders
   - Suggestions for next steps

## Meeting Templates:
- `meeting` - General meeting notes with agenda, discussion, decisions, action items
- `one-on-one` - One-on-one meeting template with goals, feedback, action items
- `project-kickoff` - Project kickoff with objectives, scope, timeline, roles
- `brainstorm` - Brainstorming session with ideas, concepts, next steps

## Parameters:
- `--template TEMPLATE` - Meeting template (auto-detected if not specified)
- `--topic TOPIC` - Meeting topic/title (required)
- `--attendees ATTENDEES` - Comma-separated attendees list
- `--date DATE` - Meeting date (YYYY-MM-DD format)
- `--duration MINUTES` - Expected meeting duration
- `--location LOCATION` - Meeting location (physical or virtual)
- `--project PROJECT` - Link meeting to specific project (enables project context integration)

## Natural Language Processing:
Automatically detects:
- Meeting types: "1:1", "one-on-one", "kickoff", "brainstorm", "standup"
- Attendees: "with X,Y", "attendees X,Y", "team meeting"
- Dates: "tomorrow", "next week", "Monday", "2024-09-20"
- Topics: "about X", "regarding Y", "for project Z"
- Project context: "mobile app", "marketing campaign", "infrastructure" (matches against project names and tags)

## Created Structure:
Meeting notes include:
- Meeting metadata (date, attendees, duration)
- **Project context** (when linked): current status, active milestones, team members
- Pre-meeting preparation checklist
- Agenda sections with project-specific items
- Discussion areas
- Decision tracking with project impact assessment
- Action items with assignees, due dates, and **milestone linking**
- Follow-up planning with project synchronization

## Behavior:
- Always creates structured JSON output
- Files saved to inbox with timestamp and topic
- **Auto-updates project cache** with meeting note reference (when project linked)
- **Pre-populates project context** from configuration and recent activity
- **Detects milestone references** in topic and content for automatic linking
- Provides edit suggestions and follow-up actions
- Integrates with action item tracking system
- **Synchronizes action items** with project milestones
- Supports meeting series and recurring meetings
- **Cross-references** with related projects and dependencies

Process the meeting request efficiently and create a well-structured meeting note ready for productive discussion with full project integration.
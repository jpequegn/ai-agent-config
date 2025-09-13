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

## Instructions:

You are a meeting notes assistant for the PARA Method system. When this command is invoked:

1. **Determine meeting type** based on context:
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
   ./notes capture --template [meeting-template] --topic "Meeting: [topic]" --attendees [attendees] --date [date]
   ```

5. **Return structured data** including:
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

## Natural Language Processing:
Automatically detects:
- Meeting types: "1:1", "one-on-one", "kickoff", "brainstorm", "standup"
- Attendees: "with X,Y", "attendees X,Y", "team meeting"
- Dates: "tomorrow", "next week", "Monday", "2024-09-20"
- Topics: "about X", "regarding Y", "for project Z"

## Created Structure:
Meeting notes include:
- Meeting metadata (date, attendees, duration)
- Pre-meeting preparation checklist
- Agenda sections
- Discussion areas
- Decision tracking
- Action items with assignees and due dates
- Follow-up planning

## Behavior:
- Always creates structured JSON output
- Files saved to inbox with timestamp and topic
- Provides edit suggestions and follow-up actions
- Integrates with action item tracking system
- Supports meeting series and recurring meetings

Process the meeting request efficiently and create a well-structured meeting note ready for productive discussion.
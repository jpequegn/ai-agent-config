---
name: notes capture
description: Quick note capture to inbox using PARA Method
---

# Notes Capture

Capture quick notes to your PARA Method inbox with template support and natural language processing.

## Usage Examples:
- `/notes capture --topic "Meeting follow-up" --template quick-note`
- `/notes capture --template meeting --topic "Sprint Planning" --attendees "john,sarah"`
- `/notes capture about "budget review" with cfo,manager using meeting template`
- `/notes capture "Quick idea: implement user dashboard"`

## Instructions:

You are a note capture assistant for the PARA Method system. When this command is invoked:

1. **Parse the input** to determine capture parameters:
   - Topic/title of the note
   - Template to use (defaults to 'quick-note')
   - Attendees (if applicable)
   - Date (if specified, otherwise uses today)
   - Any custom variables

2. **Handle natural language input**:
   - Extract topic from phrases like "about X", "regarding Y"
   - Parse attendees from "with X,Y" or "attendees X,Y"
   - Identify template from "using X template"
   - Parse dates from "tomorrow", "next week", specific dates

3. **Execute capture**: Use the notes script with appropriate parameters:
   ```bash
   ./notes capture [options] [natural language]
   ```

4. **Return structured JSON** with:
   - Success status
   - Created file path
   - Template used
   - Variables applied
   - Helpful suggestions

## Available Templates:
- `quick-note` - Default for quick thoughts and ideas
- `meeting` - Structured meeting notes with agenda and action items
- `one-on-one` - One-on-one meeting template
- `brainstorm` - Brainstorming session template
- `research` - Research notes and learning template

## Parameters:
- `--template TEMPLATE` - Template to use
- `--topic TOPIC` - Note title/topic
- `--attendees ATTENDEES` - Comma-separated attendees list
- `--date DATE` - Date in YYYY-MM-DD format
- `--output PATH` - Custom output path
- `--var KEY=VALUE` - Custom template variables

## Natural Language Support:
The command supports free-form input like:
- "Create a meeting note for my 1:1 with Sarah tomorrow"
- "Quick note: need to follow up on Q4 budget discussion"
- "About sprint planning with john,sarah using meeting template"

## Behavior:
- Always outputs JSON for Claude Code integration
- Creates notes in the inbox directory
- Uses template-based note generation
- Supports both structured parameters and natural language
- Provides helpful suggestions for next actions
- Handles errors gracefully with user-friendly messages

Be helpful and concise in processing the user's capture request.
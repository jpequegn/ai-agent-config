# PARA Notes API Reference

Complete API specification for the PARA Method note-taking system with Claude Code integration.

## Version: 1.0.0

## Overview

The PARA Notes API provides a unified interface for creating, managing, and organizing notes using the PARA Method (Projects, Areas, Resources, Archive). All commands return structured JSON responses optimized for Claude Code integration.

## Base Command

All commands are accessed through the `./notes` script:

```bash
./notes [COMMAND] [OPTIONS] [NATURAL_LANGUAGE_INPUT]
```

## Global Options

- `--json` - Force JSON output format (default)
- `--format {json,text}` - Output format selection
- `-h, --help` - Show help information

## Commands Reference

### 1. capture - Create Notes from Templates

Create new notes using predefined templates with support for natural language input.

**Syntax:**
```bash
./notes capture [--template TEMPLATE] [--topic TOPIC] [--attendees ATTENDEES] [--date DATE] [--output OUTPUT] [--var VAR] [NATURAL_INPUT...]
```

**Parameters:**
- `--template TEMPLATE` - Template to use (default: quick-note)
  - Available: `brainstorm`, `meeting`, `one-on-one`, `quick-note`, `research`, `project-kickoff`
- `--topic TOPIC` - Note topic/title
- `--attendees ATTENDEES` - Comma-separated attendees list
- `--date DATE` - Date in YYYY-MM-DD format (default: today)
- `--output, -o OUTPUT` - Custom output file path
- `--var VAR` - Custom template variables (key=value format)
- `NATURAL_INPUT` - Free-form natural language input

**Natural Language Patterns:**
- `about "TOPIC"` - Sets the topic
- `with USER1,USER2` - Sets attendees
- `using TEMPLATE template` - Sets template
- `on DATE` - Sets date

**Examples:**
```bash
# Basic usage
./notes capture --template meeting --topic "Sprint Planning" --attendees "john,sarah"

# Natural language
./notes capture about "budget review" with cfo,manager using meeting template

# Custom variables
./notes capture --template project-kickoff --var project="New Website" --var deadline="2024-12-01"
```

**Response Schema:**
```json
{
  "success": true,
  "command": "capture",
  "message": "Created note: inbox/2024-09-13-1025_sprint-planning.md",
  "data": {
    "file_path": "inbox/2024-09-13-1025_sprint-planning.md",
    "template": "meeting",
    "variables": {
      "title": "Sprint Planning",
      "attendees": "john,sarah",
      "date": "2024-09-13"
    }
  },
  "suggestions": [
    "Edit with: code inbox/2024-09-13-1025_sprint-planning.md",
    "Process with: /notes research --file inbox/2024-09-13-1025_sprint-planning.md"
  ],
  "error_details": null
}
```

### 2. process-inbox - Batch Process Inbox Notes

Process multiple notes in the inbox directory with PARA categorization suggestions.

**Syntax:**
```bash
./notes process-inbox [--directory DIRECTORY] [--pattern PATTERN] [--auto-suggest] [--batch BATCH]
```

**Parameters:**
- `--directory DIRECTORY` - Directory to process (default: inbox)
- `--pattern PATTERN` - File pattern to match (default: *.md)
- `--auto-suggest` - Enable PARA category suggestions
- `--batch BATCH` - Limit number of notes to process

**Examples:**
```bash
# Process all inbox notes with suggestions
./notes process-inbox --auto-suggest

# Process limited batch
./notes process-inbox --auto-suggest --batch 5

# Process specific directory
./notes process-inbox --directory "temp-notes" --pattern "meeting-*.md"
```

**Response Schema:**
```json
{
  "success": true,
  "command": "process-inbox",
  "message": "Processed 5 notes from inbox",
  "data": {
    "notes_processed": 5,
    "total_notes": 12,
    "total_words": 2847,
    "action_items": {
      "total": 23,
      "completed": 3,
      "pending": 20
    },
    "suggestions": {
      "inbox/meeting-notes.md": "projects",
      "inbox/research.md": "resources"
    }
  },
  "suggestions": [
    "Review suggestions with: /notes review --directory inbox",
    "Find action items with: /notes follow-up --directory inbox"
  ],
  "error_details": null
}
```

### 3. research - Analyze and Research Notes

Analyze existing notes and optionally expand topics with related information.

**Syntax:**
```bash
./notes research [--file FILE] [--expand-topics] [--graceful]
```

**Parameters:**
- `--file FILE` - Specific note file to analyze
- `--expand-topics` - Find and suggest related topics
- `--graceful` - Handle malformed notes gracefully

**Examples:**
```bash
# Analyze specific file
./notes research --file "inbox/project-meeting.md"

# Analyze with topic expansion
./notes research --file "notes/ai-research.md" --expand-topics

# Graceful handling of malformed notes
./notes research --file "problematic-note.md" --graceful
```

**Response Schema:**
```json
{
  "success": true,
  "command": "research",
  "message": "Analyzed note: inbox/project-meeting.md",
  "data": {
    "file_path": "inbox/project-meeting.md",
    "analysis": {
      "word_count": 432,
      "estimated_read_time": 2,
      "action_items": 5,
      "attendees": ["john", "sarah", "mike"],
      "dates": ["2024-09-13", "2024-09-20"],
      "tags": ["meeting", "project", "planning"]
    },
    "suggestions": {
      "category": "projects",
      "related_topics": ["sprint planning", "project management", "team coordination"],
      "next_actions": ["schedule follow-up", "assign action items"]
    }
  },
  "suggestions": [
    "Move to projects: /notes categorize --file inbox/project-meeting.md --category projects",
    "Find related notes: /notes find --query 'project planning'"
  ],
  "error_details": null
}
```

### 4. find - Search Notes

Search for notes using text queries, date ranges, and other filters.

**Syntax:**
```bash
./notes find [--query QUERY] [--date-range RANGE] [--directory DIRECTORY] [--limit LIMIT]
```

**Parameters:**
- `--query QUERY` - Text search query
- `--date-range RANGE` - Date range filter: `today`, `yesterday`, `last-week`, `last-month`
- `--directory DIRECTORY` - Directory to search in
- `--limit LIMIT` - Maximum number of results

**Examples:**
```bash
# Text search
./notes find --query "budget planning"

# Date-based search
./notes find --date-range last-week

# Combined search
./notes find --query "meeting" --date-range last-month --limit 10
```

**Response Schema:**
```json
{
  "success": true,
  "command": "find",
  "message": "Found 8 notes matching criteria",
  "data": {
    "query": "budget planning",
    "total_results": 8,
    "results": [
      {
        "file_path": "projects/q4-budget.md",
        "title": "Q4 Budget Planning",
        "created": "2024-09-10",
        "category": "projects",
        "excerpt": "Meeting notes for Q4 budget planning session with finance team...",
        "relevance_score": 0.92
      }
    ],
    "search_metadata": {
      "search_time_ms": 45,
      "directories_searched": ["inbox", "projects", "areas", "resources"]
    }
  },
  "suggestions": [
    "Refine search with: /notes find --query 'budget planning Q4'",
    "Create new note: /notes capture --topic 'Budget Planning Follow-up'"
  ],
  "error_details": null
}
```

### 5. follow-up - Manage Action Items

Find and manage action items across all notes.

**Syntax:**
```bash
./notes follow-up [--status STATUS] [--assignee ASSIGNEE] [--directory DIRECTORY]
```

**Parameters:**
- `--status STATUS` - Filter by status: `all`, `overdue`, `pending`, `completed`
- `--assignee ASSIGNEE` - Filter by assignee name
- `--directory DIRECTORY` - Directory to search in

**Examples:**
```bash
# Find all overdue items
./notes follow-up --status overdue

# Find items assigned to specific person
./notes follow-up --assignee "john"

# All pending items
./notes follow-up --status pending
```

**Response Schema:**
```json
{
  "success": true,
  "command": "follow-up",
  "message": "Found 12 action items",
  "data": {
    "filter_criteria": {
      "status": "overdue",
      "assignee": null
    },
    "total_items": 12,
    "items": [
      {
        "id": "action_1",
        "text": "Review budget proposal",
        "assignee": "john",
        "due_date": "2024-09-10",
        "status": "overdue",
        "source_file": "projects/budget-meeting.md",
        "line_number": 23,
        "priority": "high"
      }
    ],
    "summary": {
      "overdue": 12,
      "pending": 45,
      "completed": 123
    }
  },
  "suggestions": [
    "Create follow-up meeting: /notes capture --template meeting --topic 'Action Items Review'",
    "Filter by assignee: /notes follow-up --assignee 'john'"
  ],
  "error_details": null
}
```

### 6. prep - Prepare Meeting Notes

Create and prepare meeting notes with agenda templates.

**Syntax:**
```bash
./notes prep [--topic TOPIC] [--attendees ATTENDEES] [--output OUTPUT]
```

**Parameters:**
- `--topic TOPIC` - Meeting topic/title
- `--attendees ATTENDEES` - Comma-separated attendees list
- `--output OUTPUT` - Custom output file path

**Examples:**
```bash
# Basic meeting prep
./notes prep --topic "Sprint Review" --attendees "team,stakeholders"

# Custom output location
./notes prep --topic "Budget Review" --attendees "cfo,manager" --output "meetings/budget-review.md"
```

**Response Schema:**
```json
{
  "success": true,
  "command": "prep",
  "message": "Created meeting preparation: inbox/2024-09-13-1030_sprint-review.md",
  "data": {
    "file_path": "inbox/2024-09-13-1030_sprint-review.md",
    "meeting_info": {
      "topic": "Sprint Review",
      "attendees": ["team", "stakeholders"],
      "date": "2024-09-13",
      "template_used": "meeting"
    },
    "preparation_items": [
      "agenda prepared",
      "materials shared",
      "participants notified"
    ]
  },
  "suggestions": [
    "Add agenda items to the note",
    "Set meeting reminder: /notes capture --topic 'Meeting reminder: Sprint Review'"
  ],
  "error_details": null
}
```

### 7. list-templates - Template Management

List and manage available note templates.

**Syntax:**
```bash
./notes list-templates
```

**Parameters:**
None - this command lists all available templates

**Examples:**
```bash
# List all templates
./notes list-templates
```

**Response Schema:**
```json
{
  "success": true,
  "command": "list-templates",
  "message": "Found 6 available templates",
  "data": {
    "templates": {
      "Built-in": [
        {
          "name": "brainstorm",
          "description": "Brainstorming session template"
        },
        {
          "name": "meeting",
          "description": "General meeting notes template"
        },
        {
          "name": "one-on-one",
          "description": "One-on-one meeting template"
        },
        {
          "name": "quick-note",
          "description": "Quick capture template for ideas and thoughts"
        },
        {
          "name": "research",
          "description": "Research notes and learning template"
        }
      ],
      "Custom": [
        {
          "name": "project-kickoff",
          "description": "Custom template: project-kickoff"
        }
      ]
    },
    "total": 6
  },
  "suggestions": [
    "Create note: /notes capture --template meeting --topic 'Your Topic'",
    "View template details: /notes template-info --name meeting"
  ],
  "error_details": null
}
```

## Error Response Format

All commands use a standardized error response format:

```json
{
  "success": false,
  "command": "capture",
  "message": "Template 'invalid-template' not found",
  "data": null,
  "suggestions": [
    "Use /notes list-templates to see available templates",
    "Try with --template meeting or --template quick-note"
  ],
  "error_details": "TEMPLATE_NOT_FOUND: Template 'invalid-template' not found in built-in or custom templates"
}
```

## Response Field Definitions

### Standard Fields (All Responses)
- `success` (boolean) - Whether the command executed successfully
- `command` (string) - The command that was executed
- `message` (string) - Human-readable status message
- `data` (object|null) - Command-specific data payload
- `suggestions` (array) - Helpful next action suggestions
- `error_details` (string|null) - Detailed error information (null on success)

### Data Field Contents
The `data` field contains command-specific information:
- File paths for created/modified files
- Processing statistics and metrics
- Analysis results and insights
- Search results and metadata
- Template information
- Action item details

### Suggestions Field
The `suggestions` array provides:
- Follow-up commands to run
- Alternative approaches to try
- Related actions that might be helpful
- Troubleshooting guidance

## Natural Language Support

All commands support natural language input patterns. See [Natural Language Guide](natural-language-guide.md) for complete specification.

## Error Codes

See [Error Codes Reference](error-codes.md) for complete list of error conditions and handling.

## Integration

For Claude Code integration patterns and examples, see [Claude Code Integration Guide](claude-code-guide.md).
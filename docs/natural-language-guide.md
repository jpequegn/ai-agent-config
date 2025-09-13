# Natural Language Processing Guide

The PARA Notes system supports natural language input for more intuitive note creation and management. This guide documents the patterns, processing rules, and examples for natural language support.

## Overview

Natural language processing (NLP) allows users to provide free-form text input that is intelligently parsed to extract structured parameters. This makes the system more conversational and user-friendly, especially in Claude Code interactions.

## Supported Commands

The following commands support natural language input:
- `capture` - Primary NLP support with full parameter extraction
- `find` - Basic query interpretation
- `prep` - Meeting preparation with topic/attendee extraction

## Pattern Matching System

### Processing Order

Natural language parsing follows a specific order to avoid parameter conflicts:

1. **Template Detection** - Extract template specifications first
2. **Topic/Title Extraction** - Identify the main subject
3. **Attendee Parsing** - Extract participant lists
4. **Date Recognition** - Process temporal references
5. **Cleanup** - Remove parsed elements to prevent overlap

### Template Pattern Recognition

**Patterns:**
- `using TEMPLATE template`
- `template: TEMPLATE`
- `as a TEMPLATE`

**Examples:**
```
"using meeting template" → template: "meeting"
"using one-on-one template" → template: "one-on-one"
"template: brainstorm" → template: "brainstorm"
"as a research note" → template: "research"
```

**Processing Logic:**
```regex
using\s+(\w+)\s+template      # "using meeting template"
template\s*:?\s*(\w+)         # "template: meeting"
as\s+(?:a\s+)?(\w+)          # "as a meeting" or "as meeting"
```

### Topic/Title Extraction

**Patterns:**
- `about "TOPIC"`
- `about TOPIC`
- `topic: TOPIC`
- `regarding TOPIC`
- `for TOPIC`

**Examples:**
```
'about "sprint planning"' → topic: "sprint planning"
'about budget review' → topic: "budget review"
'topic: Q4 goals' → topic: "Q4 goals"
'regarding the new project' → topic: "the new project"
'for team building session' → topic: "team building session"
```

**Processing Logic:**
```regex
about\s+"([^"]+)"             # Quoted topic (highest priority)
about\s+([^,\n]+)            # Unquoted topic
topic\s*:?\s*"([^"]+)"       # Quoted topic with label
topic\s*:?\s*([^,\n]+)       # Unquoted topic with label
regarding\s+([^,\n]+)        # Regarding format
for\s+([^,\n]+)              # For format
```

**Cleanup Rules:**
- Remove "with ATTENDEES" from extracted topics
- Remove template references from topics
- Trim whitespace and quotes

### Attendee Parsing

**Patterns:**
- `with USER1,USER2`
- `attendees: USER1,USER2`
- `participants: USER1,USER2`

**Examples:**
```
'with john,sarah' → attendees: "john,sarah"
'with alice, bob, charlie' → attendees: "alice,bob,charlie"
'attendees: team leads' → attendees: "team leads"
'participants john and sarah' → attendees: "john and sarah"
```

**Processing Logic:**
```regex
with\s+([^,\n]+(?:,\s*[^,\n]+)*)     # "with john,sarah"
attendees?\s*:?\s*([^,\n]+(?:,\s*[^,\n]+)*)  # "attendees: john,sarah"
participants?\s*:?\s*([^,\n]+(?:,\s*[^,\n]+)*) # "participants: john,sarah"
```

**Cleanup Rules:**
- Remove template references: `sarah using meeting template` → `sarah`
- Remove date references: `john,sarah tomorrow` → `john,sarah`
- Normalize spacing: `john , sarah` → `john,sarah`

### Date Recognition

**Supported Formats:**
- **Relative dates**: "today", "tomorrow", "yesterday"
- **Relative periods**: "next week", "last month", "next Monday"
- **ISO dates**: "2024-09-13"
- **Natural dates**: "September 13", "Sep 13, 2024"

**Patterns:**
- `on DATE`
- `for DATE`
- `date: DATE`

**Examples:**
```
'on tomorrow' → date: "2024-09-14" (relative to current date)
'for next week' → date: "2024-09-20" (next Monday)
'date: 2024-12-25' → date: "2024-12-25"
'on September 15' → date: "2024-09-15"
```

**Processing Logic:**
```regex
on\s+(\d{4}-\d{2}-\d{2})           # ISO format
on\s+(tomorrow|today|yesterday)     # Relative days
for\s+(\d{4}-\d{2}-\d{2})          # ISO format with "for"
date\s*:?\s*(\d{4}-\d{2}-\d{2})    # Explicit date label
```

**Date Resolution:**
- `today` → Current date
- `tomorrow` → Current date + 1 day
- `yesterday` → Current date - 1 day
- `next week` → Current date + 7 days (or next Monday)
- `next Monday` → Date of next Monday

## Advanced Parsing Features

### Context-Aware Template Detection

The system can infer templates based on content patterns:

**Meeting Indicators:**
- "1:1", "one-on-one" → `one-on-one` template
- "standup", "daily" → `meeting` template
- "brainstorm", "ideation" → `brainstorm` template
- "kickoff", "project start" → `project-kickoff` template

**Content Analysis:**
- Presence of attendee lists suggests `meeting` template
- Research-related keywords suggest `research` template
- Action-oriented content suggests `quick-note` template

### Smart Content Extraction

When processing natural language input, the system extracts:

1. **Implicit Action Items**
   - "need to follow up" → Creates action item
   - "must complete by Friday" → Action with due date
   - "assign to john" → Action with assignee

2. **Project References**
   - "Q4 budget project" → Links to Q4 budget project
   - "website redesign" → Project context

3. **Urgency Indicators**
   - "urgent", "ASAP", "high priority" → Priority flags
   - "by tomorrow", "end of week" → Due date extraction

## Error Handling

### Ambiguous Input

When natural language input is ambiguous:

```json
{
  "success": true,
  "command": "capture",
  "message": "Created note with best-guess interpretation",
  "data": { ... },
  "suggestions": [
    "If the topic should be 'project planning' instead of 'project', use: /notes capture --topic 'project planning'",
    "To specify attendees more clearly, use: --attendees 'john,sarah'"
  ],
  "warnings": [
    "Parsed attendees as 'john,sarah tomorrow' - date may have been included"
  ]
}
```

### Parsing Failures

When parsing completely fails:

```json
{
  "success": false,
  "command": "capture",
  "message": "Could not parse natural language input",
  "error_details": "PARSE_ERROR: No recognizable patterns found in input",
  "suggestions": [
    "Try using structured parameters: --topic 'your topic' --attendees 'names'",
    "Example: /notes capture --template meeting --topic 'Sprint Planning'"
  ]
}
```

## Examples by Use Case

### Meeting Creation

**Input:** `"Create a meeting note about sprint planning with john,sarah using meeting template"`

**Processing:**
1. Template: "using meeting template" → `meeting`
2. Topic: "about sprint planning" → `sprint planning`
3. Attendees: "with john,sarah" → `john,sarah`
4. Cleanup: Remove parsed elements to prevent conflicts

**Result:**
```bash
./notes capture --template meeting --topic "sprint planning" --attendees "john,sarah"
```

### Quick Notes

**Input:** `"Quick note: need to follow up on budget discussion"`

**Processing:**
1. No template specified → defaults to `quick-note`
2. Content after ":" extracted as topic
3. Action item detected: "need to follow up"

**Result:**
```bash
./notes capture --template quick-note --topic "need to follow up on budget discussion"
```

### Research Notes

**Input:** `"Research about AI trends for next week"`

**Processing:**
1. Template inferred from "Research" → `research`
2. Topic: "about AI trends" → `AI trends`
3. Date: "for next week" → calculated date

**Result:**
```bash
./notes capture --template research --topic "AI trends" --date "2024-09-20"
```

## Claude Code Integration

### Conversational Patterns

**User Intent → NLP Processing → Command Execution → Formatted Response**

1. **User:** "I need to capture notes from my meeting with the design team about the new website"

2. **Claude Code Processing:**
   - Extracts: template=meeting, topic="new website", attendees="design team"
   - Calls: `/notes capture about "new website" with design team using meeting template`

3. **System Response:** JSON with file path and suggestions

4. **Claude Code Formatting:** "I've created your meeting note for 'new website' with the design team. The note is saved as `inbox/2024-09-13-1025_new-website.md`. Would you like me to help you add agenda items?"

### Multi-Turn Interactions

Natural language processing supports multi-turn conversations:

1. User: "Create a quick note"
2. Claude: Asks for topic
3. User: "about the server maintenance"
4. Processing: Combines context from previous turns

## Implementation Notes

### Performance Considerations

- Regex patterns are processed in priority order
- Parsing stops at first successful match per category
- Complex patterns are cached for repeated use
- Date calculations are memoized for session duration

### Extensibility

The NLP system is designed for easy extension:
- New patterns can be added to existing categories
- New categories can be added with custom processing
- Template detection rules can be updated
- Date formats can be extended

### Testing

Natural language patterns are tested with:
- Unit tests for individual regex patterns
- Integration tests for full input processing
- Edge case testing for ambiguous inputs
- Performance testing for complex input parsing
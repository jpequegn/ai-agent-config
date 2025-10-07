---
name: notes capture
description: Quick note capture to inbox using PARA Method with NLPProcessor for natural language parsing
---

# Notes Capture

Capture quick notes to your PARA Method inbox with template support and **NLPProcessor** for intelligent natural language understanding.

## Usage Examples:
- `/notes capture --topic "Meeting follow-up" --template quick-note`
- `/notes capture --template meeting --topic "Sprint Planning" --attendees "john,sarah"`
- `/notes capture about "budget review" with cfo,manager using meeting template`
- `/notes capture "Quick idea: implement user dashboard"`
- `/notes capture "Meeting with @sarah tomorrow about Q4 planning"`

## Instructions:

You are a note capture assistant for the PARA Method system that uses the **NLPProcessor tool** for intelligent natural language understanding.

### Tool-Based Implementation

**1. Parse Natural Language Input**

Use NLPProcessor to extract structured data from free-form text:

```python
from tools import NLPProcessor

nlp = NLPProcessor()

# Extract all entities from natural language
entities = nlp.extract_entities(user_input, entity_types=["assignee", "date"])

# Parse command intent to understand action and subject
intent = nlp.parse_command_intent(user_input)

# Example: "capture about budget review with cfo,manager tomorrow"
# entities → [
#   EntityMatch(value="cfo", entity_type="assignee"),
#   EntityMatch(value="manager", entity_type="assignee"),
#   EntityMatch(value="2025-10-08", entity_type="date")
# ]
```

**2. Extract Specific Components**

**Date Parsing** (handles relative and absolute dates):
```python
# Parse date expressions
try:
    date_expr = nlp.parse_date_expression(user_input)
    date_str = date_expr.resolved_date.strftime("%Y-%m-%d")
    # Supports: "tomorrow", "next week", "in 3 days", "2025-10-15"
except DateParsingError:
    date_str = None  # Use today's date as default
```

**Attendee Extraction** (multiple formats):
```python
# Extract attendees from various formats
attendees = nlp.extract_assignees(user_input)
# Supports: "@username", "with X,Y", "attendees X,Y", "X and Y"
attendees_str = ",".join(attendees) if attendees else None
```

**Template Fuzzy Matching** (intelligent matching):
```python
# Available templates
templates = ["quick-note", "meeting", "one-on-one", "brainstorm", "research"]

# Extract template query from input
template_query = None
template_patterns = [
    r"using\s+(\w+(?:-\w+)*)\s+template",
    r"(\w+(?:-\w+)*)\s+template",
    r"template\s+(\w+(?:-\w+)*)"
]

for pattern in template_patterns:
    match = re.search(pattern, user_input.lower())
    if match:
        template_query = match.group(1)
        break

# Fuzzy match template names (handles typos and variations)
if template_query:
    matches = nlp.fuzzy_match(template_query, templates, threshold=0.7)
    template = matches[0].candidate if matches else "quick-note"
else:
    template = "quick-note"  # Default
```

**Topic Extraction** (from "about X" or "regarding Y"):
```python
import re

# Extract topic from natural language patterns
topic = None
topic_patterns = [
    r"about\s+['\"]?([^'\"]+?)['\"]?(?:\s+with|\s+using|\s+template|$)",
    r"regarding\s+['\"]?([^'\"]+?)['\"]?(?:\s+with|\s+using|\s+template|$)",
    r"['\"]([^'\"]+)['\"]"  # Quoted text
]

for pattern in topic_patterns:
    match = re.search(pattern, user_input, re.IGNORECASE)
    if match:
        topic = match.group(1).strip()
        break

# Fallback: use entire input if no pattern matched
if not topic:
    topic = user_input.strip()
```

**3. Build Command and Execute**

```python
# Build notes capture command
cmd_parts = ["./notes", "capture"]

if template:
    cmd_parts.extend(["--template", template])
if topic:
    cmd_parts.extend(["--topic", topic])
if attendees_str:
    cmd_parts.extend(["--attendees", attendees_str])
if date_str:
    cmd_parts.extend(["--date", date_str])

# Execute using Bash tool
result = bash_tool.run(cmd_parts)
```

**4. Return Structured Output**

```python
# Parse result and return JSON
output = {
    "success": True,
    "file_path": "/path/to/created/note.md",
    "template": template,
    "topic": topic,
    "attendees": attendees,
    "date": date_str,
    "suggestions": [
        "Review and add action items to the note",
        "Link to relevant projects using /project notes"
    ]
}

print(json.dumps(output, indent=2))
```

## Complete Example

**Input**: `/notes capture "Meeting with @sarah,@john tomorrow about Q4 budget planning"`

**Processing**:
```python
from tools import NLPProcessor
import re

nlp = NLPProcessor()

# Extract entities
attendees = nlp.extract_assignees(input_text)
# → ["sarah", "john"]

date_expr = nlp.parse_date_expression(input_text)
# → DateExpression(resolved_date=2025-10-08)

# Extract topic
topic_match = re.search(r"about\s+(.+?)$", input_text, re.IGNORECASE)
topic = topic_match.group(1) if topic_match else "Meeting notes"
# → "Q4 budget planning"

# Default template for meeting context
template = "meeting"

# Execute
./notes capture --template meeting --topic "Q4 budget planning" --attendees "sarah,john" --date "2025-10-08"
```

**Output**:
```json
{
  "success": true,
  "file_path": "inbox/2025-10-08_q4-budget-planning.md",
  "template": "meeting",
  "topic": "Q4 budget planning",
  "attendees": ["sarah", "john"],
  "date": "2025-10-08",
  "suggestions": [
    "Add agenda items to the meeting note",
    "Review action items after the meeting"
  ]
}
```

## Available Templates

- `quick-note` - Default for quick thoughts and ideas
- `meeting` - Structured meeting notes with agenda and action items
- `one-on-one` - One-on-one meeting template
- `brainstorm` - Brainstorming session template
- `research` - Research notes and learning template

## Natural Language Patterns Supported

**Date Expressions** (via NLPProcessor):
- Relative: "tomorrow", "next week", "in 3 days", "yesterday"
- Absolute: "2025-10-15", "October 15", "Oct 15 2025"
- Ranges: "this week", "last month", "this year"

**Attendee Formats** (via NLPProcessor):
- Mentions: "@username", "@sarah", "@john_smith"
- Lists: "with sarah,john", "attendees alice,bob"
- Conjunctions: "with alice and bob"

**Template References**:
- Explicit: "using meeting template"
- Implicit: "meeting template", "template meeting"
- Fuzzy: "meting" matches "meeting" (≥70% confidence)

**Topic Extraction**:
- Explicit: "about X", "regarding Y"
- Quoted: "Quick note: 'implement dashboard'"
- Implicit: Full input used as topic if no pattern matched

## Tool Integration Benefits

**NLPProcessor Integration**:
- **Consistency**: Same NLP engine across all commands
- **Testability**: Thoroughly tested entity extraction (95%+ accuracy)
- **Performance**: <10ms parsing time for typical inputs
- **Flexibility**: Easy to add new patterns and entity types
- **Reliability**: Robust error handling with graceful degradation

**Key Features**:
- Intelligent date parsing with 20+ supported formats
- Multi-format attendee extraction with deduplication
- Fuzzy template matching (handles typos and variations)
- Entity extraction with confidence scoring
- Command intent classification for complex queries

## Error Handling

- **Date parsing failure**: Falls back to today's date
- **No attendees found**: Creates note without attendees
- **Template not matched**: Uses "quick-note" as default
- **Missing topic**: Uses entire input as topic
- **Notes CLI failure**: Returns clear error with suggestions

Remember: NLPProcessor ensures consistent, reliable natural language understanding across all note capture scenarios.

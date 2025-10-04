# NoteProcessor API Reference

Quick reference for the NoteProcessor tool API.

## Table of Contents

1. [Initialization](#initialization)
2. [Core Operations](#core-operations)
3. [Action Items](#action-items)
4. [Note Search](#note-search)
5. [Project Integration](#project-integration)
6. [Categorization](#categorization)
7. [Frontmatter](#frontmatter)
8. [Batch Operations](#batch-operations)
9. [Data Models](#data-models)
10. [Error Handling](#error-handling)

## Initialization

```python
from tools import NoteProcessor

# Initialize with default config
processor = NoteProcessor()

# Initialize with custom config root
from pathlib import Path
processor = NoteProcessor(config_root=Path("/custom/path/.claude"))
```

## Core Operations

### parse_note()

Parse a note file and extract all information.

```python
note = processor.parse_note(file_path: str) -> ParsedNote
```

**Returns**: `ParsedNote` with:
- `file_path`: Path to the note file
- `content`: Full note content
- `action_items`: List[ActionItem]
- `tags`: List[str]
- `categorization_result`: CategorizationResult (if available)

**Example**:
```python
note = processor.parse_note("inbox/meeting-notes.md")
print(f"Found {len(note.action_items)} action items")
print(f"Tags: {note.tags}")
```

**Raises**: `NoteProcessorError` if parsing fails

---

## Action Items

### extract_action_items()

Extract action items from notes with filtering.

```python
items = processor.extract_action_items(
    scope: str = "all",
    filters: Optional[ActionItemFilters] = None
) -> List[Dict[str, Any]]
```

**Parameters**:
- `scope`: `"all"`, `"project:<id>"`, or `"inbox"`
- `filters`: ActionItemFilters for filtering results

**Example**:
```python
# All action items
all_items = processor.extract_action_items(scope="all")

# Project-specific
project_items = processor.extract_action_items(scope="project:mobile-app-v2")

# With filters
from tools.note_models import ActionItemFilters
filters = ActionItemFilters(status="pending", assignee="alice", priority="high")
filtered = processor.extract_action_items(scope="all", filters=filters)
```

### get_action_items_by_status()

Get action items filtered by status.

```python
items = processor.get_action_items_by_status(
    status: str,
    project: Optional[str] = None
) -> List[Dict[str, Any]]
```

**Parameters**:
- `status`: `"pending"`, `"completed"`, or `"overdue"`
- `project`: Optional project ID filter

**Example**:
```python
pending = processor.get_action_items_by_status("pending")
overdue = processor.get_action_items_by_status("overdue", project="mobile-app-v2")
completed = processor.get_action_items_by_status("completed")
```

---

## Note Search

### search_notes()

Search for notes with optional filters.

```python
notes = processor.search_notes(
    query: Optional[str] = None,
    filters: Optional[NoteSearchFilters] = None,
    para_category: Optional[ParaCategory] = None
) -> List[ParsedNote]
```

**Parameters**:
- `query`: Search query string
- `filters`: NoteSearchFilters with additional criteria
- `para_category`: Filter by PARA category

**Example**:
```python
from tools.note_models import NoteSearchFilters, ParaCategory

# Basic search
notes = processor.search_notes(query="sprint planning")

# With filters
filters = NoteSearchFilters(project="mobile-app", status="active", tags=["meeting"])
notes = processor.search_notes(query="architecture", filters=filters)

# By category
notes = processor.search_notes(para_category=ParaCategory.PROJECTS)
```

---

## Project Integration

### get_project_notes()

Get all notes linked to a specific project.

```python
notes = processor.get_project_notes(project_id: str) -> List[ParsedNote]
```

**Example**:
```python
notes = processor.get_project_notes("mobile-app-v2")
print(f"Found {len(notes)} notes for mobile-app-v2")
```

### link_note_to_project()

Link a note to a project.

```python
success = processor.link_note_to_project(
    note_path: str,
    project_id: str
) -> bool
```

**Example**:
```python
processor.link_note_to_project("inbox/feature-brainstorm.md", "mobile-app-v2")
```

### sync_project_notes()

Synchronize project notes with cache system.

```python
result = processor.sync_project_notes(project_id: str) -> Dict[str, Any]
```

**Returns**: Dict with:
- `project_id`: Project identifier
- `synced_count`: Number of notes synced
- `cache_path`: Path to cache file
- `synced_at`: ISO timestamp

**Example**:
```python
result = processor.sync_project_notes("mobile-app-v2")
print(f"Synced {result['synced_count']} notes")
```

---

## Categorization

### categorize_note()

Analyze and categorize a note using PARA Method.

```python
result = processor.categorize_note(
    note_path: str,
    auto_move: bool = False
) -> CategorizationResult
```

**Parameters**:
- `note_path`: Path to note file
- `auto_move`: Whether to automatically move the file (default: False)

**Returns**: `CategorizationResult` with:
- `category`: ParaCategory (PROJECTS, AREAS, RESOURCES, ARCHIVE)
- `confidence`: Float (0.0-1.0)
- `reasoning`: List[str] of reasons

**Example**:
```python
# Analyze without moving
result = processor.categorize_note("inbox/meeting-notes.md")
print(f"Category: {result.category.value}")
print(f"Confidence: {result.confidence:.1%}")
print(f"Reasoning: {', '.join(result.reasoning)}")

# Auto-move if high confidence
result = processor.categorize_note("inbox/feature-spec.md", auto_move=True)
```

---

## Frontmatter

### update_frontmatter()

Update note frontmatter with atomic write and rollback.

```python
success = processor.update_frontmatter(
    note_path: str,
    updates: Dict[str, Any],
    create_backup: bool = True
) -> bool
```

**Parameters**:
- `note_path`: Path to note file
- `updates`: Dictionary of frontmatter updates
- `create_backup`: Whether to create backup before update

**Example**:
```python
processor.update_frontmatter(
    "1-projects/mobile-app/sprint-notes.md",
    {
        "status": "in-progress",
        "priority": "high",
        "reviewed": True,
        "updated_at": datetime.now().isoformat()
    }
)
```

---

## Batch Operations

### batch_process_inbox()

Batch process notes in inbox with optional categorization.

```python
results = processor.batch_process_inbox(
    max_notes: Optional[int] = None,
    auto_categorize: bool = False
) -> BatchProcessResult
```

**Parameters**:
- `max_notes`: Maximum number of notes to process
- `auto_categorize`: Whether to auto-categorize with high confidence

**Returns**: `BatchProcessResult` with:
- `total_processed`: Total notes processed
- `successful`: Number of successful operations
- `failed`: Number of failed operations
- `notes`: List of processed note data
- `errors`: List of error details

**Example**:
```python
results = processor.batch_process_inbox(max_notes=10, auto_categorize=True)
print(f"Processed: {results.successful}/{results.total_processed}")
print(f"Errors: {len(results.errors)}")

for error in results.errors:
    print(f"  {error['path']}: {error['error']}")
```

### get_processing_stats()

Get statistics about notes and processing status.

```python
stats = processor.get_processing_stats() -> Dict[str, Any]
```

**Returns**: Dict with:
- `inbox_count`: Number of notes in inbox
- `total_notes`: Total notes across all categories
- `total_action_items`: Total action items
- `pending_action_items`: Pending action items
- `categories`: Dict with note counts per category

**Example**:
```python
stats = processor.get_processing_stats()
print(f"Inbox: {stats['inbox_count']} notes")
print(f"Total action items: {stats['total_action_items']}")
print(f"Pending: {stats['pending_action_items']}")
```

---

## Data Models

### ActionItemFilters

```python
from tools.note_models import ActionItemFilters

filters = ActionItemFilters(
    status: Optional[str] = None,        # "pending", "completed", "overdue"
    assignee: Optional[str] = None,      # Filter by assignee
    priority: Optional[str] = None       # "high", "medium", "low"
)
```

### NoteSearchFilters

```python
from tools.note_models import NoteSearchFilters

filters = NoteSearchFilters(
    project: Optional[str] = None,       # Filter by project ID
    status: Optional[str] = None,        # Note status
    tags: Optional[List[str]] = None     # Filter by tags
)
```

### ParaCategory

```python
from tools.note_models import ParaCategory

# Available categories
ParaCategory.PROJECTS      # "1-projects"
ParaCategory.AREAS         # "2-areas"
ParaCategory.RESOURCES     # "3-resources"
ParaCategory.ARCHIVE       # "4-archive"
ParaCategory.INBOX         # "inbox"
```

### ParsedNote

Result from `parse_note()`:
```python
note.file_path          # str
note.content            # str
note.action_items       # List[ActionItem]
note.tags               # List[str]
note.categorization_result  # Optional[CategorizationResult]
```

### CategorizationResult

Result from `categorize_note()`:
```python
result.category         # ParaCategory
result.confidence       # float (0.0-1.0)
result.reasoning        # List[str]
```

### BatchProcessResult

Result from `batch_process_inbox()`:
```python
result.total_processed  # int
result.successful       # int
result.failed           # int
result.notes            # List[Dict]
result.errors           # List[Dict]
```

---

## Error Handling

### NoteProcessorError

Base exception for all NoteProcessor errors.

```python
from tools.note_processor import NoteProcessorError

try:
    notes = processor.get_project_notes(project_id)
except NoteProcessorError as e:
    print(f"Error: {e}")
    # Handle error gracefully
```

### Common Error Scenarios

```python
# File not found
try:
    note = processor.parse_note("nonexistent.md")
except NoteProcessorError as e:
    print("Note file not found")

# Invalid scope
try:
    items = processor.extract_action_items(scope="invalid:scope")
except NoteProcessorError as e:
    print("Invalid scope format")

# Parse errors
try:
    note = processor.parse_note("malformed-note.md")
except NoteProcessorError as e:
    print(f"Parse error: {e}")
```

---

## Quick Reference Cheat Sheet

```python
from tools import NoteProcessor
from tools.note_models import ActionItemFilters, NoteSearchFilters, ParaCategory

processor = NoteProcessor()

# Action items
pending = processor.get_action_items_by_status("pending")
items = processor.extract_action_items(scope="project:id", filters=ActionItemFilters(assignee="alice"))

# Notes
notes = processor.get_project_notes("project-id")
notes = processor.search_notes(query="query", filters=NoteSearchFilters(status="active"))

# Categorization
result = processor.categorize_note(path, auto_move=True)

# Frontmatter
processor.update_frontmatter(path, {"status": "reviewed"})

# Batch
results = processor.batch_process_inbox(max_notes=20, auto_categorize=True)

# Project integration
processor.link_note_to_project(note_path, project_id)
sync_result = processor.sync_project_notes(project_id)
```

---

**See Also**:
- [NoteProcessor Adoption Guide](noteprocessor_adoption_guide.md)
- [NoteProcessor Source Code](../../tools/note_processor.py)
- [Data Models](../../tools/note_models.py)

**Last Updated**: 2025-10-04

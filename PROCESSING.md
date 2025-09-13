# PARA Note Processing Engine

The PARA Note Processing Engine is a comprehensive tool for parsing, analyzing, and manipulating markdown notes within the PARA Method framework.

## Overview

The processing engine can:
- Parse markdown files with YAML frontmatter
- Extract action items, attendees, dates, and tags
- Analyze content for automatic PARA categorization
- Safely update notes with backup protection
- Handle malformed notes gracefully
- Process entire directories in batch mode

## Installation

The processing engine requires Python 3.7+ and dependencies from `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

## Command Reference

### `parse` - Parse Single Note

Parse and analyze a single markdown note file.

```bash
./para-processor.py parse path/to/note.md
```

**Options:**
- `--json` - Output results in JSON format
- `--graceful` - Handle malformed notes gracefully (don't fail on YAML errors)

**Output:**
- File path and word count
- Estimated reading time
- Suggested PARA category
- Frontmatter field count
- Action items (first 3 shown)
- Attendees (first 3 shown)
- Tags

### `batch` - Process Multiple Notes

Process all markdown files in a directory.

```bash
./para-processor.py batch directory/
```

**Options:**
- `--pattern PATTERN` - File pattern to match (default: `*.md`)
- `--summary` - Show summary statistics only

**Summary Output:**
- Total notes processed
- Total word count across all notes
- Action item completion statistics
- PARA category distribution
- Processing errors (if any)

### `actions` - Find Action Items

Find and analyze action items across notes.

```bash
./para-processor.py actions --directory path/
```

**Options:**
- `--directory DIR` - Directory to search (default: current directory)
- `--orphaned` - Show only potentially orphaned action items

**Orphaned Criteria:**
Action items are considered potentially orphaned if they:
- Are not completed
- Have no assignee
- Are overdue (if due date is specified)

### `update` - Update Note Frontmatter

Safely update YAML frontmatter in notes with automatic backup.

```bash
./para-processor.py update note.md --key status=reviewed --key priority=high
```

**Options:**
- `--key KEY=VALUE` - Key-value pair to add/update (can be used multiple times)

**Safety Features:**
- Automatic backup creation in `.para-backups/`
- Atomic operations (all changes succeed or none do)
- Validation of existing note structure

## Extraction Capabilities

### Action Items

Extracts action items from checkbox patterns:

```markdown
- [ ] Simple action item
- [x] Completed action item
- [ ] Action with assignee - @username
- [ ] Action with due date - Due: 2024-12-25
- [ ] Action with priority [high]
- [ ] Complex action - @alice - Due: 2024-12-25 [medium]
```

**Extracted Data:**
- Text content
- Completion status (checked/unchecked)
- Assignee (from `@username` pattern)
- Due date (from `Due:` pattern)
- Priority level (from `[priority]` pattern)
- Line number in file

### Attendees and People

Extracts people from structured patterns:

```markdown
**Attendees:** Alice Johnson, Bob Smith, charlie@company.com
Participants: Jane Doe <jane@example.com>
```

**Extraction Rules:**
- Recognizes "Attendees:" and "Participants:" labels
- Splits on commas, semicolons, and line breaks
- Extracts email addresses separately
- Cleans up formatting and removes empty entries

### Dates

Extracts dates in ISO format:

```markdown
Date: 2024-09-13
Meeting scheduled for 2024-12-25 14:30
Deadline is 2024-10-01
```

**Supported Formats:**
- `YYYY-MM-DD` (ISO date)
- `YYYY-MM-DD HH:MM` (ISO datetime)
- `YYYY-MM-DD HH:MM:SS` (full timestamp)

### Tags

Extracts tags from multiple sources:

```markdown
# In content as hashtags
#project #meeting #important

# In frontmatter as list
tags: ["project", "meeting", "important"]

# In frontmatter as comma-separated
tags: "project, meeting, important"
```

## Auto-Categorization

The engine analyzes content to suggest appropriate PARA categories based on keyword presence and weighting.

### Category Keywords

**Projects (1-projects)**
- High weight: project, deadline, deliverable, milestone, launch, complete, finish
- Medium weight: task, goal, objective, outcome, result
- Low weight: plan, strategy, roadmap

**Areas (2-areas)**
- High weight: responsibility, maintain, ongoing, continuous, regular
- Medium weight: team, process, standard, policy, procedure
- Low weight: management, oversight, monitoring

**Resources (3-resources)**
- High weight: reference, documentation, guide, tutorial, research
- Medium weight: knowledge, learning, study, article, book
- Low weight: information, data, facts, resource

**Archive (4-archive)**
- Content identified as completed or inactive

**Inbox (inbox)**
- Default category when no clear pattern is detected

### Categorization Algorithm

1. **Explicit Frontmatter**: Check for `para_suggestion` field
2. **Keyword Scoring**: Score content against category keywords
3. **Weight Calculation**: Apply weight multipliers (high=3, medium=2, low=1)
4. **Minimum Threshold**: Require score ≥2 for suggestion
5. **Fallback**: Default to "inbox" if no clear category

## Error Handling

The engine includes comprehensive error handling:

### Strict Mode (Default)
- Fails on malformed YAML frontmatter
- Reports parsing errors with line numbers
- Validates file structure before processing

### Graceful Mode (`--graceful`)
- Continues processing despite YAML errors
- Extracts what it can from content
- Provides partial results for malformed notes
- Suitable for bulk processing mixed-quality notes

### File Safety
- Creates timestamped backups before modifications
- Atomic operations (succeed or fail completely)
- Detailed error reporting
- Rollback capability using backup files

## Backup System

All file modifications create automatic backups:

**Backup Location:** `.para-backups/`
**Naming Pattern:** `filename_YYYYMMDD_HHMMSS.bak`
**Content:** Exact copy of original file before modification

### Managing Backups

```bash
# List recent backups
ls -la .para-backups/

# Restore from backup
cp .para-backups/note_20240913_143022.bak original-note.md

# Clean old backups (manual)
find .para-backups -name "*.bak" -mtime +30 -delete
```

## Integration with PARA System

The processing engine is designed to work seamlessly with:

- **Template System** (`para-templates.py`) - Process notes created from templates
- **PARA Configuration** (`.para-config.yaml`) - Use user preferences and settings
- **Directory Structure** - Respect PARA folder hierarchy
- **Git Integration** - Safe operations that work with version control

## Performance

### Processing Speed
- Single note: ~1-5ms per file
- Batch processing: ~100-500 notes/second
- Memory usage: <10MB for typical workflows

### Optimization Tips
- Use `--summary` for large batch operations
- Use specific `--pattern` to limit scope
- Process directories rather than individual files when possible
- Use graceful mode for mixed-quality note collections

## Troubleshooting

### Common Issues

**"Invalid YAML frontmatter"**
- Use `--graceful` mode to continue processing
- Check YAML syntax (quotes, brackets, indentation)
- Validate frontmatter with online YAML validator

**"File does not exist"**
- Check file path (use absolute paths when possible)
- Ensure file has `.md` extension
- Verify read permissions

**"No action items found"**
- Check checkbox format: `- [ ]` not `- []`
- Ensure proper markdown structure
- Verify action items are at line start (no extra indentation)

**"Permission denied"**
- Check file write permissions
- Ensure `.para-backups` directory is writable
- Run with appropriate user permissions

### Debug Mode

For detailed debugging information:

```bash
# Enable Python debugging
PYTHONPATH=. python3 -v para-processor.py parse note.md

# Check regex patterns with test content
python3 -c "
import re
content = 'your test content'
pattern = re.compile(r'pattern here')
print(pattern.findall(content))
"
```

## API Usage

The processing engine can also be used as a Python library:

```python
from para_processor import ParaNoteProcessor

# Create processor instance
processor = ParaNoteProcessor()

# Parse a note
note = processor.parse_note('path/to/note.md')

# Access extracted data
print(f"Found {len(note.action_items)} action items")
print(f"Suggested category: {note.suggested_category}")

# Batch process
notes = processor.batch_process_notes('directory/')

# Safe updates
processor.update_note_frontmatter('note.md', {'status': 'reviewed'})
```

## Contributing

When contributing to the processing engine:

1. Add test cases for new extraction patterns
2. Update regex patterns with proper escaping
3. Include error handling for new features
4. Document new command-line options
5. Test with various markdown flavors and edge cases

## License

Part of the PARA Method implementation, provided as-is for personal and educational use.
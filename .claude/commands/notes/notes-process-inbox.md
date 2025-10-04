---
name: notes process-inbox
description: Process inbox notes with Claude Code guidance and interactive review
---

# Notes Process Inbox

Intelligently process inbox notes with Claude Code guidance, providing interactive review options and batch processing capabilities.

## Usage Examples:
- `/notes process-inbox --list` - List inbox notes for review
- `/notes process-inbox --interactive --batch 3` - Interactive review of 3 notes
- `/notes process-inbox --auto-suggest --batch 5` - Process 5 notes with AI suggestions
- `/notes process-inbox` - Standard batch processing

## Instructions:

You are an inbox processing assistant for the PARA Method system. When this command is invoked:

1. **Determine the processing mode** based on parameters:
   - `--list`: Show note summaries for review planning
   - `--interactive`: Provide detailed note reviews for conversational processing
   - `--auto-suggest`: Process with AI category suggestions
   - Default: Standard batch processing

2. **For --list mode**:
   - Return note summaries with previews
   - Include suggested categories and confidence
   - Provide actions for each note

3. **For --interactive mode**:
   - Present notes one-by-one with full context
   - Show content previews, action items, and suggested categories
   - Offer specific actions: categorize, edit, skip, delete
   - Guide user through decisions with natural conversation

4. **Handle user responses conversationally**:
   - "Move the first note to projects" → `/notes review-note --file [path] --category projects`
   - "Show me the next batch" → `/notes process-inbox --interactive --batch [n]`
   - "Skip this one for now" → Continue to next note

5. **Execute using NoteProcessor tool** for simplified, type-safe operations:
   ```python
   from tools import NoteProcessor

   processor = NoteProcessor()

   # Batch process inbox with auto-categorization
   results = processor.batch_process_inbox(
       max_notes=batch_size,
       auto_categorize=auto_suggest
   )

   # For individual note review
   result = processor.categorize_note(note_path, auto_move=False)
   ```

6. **Return structured JSON** optimized for conversational flow:
   - Note previews and summaries
   - Available actions and suggestions
   - Progress tracking (processed/remaining)
   - Next step recommendations

## Processing Modes:

### List Mode (`--list`)
Present inbox contents for review planning:
- Note summaries with titles and previews
- Suggested PARA categories with confidence scores
- Available actions for each note
- Overall statistics

### Interactive Mode (`--interactive`)
Guide through individual note review:
- Detailed note content with action items
- Category suggestions with reasoning
- Conversational decision prompts
- Progress through batch with user control

### Auto-Suggest Mode (`--auto-suggest`)
Process notes with AI assistance:
- Automatic category suggestions
- Batch processing with confirmations
- Summary of suggested categorizations
- Review options for suggested moves

## Parameters:
- `--list` - Show note summaries without processing
- `--interactive` - Interactive review mode for conversational processing
- `--auto-suggest` - Enable AI category suggestions
- `--batch N` - Limit number of notes to process (default: 10, interactive: 3)
- `--directory PATH` - Directory to process (default: inbox)
- `--pattern PATTERN` - File pattern to match (default: *.md)

## Conversational Flow Examples:

**User**: "Process my inbox notes"
**Response**:
1. Execute: `/notes process-inbox --list`
2. Present: "You have 8 notes in inbox. Here's what I found..."
3. Show note summaries with suggested actions
4. Offer: "Would you like to review them interactively or process with AI suggestions?"

**User**: "Review them one by one"
**Response**:
1. Execute: `/notes process-inbox --interactive --batch 3`
2. Present first note with content preview and suggestions
3. Ask: "This note about 'Sprint Planning' looks like a project meeting. Should I move it to projects?"

**User**: "Yes, move it to projects"
**Response**:
1. Execute: `/notes review-note --file [path] --category projects`
2. Confirm: "✅ Moved 'Sprint Planning' to projects"
3. Continue: "Next note is about API documentation..."

## Behavior:
- Always output JSON for Claude Code integration
- Present notes in digestible batches (default: 3 for interactive, 10 for processing)
- Track progress through inbox with remaining counts
- Provide clear next actions and suggestions
- Handle errors gracefully with recovery options
- Support undo operations for recent moves

## Error Handling:
NoteProcessor provides automatic error handling:
- Empty inbox: NoteProcessorError with helpful suggestions
- Permission errors: Clear error messages with recovery options
- Invalid files: Graceful skipping with warnings in batch results
- Type-safe operations prevent common programming errors

## Implementation Notes:
- Uses NoteProcessor for **80-100 lines → 5-10 lines** complexity reduction
- Type-safe operations with Pydantic models
- Automatic backup creation before file moves
- Batch processing returns BatchProcessResult with statistics
- Individual categorization returns CategorizationResult with confidence scores

Be conversational, helpful, and guide users through inbox processing decisions naturally while maintaining the structure needed for effective PARA organization.
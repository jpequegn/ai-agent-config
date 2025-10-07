---
name: todo
description: Manage project todos in todos.md file
---

# Project Todo Manager

Manage todos in a `todos.md` file at the root of your current project directory.

## Usage Examples:
- `/todo add "Fix navigation bug"`
- `/todo add "Fix navigation bug" tomorrow` - Set due date with relative time
- `/todo add "Deploy to production" 12-24-2025` - Set due date with absolute date
- `/todo add "Review PR" next week` - Set due date with relative time
- `/todo add "Team meeting" in 3 days` - Set due date with offset
- `/todo due 1 June 9` - Update due date for todo #1
- `/todo complete 1`
- `/todo remove 2`
- `/todo list`
- `/todo past due` - Show overdue tasks
- `/todo next` - Show next task by due date
- `/todo undo 1`

## Instructions:

You are a todo manager for the current project that uses **NLPProcessor tool** for robust date parsing.

### Date Parsing with NLPProcessor

**All date operations should use NLPProcessor**:

```python
from tools import NLPProcessor
from datetime import datetime

# Initialize NLP processor
nlp = NLPProcessor()

# Parse due dates from natural language
def parse_due_date(date_text: str):
    """Parse any date format to datetime object."""
    try:
        date_expr = nlp.parse_date_expression(date_text)
        return date_expr.resolved_date
    except Exception as e:
        print(f"⚠️ Could not parse date '{date_text}'. Please use formats like: tomorrow, next week, June 9, 12-24-2025")
        return None

# Check if tasks are past due
def get_past_due_tasks(tasks):
    """Filter tasks that are past their due date."""
    now = datetime.now()
    return [task for task in tasks if task.get('due_date') and task['due_date'] < now]

# Format date for display
def format_date(dt: datetime) -> str:
    """Format datetime for todos.md display."""
    return dt.strftime("%m/%d/%Y")  # or "%d/%m/%Y" for non-US locales
```

### Supported Date Formats (via NLPProcessor)

**Relative Dates:**
- `tomorrow`, `yesterday`, `today`
- `next week`, `last week`
- `next month`, `last month`

**Date Offsets:**
- `in 3 days`, `in 2 weeks`, `in 5 months`
- `3 days ago`, `2 weeks ago`, `5 months ago`

**Absolute Dates:**
- ISO format: `2024-12-25`, `2024-12-25T10:30:00`
- US format: `12/25/2024`, `12-25-2024`
- Named months: `June 9`, `December 25, 2024`
- Fuzzy parsing: Any reasonable date format

**Benefits:**
- ✅ <2ms parsing time per date
- ✅ 93% test coverage
- ✅ Consistent across all commands
- ✅ Handles timezone-aware dates
- ✅ Graceful error messages

When this command is invoked:

1. **Determine the project root** by looking for common indicators (.git, package.json, etc.)
2. **Locate or create** `todos.md` in the project root
3. **Parse the command arguments** to determine the action:
   - `add "task description"` - Add a new todo
   - `add "task description" [tomorrow|next week|4 days|June 9|12-24-2025|etc...]` - Add a new todo with the provided due date
   - `due N [tomorrow|next week|4 days|June 9|12-24-2025|etc...]` - Mark todo N with the due date provided
   - `complete N` - Mark todo N as completed and move from the ##Active list to the ##Completed list
   - `remove N` - Remove todo N entirely
   - `undo N` - Mark completed todo N as incomplete
   - `list [N]` or no args - Show all (or N number of) todos in a user-friendly format, with each todo numbered for reference
   - `past due` - Show all of the tasks which are past due and still active
   - `next` - Shows the next active task in the list, this should respect Due dates, if there are any. If not, just show the first todo in the Active list

## Todo Format:
Use this markdown format in todos.md:
```markdown
# Project Todos

## Active
- [ ] Task description here | Due: MM-DD-YYYY (conditionally include HH:MM AM/PM, if specified)
- [ ] Another task 

## Completed  
- [x] Finished task | Done: MM-DD-YYYY (conditionally include HH:MM AM/PM, if specified) 
- [x] Another completed task | Due: MM-DD-YYYY (conditionally include HH:MM AM/PM, if specified) | Done: MM-DD-YYYY (conditionally include HH:MM AM/PM, if specified) 
```

## Behavior:
- Number todos when displaying (1, 2, 3...)
- Keep completed todos in a separate section
- Todos do not need to have Due Dates/Times
- Keep the Active list sorted descending by Due Date, if there are any; though in a list with mixed tasks with and without Due Dates, those with Due Dates should come before those without Due Dates
- If todos.md doesn't exist, create it with the basic structure
- Show helpful feedback after each action
- Handle edge cases gracefully (invalid numbers, missing file, etc.)
- **Use NLPProcessor for all date parsing** - Never manually parse dates
- All provided dates/times should be saved/formatted in a standardized format of MM/DD/YYYY (or DD/MM/YYYY depending on locale), unless the user specifies a different format
- Times should not be included in the due date format unless requested (`due N in 2 hours` should be MM/DD/YYYY @ [+ 2 hours from now])
- **For past due detection**: Use NLPProcessor's date comparison capabilities
- **For date validation**: Let NLPProcessor handle all validation and error messages

### Implementation Notes

**Date Parsing Best Practices:**
1. Always use `nlp.parse_date_expression()` for parsing dates
2. Handle DateParsingError exceptions gracefully
3. Format parsed dates using `format_date()` helper
4. Use datetime comparison for past due checks
5. Sort todos by due date using datetime objects

**Error Handling:**
- Invalid date formats: Show NLPProcessor error message
- Past due tasks: Calculate using datetime comparison
- Missing dates: Allow todos without due dates
- Invalid todo numbers: Provide helpful feedback

Always be concise and helpful in your responses.
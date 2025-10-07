---
name: follow-up-check
description: Comprehensive follow-up and task management system for action items across all notes
---

# Follow-up and Task Management System

Comprehensive system for tracking and managing action items using the **NoteProcessor tool** for intelligent action item analysis and reporting.

## Usage Examples:
- `/cc follow-up-check` - Full status report with overdue highlighting
- `/cc follow-up-check status` - Quick status summary with key metrics
- `/cc follow-up-check overdue` - Show only overdue items with urgency
- `/cc follow-up-check assignee @alice` - Show items for specific assignee
- `/cc follow-up-check priority` - Show items by priority (high → medium → low)
- `/cc follow-up-check team` - Team performance and workload analysis
- `/cc follow-up-check stale` - Find items >30 days old without updates
- `/cc follow-up-check urgent` - Focus on high-priority and overdue items only

## Instructions:

You are a comprehensive follow-up and task management system that uses the **NoteProcessor tool** for intelligent action item tracking and analysis.

### Tool-Based Implementation

**Default Status Report** `/cc follow-up-check`:

```python
from tools import NoteProcessor
from datetime import datetime

# Initialize processor
processor = NoteProcessor()

# Get all action items
all_items = processor.extract_action_items()

# Categorize items
pending_items = [item for item in all_items if not item.get("completed", False)]
completed_items = [item for item in all_items if item.get("completed", False)]
overdue_items = processor.get_action_items_by_status("overdue")

# Group by project for organized view
grouped_items = processor.group_action_items_by_project(pending_items)

# Get top priority items
prioritized = processor.prioritize_action_items(pending_items)[:5]

# Display comprehensive dashboard
print("# 📋 Follow-up Status Dashboard\n")
print(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

# Summary statistics
print("## 📊 Summary\n")
print(f"- **Total Items**: {len(all_items)}")
print(f"- **Pending**: {len(pending_items)}")
print(f"- **Completed**: {len(completed_items)}")
print(f"- **Overdue**: ⚠️ {len(overdue_items)}\n")

# Overdue items (highlighted)
if overdue_items:
    print("## ⚠️ Overdue Items\n")
    for item in overdue_items[:10]:  # Top 10
        print(f"- **{item.get('text', 'No description')}**")
        print(f"  - Due: {item.get('due_date', 'Not set')}")
        print(f"  - Assignee: {item.get('assignee', 'Unassigned')}")
        print(f"  - Priority: {item.get('priority', 'Not set')}")
        print()

# Top priority items
print("## 🎯 Top 5 Priority Items\n")
for item in prioritized:
    status = "⚠️ OVERDUE" if item in overdue_items else "Pending"
    print(f"- **{item.get('text', 'No description')}** [{status}]")
    print(f"  - Due: {item.get('due_date', 'Not set')}")
    print(f"  - Priority: {item.get('priority', 'Not set')}")
    print()

# Items by project
print("## 📂 Items by Project\n")
for project, items in sorted(grouped_items.items()):
    pending = len([i for i in items if not i.get("completed", False)])
    if pending > 0:
        print(f"### {project} ({pending} items)\n")
        for item in items[:3]:  # Top 3 per project
            print(f"- {item.get('text', 'No description')}")
        print()
```

**Quick Status** `/cc follow-up-check status`:

```python
from tools import NoteProcessor

processor = NoteProcessor()

# Get counts
all_items = processor.extract_action_items()
pending = [i for i in all_items if not i.get("completed", False)]
overdue = processor.get_action_items_by_status("overdue")

# Count by priority
high_priority = [i for i in pending if i.get("priority") == "high"]
medium_priority = [i for i in pending if i.get("priority") == "medium"]
low_priority = [i for i in pending if i.get("priority") == "low"]

# Unique assignees
assignees = set(i.get("assignee") for i in pending if i.get("assignee"))

print("# 📊 Quick Status\n")
print(f"**Total**: {len(all_items)} | **Pending**: {len(pending)} | **Overdue**: ⚠️ {len(overdue)}\n")
print("## Priority Distribution\n")
print(f"- 🔴 High: {len(high_priority)}")
print(f"- 🟡 Medium: {len(medium_priority)}")
print(f"- 🟢 Low: {len(low_priority)}")
print(f"- ⚪ Unset: {len(pending) - len(high_priority) - len(medium_priority) - len(low_priority)}\n")
print(f"**Assignees**: {len(assignees)} people involved")
```

**Overdue Items** `/cc follow-up-check overdue`:

```python
from tools import NoteProcessor
from datetime import datetime

processor = NoteProcessor()

# Get overdue items
overdue_items = processor.get_action_items_by_status("overdue")

# Sort by days overdue
def days_overdue(item):
    try:
        due_date = datetime.fromisoformat(item.get("due_date", "")).date()
        return (datetime.now().date() - due_date).days
    except:
        return 0

overdue_sorted = sorted(overdue_items, key=days_overdue, reverse=True)

print(f"# ⚠️ Overdue Action Items ({len(overdue_items)} total)\n")

for item in overdue_sorted:
    days = days_overdue(item)
    urgency = "🔴 CRITICAL" if days > 7 else "🟡 URGENT" if days > 3 else "⚠️ OVERDUE"

    print(f"## {urgency} - {days} days overdue\n")
    print(f"**{item.get('text', 'No description')}**\n")
    print(f"- Due: {item.get('due_date')}")
    print(f"- Assignee: {item.get('assignee', 'Unassigned')}")
    print(f"- Priority: {item.get('priority', 'Not set')}")
    print(f"- Note: {item.get('note', 'Unknown')}\n")
```

**Assignee Filter** `/cc follow-up-check assignee @alice`:

```python
from tools import NoteProcessor, ActionItemFilters

processor = NoteProcessor()

# Extract assignee from command
assignee = "{assignee_from_command}"  # e.g., "alice"

# Get items for assignee
items = processor.extract_action_items(
    filters=ActionItemFilters(assignee=assignee)
)

pending = [i for i in items if not i.get("completed", False)]
overdue = [i for i in pending if i in processor.get_action_items_by_status("overdue")]

print(f"# 👤 Action Items for @{assignee}\n")
print(f"**Total**: {len(items)} | **Pending**: {len(pending)} | **Overdue**: {len(overdue)}\n")

# Group by priority
high = [i for i in pending if i.get("priority") == "high"]
medium = [i for i in pending if i.get("priority") == "medium"]
low = [i for i in pending if i.get("priority") == "low"]

if overdue:
    print("## ⚠️ Overdue Items\n")
    for item in overdue:
        print(f"- {item.get('text')} (Due: {item.get('due_date')})")
    print()

print(f"## 🔴 High Priority ({len(high)})\n")
for item in high:
    print(f"- {item.get('text')}")
print()

print(f"## 🟡 Medium Priority ({len(medium)})\n")
for item in medium:
    print(f"- {item.get('text')}")
```

**Priority View** `/cc follow-up-check priority`:

```python
from tools import NoteProcessor

processor = NoteProcessor()

# Get all pending items
pending = processor.extract_action_items(
    filters=ActionItemFilters(status="pending")
)

# Group by priority
high = [i for i in pending if i.get("priority") == "high"]
medium = [i for i in pending if i.get("priority") == "medium"]
low = [i for i in pending if i.get("priority") == "low"]
unset = [i for i in pending if not i.get("priority")]

print("# 🎯 Action Items by Priority\n")
print(f"**Distribution**: High: {len(high)} | Medium: {len(medium)} | Low: {len(low)} | Unset: {len(unset)}\n")

# Show each priority level
for priority_name, priority_items, emoji in [
    ("High Priority", high, "🔴"),
    ("Medium Priority", medium, "🟡"),
    ("Low Priority", low, "🟢"),
    ("No Priority Set", unset, "⚪")
]:
    if priority_items:
        print(f"## {emoji} {priority_name} ({len(priority_items)} items)\n")
        for item in priority_items[:10]:  # Top 10 per priority
            print(f"- **{item.get('text')}**")
            print(f"  - Due: {item.get('due_date', 'Not set')}")
            print(f"  - Assignee: {item.get('assignee', 'Unassigned')}")
        print()
```

**Stale Items** `/cc follow-up-check stale`:

```python
from tools import NoteProcessor

processor = NoteProcessor()

# Get stale items (>30 days old)
stale_items = processor.get_stale_action_items(days=30)

print(f"# 🕒 Stale Action Items ({len(stale_items)} items >30 days old)\n")

if stale_items:
    print("These items have not been updated in over 30 days:\n")
    for item in stale_items:
        print(f"- **{item.get('text')}**")
        print(f"  - Created: {item.get('created', 'Unknown')}")
        print(f"  - Assignee: {item.get('assignee', 'Unassigned')}")
        print(f"  - Priority: {item.get('priority', 'Not set')}")
        print()

    print("\n**Recommendations**:")
    print("- Review if these items are still relevant")
    print("- Update or complete active items")
    print("- Archive or delete obsolete items")
else:
    print("✅ No stale items found. All action items are recent!")
```

**Urgent Items** `/cc follow-up-check urgent`:

```python
from tools import NoteProcessor

processor = NoteProcessor()

# Get all pending items
pending = processor.extract_action_items(
    filters=ActionItemFilters(status="pending")
)

# Get overdue items
overdue = processor.get_action_items_by_status("overdue")

# Get high priority items
high_priority = [i for i in pending if i.get("priority") == "high"]

# Prioritize all urgent items
urgent_items = processor.prioritize_action_items(
    list(set(overdue + high_priority))
)

print(f"# 🚨 Urgent Action Items\n")
print(f"**Requires Immediate Attention**: {len(urgent_items)} items\n")

for i, item in enumerate(urgent_items, 1):
    is_overdue = item in overdue
    status = "⚠️ OVERDUE" if is_overdue else "🔴 HIGH PRIORITY"

    print(f"## {i}. {status}\n")
    print(f"**{item.get('text')}**\n")
    print(f"- Due: {item.get('due_date', 'Not set')}")
    print(f"- Assignee: {item.get('assignee', 'Unassigned')}")
    print(f"- Priority: {item.get('priority', 'Not set')}")
    print(f"- Note: {item.get('note', 'Unknown')}\n")
```

**Team Performance** `/cc follow-up-check team`:

```python
from tools import NoteProcessor

processor = NoteProcessor()

# Get all items
all_items = processor.extract_action_items()

# Group by assignee
assignee_items = {}
for item in all_items:
    assignee = item.get("assignee", "Unassigned")
    if assignee not in assignee_items:
        assignee_items[assignee] = {"total": 0, "pending": 0, "completed": 0, "overdue": 0}

    assignee_items[assignee]["total"] += 1
    if item.get("completed", False):
        assignee_items[assignee]["completed"] += 1
    else:
        assignee_items[assignee]["pending"] += 1

# Get overdue items
overdue = processor.get_action_items_by_status("overdue")
for item in overdue:
    assignee = item.get("assignee", "Unassigned")
    if assignee in assignee_items:
        assignee_items[assignee]["overdue"] += 1

print("# 👥 Team Performance Dashboard\n")

for assignee, stats in sorted(assignee_items.items()):
    if assignee == "Unassigned":
        continue

    completion_rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0

    print(f"## {assignee}\n")
    print(f"- Total: {stats['total']} items")
    print(f"- Pending: {stats['pending']}")
    print(f"- Completed: {stats['completed']} ({completion_rate:.0f}% completion rate)")
    if stats["overdue"] > 0:
        print(f"- ⚠️ Overdue: {stats['overdue']}")
    print()
```

### Tool Integration Benefits

**NoteProcessor Integration**:
- **Simplification**: 372 lines → ~150 lines (60% reduction) through tool delegation
- **Consistency**: Standardized action item extraction and analysis
- **Performance**: Cached note processing with optimized queries
- **Testability**: Centralized action item logic with comprehensive unit tests
- **Reusability**: Same tool used across all notes-related commands

**Key Features**:
- Intelligent prioritization based on urgency, importance, and age
- Project-based grouping for organized follow-up
- Stale item detection for cleanup recommendations
- Flexible filtering by status, assignee, priority
- Comprehensive team performance analytics

### Error Handling

- **No Action Items Found**: Clear message with suggestion to create action items
- **Missing Note Data**: Graceful degradation with available information
- **Invalid Filters**: Clear error message with valid filter options
- **CLI Failures**: Fallback to manual note scanning with warning

Remember: Effective follow-up requires regular checking, clear prioritization, and timely action. NoteProcessor ensures consistent, comprehensive action item tracking.

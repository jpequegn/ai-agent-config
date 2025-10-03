---
name: follow-up-check
description: Comprehensive follow-up and task management system for action items across all notes
---

# Follow-up and Task Management System

Comprehensive system for tracking and managing action items extracted from notes with status tracking, due date management, and progress reporting.

## Usage Examples:
- `/cc follow-up-check` - Full status report with overdue highlighting
- `/cc follow-up-check status` - Quick status summary with key metrics
- `/cc follow-up-check overdue` - Show only overdue items with urgency
- `/cc follow-up-check assignee @alice` - Show items for specific assignee
- `/cc follow-up-check priority` - Show items by priority (high → medium → low)
- `/cc follow-up-check report` - Generate comprehensive progress report
- `/cc follow-up-check team` - Team performance and workload analysis
- `/cc follow-up-check trends` - Show completion trends and patterns
- `/cc follow-up-check stale` - Find items >30 days old without updates
- `/cc follow-up-check urgent` - Focus on high-priority and overdue items only

## Instructions:

You are a comprehensive follow-up and task management system. When this command is invoked:

### Core Functionality

1. **Extract and Analyze Action Items**
   - Use DataCollector tool to get comprehensive action item data from notes
   - Automatic 5-minute caching for performance
   - Parse and organize items by status, assignee, due date, and priority
   - Identify patterns and provide intelligent insights

2. **Status Tracking and Reporting**
   - **Pending**: Incomplete items that need attention
   - **Completed**: Finished items for reference
   - **Overdue**: Items past their due date (highlight with ⚠️ )
   - **Orphaned**: Items without assignees or due dates (suggest improvements)

3. **Command Actions**

   **Default `/cc follow-up-check`:**
   - Generate comprehensive status dashboard
   - Highlight overdue items prominently
   - Show top 5 priority items by urgency
   - Provide summary statistics (total, pending, completed, overdue)
   - Suggest immediate actions needed

   **`status`:**
   - Quick summary with key metrics
   - Count of items by status and priority
   - Number of assignees involved
   - Overdue item count with urgency indicators

   **`overdue`:**
   - List all overdue items with urgency calculations
   - Sort by days overdue (most urgent first)
   - Include assignee and priority information
   - Provide specific action recommendations

   **`assignee @username`:**
   - Filter items for specific assignee
   - Show their workload distribution
   - Highlight their overdue items
   - Provide productivity metrics

   **`priority`:**
   - Organize items by priority level (high → medium → low → unset)
   - Show distribution across priority levels
   - Highlight high-priority overdue items
   - Suggest priority assignments for unset items

   **`report`:**
   - Comprehensive progress report
   - Completion rates and trends
   - Team productivity insights
   - Bottleneck identification
   - Actionable recommendations

   **`team`:**
   - Team performance dashboard with individual metrics
   - Workload distribution and balance analysis
   - Identify top performers and bottlenecks
   - Suggest task redistribution opportunities

   **`trends`:**
   - Completion rate trends over time
   - Average time to completion by priority
   - Identify patterns in overdue items
   - Success rate by assignee and project type

   **`stale`:**
   - Items >30 days old without status updates
   - Orphaned items without assignees or due dates
   - Suggest archiving or reactivation
   - Identify forgotten or blocked tasks

   **`urgent`:**
   - Focus view on critical and overdue items only
   - Prioritized action list for immediate attention
   - Escalation recommendations for blocked items
   - Emergency task assignment suggestions

### Output Format

Structure your response as a professional task management report:

```
# 📋 Follow-up Status Report
**Generated:** [timestamp]
**Scope:** [number] action items across [number] notes

## 🚨 Urgent Actions Required
[List overdue and high-priority items]

## 📊 Status Summary
- **Pending:** [count] items
- **Completed:** [count] items
- **Overdue:** [count] items ⚠️
- **Total:** [count] items

## 🎯 Priority Breakdown
- **High:** [count] items ([overdue count] overdue)
- **Medium:** [count] items ([overdue count] overdue)
- **Low:** [count] items ([overdue count] overdue)
- **Unset:** [count] items (needs prioritization)

## 👥 Assignee Workload
[List assignees with their item counts and overdue status]

## 💡 Recommendations
[Intelligent suggestions for improving task management]

## 📋 Next Actions
[Specific steps to take based on analysis]
```

### Intelligence Features

1. **Smart Overdue Detection**
   - Calculate days overdue for items with due dates
   - Flag items >30 days old without due dates as potentially stale
   - Prioritize by business impact and urgency

2. **Workload Analysis**
   - Identify assignees with heavy workloads
   - Detect bottlenecks and suggest redistribution
   - Track completion patterns

3. **Pattern Recognition**
   - Identify frequently overdue assignees
   - Detect projects with poor follow-through
   - Suggest process improvements

4. **Actionable Insights**
   - Recommend specific items to prioritize today
   - Suggest status updates for stale items
   - Provide completion rate trends

### Implementation Steps

When executing this command:

1. **Initialize Data Collection**
   ```python
   from tools import DataCollector, ConfigManager

   config = ConfigManager()
   collector = DataCollector(config)
   ```

2. **Collect Action Items Data**
   ```python
   # Collect notes data with action items across all projects
   notes_data = collector.collect_notes_data(
       project="all",  # or specific project name for filtered view
       include_action_items=True
   )

   # Access action items
   action_items = notes_data.action_items
   # Each action item has: description, assignee, due_date, priority, status

   # Access other notes data if needed
   project_notes = notes_data.project_notes
   decisions = notes_data.decisions
   ```

3. **Filter and Analyze Based on Command Mode**
   ```python
   # Filter by status
   pending = [item for item in action_items if item.get('status') == 'pending']
   completed = [item for item in action_items if item.get('status') == 'completed']
   overdue = [item for item in action_items if item.get('is_overdue', False)]

   # Filter by assignee (for assignee mode)
   if assignee_filter:
       filtered = [item for item in action_items if item.get('assignee') == assignee_filter]

   # Sort by priority (for priority mode)
   priority_order = {'high': 0, 'medium': 1, 'low': 2, None: 3}
   sorted_items = sorted(action_items, key=lambda x: priority_order.get(x.get('priority'), 3))
   ```

4. **Generate Intelligence and Insights**
   - Calculate metrics (counts, percentages, trends)
   - Identify patterns (frequently overdue assignees, bottlenecks)
   - Generate recommendations based on data

5. **Format Output**
   - Use the structured format template above
   - Highlight urgent items prominently
   - Provide actionable next steps

### Error Handling

DataCollector handles errors automatically with:
- Automatic retry with exponential backoff (3 attempts)
- Graceful degradation when notes CLI unavailable
- Detailed error messages with recovery suggestions
- Continuation with partial data when some sources fail

Additional handling:
- If no action items found, suggest creating some with templates
- Handle missing assignees gracefully with "unassigned" designation
- Provide helpful hints for improving action item format
- Offer to create sample action items for demonstration

### Integration Notes

- Uses DataCollector tool for efficient data retrieval with caching
- Automatic 5-minute cache reduces repeated queries
- Compatible with current action item format in markdown
- Supports all existing patterns: `@assignee`, `Due: YYYY-MM-DD`, `[priority]`
- Graceful degradation when notes CLI unavailable
- Enhances user experience with intelligent analysis and recommendations

### Command Ecosystem Integration

The follow-up-check command works seamlessly with other Claude Code commands:

- **Use with `/cc todo`**: Convert follow-up items to project todos
- **Combine with `/cc notes-meeting`**: Review action items before meetings
- **Integrate with `/cc daily-checkin`**: Include follow-up status in daily reviews
- **Pair with `/cc task`**: Elevate critical items to formal project tasks

### Suggested Workflows

1. **Weekly Review**: `/cc follow-up-check` → address overdue → `/cc follow-up-check team`
2. **Project Planning**: `/cc follow-up-check priority` → `/cc task` for high-priority items
3. **Daily Standup Prep**: `/cc follow-up-check urgent` → `/cc notes-meeting`
4. **Sprint Planning**: `/cc follow-up-check stale` → archive or reactivate

Always provide actionable, professional output that helps users stay organized and productive.
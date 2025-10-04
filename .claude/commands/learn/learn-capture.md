---
name: learn capture
description: Capture insights, concepts, and learnings from various sources with automatic categorization and linking
---

# Learn Capture

Capture insights, concepts, and learnings from various sources with intelligent categorization, automatic source linking, and integration with learning goals and projects.

## Usage Examples:
- `/learn capture --insight "Progressive summarization improves retention" --source building-a-second-brain`
- `/learn capture --concept "Agent orchestration patterns" --category technical --goal ai-agent-architecture`
- `/learn capture from "Claude Code documentation" about "MCP server integration"`
- `/learn capture --type application --title "Automated project sync" --description "Implemented bidirectional sync"`

## Instructions:

You are a learning capture assistant for the PARA Method learning system. When this command is invoked:

1. **Parse capture request** and extract:
   - Insight/concept/application content
   - Source reference (if provided)
   - Learning goal associations
   - Category and tags
   - Priority and urgency indicators

2. **Validate and enrich metadata**:
   - Check source exists in sources.yaml
   - Validate learning goal references
   - Auto-generate tags based on content analysis
   - Determine appropriate category if not specified
   - Set priority based on learning goal alignment

3. **Handle different capture types**:
   - **Insights**: Key learnings, aha moments, important realizations
   - **Concepts**: Theoretical frameworks, models, principles
   - **Applications**: Practical implementations, use cases, examples
   - **Questions**: Follow-up questions, areas needing clarification
   - **Connections**: Links between different concepts or sources

4. **Create structured learning entry**:
   ```bash
   # Capture to structured format
   python3 -c "
   import json, yaml, datetime
   from pathlib import Path

   # Load existing learning data
   learning_file = Path('.claude/cache/learning_captures.json')
   learning_data = json.loads(learning_file.read_text()) if learning_file.exists() else {'captures': []}

   # Create new capture entry
   capture_entry = {
       'id': f'capture-{len(learning_data[\"captures\"]) + 1:04d}',
       'timestamp': datetime.datetime.now().isoformat(),
       'type': '${capture_type}',
       'title': '${title}',
       'content': '${content}',
       'source': '${source_id}',
       'category': '${category}',
       'tags': ${tags_json},
       'learning_goals': ${goals_json},
       'priority': '${priority}',
       'status': 'active',
       'connections': [],
       'applications': []
   }

   # Add to learning data
   learning_data['captures'].append(capture_entry)

   # Save updated data
   learning_file.parent.mkdir(exist_ok=True)
   learning_file.write_text(json.dumps(learning_data, indent=2))

   print(f'✅ Captured: {capture_entry[\"title\"]}')
   print(f'📝 ID: {capture_entry[\"id\"]}')
   print(f'🏷️ Tags: {', '.join(capture_entry[\"tags\"])}')
   if capture_entry['learning_goals']:
       print(f'🎯 Goals: {', '.join(capture_entry[\"learning_goals\"])}')
   "
   ```

5. **Provide intelligent suggestions**:
   - Related concepts or insights
   - Potential applications
   - Connected learning goals
   - Recommended follow-up actions
   - Source material recommendations

6. **Update cross-references**:
   - Link to source in sources.yaml
   - Update learning goal progress
   - Create connections with existing captures
   - Add to relevant project contexts

## Capture Types:
- `insight` - Key learnings and realizations
- `concept` - Theoretical frameworks and models
- `application` - Practical implementations
- `question` - Follow-up questions and clarifications
- `connection` - Links between ideas
- `quote` - Important quotes and references
- `tool` - Useful tools and resources
- `pattern` - Recurring patterns and templates

## Parameters:
- `--type TYPE` - Type of capture (insight, concept, application, etc.)
- `--title TITLE` - Brief title for the capture
- `--content TEXT` - Main content or description
- `--source SOURCE_ID` - Source reference from sources.yaml
- `--category CATEGORY` - Primary category (technical, productivity, etc.)
- `--goal GOAL_ID` - Associated learning goal
- `--tags TAGS` - Comma-separated tags
- `--priority PRIORITY` - Priority level (high, medium, low)
- `--private` - Mark as private/personal learning

## Natural Language Processing:
Automatically detects:
- Capture types: "I learned...", "Key insight...", "Important concept..."
- Sources: "from X", "while reading Y", "during course Z"
- Categories: Technical terms, productivity keywords, etc.
- Priority: "Important", "critical", "key", "essential"
- Learning goals: References to existing goals or related topics

## Integration Features:
- **Source Linking**: Automatic connection to sources.yaml entries
- **Goal Alignment**: Maps captures to learning goals and tracks progress
- **Project Integration**: Links to relevant projects when applicable
- **Cross-References**: Builds connections between related captures
- **Search Integration**: Full-text search across all learning content

## Output Structure:
```json
{
  "capture_id": "capture-0123",
  "title": "Progressive Summarization Technique",
  "type": "concept",
  "content": "Layer-by-layer highlighting to extract key insights...",
  "source": "building-a-second-brain",
  "category": "productivity",
  "tags": ["note-taking", "knowledge-management", "para-method"],
  "learning_goals": ["para-method-mastery"],
  "priority": "high",
  "created": "2024-09-14T10:30:00",
  "connections": ["capture-0089", "capture-0112"],
  "applications": ["implemented in daily note workflow"],
  "next_actions": ["Practice with technical documentation", "Create template"]
}
```

## Behavior:
- Always creates structured JSON in `.claude/cache/learning_captures.json`
- Provides immediate feedback with capture ID and metadata
- Suggests related content and potential applications
- Updates learning goal progress automatically
- Integrates with existing PARA Method workflows
- Supports both quick captures and detailed entries

## Implementation Notes

**NoteProcessor Integration for Enhanced Workflow:**

The command can be enhanced by creating markdown notes alongside JSON captures:

```python
from tools import NoteProcessor
from pathlib import Path

processor = NoteProcessor()

# After creating JSON capture, also create a markdown note
note_content = f"""---
title: {title}
capture_type: {capture_type}
source: {source_id}
category: {category}
tags: {tags}
learning_goals: {learning_goals}
priority: {priority}
created: {timestamp}
---

# {title}

{content}

## Source
{source_reference}

## Applications
- {applications}

## Next Actions
- {next_actions}
"""

# Write to inbox
note_path = Path("inbox") / f"{timestamp}_{capture_id}.md"
note_path.write_text(note_content)

# Auto-categorize with NoteProcessor
result = processor.categorize_note(str(note_path), auto_move=True)
print(f"✓ Note categorized: {result.category.value} (confidence: {result.confidence:.1%})")

# Update frontmatter with category and confidence
processor.update_frontmatter(str(note_path), {
    "para_category": result.category.value,
    "categorization_confidence": result.confidence,
    "auto_categorized": True
})

# Extract any action items from the content
if "next actions" in content.lower() or "todo" in content.lower():
    items = processor.extract_action_items(scope=f"file:{note_path}")
    print(f"✓ Extracted {len(items)} action items")
```

**Benefits of NoteProcessor Integration:**
- Automatic PARA categorization beyond learning categories
- Type-safe note parsing and validation
- Integrated action item extraction from learning captures
- Consistent frontmatter management
- Better integration with notes system
- Dual storage: JSON for learning data + markdown for PARA

**Current Implementation:**
- Uses learning_captures.json for structured learning data
- Manual categorization by learning category
- Learning goal association and tracking
- Source linking and cross-referencing

**Recommended Workflow:**
1. Create JSON capture for learning system tracking
2. Generate markdown note from capture data
3. Use NoteProcessor for PARA categorization
4. Extract action items if present
5. Maintain both formats for different purposes

Process learning captures efficiently and build a comprehensive knowledge base that enhances personal learning and productivity.
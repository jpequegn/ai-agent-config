---
name: learn book
description: Capture structured book notes with key insights, concept extraction, and reading progress tracking
---

# Learn Book

Capture comprehensive book notes with structured insights, automatic concept extraction, reading progress tracking, and intelligent connections to learning goals and existing knowledge.

## Usage Examples:
- `/learn book --title "Building a Second Brain" --author "Tiago Forte" --chapter 3 --insights "Progressive summarization technique"`
- `/learn book "Atomic Habits" --progress 45% --key-concept "habit stacking" --application "morning routine"`
- `/learn book --isbn 978-1-4516-4873-3 --quote "Systems are better than goals" --page 23`
- `/learn book --complete "Deep Work" --rating 5 --summary "Focus is the new superpower"`

## Instructions:

You are a book learning assistant for the PARA Method learning system. When this command is invoked:

1. **Parse book capture request**:
   - Book title and author information
   - Current reading progress or completion status
   - Specific chapter, page, or section references
   - Key insights, concepts, quotes, or takeaways
   - Personal applications and connections

2. **Enrich book metadata**:
   - Check if book exists in sources.yaml as a learning resource
   - Auto-identify genre, category, and relevant learning goals
   - Extract ISBN, publication info if provided
   - Determine reading status (planning, reading, completed)
   - Calculate reading progress and velocity

3. **Process learning content**:
   - **Key Insights**: Important realizations and aha moments
   - **Concepts**: Theoretical frameworks, models, principles
   - **Quotes**: Memorable passages with page references
   - **Applications**: Practical implementations and use cases
   - **Questions**: Follow-up questions and areas for exploration
   - **Connections**: Links to other books, sources, or knowledge

4. **Create structured book learning entry**:
   ```bash
   python3 -c "
   import json, yaml, datetime, re
   from pathlib import Path

   # Load learning data
   captures_file = Path('.claude/cache/learning_captures.json')
   sources_file = Path('.claude/sources.yaml')
   goals_file = Path('.claude/learning_goals.yaml')

   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {'sources': {}}
   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}

   # Generate book ID from title
   book_title = '${book_title}'
   book_id = re.sub(r'[^a-z0-9]+', '-', book_title.lower())

   # Create book learning capture
   capture = {
       'id': f'book-{book_id}-{len([c for c in captures_data.get(\"captures\", []) if c.get(\"source_type\") == \"book\" and c.get(\"book_title\") == book_title]) + 1:03d}',
       'timestamp': datetime.datetime.now().isoformat(),
       'type': 'book_learning',
       'source_type': 'book',
       'book_title': book_title,
       'author': '${author}' or None,
       'isbn': '${isbn}' or None,
       'chapter': '${chapter}' or None,
       'page': '${page}' or None,
       'progress_percentage': int('${progress}'.replace('%', '')) if '${progress}' else None,
       'reading_status': '${status}' or ('completed' if '${complete}' else 'reading'),
       'content': {
           'insights': [insight.strip() for insight in '${insights}'.split('|') if insight.strip()],
           'key_concepts': [concept.strip() for concept in '${concepts}'.split(',') if concept.strip()],
           'quotes': [{'text': '${quote}', 'page': '${page}'} if '${quote}' else {}],
           'applications': [app.strip() for app in '${applications}'.split(',') if app.strip()],
           'questions': [q.strip() for q in '${questions}'.split(',') if q.strip()],
           'summary': '${summary}' or None
       },
       'metadata': {
           'rating': int('${rating}') if '${rating}' else None,
           'genre': '${genre}' or None,
           'category': '${category}' or 'general',
           'reading_started': '${start_date}' or None,
           'reading_completed': '${complete_date}' if '${complete}' else None,
           'reading_time_minutes': int('${reading_time}') if '${reading_time}' else None
       },
       'connections': {
           'learning_goals': [],
           'related_captures': [],
           'source_references': []
       },
       'tags': [],
       'created_by': 'learn-book-command'
   }

   # Auto-identify learning goal connections
   for goal_id, goal in goals_data.get('learning_goals', {}).items():
       goal_keywords = set((goal.get('name', '') + ' ' + ' '.join(goal.get('tags', []))).lower().split())
       capture_text = (book_title + ' ' + ' '.join(capture['content']['insights']) + ' ' + ' '.join(capture['content']['key_concepts'])).lower()

       if any(keyword in capture_text for keyword in goal_keywords if len(keyword) > 3):
           capture['connections']['learning_goals'].append(goal_id)

   # Auto-generate tags from content
   all_content = (book_title + ' ' + ' '.join(capture['content']['insights']) + ' ' + ' '.join(capture['content']['key_concepts'])).lower()
   common_tags = ['productivity', 'leadership', 'technology', 'business', 'personal-development', 'psychology', 'strategy', 'innovation', 'management', 'communication']

   for tag in common_tags:
       if tag.replace('-', ' ') in all_content or tag.replace('-', '') in all_content:
           capture['tags'].append(tag)

   # Find connections to existing book captures
   for existing_capture in captures_data.get('captures', []):
       if existing_capture.get('source_type') == 'book' and existing_capture.get('id') != capture['id']:
           # Check for concept overlap
           existing_concepts = set(existing_capture.get('content', {}).get('key_concepts', []))
           new_concepts = set(capture['content']['key_concepts'])

           if existing_concepts.intersection(new_concepts):
               capture['connections']['related_captures'].append(existing_capture['id'])

   # Add to captures
   captures_data.setdefault('captures', []).append(capture)

   # Save updated data
   captures_file.parent.mkdir(exist_ok=True)
   captures_file.write_text(json.dumps(captures_data, indent=2))

   # Generate response
   response = {
       'status': 'success',
       'command': '/learn book',
       'data': {
           'note_id': capture['id'],
           'book_title': book_title,
           'concepts_identified': capture['content']['key_concepts'],
           'connections': {
               'learning_goals': capture['connections']['learning_goals'],
               'related_books': [c for c in capture['connections']['related_captures']],
               'total_connections': len(capture['connections']['learning_goals']) + len(capture['connections']['related_captures'])
           },
           'progress': {
               'reading_status': capture['reading_status'],
               'progress_percentage': capture['progress_percentage'],
               'insights_captured': len(capture['content']['insights'])
           },
           'metadata': {
               'tags': capture['tags'],
               'rating': capture['metadata']['rating'],
               'category': capture['metadata']['category']
           }
       },
       'insights': {
           'concept_analysis': f'Identified {len(capture[\"content\"][\"key_concepts\"])} key concepts from this reading session',
           'learning_alignment': f'Connected to {len(capture[\"connections\"][\"learning_goals\"])} active learning goals',
           'knowledge_network': f'Found {len(capture[\"connections\"][\"related_captures\"])} related book notes in your knowledge base'
       },
       'next_actions': []
   }

   # Generate intelligent suggestions
   if capture['reading_status'] == 'reading' and capture['progress_percentage']:
       if capture['progress_percentage'] > 80:
           response['next_actions'].append('Consider scheduling time to complete the book this week')
       elif capture['progress_percentage'] < 20:
           response['next_actions'].append('Set a daily reading goal to maintain momentum')

   if capture['connections']['learning_goals']:
       response['next_actions'].append(f'Review how these insights apply to your {capture[\"connections\"][\"learning_goals\"][0]} goal')

   if len(capture['content']['key_concepts']) > 3:
       response['next_actions'].append('Consider creating connections between related concepts using /learn connect')

   if capture['content']['applications']:
       response['next_actions'].append('Plan practical implementation of these applications')

   print(json.dumps(response, indent=2))
   "
   ```

5. **Provide intelligent book insights**:
   - Reading progress analysis and velocity tracking
   - Concept density and complexity assessment
   - Connection opportunities with existing knowledge
   - Application potential for current projects
   - Reading goal alignment and optimization

## Book Learning Types:

### Reading Progress Capture
- **Daily Sessions**: Regular reading progress with key takeaways
- **Chapter Summaries**: Structured chapter-by-chapter insights
- **Completion Reviews**: Comprehensive book summaries and ratings

### Content Analysis
- **Concept Extraction**: Identify and categorize key concepts
- **Quote Collection**: Memorable passages with context
- **Application Mapping**: Practical use cases and implementations

### Knowledge Integration
- **Cross-Book Connections**: Link concepts across multiple books
- **Goal Alignment**: Connect insights to learning objectives
- **Project Applications**: Identify real-world implementation opportunities

## Parameters:
- `--title TITLE` - Book title (required)
- `--author AUTHOR` - Book author
- `--isbn ISBN` - Book ISBN for precise identification
- `--chapter CHAPTER` - Current chapter or section
- `--page PAGE` - Page reference for quotes or insights
- `--progress PERCENTAGE` - Reading progress (e.g., 45%)
- `--status STATUS` - Reading status (planning, reading, completed)
- `--insights TEXT` - Key insights (separate multiple with |)
- `--concepts LIST` - Key concepts (comma-separated)
- `--quote TEXT` - Important quote or passage
- `--applications LIST` - Practical applications (comma-separated)
- `--questions LIST` - Follow-up questions (comma-separated)
- `--summary TEXT` - Book summary or chapter summary
- `--rating RATING` - Book rating (1-5 stars)
- `--genre GENRE` - Book genre or category
- `--complete` - Mark book as completed
- `--reading-time MINUTES` - Time spent reading

## Natural Language Processing:
Automatically detects:
- Book references: "I'm reading...", "Just finished...", "Chapter 3 of..."
- Progress indicators: "halfway through", "75% done", "completed"
- Insight markers: "key insight", "important concept", "learned that"
- Application cues: "I can apply this to", "practical use", "implement"
- Connection signals: "similar to", "builds on", "contradicts"

## Reading Analytics:

### Progress Tracking
```markdown
📖 **Reading Progress**: 67% (Chapter 8 of 12)
⏱️ **Reading Velocity**: 2.3 chapters/week
📅 **Estimated Completion**: November 15, 2024
🎯 **Reading Goal**: On track for monthly target
```

### Concept Analysis
```markdown
💡 **Key Concepts This Session**:
- System thinking vs. goal setting
- Habit stacking methodology
- Environmental design principles

🔗 **New Connections Identified**:
- Links to "Atomic Habits" concepts (3 connections)
- Relates to productivity-systems learning goal
- Applicable to morning-routine project
```

### Knowledge Integration
```markdown
🧠 **Knowledge Network Growth**:
- Total book notes: 23 → 24
- Concept connections: 156 → 162
- Learning goal progress: +3% on Productivity Systems
- Cross-book insights: 4 new connections discovered
```

## Output Examples:

### Reading Session Capture
```json
{
  "status": "success",
  "command": "/learn book",
  "data": {
    "note_id": "book-atomic-habits-003",
    "book_title": "Atomic Habits",
    "concepts_identified": ["habit-stacking", "environmental-design", "identity-change"],
    "connections": {
      "learning_goals": ["productivity-systems", "personal-development"],
      "related_books": ["book-deep-work-001", "book-power-of-habit-002"],
      "total_connections": 4
    },
    "progress": {
      "reading_status": "reading",
      "progress_percentage": 67,
      "insights_captured": 3
    }
  },
  "insights": {
    "concept_analysis": "Identified 3 key concepts from this reading session",
    "learning_alignment": "Connected to 2 active learning goals",
    "knowledge_network": "Found 2 related book notes in your knowledge base"
  },
  "next_actions": [
    "Consider creating connections between habit-stacking and environmental-design concepts",
    "Review how these insights apply to your productivity-systems goal",
    "Plan practical implementation of habit-stacking in morning routine"
  ]
}
```

### Book Completion Summary
```json
{
  "status": "success",
  "command": "/learn book",
  "data": {
    "note_id": "book-building-second-brain-complete",
    "book_title": "Building a Second Brain",
    "reading_summary": {
      "total_insights": 12,
      "key_concepts": 8,
      "practical_applications": 6,
      "reading_time_hours": 14,
      "rating": 5
    },
    "knowledge_impact": {
      "learning_goals_advanced": ["knowledge-management", "productivity-systems"],
      "new_connections": 15,
      "actionable_takeaways": 8
    }
  },
  "completion_analysis": "Exceptional book with transformative impact on knowledge management approach"
}
```

## Integration Features:
- **Source Synchronization**: Auto-link with sources.yaml entries
- **Learning Goal Progress**: Update goal completion based on relevant insights
- **Reading Schedule**: Integrate with calendar for reading time management
- **Cross-Book Analysis**: Identify patterns and themes across multiple books
- **Application Tracking**: Monitor implementation of book concepts in projects

## Behavior:
- Creates structured book learning entries with comprehensive metadata
- Provides intelligent progress tracking and reading analytics
- Identifies connections between books and existing knowledge
- Generates actionable insights for concept application
- Maintains reading history and progress across multiple books
- Supports both detailed analysis and quick capture workflows
- Integrates with existing PARA Method learning infrastructure

Transform your reading into structured learning with intelligent insights, progress tracking, and knowledge network integration.
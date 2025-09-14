---
name: learn sources
description: Comprehensive learning source management with effectiveness tracking, curation automation, and intelligent recommendations
---

# Learn Sources

Comprehensive learning source management system with effectiveness tracking, automated curation, intelligent recommendations, and integration with learning goals and knowledge capture workflows.

## Usage Examples:
- `/learn sources add --title "Deep Learning Patterns" --type book --category technical --url "https://example.com"`
- `/learn sources update building-a-second-brain --rating 5 --status completed --review-notes "Transformative approach"`
- `/learn sources list --category technical --status active --sort-by rating`
- `/learn sources analyze --source claude-code-documentation --effectiveness --recommendations`
- `/learn sources discover --goal ai-agent-architecture --suggest 5`

## Instructions:

You are a learning source management assistant for the PARA Method learning system. When this command is invoked:

1. **Parse source management request**:
   - **Source Addition**: New learning resource with metadata
   - **Source Updates**: Progress, ratings, status changes
   - **Source Analysis**: Effectiveness assessment and insights
   - **Source Discovery**: Find new relevant sources
   - **Source Curation**: Quality assessment and organization

2. **Handle source operations**:

   **Add New Source**:
   ```bash
   python3 -c "
   import yaml, datetime, re
   from pathlib import Path

   # Load existing sources
   sources_file = Path('.claude/sources.yaml')
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {'sources': {}}

   # Generate source ID
   title = '${title}'
   source_id = re.sub(r'[^a-z0-9]+', '-', title.lower().strip())[:50]

   # Create new source
   new_source = {
       'title': title,
       'author': '${author}' or None,
       'type': '${source_type}',
       'category': '${category}',
       'status': 'planned',
       'added_date': datetime.date.today().strftime('%Y-%m-%d'),
       'rating': None,
       'tags': [tag.strip() for tag in '${tags}'.split(',') if tag.strip()],
       'url': '${url}' or None,
       'notes_location': None,
       'key_concepts': [],
       'learning_goals': [goal.strip() for goal in '${goals}'.split(',') if goal.strip()],
       'insights_captured': 0,
       'applications_implemented': 0,
       'review_frequency': '${review_frequency}' or 'monthly',
       'last_reviewed': None
   }

   # Add optional fields
   if '${description}': new_source['description'] = '${description}'
   if '${estimated_hours}': new_source['estimated_hours'] = int('${estimated_hours}')

   # Add to sources data
   sources_data['sources'][source_id] = new_source

   # Save updated sources
   sources_file.write_text(yaml.dump(sources_data, default_flow_style=False, indent=2))

   print(f'✅ Source added: {source_id}')
   print(f'📖 Title: {new_source[\"title\"]}')
   print(f'📂 Type: {new_source[\"type\"]} | Category: {new_source[\"category\"]}')
   if new_source['learning_goals']:
       print(f'🎯 Goals: {\", \".join(new_source[\"learning_goals\"])}')
   "
   ```

   **Update Existing Source**:
   ```bash
   python3 -c "
   import yaml, datetime
   from pathlib import Path

   # Load and update source
   sources_file = Path('.claude/sources.yaml')
   sources_data = yaml.safe_load(sources_file.read_text())

   source_id = '${source_id}'
   if source_id in sources_data['sources']:
       source = sources_data['sources'][source_id]

       # Update fields
       if '${rating}': source['rating'] = int('${rating}')
       if '${status}': source['status'] = '${status}'
       if '${progress}': source['progress_percentage'] = int('${progress}')
       if '${completion_date}' and '${status}' == 'completed':
           source['completion_date'] = '${completion_date}'
       if '${notes_location}': source['notes_location'] = '${notes_location}'
       if '${key_concepts}':
           concepts = [c.strip() for c in '${key_concepts}'.split(',') if c.strip()]
           source['key_concepts'] = concepts
       if '${review_update}':
           source['last_reviewed'] = datetime.date.today().strftime('%Y-%m-%d')

       # Save changes
       sources_file.write_text(yaml.dump(sources_data, default_flow_style=False, indent=2))
       print(f'✅ Source updated: {source[\"title\"]}')

       if source.get('rating'):
           print(f'⭐ Rating: {source[\"rating\"]}/5')
       if source.get('progress_percentage'):
           print(f'📊 Progress: {source[\"progress_percentage\"]}%')
   else:
       print(f'❌ Source not found: {source_id}')
   "
   ```

3. **Provide source analytics**:
   - Effectiveness scoring based on insights generated
   - ROI analysis (time invested vs. applications)
   - Learning goal contribution assessment
   - Source completion velocity tracking
   - Quality and relevance ratings

4. **Generate intelligent recommendations**:
   - Suggest sources for specific learning goals
   - Identify underutilized high-quality sources
   - Recommend optimal reading/learning sequences
   - Flag outdated or low-performing sources
   - Suggest source diversification strategies

## Source Management Operations:

### Add Sources
- **Manual Addition**: Full metadata specification
- **URL Import**: Automatic metadata extraction from URLs
- **Batch Import**: Multiple sources from reading lists
- **Template Creation**: Reusable source templates

### Update Sources
- **Progress Tracking**: Completion percentage, time spent
- **Quality Assessment**: Ratings, effectiveness scores
- **Status Management**: planned → active → completed → archived
- **Content Linking**: Notes location, key concepts extraction

### Analyze Sources
- **Effectiveness Analysis**: ROI, insight generation rates
- **Goal Contribution**: Impact on learning objectives
- **Usage Patterns**: Reading frequency, completion rates
- **Quality Assessment**: Rating vs. outcome correlation

### Discover Sources
- **Goal-Based Discovery**: Find sources for specific objectives
- **Recommendation Engine**: Suggest based on preferences
- **Gap Analysis**: Identify missing source types
- **Trending Sources**: Popular and highly-rated additions

## Parameters:
- `--action ACTION` - Source operation (add, update, list, analyze, discover)
- `--title TITLE` - Source title for addition
- `--source SOURCE_ID` - Target source ID for operations
- `--type TYPE` - Source type (book, article, course, etc.)
- `--category CATEGORY` - Source category
- `--author AUTHOR` - Source author or creator
- `--url URL` - Source URL or reference
- `--rating RATING` - Quality rating (1-5 stars)
- `--status STATUS` - Reading/learning status
- `--progress PERCENTAGE` - Completion progress (0-100)
- `--tags TAGS` - Comma-separated tag list
- `--goals GOALS` - Associated learning goals
- `--notes-location PATH` - Path to notes file
- `--key-concepts CONCEPTS` - Main concepts learned
- `--effectiveness` - Include effectiveness analysis
- `--recommendations` - Generate source recommendations
- `--discover-count N` - Number of sources to discover

## Source Types:
- `book` - Books, ebooks, audiobooks
- `article` - Articles, blog posts, papers
- `video` - Video tutorials, lectures, courses
- `podcast` - Podcast episodes, audio content
- `course` - Online courses, MOOCs, workshops
- `documentation` - Technical documentation, guides
- `tutorial` - Step-by-step tutorials, how-tos
- `research-paper` - Academic papers, research studies
- `conference-talk` - Conference presentations, talks
- `white-paper` - Industry white papers, reports

## Status Progression:
- `planned` → `active` → `completed`
- Alternative: `paused`, `abandoned`, `archived`

## Analytics Dashboard:

### Source Effectiveness Report
```markdown
# Learning Sources Analytics

## 📊 Source Portfolio Summary
- **Total Sources**: 23
- **Active Sources**: 8 (35%)
- **Completed Sources**: 12 (52%)
- **Average Rating**: 4.2/5
- **High-Impact Sources**: 6 (26%)

## 🎯 Top Performing Sources
### Building a Second Brain (Rating: 5/5)
- **Insights Generated**: 15 (highest)
- **Applications**: 8 implementations
- **Goal Contribution**: PARA Method Mastery (primary)
- **ROI**: 4.2x (time invested vs. outcomes)

### AI Agent Coordination Paper (Rating: 5/5)
- **Insights Generated**: 8
- **Applications**: 3 implementations
- **Goal Contribution**: AI Agent Architecture
- **ROI**: 3.8x

## ⚠️ Underperforming Sources
### Productivity Automation Course (Rating: 4/5, Progress: 65%)
- **Issue**: Slow progress, low application rate
- **Recommendation**: Focus on practical modules
- **Action**: Set completion deadline, increase weekly hours

## 🔍 Source Gaps Identified
- **Missing**: Advanced system design resources
- **Weakness**: Limited hands-on practice materials
- **Opportunity**: Add more case study sources
```

### Recommendation Engine
```markdown
# Source Recommendations for AI Agent Architecture Goal

## 🎯 High-Priority Additions
### Multi-Agent Systems: Design Patterns (Book)
- **Relevance**: 95% match for goal
- **Quality Score**: 4.7/5 (community rating)
- **Estimated Value**: High impact on coordination understanding
- **Time Investment**: ~20 hours

### Distributed Systems Architecture Course (Online)
- **Relevance**: 88% match for goal
- **Quality Score**: 4.5/5
- **Estimated Value**: Strong foundation for agent systems
- **Time Investment**: ~40 hours

## 📚 Supporting Resources
- "Agent-Based Modeling" research papers collection
- "Microservices Patterns" for architectural insights
- "Consensus Algorithms" tutorial series

## 🔄 Cross-Goal Synergies
- System design resources support both AI Architecture and Claude Code goals
- Automation patterns bridge productivity and technical learning
```

## Source Discovery Features:

### Intelligent Search
```python
# Automatic source discovery
discovery_engine = {
    'goal_analysis': 'Extract keywords and concepts from learning goals',
    'semantic_search': 'Find sources matching conceptual requirements',
    'quality_filtering': 'Apply minimum rating and review thresholds',
    'relevance_ranking': 'Score sources by goal alignment and user preferences',
    'diversity_optimization': 'Ensure variety in source types and perspectives'
}
```

### Quality Assessment
- **Community Ratings**: Aggregate ratings from learning platforms
- **Content Analysis**: Depth, accuracy, practical value assessment
- **Outcome Tracking**: Measure actual learning effectiveness
- **Peer Recommendations**: Sources used by similar learners
- **Expert Curation**: Industry expert recommendations

### Source Curation Rules
```yaml
automatic_curation:
  quality_thresholds:
    minimum_rating: 3.0
    minimum_reviews: 10
    recency_preference: 2_years

  effectiveness_metrics:
    insights_per_hour: 1.5
    application_rate: 0.3
    goal_contribution: 0.7

  archival_criteria:
    outdated_content: true
    superseded_by_better: true
    goal_no_longer_relevant: true
```

## Integration Features:

### Learning Goal Mapping
- Automatic goal alignment based on content analysis
- Goal progress updates from source completion
- Source recommendation for goal milestones
- Cross-goal synergy identification

### Knowledge Capture Integration
- Automatic linking of captures to source materials
- Source citation in insight records
- Key concept extraction and indexing
- Application tracking from source learning

### Project Integration
- Source recommendations based on project needs
- Practical application opportunities identification
- Just-in-time learning source suggestions
- Project-source effectiveness correlation

## Output Examples:

### Source Addition
```json
{
  "source_id": "deep-learning-patterns",
  "title": "Deep Learning Patterns",
  "status": "added",
  "type": "book",
  "category": "technical",
  "estimated_value": "high",
  "learning_goals": ["ai-agent-architecture"],
  "suggested_timeline": "6 weeks",
  "related_sources": ["ai-architecture-basics", "neural-networks-guide"]
}
```

### Effectiveness Analysis
```markdown
✅ Source Analysis: Claude Code Documentation
📊 Effectiveness Score: 8.7/10
🎯 Goal Contribution: Claude Code Mastery (primary), AI Architecture (secondary)
📈 Insights Generated: 23 (above average)
🛠️ Applications: 12 implementations (excellent)
⏰ ROI: 3.4x (time invested vs. outcomes)
💡 Recommendation: Continue regular review, focus on advanced patterns
📚 Similar Sources: MCP Server Specification, Agent Framework Docs
```

## Behavior:
- Maintains comprehensive source catalog in sources.yaml
- Tracks source effectiveness and learning outcomes
- Provides intelligent source recommendations
- Automates quality assessment and curation
- Integrates with learning goals and knowledge capture
- Generates actionable insights for source optimization
- Supports both individual sources and source collections

Master your learning resources through intelligent source management, effectiveness tracking, and strategic content curation.
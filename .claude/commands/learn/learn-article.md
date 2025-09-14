---
name: learn article
description: Capture article summaries with intelligent concept extraction, source analysis, and knowledge integration
---

# Learn Article

Capture comprehensive article insights with intelligent concept extraction, automatic source analysis, credibility assessment, and seamless integration with learning goals and knowledge networks.

## Usage Examples:
- `/learn article --title "AI in Project Management" --source "Harvard Business Review" --url "https://hbr.org/ai-pm"`
- `/learn article "GPT-4 Technical Report" --type research --concepts "multimodal learning, emergent abilities"`
- `/learn article --quick --title "10 Productivity Tips" --source "Medium" --takeaway "Time blocking increases focus by 40%"`
- `/learn article --from-url https://example.com/article --auto-extract --goal productivity-systems`

## Instructions:

You are an article learning assistant for the PARA Method learning system. When this command is invoked:

1. **Parse article capture request**:
   - Article title, URL, and publication source
   - Publication type (blog, research, news, tutorial)
   - Key concepts, insights, and takeaways
   - Credibility indicators and source authority
   - Relevance to learning goals and current projects

2. **Analyze article metadata**:
   - Extract publication date, author, and source credibility
   - Classify article type (research, opinion, tutorial, news)
   - Assess content depth and technical complexity
   - Identify target audience and reading level
   - Determine content freshness and relevance

3. **Extract learning content**:
   - **Key Insights**: Primary takeaways and novel information
   - **Concepts**: Technical terms, frameworks, methodologies
   - **Data Points**: Statistics, research findings, metrics
   - **Actionable Items**: Practical recommendations and steps
   - **Opinions vs Facts**: Distinguish subjective from objective content
   - **Credibility Assessment**: Source authority and evidence quality

4. **Create structured article learning entry**:
   ```bash
   python3 -c "
   import json, yaml, datetime, re, hashlib
   from pathlib import Path
   from urllib.parse import urlparse

   # Load learning data
   captures_file = Path('.claude/cache/learning_captures.json')
   sources_file = Path('.claude/sources.yaml')
   goals_file = Path('.claude/learning_goals.yaml')

   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {'sources': {}}
   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}

   # Generate article ID from title and source
   article_title = '${article_title}'
   source_name = '${source}' or 'unknown'
   article_url = '${url}' or ''

   # Create content hash for uniqueness
   content_hash = hashlib.md5(f'{article_title}{source_name}{article_url}'.encode()).hexdigest()[:8]
   article_id = f'article-{re.sub(r\"[^a-z0-9]+\", \"-\", article_title.lower())[:30]}-{content_hash}'

   # Assess source credibility
   def assess_credibility(source, url):
       credible_sources = ['harvard business review', 'mit technology review', 'nature', 'science', 'arxiv', 'acm', 'ieee']
       high_authority_domains = ['.edu', '.gov', 'hbr.org', 'technologyreview.com', 'nature.com', 'arxiv.org']

       credibility_score = 5  # Default medium credibility

       if any(cs in source.lower() for cs in credible_sources):
           credibility_score = 9
       elif any(domain in url.lower() for domain in high_authority_domains):
           credibility_score = 8
       elif 'medium.com' in url.lower() or 'substack.com' in url.lower():
           credibility_score = 6
       elif 'blog' in source.lower():
           credibility_score = 5

       return credibility_score

   credibility_score = assess_credibility(source_name, article_url)

   # Create article learning capture
   capture = {
       'id': article_id,
       'timestamp': datetime.datetime.now().isoformat(),
       'type': 'article_learning',
       'source_type': 'article',
       'article_title': article_title,
       'source': source_name,
       'url': article_url,
       'author': '${author}' or None,
       'publication_date': '${pub_date}' or None,
       'article_type': '${article_type}' or 'general',
       'content': {
           'summary': '${summary}' or None,
           'key_insights': [insight.strip() for insight in '${insights}'.split('|') if insight.strip()],
           'concepts': [concept.strip() for concept in '${concepts}'.split(',') if concept.strip()],
           'data_points': [dp.strip() for dp in '${data_points}'.split('|') if dp.strip()],
           'actionable_items': [action.strip() for action in '${actions}'.split(',') if action.strip()],
           'quotes': [{'text': q.strip(), 'context': None} for q in '${quotes}'.split('|') if q.strip()],
           'takeaway': '${takeaway}' or None
       },
       'analysis': {
           'complexity_level': '${complexity}' or 'intermediate',
           'reading_time_minutes': int('${reading_time}') if '${reading_time}' else 5,
           'credibility_score': credibility_score,
           'evidence_quality': '${evidence_quality}' or 'moderate',
           'bias_assessment': '${bias}' or 'neutral',
           'content_type': '${content_type}' or 'informational'  # informational, persuasive, analytical, tutorial
       },
       'connections': {
           'learning_goals': [],
           'related_captures': [],
           'source_references': [],
           'follow_up_articles': []
       },
       'metadata': {
           'domain': urlparse(article_url).netloc if article_url else None,
           'word_count': int('${word_count}') if '${word_count}' else None,
           'publication_type': '${pub_type}' or 'article',  # article, blog, research, news, tutorial
           'target_audience': '${audience}' or 'general',
           'technical_depth': '${tech_depth}' or 'medium',
           'relevance_score': 8,  # Default high relevance since user chose to capture
           'tags': [],
           'category': '${category}' or 'general'
       },
       'created_by': 'learn-article-command',
       'quality_indicators': {
           'has_references': bool('${has_refs}'),
           'peer_reviewed': bool('${peer_reviewed}'),
           'expert_authored': bool('${expert_author}'),
           'recent_publication': True if not '${pub_date}' else (datetime.datetime.now() - datetime.datetime.strptime('${pub_date}', '%Y-%m-%d')).days < 365
       }
   }

   # Auto-identify learning goal connections
   for goal_id, goal in goals_data.get('learning_goals', {}).items():
       goal_keywords = set((goal.get('name', '') + ' ' + ' '.join(goal.get('tags', []))).lower().split())
       article_content = (article_title + ' ' + ' '.join(capture['content']['key_insights']) + ' ' + ' '.join(capture['content']['concepts'])).lower()

       # Score relevance to learning goal
       keyword_matches = sum(1 for keyword in goal_keywords if len(keyword) > 3 and keyword in article_content)
       if keyword_matches >= 2 or any(kw in article_title.lower() for kw in goal_keywords if len(kw) > 4):
           capture['connections']['learning_goals'].append(goal_id)

   # Auto-generate tags from content analysis
   all_content = (article_title + ' ' + source_name + ' ' + ' '.join(capture['content']['key_insights']) + ' ' + ' '.join(capture['content']['concepts'])).lower()

   # Technical and domain-specific tags
   tech_tags = {
       'ai': ['artificial intelligence', 'machine learning', 'deep learning', 'neural network', 'gpt'],
       'productivity': ['productivity', 'efficiency', 'time management', 'workflow', 'automation'],
       'business': ['business', 'strategy', 'management', 'leadership', 'entrepreneurship'],
       'technology': ['technology', 'software', 'programming', 'development', 'tech'],
       'research': ['research', 'study', 'findings', 'analysis', 'data'],
       'innovation': ['innovation', 'disruption', 'emerging', 'future', 'trends']
   }

   for tag, keywords in tech_tags.items():
       if any(keyword in all_content for keyword in keywords):
           capture['metadata']['tags'].append(tag)

   # Find connections to related articles
   for existing_capture in captures_data.get('captures', []):
       if existing_capture.get('source_type') == 'article' and existing_capture.get('id') != capture['id']:
           # Check for concept overlap
           existing_concepts = set(existing_capture.get('content', {}).get('concepts', []))
           new_concepts = set(capture['content']['concepts'])

           if existing_concepts.intersection(new_concepts) or existing_capture.get('source') == capture['source']:
               capture['connections']['related_captures'].append(existing_capture['id'])

   # Add to captures
   captures_data.setdefault('captures', []).append(capture)

   # Save updated data
   captures_file.parent.mkdir(exist_ok=True)
   captures_file.write_text(json.dumps(captures_data, indent=2))

   # Generate intelligent response
   response = {
       'status': 'success',
       'command': '/learn article',
       'data': {
           'note_id': capture['id'],
           'article_title': article_title,
           'source': source_name,
           'concepts_identified': capture['content']['concepts'],
           'key_insights': len(capture['content']['key_insights']),
           'connections': {
               'learning_goals_updated': capture['connections']['learning_goals'],
               'related_articles': len(capture['connections']['related_captures']),
               'total_connections': len(capture['connections']['learning_goals']) + len(capture['connections']['related_captures'])
           },
           'quality_assessment': {
               'credibility_score': f'{credibility_score}/10',
               'evidence_quality': capture['analysis']['evidence_quality'],
               'content_type': capture['analysis']['content_type'],
               'technical_depth': capture['metadata']['technical_depth']
           },
           'learning_impact': {
               'actionable_items': len(capture['content']['actionable_items']),
               'data_points_captured': len(capture['content']['data_points']),
               'reading_investment': f'{capture[\"analysis\"][\"reading_time_minutes\"]} minutes'
           }
       },
       'analysis': {
           'content_quality': f'High-quality {capture[\"metadata\"][\"publication_type\"]} from {source_name}' if credibility_score >= 8 else f'Moderate-quality content from {source_name}',
           'learning_alignment': f'Strongly aligned with {len(capture[\"connections\"][\"learning_goals\"])} learning goals' if capture['connections']['learning_goals'] else 'General knowledge capture',
           'knowledge_network': f'Connected to {len(capture[\"connections\"][\"related_captures\"])} related articles in your knowledge base'
       },
       'suggested_applications': [],
       'next_actions': []
   }

   # Generate intelligent suggestions based on content
   if capture['content']['actionable_items']:
       response['suggested_applications'] = capture['content']['actionable_items'][:3]
       response['next_actions'].append('Plan implementation of these actionable insights')

   if capture['connections']['learning_goals']:
       response['next_actions'].append(f'Update progress on {capture[\"connections\"][\"learning_goals\"][0]} learning goal')

   if len(capture['content']['concepts']) > 2:
       response['next_actions'].append('Create concept connections using /learn connect')

   if credibility_score >= 8 and capture['quality_indicators']['has_references']:
       response['next_actions'].append('Consider exploring referenced sources for deeper learning')

   if capture['content']['data_points']:
       response['next_actions'].append('Validate key statistics and consider fact-checking')

   print(json.dumps(response, indent=2))
   "
   ```

5. **Provide intelligent article analysis**:
   - Source credibility assessment and bias detection
   - Content quality evaluation and evidence review
   - Learning goal alignment and relevance scoring
   - Cross-article connection identification
   - Application potential analysis

## Article Learning Types:

### Quick Capture
- **Rapid Insights**: Fast capture of key takeaways during reading
- **Mobile Friendly**: Designed for on-the-go article consumption
- **Headline Analysis**: Extract insights from article titles and summaries

### Deep Analysis
- **Comprehensive Summary**: Detailed analysis with concept extraction
- **Source Evaluation**: Credibility assessment and bias analysis
- **Cross-References**: Connections to existing knowledge and sources

### Research Integration
- **Academic Articles**: Specialized handling of research papers
- **Data Validation**: Fact-checking and statistical analysis
- **Citation Tracking**: Reference management and source following

## Parameters:
- `--title TITLE` - Article title (required)
- `--source SOURCE` - Publication source (e.g., Harvard Business Review)
- `--url URL` - Article URL for reference
- `--author AUTHOR` - Article author
- `--type TYPE` - Article type (research, blog, news, tutorial)
- `--summary TEXT` - Article summary
- `--insights TEXT` - Key insights (separate multiple with |)
- `--concepts LIST` - Key concepts (comma-separated)
- `--data-points TEXT` - Statistics and data (separate with |)
- `--actions LIST` - Actionable items (comma-separated)
- `--quotes TEXT` - Important quotes (separate with |)
- `--takeaway TEXT` - Main takeaway or conclusion
- `--goal GOAL_ID` - Associate with learning goal
- `--category CATEGORY` - Content category
- `--quick` - Quick capture mode (minimal processing)
- `--auto-extract` - Auto-extract content from URL
- `--credibility-check` - Enhanced credibility analysis

## Natural Language Processing:
Automatically detects:
- Article references: "I read an article about...", "interesting piece on..."
- Source indicators: "from Harvard Business Review", "published in Nature"
- Insight markers: "key finding", "important insight", "main takeaway"
- Action cues: "actionable advice", "practical steps", "recommendations"
- Evidence signals: "research shows", "data indicates", "study found"

## Content Analysis Features:

### Credibility Assessment
```markdown
🔍 **Source Analysis**: Harvard Business Review
⭐ **Credibility Score**: 9/10 (High Authority)
📊 **Evidence Quality**: Strong (peer-reviewed, data-backed)
🎯 **Bias Assessment**: Minimal (fact-focused, balanced perspective)
📅 **Recency**: Published 2 weeks ago (Current)
```

### Concept Extraction
```markdown
💡 **Key Concepts Identified**:
- Decision automation in project planning
- Predictive risk analysis methodologies
- Resource optimization algorithms
- Human-AI collaboration frameworks

🔗 **Related Concepts** (from your knowledge base):
- Connects to "Project Management Systems" (3 articles)
- Builds on "AI in Business" learning thread
- Complements "Automation Strategies" framework
```

### Learning Integration
```markdown
🎯 **Learning Goals Updated**:
- AI/ML Leadership: +15% progress
- Project Management: +8% progress

📚 **Knowledge Network Growth**:
- Total articles: 45 → 46
- Concept connections: 203 → 208
- Cross-references: 5 new connections identified
```

## Output Examples:

### Research Article Capture
```json
{
  "status": "success",
  "command": "/learn article",
  "data": {
    "note_id": "article-ai-project-management-hbr-a1b2c3d4",
    "article_title": "AI in Project Management",
    "source": "Harvard Business Review",
    "concepts_identified": ["decision-automation", "predictive-risk-analysis", "resource-optimization"],
    "key_insights": 4,
    "connections": {
      "learning_goals_updated": ["ai-ml-leadership", "project-management"],
      "related_articles": 3,
      "total_connections": 5
    },
    "quality_assessment": {
      "credibility_score": "9/10",
      "evidence_quality": "strong",
      "content_type": "analytical",
      "technical_depth": "high"
    }
  },
  "analysis": {
    "content_quality": "High-quality research from Harvard Business Review",
    "learning_alignment": "Strongly aligned with 2 learning goals",
    "knowledge_network": "Connected to 3 related articles in your knowledge base"
  },
  "suggested_applications": [
    "Implement predictive risk analysis in Q4 projects",
    "Test decision automation tools for team workflows",
    "Design human-AI collaboration framework"
  ],
  "next_actions": [
    "Plan implementation of these actionable insights",
    "Update progress on ai-ml-leadership learning goal",
    "Create concept connections using /learn connect"
  ]
}
```

### Quick Blog Post Capture
```json
{
  "status": "success",
  "command": "/learn article",
  "data": {
    "note_id": "article-productivity-tips-medium-e5f6g7h8",
    "article_title": "10 Productivity Tips for Remote Workers",
    "source": "Medium",
    "concepts_identified": ["time-blocking", "deep-work", "environment-design"],
    "quality_assessment": {
      "credibility_score": "6/10",
      "content_type": "informational"
    }
  },
  "analysis": {
    "content_quality": "Moderate-quality content from Medium",
    "learning_alignment": "Aligned with productivity-systems goal"
  },
  "next_actions": [
    "Test time-blocking technique this week",
    "Validate productivity statistics from independent sources"
  ]
}
```

## Integration Features:
- **Source Verification**: Cross-check with sources.yaml and add credible sources automatically
- **Bias Detection**: Identify potential bias in opinion pieces and persuasive content
- **Fact Validation**: Flag statistical claims for independent verification
- **Knowledge Graph**: Build connections between articles, concepts, and learning goals
- **Reading Analytics**: Track article consumption patterns and learning efficiency

## Behavior:
- Creates comprehensive article learning entries with quality assessment
- Provides intelligent credibility analysis and bias detection
- Identifies cross-article connections and concept relationships
- Generates actionable insights and practical application suggestions
- Maintains article knowledge network with semantic connections
- Supports both quick capture and deep analysis workflows
- Integrates with existing PARA Method learning infrastructure

Transform your article consumption into structured learning with intelligent analysis, credibility assessment, and knowledge network integration.
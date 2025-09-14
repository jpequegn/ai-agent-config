---
name: learn meeting
description: Capture learning insights from conversations, meetings, and discussions with intelligent knowledge extraction
---

# Learn Meeting

Capture valuable learning insights from conversations, meetings, and discussions with intelligent knowledge extraction, relationship mapping, and professional development tracking.

## Usage Examples:
- `/learn meeting --attendees "Sarah, John" --topic "team dynamics" --insight "Psychological safety increases innovation"`
- `/learn meeting "1:1 with mentor" --key-advice "Focus on systems over goals" --context "career development"`
- `/learn meeting --call "client discussion" --industry-insight "AI adoption challenges in healthcare" --follow-up "research HIPAA compliance"`
- `/learn meeting --retrospective --team "engineering" --lessons "async communication improves velocity" --actions "implement daily standups"`

## Instructions:

You are a meeting learning assistant for the PARA Method learning system. When this command is invoked:

1. **Parse meeting learning request**:
   - Meeting context and participants involved
   - Discussion topic and conversation theme
   - Key insights, advice, and wisdom shared
   - Learning moments and knowledge exchanges
   - Professional development opportunities identified

2. **Analyze conversation value**:
   - Assess learning quality and applicability
   - Identify expertise sources and credibility
   - Categorize knowledge type (technical, strategic, interpersonal)
   - Map relationship dynamics and communication patterns
   - Extract actionable insights and follow-up opportunities

3. **Process learning content**:
   - **Key Insights**: Important realizations and knowledge gained
   - **Expert Advice**: Wisdom and guidance from experienced individuals
   - **Best Practices**: Proven methods and successful approaches
   - **Industry Intelligence**: Market insights and sector knowledge
   - **Interpersonal Learning**: Communication and relationship insights
   - **Strategic Thinking**: High-level perspectives and frameworks

4. **Create structured meeting learning entry**:
   ```bash
   python3 -c "
   import json, yaml, datetime, re, hashlib
   from pathlib import Path

   # Load learning data
   captures_file = Path('.claude/cache/learning_captures.json')
   goals_file = Path('.claude/learning_goals.yaml')

   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}

   # Generate meeting ID
   topic = '${topic}' or 'discussion'
   attendees = '${attendees}' or 'conversation'
   timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')

   # Create content hash for uniqueness
   content_hash = hashlib.md5(f'{topic}{attendees}{timestamp}'.encode()).hexdigest()[:6]
   meeting_id = f'meeting-{re.sub(r\"[^a-z0-9]+\", \"-\", topic.lower())[:20]}-{content_hash}'

   # Assess learning quality and source credibility
   def assess_learning_quality(attendees_str, context, insights):
       quality_score = 5  # Default medium quality

       # Increase for senior/expert interactions
       if any(keyword in attendees_str.lower() for keyword in ['ceo', 'director', 'senior', 'principal', 'lead', 'expert', 'mentor']):
           quality_score += 2

       # Increase for strategic contexts
       if any(keyword in context.lower() for keyword in ['strategy', 'leadership', 'vision', 'planning', 'transformation']):
           quality_score += 1

       # Increase for actionable insights
       if any(keyword in insights for keyword in ['implement', 'apply', 'action', 'next steps', 'follow-up']):
           quality_score += 1

       # Increase for specific, detailed insights
       insight_length = sum(len(insight.split()) for insight in insights if insight)
       if insight_length > 50:
           quality_score += 1

       return min(quality_score, 10)

   attendees_list = [a.strip() for a in '${attendees}'.split(',') if a.strip()]
   insights_list = [i.strip() for i in '${insights}'.split('|') if i.strip()]
   context = '${context}' or 'general discussion'

   quality_score = assess_learning_quality('${attendees}', context, insights_list)

   # Create meeting learning capture
   capture = {
       'id': meeting_id,
       'timestamp': datetime.datetime.now().isoformat(),
       'type': 'meeting_learning',
       'source_type': 'conversation',
       'meeting_topic': topic,
       'meeting_type': '${meeting_type}' or 'discussion',
       'context': context,
       'participants': {
           'attendees': attendees_list,
           'primary_contact': attendees_list[0] if attendees_list else None,
           'expertise_level': '${expertise_level}' or 'mixed',
           'relationship_type': '${relationship}' or 'professional'
       },
       'content': {
           'key_insights': insights_list,
           'expert_advice': [advice.strip() for advice in '${advice}'.split('|') if advice.strip()],
           'best_practices': [bp.strip() for bp in '${best_practices}'.split(',') if bp.strip()],
           'industry_intelligence': [intel.strip() for intel in '${industry_intel}'.split('|') if intel.strip()],
           'strategic_thinking': [st.strip() for st in '${strategic}'.split('|') if st.strip()],
           'interpersonal_learning': [il.strip() for il in '${interpersonal}'.split('|') if il.strip()],
           'questions_raised': [q.strip() for q in '${questions}'.split(',') if q.strip()],
           'lessons_learned': [ll.strip() for ll in '${lessons}'.split('|') if ll.strip()],
           'quotes': [{'text': q.strip(), 'speaker': None} for q in '${quotes}'.split('|') if q.strip()]
       },
       'outcomes': {
           'follow_up_actions': [action.strip() for action in '${actions}'.split(',') if action.strip()],
           'research_topics': [topic.strip() for topic in '${research}'.split(',') if topic.strip()],
           'connections_to_make': [conn.strip() for conn in '${connections}'.split(',') if conn.strip()],
           'skills_to_develop': [skill.strip() for skill in '${skills}'.split(',') if skill.strip()],
           'books_recommended': [book.strip() for book in '${books}'.split(',') if book.strip()],
           'next_meeting_planned': bool('${next_meeting}')
       },
       'analysis': {
           'learning_quality': quality_score,
           'knowledge_density': len(insights_list) + len([advice.strip() for advice in '${advice}'.split('|') if advice.strip()]),
           'actionability_score': len([action.strip() for action in '${actions}'.split(',') if action.strip()]),
           'strategic_value': '${strategic_value}' or 'medium',
           'relationship_building': len(attendees_list) > 1,
           'expertise_accessed': quality_score >= 7,
           'meeting_duration_minutes': int('${duration}') if '${duration}' else None
       },
       'connections': {
           'learning_goals': [],
           'related_captures': [],
           'project_applications': [],
           'people_network': attendees_list
       },
       'metadata': {
           'meeting_date': '${meeting_date}' or datetime.date.today().strftime('%Y-%m-%d'),
           'location': '${location}' or 'virtual',
           'meeting_format': '${format}' or 'discussion',  # discussion, presentation, workshop, interview
           'planned_vs_spontaneous': '${planned}' or 'spontaneous',
           'formality_level': '${formality}' or 'professional',  # casual, professional, formal
           'category': '${category}' or 'professional-development',
           'tags': [],
           'confidentiality': '${confidentiality}' or 'standard'
       },
       'created_by': 'learn-meeting-command'
   }

   # Auto-identify learning goal connections
   all_content = (topic + ' ' + context + ' ' + ' '.join(insights_list) + ' ' + ' '.join(capture['content']['expert_advice'])).lower()

   for goal_id, goal in goals_data.get('learning_goals', {}).items():
       goal_keywords = set((goal.get('name', '') + ' ' + ' '.join(goal.get('tags', []))).lower().split())

       # Check for keyword matches
       keyword_matches = sum(1 for keyword in goal_keywords if len(keyword) > 3 and keyword in all_content)
       if keyword_matches >= 1:
           capture['connections']['learning_goals'].append(goal_id)

   # Auto-generate tags based on content analysis
   tag_mapping = {
       'leadership': ['leadership', 'management', 'team', 'director', 'strategy'],
       'technical': ['technology', 'engineering', 'development', 'software', 'system'],
       'business': ['business', 'revenue', 'growth', 'market', 'sales', 'customer'],
       'communication': ['communication', 'presentation', 'feedback', 'discussion'],
       'career': ['career', 'promotion', 'development', 'skills', 'mentor'],
       'strategy': ['strategy', 'planning', 'vision', 'roadmap', 'goals'],
       'innovation': ['innovation', 'creative', 'ideas', 'breakthrough', 'experimental'],
       'networking': ['networking', 'relationship', 'connection', 'introduction']
   }

   for tag, keywords in tag_mapping.items():
       if any(keyword in all_content for keyword in keywords):
           capture['metadata']['tags'].append(tag)

   # Find connections to related meeting captures
   for existing_capture in captures_data.get('captures', []):
       if existing_capture.get('source_type') == 'conversation' and existing_capture.get('id') != capture['id']:
           # Check for attendee overlap
           existing_attendees = set(existing_capture.get('participants', {}).get('attendees', []))
           new_attendees = set(attendees_list)

           if existing_attendees.intersection(new_attendees) or existing_capture.get('meeting_topic') == topic:
               capture['connections']['related_captures'].append(existing_capture['id'])

   # Add to captures
   captures_data.setdefault('captures', []).append(capture)

   # Save updated data
   captures_file.parent.mkdir(exist_ok=True)
   captures_file.write_text(json.dumps(captures_data, indent=2))

   # Generate intelligent response
   response = {
       'status': 'success',
       'command': '/learn meeting',
       'data': {
           'note_id': capture['id'],
           'meeting_topic': topic,
           'attendees': attendees_list,
           'insights_captured': len(insights_list),
           'learning_quality': f'{quality_score}/10',
           'connections': {
               'learning_goals_updated': capture['connections']['learning_goals'],
               'people_network': len(capture['connections']['people_network']),
               'related_meetings': len(capture['connections']['related_captures'])
           },
           'learning_value': {
               'knowledge_density': capture['analysis']['knowledge_density'],
               'actionable_items': capture['analysis']['actionability_score'],
               'strategic_insights': len(capture['content']['strategic_thinking']),
               'expert_guidance': len(capture['content']['expert_advice'])
           },
           'follow_up_needed': {
               'action_items': len(capture['outcomes']['follow_up_actions']),
               'research_topics': len(capture['outcomes']['research_topics']),
               'connections_to_make': len(capture['outcomes']['connections_to_make']),
               'skills_to_develop': len(capture['outcomes']['skills_to_develop'])
           }
       },
       'analysis': {
           'conversation_quality': f'High-value learning conversation' if quality_score >= 7 else f'Moderate learning value from discussion',
           'expertise_accessed': f'Gained insights from {len(attendees_list)} participants' + (f' including senior expertise' if any('senior' in a.lower() or 'director' in a.lower() for a in attendees_list) else ''),
           'knowledge_network': f'Connected to {len(capture[\"connections\"][\"related_captures\"])} related conversations'
       },
       'immediate_actions': [],
       'next_steps': []
   }

   # Generate contextual recommendations
   if capture['outcomes']['follow_up_actions']:
       response['immediate_actions'] = capture['outcomes']['follow_up_actions'][:3]
       response['next_steps'].append('Schedule time to complete follow-up actions')

   if capture['connections']['learning_goals']:
       response['next_steps'].append(f'Update progress on {capture[\"connections\"][\"learning_goals\"][0]} learning goal')

   if capture['outcomes']['research_topics']:
       response['next_steps'].append('Add research topics to learning pipeline')

   if capture['outcomes']['books_recommended']:
       response['next_steps'].append('Add recommended books to reading list using /learn sources')

   if capture['outcomes']['connections_to_make']:
       response['next_steps'].append('Reach out to suggested connections within 48 hours')

   if quality_score >= 8:
       response['next_steps'].append('Consider scheduling follow-up conversation to deepen insights')

   if len(insights_list) > 3:
       response['next_steps'].append('Create concept connections using /learn connect')

   print(json.dumps(response, indent=2))
   "
   ```

5. **Provide intelligent conversation analysis**:
   - Learning quality assessment based on expertise and insights
   - Relationship value evaluation and network building opportunities
   - Knowledge transfer effectiveness and actionability scoring
   - Professional development impact and career advancement insights
   - Communication pattern analysis and interpersonal learning

## Meeting Learning Types:

### Strategic Conversations
- **Leadership Insights**: Learning from senior leaders and executives
- **Industry Intelligence**: Market trends and sector knowledge
- **Vision and Planning**: Strategic thinking and long-term perspectives

### Technical Discussions
- **Expert Knowledge**: Learning from technical specialists
- **Best Practices**: Proven methods and successful approaches
- **Problem Solving**: Collaborative solution development

### Professional Development
- **Mentorship Sessions**: Career guidance and skill development
- **Peer Learning**: Knowledge exchange with colleagues
- **Network Building**: Relationship development and connection building

### Client and Stakeholder Meetings
- **Industry Learning**: Customer and market insights
- **Requirements Understanding**: Business needs and challenges
- **Solution Design**: Collaborative problem definition and resolution

## Parameters:
- `--attendees PEOPLE` - Meeting participants (comma-separated)
- `--topic TOPIC` - Meeting or conversation topic
- `--context CONTEXT` - Meeting context or purpose
- `--meeting-type TYPE` - Type of meeting (1:1, team, client, workshop)
- `--insights TEXT` - Key insights (separate multiple with |)
- `--advice TEXT` - Expert advice received (separate with |)
- `--best-practices LIST` - Best practices discussed (comma-separated)
- `--industry-intel TEXT` - Industry intelligence (separate with |)
- `--strategic TEXT` - Strategic thinking insights (separate with |)
- `--interpersonal TEXT` - Interpersonal learning (separate with |)
- `--lessons TEXT` - Lessons learned (separate with |)
- `--quotes TEXT` - Important quotes (separate with |)
- `--actions LIST` - Follow-up actions (comma-separated)
- `--research LIST` - Research topics (comma-separated)
- `--connections LIST` - Connections to make (comma-separated)
- `--skills LIST` - Skills to develop (comma-separated)
- `--books LIST` - Books recommended (comma-separated)
- `--duration MINUTES` - Meeting duration
- `--goal GOAL_ID` - Associate with learning goal
- `--category CATEGORY` - Learning category
- `--expertise-level LEVEL` - Expertise level (junior, mixed, senior, expert)
- `--strategic-value VALUE` - Strategic value assessment (low, medium, high)

## Natural Language Processing:
Automatically detects:
- Meeting references: "talked with...", "discussion with...", "meeting about..."
- Insight markers: "learned that...", "realized...", "key insight...", "important point..."
- Advice indicators: "recommended...", "suggested...", "advised...", "shared wisdom..."
- Action cues: "follow up on...", "need to research...", "should connect with..."
- People references: Names, titles, roles, and relationship contexts

## Conversation Analysis Features:

### Learning Quality Assessment
```markdown
💡 **Learning Value**: 8/10 (High-quality insights)
👥 **Expertise Accessed**: Senior Director level
🎯 **Strategic Alignment**: Strongly aligned with 2 learning goals
⚡ **Actionability**: 5 specific follow-up actions identified
🔗 **Network Value**: 3 new professional connections
```

### Knowledge Extraction
```markdown
🧠 **Key Insights Captured**:
- Psychological safety increases team innovation by 35%
- Async communication reduces meeting overhead by 40%
- Cross-functional alignment requires weekly check-ins
- Technical debt impacts feature velocity exponentially

💼 **Expert Advice Received**:
- "Focus on systems over individual performance metrics"
- "Invest in automation early, even if it seems slower initially"
- "Build trust through consistent small commitments"
```

### Relationship Intelligence
```markdown
👥 **People Network Growth**:
- Attendees: Sarah (Engineering Director), John (Product Manager)
- Relationship Level: Professional mentoring
- Connection Strength: High (ongoing collaboration)
- Follow-up Scheduled: Monthly 1:1 with Sarah

🤝 **Networking Opportunities**:
- Introduction to AI team lead next week
- Connection to Bay Area tech meetup group
- Potential collaboration on Q4 automation project
```

## Output Examples:

### Strategic Conversation Capture
```json
{
  "status": "success",
  "command": "/learn meeting",
  "data": {
    "note_id": "meeting-team-dynamics-a1b2c3",
    "meeting_topic": "team dynamics",
    "attendees": ["Sarah (Director)", "John (PM)"],
    "insights_captured": 4,
    "learning_quality": "8/10",
    "connections": {
      "learning_goals_updated": ["leadership-development", "team-management"],
      "people_network": 2,
      "related_meetings": 1
    },
    "learning_value": {
      "knowledge_density": 6,
      "actionable_items": 3,
      "strategic_insights": 2,
      "expert_guidance": 3
    }
  },
  "analysis": {
    "conversation_quality": "High-value learning conversation",
    "expertise_accessed": "Gained insights from 2 participants including senior expertise",
    "knowledge_network": "Connected to 1 related conversations"
  },
  "immediate_actions": [
    "Implement weekly team alignment meetings",
    "Research psychological safety assessment tools",
    "Schedule follow-up with engineering team"
  ],
  "next_steps": [
    "Schedule time to complete follow-up actions",
    "Update progress on leadership-development learning goal",
    "Create concept connections using /learn connect"
  ]
}
```

### Mentor Conversation Capture
```json
{
  "status": "success",
  "command": "/learn meeting",
  "data": {
    "note_id": "meeting-mentor-session-d4e5f6",
    "meeting_topic": "career development guidance",
    "attendees": ["Emma (Senior VP)"],
    "learning_quality": "9/10",
    "learning_value": {
      "expert_guidance": 5,
      "strategic_insights": 3,
      "actionable_items": 4
    }
  },
  "analysis": {
    "conversation_quality": "High-value learning conversation",
    "expertise_accessed": "Gained insights from senior executive perspective"
  },
  "next_steps": [
    "Add recommended books to reading list using /learn sources",
    "Reach out to suggested connections within 48 hours",
    "Consider scheduling follow-up conversation to deepen insights"
  ]
}
```

## Integration Features:
- **People Network Mapping**: Track relationships and build professional network graph
- **Learning Goal Progression**: Connect insights to specific learning objectives
- **Action Item Management**: Integration with task and project management systems
- **Knowledge Cross-Pollination**: Link conversation insights to books, articles, and courses
- **Meeting Series Tracking**: Connect related conversations over time

## Behavior:
- Creates comprehensive meeting learning entries with relationship context
- Provides intelligent assessment of learning quality and strategic value
- Identifies actionable follow-up items and professional development opportunities
- Maps professional network connections and relationship building
- Maintains conversation history and insight evolution over time
- Supports both formal meetings and informal conversations
- Integrates with existing PARA Method learning and relationship management

Transform your conversations into structured learning with intelligent insight extraction, relationship mapping, and professional development acceleration.
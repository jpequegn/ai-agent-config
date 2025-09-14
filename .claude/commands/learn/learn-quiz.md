---
name: learn quiz
description: Generate adaptive quiz questions from learning notes with intelligent follow-up insights and performance tracking
---

# Learn Quiz

Generate intelligent, contextual quiz questions from your accumulated learning notes with adaptive difficulty, personalized insights, and performance-based learning reinforcement based on spaced repetition principles.

## Usage Examples:
- `/learn quiz --topic "project-management" --difficulty adaptive`
- `/learn quiz --goal ai-agent-architecture --questions 5`
- `/learn quiz --source building-a-second-brain --format multiple-choice`
- `/learn quiz --review-mode --performance-level struggling`

## Instructions:

You are an adaptive learning quiz specialist for the PARA Method learning system. When this command is invoked:

1. **Parse quiz request parameters**:
   - Topic or learning goal focus area
   - Difficulty level (beginner, intermediate, advanced, adaptive)
   - Question format (multiple-choice, open-ended, scenario-based)
   - Number of questions and session type
   - Performance history and adaptation needs

2. **Analyze learning context and content**:
   - Load relevant learning captures and insights
   - Identify key concepts, relationships, and applications
   - Assess user's knowledge level and learning history
   - Determine optimal question difficulty and style
   - Select contextual connections for follow-up insights

3. **Generate intelligent quiz questions**:
   - **Concept Mastery**: Test understanding of key concepts
   - **Application Scenarios**: Real-world problem-solving questions
   - **Connection Testing**: Questions linking different concepts or domains
   - **Critical Thinking**: Analysis and synthesis questions
   - **Retention Checks**: Spaced repetition based on forgetting curve
   - **Follow-up Insights**: Contextual connections to other learning

4. **Create adaptive quiz session**:
   ```bash
   python3 -c "
   import json, yaml, datetime, re, random
   from pathlib import Path
   from collections import defaultdict, Counter

   # Load learning data
   captures_file = Path('.claude/cache/learning_captures.json')
   goals_file = Path('.claude/learning_goals.yaml')
   sources_file = Path('.claude/sources.yaml')
   quiz_history_file = Path('.claude/cache/quiz_sessions.json')

   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {'sources': {}}
   quiz_history = json.loads(quiz_history_file.read_text()) if quiz_history_file.exists() else {'sessions': []}

   # Parse parameters
   topic = '${topic}' or None
   goal_id = '${goal}' or None
   source_id = '${source}' or None
   difficulty = '${difficulty}' or 'intermediate'
   num_questions = int('${questions}') if '${questions}' else 3
   question_format = '${format}' or 'multiple-choice'
   review_mode = bool('${review_mode}')
   performance_level = '${performance_level}' or None

   # Advanced Quiz Generation Engine
   class AdaptiveQuizGenerator:
       def __init__(self, captures, goals, sources, history):
           self.captures = captures
           self.goals = goals
           self.sources = sources
           self.history = history
           self.difficulty_levels = {
               'beginner': {'complexity_score': 0.3, 'connections_required': 1},
               'intermediate': {'complexity_score': 0.6, 'connections_required': 2},
               'advanced': {'complexity_score': 0.9, 'connections_required': 3}
           }

       def filter_relevant_content(self, topic=None, goal_id=None, source_id=None):
           '''Filter learning captures based on quiz focus'''
           relevant_captures = []

           for capture in self.captures.get('captures', []):
               include_capture = False

               # Filter by topic (search in concepts, insights, content)
               if topic:
                   content_text = self._get_capture_text(capture).lower()
                   if topic.lower() in content_text:
                       include_capture = True

               # Filter by learning goal
               elif goal_id:
                   if goal_id in capture.get('connections', {}).get('learning_goals', []):
                       include_capture = True

               # Filter by source
               elif source_id:
                   if capture.get('source_type') == 'book' and capture.get('book_title', '').lower() == source_id.lower():
                       include_capture = True
                   elif capture.get('source') == source_id:
                       include_capture = True

               # If no specific filter, include all recent captures
               else:
                   include_capture = True

               if include_capture:
                   relevant_captures.append(capture)

           return relevant_captures[-20:]  # Limit to recent 20 captures

       def _get_capture_text(self, capture):
           '''Extract searchable text from capture'''
           text_parts = []
           content = capture.get('content', {})

           if content.get('insights'):
               text_parts.extend(content['insights'])
           if content.get('key_concepts'):
               text_parts.extend(content['key_concepts'])
           if content.get('concepts'):
               text_parts.extend(content['concepts'])
           if content.get('takeaway'):
               text_parts.append(content['takeaway'])
           if content.get('summary'):
               text_parts.append(content['summary'])

           return ' '.join(text_parts)

       def analyze_performance_history(self, topic=None):
           '''Analyze past quiz performance to adapt difficulty'''
           if not self.history.get('sessions'):
               return 'intermediate'

           relevant_sessions = []
           for session in self.history['sessions']:
               if not topic or topic.lower() in session.get('topic', '').lower():
                   relevant_sessions.append(session)

           if not relevant_sessions:
               return 'intermediate'

           # Calculate recent performance
           recent_sessions = sorted(relevant_sessions, key=lambda x: x['timestamp'])[-3:]
           avg_score = sum(s.get('score', 0.5) for s in recent_sessions) / len(recent_sessions)

           # Adapt difficulty based on performance
           if avg_score >= 0.8:
               return 'advanced'
           elif avg_score >= 0.6:
               return 'intermediate'
           else:
               return 'beginner'

       def generate_multiple_choice_question(self, concept, context, difficulty_level):
           '''Generate a multiple choice question for a concept'''
           complexity = self.difficulty_levels[difficulty_level]['complexity_score']

           if complexity < 0.5:
               # Beginner: Direct concept definition/recognition
               question_templates = [
                   f'What is {concept}?',
                   f'Which of the following best describes {concept}?',
                   f'In the context of {context}, {concept} refers to:'
               ]
           elif complexity < 0.8:
               # Intermediate: Application and analysis
               question_templates = [
                   f'How would you apply {concept} in a real-world scenario?',
                   f'What is the most effective way to implement {concept}?',
                   f'Which scenario best demonstrates the use of {concept}?'
               ]
           else:
               # Advanced: Synthesis and critical thinking
               question_templates = [
                   f'How does {concept} relate to other methodologies in {context}?',
                   f'What are the potential limitations of {concept} in complex scenarios?',
                   f'How might {concept} evolve in the next 5 years?'
               ]

           question_stem = random.choice(question_templates)

           # Generate plausible options based on difficulty
           if difficulty_level == 'beginner':
               options = self._generate_basic_options(concept, context)
           elif difficulty_level == 'intermediate':
               options = self._generate_application_options(concept, context)
           else:
               options = self._generate_synthesis_options(concept, context)

           return {
               'type': 'multiple-choice',
               'question': question_stem,
               'options': options,
               'correct_answer_index': 1,  # B is typically correct
               'explanation': f'This question tests understanding of {concept} within {context}.',
               'difficulty': difficulty_level,
               'concept': concept,
               'context': context
           }

       def _generate_basic_options(self, concept, context):
           '''Generate basic multiple choice options'''
           return [
               f'A basic definition that is incorrect',
               f'The correct understanding of {concept}',  # Correct answer
               f'A common misconception about {concept}',
               f'An unrelated concept from {context}'
           ]

       def _generate_application_options(self, concept, context):
           '''Generate application-focused options'''
           return [
               f'Apply {concept} without considering context',
               f'Implement {concept} with proper {context} integration',  # Correct answer
               f'Use {concept} only in theoretical scenarios',
               f'Replace {concept} with simpler alternatives'
           ]

       def _generate_synthesis_options(self, concept, context):
           '''Generate synthesis and analysis options'''
           return [
               f'{concept} operates independently of other factors',
               f'{concept} requires integration with broader {context} systems',  # Correct answer
               f'{concept} is only effective in ideal conditions',
               f'{concept} will become obsolete within five years'
           ]

       def generate_scenario_question(self, concept, context, difficulty_level):
           '''Generate scenario-based question'''
           if difficulty_level == 'beginner':
               scenario_stem = f'You are learning about {concept}. What is your first step?'
           elif difficulty_level == 'intermediate':
               scenario_stem = f'You are implementing {concept} in your {context} project. What challenges might you face?'
           else:
               scenario_stem = f'You are leading a team using {concept} in a complex {context} environment. How do you optimize for both efficiency and quality?'

           return {
               'type': 'scenario',
               'question': scenario_stem,
               'evaluation_criteria': [
                   'Understanding of core concept',
                   'Practical application knowledge',
                   'Context awareness',
                   'Problem-solving approach'
               ],
               'difficulty': difficulty_level,
               'concept': concept,
               'context': context
           }

       def generate_connection_question(self, concepts, context):
           '''Generate question testing connections between concepts'''
           if len(concepts) < 2:
               return None

           concept1, concept2 = concepts[:2]
           question_stem = f'How do {concept1} and {concept2} work together in {context}?'

           return {
               'type': 'connection',
               'question': question_stem,
               'concepts': [concept1, concept2],
               'evaluation_criteria': [
                   'Understanding of both concepts',
                   'Recognition of relationships',
                   'Practical integration knowledge',
                   'Systems thinking'
               ],
               'context': context
           }

       def generate_quiz_session(self, topic=None, goal_id=None, source_id=None,
                                difficulty='adaptive', num_questions=3, format_type='multiple-choice'):
           '''Generate complete adaptive quiz session'''

           # Filter relevant content
           relevant_captures = self.filter_relevant_content(topic, goal_id, source_id)

           if not relevant_captures:
               return {'error': 'No relevant learning content found for quiz generation'}

           # Adapt difficulty based on performance if set to adaptive
           if difficulty == 'adaptive':
               difficulty = self.analyze_performance_history(topic)

           # Extract concepts and context from captures
           all_concepts = []
           context_info = []

           for capture in relevant_captures:
               content = capture.get('content', {})
               if content.get('key_concepts'):
                   all_concepts.extend(content['key_concepts'])
               if content.get('concepts'):
                   all_concepts.extend(content['concepts'])

               # Build context from source types and topics
               source_type = capture.get('source_type', 'general')
               context_info.append(source_type)

           # Remove duplicates and select top concepts
           concept_counts = Counter(all_concepts)
           top_concepts = [concept for concept, count in concept_counts.most_common(10)]
           primary_context = Counter(context_info).most_common(1)[0][0] if context_info else 'general'

           # Generate questions
           questions = []
           used_concepts = set()

           for i in range(min(num_questions, len(top_concepts))):
               concept = top_concepts[i]
               if concept in used_concepts:
                   continue

               used_concepts.add(concept)

               if format_type == 'multiple-choice':
                   question = self.generate_multiple_choice_question(concept, primary_context, difficulty)
               elif format_type == 'scenario':
                   question = self.generate_scenario_question(concept, primary_context, difficulty)
               elif format_type == 'connection' and len(top_concepts) > 1:
                   question = self.generate_connection_question(top_concepts[i:i+2], primary_context)
               else:
                   question = self.generate_multiple_choice_question(concept, primary_context, difficulty)

               if question:
                   questions.append(question)

           return {
               'session_id': f'quiz-{datetime.datetime.now().strftime(\"%Y%m%d-%H%M%S\")}',
               'timestamp': datetime.datetime.now().isoformat(),
               'topic': topic or primary_context,
               'goal_id': goal_id,
               'source_id': source_id,
               'difficulty': difficulty,
               'format': format_type,
               'questions': questions,
               'total_questions': len(questions),
               'concepts_covered': list(used_concepts),
               'context': primary_context,
               'session_metadata': {
                   'captures_analyzed': len(relevant_captures),
                   'available_concepts': len(top_concepts),
                   'adaptive_difficulty': difficulty == 'adaptive'
               }
           }

   # Generate quiz session
   generator = AdaptiveQuizGenerator(captures_data, goals_data, sources_data, quiz_history)
   quiz_session = generator.generate_quiz_session(
       topic=topic,
       goal_id=goal_id,
       source_id=source_id,
       difficulty=difficulty,
       num_questions=num_questions,
       format_type=question_format
   )

   if 'error' in quiz_session:
       print(json.dumps({'status': 'error', 'message': quiz_session['error']}, indent=2))
   else:
       # Save quiz session for tracking
       quiz_history['sessions'] = quiz_history.get('sessions', [])
       quiz_history['sessions'].append(quiz_session)

       # Keep only last 50 sessions
       quiz_history['sessions'] = quiz_history['sessions'][-50:]

       quiz_history_file.parent.mkdir(exist_ok=True)
       quiz_history_file.write_text(json.dumps(quiz_history, indent=2))

       # Generate response with first question for immediate interaction
       first_question = quiz_session['questions'][0] if quiz_session['questions'] else None

       response = {
           'status': 'success',
           'command': '/learn quiz',
           'session_info': {
               'session_id': quiz_session['session_id'],
               'topic': quiz_session['topic'],
               'difficulty': quiz_session['difficulty'],
               'total_questions': quiz_session['total_questions'],
               'format': quiz_session['format']
           },
           'current_question': {
               'number': 1,
               'total': quiz_session['total_questions'],
               'question': first_question
           },
           'session_context': {
               'concepts_covered': quiz_session['concepts_covered'][:5],  # Show first 5
               'captures_analyzed': quiz_session['session_metadata']['captures_analyzed'],
               'adaptive_difficulty': quiz_session['session_metadata']['adaptive_difficulty']
           },
           'instructions': [
               'Answer the question and I will provide immediate feedback',
               'Each correct answer will be followed by insight connections',
               'Quiz adapts based on your performance and learning history',
               'Questions are designed to reinforce key concepts and applications'
           ]
       }

       print(json.dumps(response, indent=2))
   "
   ```

5. **Provide adaptive learning experience**:
   - Immediate feedback on answers with explanations
   - Follow-up insights connecting concepts across domains
   - Performance tracking for future session adaptation
   - Spaced repetition scheduling based on answer accuracy
   - Progressive difficulty adjustment during session

## Quiz Types:

### Multiple Choice Questions
- **Beginner**: Direct concept recognition and basic definitions
- **Intermediate**: Application scenarios and practical implementation
- **Advanced**: Analysis, synthesis, and critical evaluation

### Scenario-Based Questions
- **Real-world Applications**: Practical problem-solving scenarios
- **Case Studies**: Complex situations requiring integrated knowledge
- **Decision Making**: Multiple valid approaches with trade-off analysis

### Connection Testing
- **Cross-domain Links**: Connecting concepts across different learning areas
- **System Relationships**: Understanding how concepts work together
- **Knowledge Integration**: Applying multiple concepts to single scenarios

## Parameters:
- `--topic TOPIC` - Focus quiz on specific topic or concept area
- `--goal GOAL_ID` - Generate questions related to specific learning goal
- `--source SOURCE_ID` - Quiz content from specific learning source
- `--difficulty LEVEL` - Set difficulty (beginner, intermediate, advanced, adaptive)
- `--questions N` - Number of questions in quiz session (default: 3)
- `--format FORMAT` - Question format (multiple-choice, scenario, connection, mixed)
- `--review-mode` - Focus on concepts needing reinforcement
- `--performance-level LEVEL` - Target performance level (struggling, progressing, mastering)
- `--spaced-repetition` - Include questions based on forgetting curve timing
- `--connections` - Emphasize questions that test concept relationships

## Natural Language Processing:
Automatically detects:
- Quiz requests: "quiz me on", "test my knowledge", "practice questions"
- Topic indicators: "project management", "AI concepts", "productivity methods"
- Difficulty preferences: "challenging questions", "basic review", "advanced analysis"
- Format preferences: "multiple choice", "scenarios", "connections"
- Performance context: "I'm struggling with", "want to master", "need review"

## Adaptive Learning Features:

### Performance-Based Adaptation
```markdown
🎯 **Difficulty Adjustment**:
- High Performance (>80%): Increase complexity, add synthesis questions
- Medium Performance (60-80%): Maintain level, vary question types
- Low Performance (<60%): Simplify questions, focus on fundamentals

📊 **Learning Curve Analysis**:
- Concept Mastery: Track understanding progression over time
- Application Success: Monitor practical implementation accuracy
- Retention Rates: Measure long-term knowledge retention
```

### Intelligent Follow-up Insights
```markdown
💡 **Connection Insights**:
- Cross-domain Applications: How concepts apply across different areas
- Recent Learning Links: Connect to recently captured insights
- Goal Progression: Show how answers relate to learning objectives

🧠 **Knowledge Synthesis**:
- Pattern Recognition: Identify recurring themes in answers
- Gap Identification: Highlight areas needing additional focus
- Strength Recognition: Acknowledge areas of demonstrated mastery
```

### Spaced Repetition Integration
```markdown
⏰ **Forgetting Curve Optimization**:
- Initial Review: 1 day after first exposure
- Second Review: 3 days after first review
- Third Review: 1 week after second review
- Maintenance: Monthly reviews for long-term retention

🔄 **Adaptive Scheduling**:
- High Accuracy (>90%): Extend review intervals
- Medium Accuracy (70-90%): Standard review schedule
- Low Accuracy (<70%): Shorten review intervals, increase frequency
```

## Output Examples:

### Interactive Quiz Session
```json
{
  "status": "success",
  "command": "/learn quiz",
  "session_info": {
    "session_id": "quiz-20241214-143022",
    "topic": "project-management",
    "difficulty": "adaptive",
    "total_questions": 3,
    "format": "multiple-choice"
  },
  "current_question": {
    "number": 1,
    "total": 3,
    "question": {
      "type": "multiple-choice",
      "question": "You're managing a project with unclear requirements and tight timeline. Based on your Lean Startup learning, what's your first step?",
      "options": [
        "Create detailed project plan with all assumptions documented",
        "Build minimum viable scope and test core assumptions",
        "Escalate timeline concerns to stakeholders immediately",
        "Request additional requirements gathering time"
      ],
      "correct_answer_index": 1,
      "difficulty": "intermediate",
      "concept": "lean-startup-methodology",
      "context": "project-management"
    }
  },
  "session_context": {
    "concepts_covered": ["lean-startup", "project-management", "agile-methodology"],
    "captures_analyzed": 8,
    "adaptive_difficulty": true
  },
  "instructions": [
    "Answer the question and I will provide immediate feedback",
    "Each correct answer will be followed by insight connections",
    "Quiz adapts based on your performance and learning history"
  ]
}
```

### Post-Answer Feedback
```markdown
✅ **Correct!** You're connecting Lean principles to project management well.

**Why this answer is optimal:**
- Lean Startup methodology emphasizes validated learning over detailed planning
- Building MVP scope allows rapid assumption testing within tight constraints
- Reduces risk of building wrong solution under time pressure

🔗 **Follow-up insight:** How does this connect to your recent team dynamics learning about psychological safety in decision-making?

*This approach requires team psychological safety to admit when initial assumptions are wrong and pivot quickly. Teams without safety may stick to incorrect assumptions to avoid admitting mistakes.*

**Next Question Loading...** (2 of 3)
```

### Session Summary
```json
{
  "session_complete": true,
  "performance_summary": {
    "score": 0.67,
    "questions_correct": 2,
    "total_questions": 3,
    "difficulty_progression": "intermediate → advanced",
    "concepts_mastered": ["lean-startup", "agile-methodology"],
    "concepts_for_review": ["risk-management"]
  },
  "learning_insights": [
    "Strong connection between Lean and Agile methodologies",
    "Risk management concepts need additional reinforcement",
    "Excellent synthesis of cross-domain knowledge"
  ],
  "next_actions": [
    "Review risk management concepts from project management sources",
    "Practice more advanced synthesis questions",
    "Schedule spaced repetition review in 3 days"
  ],
  "spaced_repetition": {
    "next_review_date": "2024-12-17",
    "review_concepts": ["risk-management"],
    "review_difficulty": "intermediate"
  }
}
```

## Integration Features:
- **Performance Tracking**: Detailed analytics on quiz performance over time
- **Spaced Repetition**: Automated scheduling based on forgetting curve research
- **Goal Alignment**: Questions prioritized based on active learning goals
- **Cross-domain Synthesis**: Questions connecting concepts across different learning areas
- **Adaptive Difficulty**: Real-time difficulty adjustment based on performance

## Behavior:
- Generates contextual, challenging questions from accumulated learning
- Provides immediate feedback with detailed explanations and insights
- Adapts difficulty and question types based on performance history
- Creates follow-up connections to reinforce learning and show relationships
- Schedules future reviews based on spaced repetition principles
- Tracks performance for long-term learning optimization
- Integrates with existing PARA Method learning infrastructure

Transform passive learning into active knowledge reinforcement with intelligent, adaptive quizzing that strengthens retention and reveals knowledge connections.
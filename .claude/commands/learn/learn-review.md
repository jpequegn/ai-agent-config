---
name: learn review
description: Conduct comprehensive reviews and spaced repetition sessions based on forgetting curve with adaptive scheduling and retention optimization
---

# Learn Review

Conduct systematic reviews of learning progress, spaced repetition sessions based on forgetting curve principles, analyze captured insights, and generate actionable recommendations for optimized retention and knowledge application.

## Usage Examples:
- `/learn review --spaced-repetition --goal ai-agent-architecture`
- `/learn review --type weekly --goal ai-agent-architecture`
- `/learn review --comprehensive --since 2024-09-01`
- `/learn review --forgetting-curve --adaptive-scheduling`
- `/learn review captures --category technical --limit 20`
- `/learn review progress --learning-pathway ai_engineer`
- `/learn review gaps --goal para-method-mastery --recommendations`

## Instructions:

You are a learning review assistant for the PARA Method learning system. When this command is invoked:

1. **Determine review scope and type**:
   - **Spaced Repetition**: Forgetting curve-based review sessions for optimal retention
   - **Weekly/Monthly Reviews**: Regular progress assessments
   - **Goal Reviews**: Focus on specific learning goals
   - **Capture Reviews**: Analysis of recent insights and concepts
   - **Gap Analysis**: Identify learning gaps and missing connections
   - **Comprehensive**: Full learning portfolio assessment
   - **Adaptive Scheduling**: Personalized review timing based on performance

2. **Load and analyze learning data**:
   ```bash
   # Load learning data for comprehensive analysis including spaced repetition
   python3 -c "
   import json, yaml, datetime, math, statistics
   from pathlib import Path
   from collections import defaultdict, Counter

   # Load configuration files
   goals_file = Path('.claude/learning_goals.yaml')
   sources_file = Path('.claude/sources.yaml')
   captures_file = Path('.claude/cache/learning_captures.json')
   quiz_history_file = Path('.claude/cache/quiz_sessions.json')
   review_history_file = Path('.claude/cache/spaced_repetition.json')

   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {}
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {}
   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   quiz_history = json.loads(quiz_history_file.read_text()) if quiz_history_file.exists() else {'sessions': []}
   review_history = json.loads(review_history_file.read_text()) if review_history_file.exists() else {'reviews': []}

   # Parse parameters
   review_type = '${review_type}' or '${type}' or 'comprehensive'
   spaced_repetition = bool('${spaced_repetition}')
   forgetting_curve = bool('${forgetting_curve}')
   adaptive_scheduling = bool('${adaptive_scheduling}')
   goal_id = '${goal}' or None

   # Enhanced Spaced Repetition Review Engine
   class SpacedRepetitionReviewer:
       def __init__(self, goals, captures, quizzes, review_history):
           self.goals = goals
           self.captures = captures
           self.quizzes = quizzes
           self.review_history = review_history

           # Forgetting curve parameters (based on Ebbinghaus research)
           self.initial_retention = 1.0  # 100% retention immediately after learning
           self.decay_constant = 1.25    # How fast forgetting occurs
           self.retrieval_practice_bonus = 2.0  # Multiplier for successful retrieval

       def calculate_forgetting_curve(self, days_since_learning, retrieval_attempts=0, success_rate=1.0):
           '''Calculate expected retention based on forgetting curve'''
           # Base forgetting curve: R(t) = e^(-t/S) where S is memory strength
           base_retention = math.exp(-days_since_learning / self.decay_constant)

           # Adjust for retrieval practice (testing effect)
           if retrieval_attempts > 0:
               practice_bonus = (self.retrieval_practice_bonus * success_rate) ** retrieval_attempts
               adjusted_retention = base_retention * practice_bonus
           else:
               adjusted_retention = base_retention

           return min(adjusted_retention, 1.0)

       def identify_review_candidates(self, goal_id=None):
           '''Identify concepts needing review based on forgetting curve'''
           current_date = datetime.datetime.now()
           review_candidates = []

           # Get learning captures to review
           captures_to_review = []
           if goal_id:
               captures_to_review = [c for c in self.captures.get('captures', [])
                                   if goal_id in c.get('connections', {}).get('learning_goals', [])]
           else:
               captures_to_review = self.captures.get('captures', [])

           for capture in captures_to_review[-50:]:  # Review last 50 captures
               try:
                   learning_date = datetime.datetime.fromisoformat(capture.get('timestamp', ''))
                   days_since_learning = (current_date - learning_date).days

                   if days_since_learning < 1:
                       continue  # Too recent to need review

                   # Get concepts from capture
                   concepts = []
                   content = capture.get('content', {})
                   if content.get('key_concepts'):
                       concepts.extend(content['key_concepts'])
                   if content.get('concepts'):
                       concepts.extend(content['concepts'])

                   for concept in concepts:
                       # Get review history for this concept
                       review_stats = self._get_concept_review_stats(concept)

                       # Calculate current retention probability
                       retention = self.calculate_forgetting_curve(
                           days_since_learning,
                           review_stats['retrieval_attempts'],
                           review_stats['success_rate']
                       )

                       # Determine review urgency
                       if retention < 0.3:  # Less than 30% retention
                           urgency = 'critical'
                           priority_score = 10
                       elif retention < 0.5:  # Less than 50% retention
                           urgency = 'high'
                           priority_score = 8
                       elif retention < 0.7:  # Less than 70% retention
                           urgency = 'medium'
                           priority_score = 6
                       else:
                           urgency = 'low'
                           priority_score = 3

                       review_candidates.append({
                           'concept': concept,
                           'capture_id': capture.get('id'),
                           'days_since_learning': days_since_learning,
                           'estimated_retention': retention,
                           'urgency': urgency,
                           'priority_score': priority_score,
                           'review_stats': review_stats,
                           'source_type': capture.get('source_type', 'unknown'),
                           'goal_connections': capture.get('connections', {}).get('learning_goals', [])
                       })

               except (ValueError, KeyError):
                   continue

           # Sort by priority score and retention level
           return sorted(review_candidates, key=lambda x: (-x['priority_score'], x['estimated_retention']))

       def _get_concept_review_stats(self, concept):
           '''Get review history statistics for a concept'''
           retrieval_attempts = 0
           successful_retrievals = 0
           last_review_date = None

           # Check quiz history
           for session in self.quizzes.get('sessions', []):
               session_concepts = session.get('concepts_covered', [])
               if concept.lower() in [c.lower() for c in session_concepts]:
                   retrieval_attempts += 1
                   if session.get('score', 0) > 0.7:  # 70% threshold for success
                       successful_retrievals += 1

                   try:
                       session_date = datetime.datetime.fromisoformat(session.get('timestamp', ''))
                       if not last_review_date or session_date > last_review_date:
                           last_review_date = session_date
                   except:
                       continue

           # Check review history
           for review in self.review_history.get('reviews', []):
               reviewed_concepts = review.get('concepts_reviewed', [])
               if concept.lower() in [c.lower() for c in reviewed_concepts]:
                   retrieval_attempts += 1
                   if review.get('performance', {}).get('overall_score', 0) > 0.7:
                       successful_retrievals += 1

           success_rate = successful_retrievals / max(retrieval_attempts, 1)

           return {
               'retrieval_attempts': retrieval_attempts,
               'successful_retrievals': successful_retrievals,
               'success_rate': success_rate,
               'last_review_date': last_review_date.isoformat() if last_review_date else None,
               'days_since_last_review': (datetime.datetime.now() - last_review_date).days if last_review_date else 999
           }

       def generate_spaced_repetition_session(self, goal_id=None, session_length=5):
           '''Generate optimized spaced repetition session'''
           review_candidates = self.identify_review_candidates(goal_id)

           if not review_candidates:
               return {
                   'session_type': 'spaced_repetition',
                   'status': 'no_reviews_needed',
                   'message': 'All concepts have sufficient retention levels',
                   'next_review_date': None
               }

           # Select concepts for this session (prioritize by urgency and retention)
           session_concepts = review_candidates[:session_length]

           # Create review session
           session = {
               'session_id': f'review-{datetime.datetime.now().strftime(\"%Y%m%d-%H%M%S\")}',
               'session_type': 'spaced_repetition',
               'timestamp': datetime.datetime.now().isoformat(),
               'goal_id': goal_id,
               'concepts_to_review': session_concepts,
               'session_stats': {
                   'total_concepts': len(session_concepts),
                   'critical_urgency': len([c for c in session_concepts if c['urgency'] == 'critical']),
                   'high_urgency': len([c for c in session_concepts if c['urgency'] == 'high']),
                   'avg_retention': sum(c['estimated_retention'] for c in session_concepts) / len(session_concepts),
                   'avg_days_since_learning': sum(c['days_since_learning'] for c in session_concepts) / len(session_concepts)
               }
           }

           return session

       def calculate_adaptive_schedule(self, concept, performance_score):
           '''Calculate next review date based on performance and forgetting curve'''
           base_intervals = {
               'first_review': 1,      # 1 day after learning
               'second_review': 3,     # 3 days after first review
               'third_review': 7,      # 1 week after second review
               'fourth_review': 21,    # 3 weeks after third review
               'maintenance': 60       # 2 months for maintenance
           }

           # Get current review number for this concept
           review_stats = self._get_concept_review_stats(concept)
           review_number = review_stats['retrieval_attempts'] + 1

           # Select base interval
           if review_number == 1:
               base_interval = base_intervals['first_review']
           elif review_number == 2:
               base_interval = base_intervals['second_review']
           elif review_number == 3:
               base_interval = base_intervals['third_review']
           elif review_number == 4:
               base_interval = base_intervals['fourth_review']
           else:
               base_interval = base_intervals['maintenance']

           # Adjust interval based on performance
           if performance_score >= 0.9:  # Excellent performance
               adjusted_interval = base_interval * 1.5
           elif performance_score >= 0.8:  # Good performance
               adjusted_interval = base_interval * 1.2
           elif performance_score >= 0.7:  # Adequate performance
               adjusted_interval = base_interval
           elif performance_score >= 0.5:  # Poor performance
               adjusted_interval = base_interval * 0.5
           else:  # Very poor performance
               adjusted_interval = max(base_interval * 0.3, 1)  # At least 1 day

           next_review_date = datetime.datetime.now() + datetime.timedelta(days=int(adjusted_interval))

           return {
               'next_review_date': next_review_date.strftime('%Y-%m-%d'),
               'interval_days': int(adjusted_interval),
               'review_number': review_number,
               'performance_adjustment': 'extended' if adjusted_interval > base_interval else 'shortened' if adjusted_interval < base_interval else 'standard'
           }

   # Generate review session based on type
   if spaced_repetition or forgetting_curve:
       reviewer = SpacedRepetitionReviewer(goals_data, captures_data, quiz_history, review_history)
       session = reviewer.generate_spaced_repetition_session(goal_id, session_length=7)

       print(json.dumps({
           'status': 'success',
           'command': '/learn review',
           'session_data': session,
           'review_type': 'spaced_repetition'
       }, indent=2))
   else:
       # Existing comprehensive review logic continues here
       print(f'📊 Learning Review: {review_type.title()}')
       print('=' * 50)
   "
   ```

3. **Generate review analysis**:

   **Progress Analysis**:
   - Learning goal completion percentages
   - Milestone achievement rates
   - Timeline adherence assessment
   - Skill development tracking
   - Application implementation rates

   **Content Analysis**:
   - Capture frequency and patterns
   - Source utilization effectiveness
   - Knowledge category distribution
   - Tag usage and clustering
   - Connection density mapping

   **Gap Identification**:
   - Underutilized sources
   - Incomplete learning pathways
   - Missing skill connections
   - Abandoned or stalled goals
   - Low-application insights

4. **Provide actionable insights**:
   - Priority adjustments needed
   - Resource reallocation recommendations
   - Timeline modifications
   - Focus area suggestions
   - Application opportunities

5. **Generate review report**:
   ```bash
   # Generate comprehensive review report
   python3 -c "
   import json, yaml, datetime
   from pathlib import Path

   # Create review report structure
   report = {
       'review_id': f'review-{datetime.datetime.now().strftime(\"%Y%m%d-%H%M%S\")}',
       'timestamp': datetime.datetime.now().isoformat(),
       'type': '${review_type}',
       'scope': '${review_scope}',
       'period': '${review_period}',
       'summary': {
           'total_captures': 0,
           'active_goals': 0,
           'completed_milestones': 0,
           'sources_utilized': 0,
           'applications_implemented': 0
       },
       'progress_highlights': [],
       'areas_for_improvement': [],
       'recommendations': [],
       'next_actions': []
   }

   # Save review report
   reviews_file = Path('.claude/cache/learning_reviews.json')
   reviews_data = json.loads(reviews_file.read_text()) if reviews_file.exists() else {'reviews': []}
   reviews_data['reviews'].append(report)

   reviews_file.parent.mkdir(exist_ok=True)
   reviews_file.write_text(json.dumps(reviews_data, indent=2))

   print(f'📋 Review completed: {report[\"review_id\"]}')
   "
   ```

## Review Types:

### Spaced Repetition Review
- **Forgetting Curve Analysis**: Calculate retention probability for each concept based on Ebbinghaus research
- **Adaptive Scheduling**: Dynamic review intervals based on performance and retrieval success
- **Priority Ranking**: Urgent reviews for concepts with <30% estimated retention
- **Retrieval Practice**: Active recall sessions to strengthen long-term memory
- **Performance Tracking**: Monitor improvement in retention rates over time

### Forgetting Curve Session
- **Retention Assessment**: Scientific analysis of memory decay over time
- **Optimal Timing**: Review scheduling at points of maximum learning efficiency
- **Concept Prioritization**: Focus on concepts approaching critical retention thresholds
- **Memory Strengthening**: Targeted practice for concepts with high forgetting risk
- **Adaptive Intervals**: Personalized review timing based on individual learning patterns

### Weekly Review
- Recent capture analysis (last 7 days)
- Goal progress assessment
- Application implementation tracking
- Priority adjustments
- Next week planning

### Monthly Review
- Goal milestone evaluation
- Source effectiveness analysis
- Learning pathway progress
- Gap identification
- Quarterly goal alignment

### Goal-Focused Review
- Single goal deep dive
- Resource utilization for goal
- Skill development tracking
- Milestone completion analysis
- Timeline and priority assessment

### Comprehensive Review
- Full learning portfolio analysis
- Cross-goal connection mapping
- Learning velocity assessment
- ROI analysis for sources
- Strategic learning planning

### Gap Analysis
- Identify knowledge gaps
- Find underutilized resources
- Highlight missing connections
- Suggest learning opportunities
- Recommend focus adjustments

### Adaptive Scheduling Review
- **Performance-Based Intervals**: Extend intervals for well-retained concepts, shorten for struggling areas
- **Success Rate Analysis**: Track retrieval success rates for optimal interval adjustment
- **Learning Goal Alignment**: Prioritize reviews based on goal deadlines and importance
- **Cognitive Load Management**: Balance review sessions to prevent cognitive overload
- **Long-term Retention**: Maintenance schedule for long-term knowledge preservation

## Parameters:
- `--type TYPE` - Review type (weekly, monthly, goal, comprehensive, gaps)
- `--spaced-repetition` - Activate spaced repetition session based on forgetting curve
- `--forgetting-curve` - Use scientific forgetting curve analysis for review prioritization
- `--adaptive-scheduling` - Enable performance-based adaptive review scheduling
- `--goal GOAL_ID` - Focus on specific learning goal
- `--category CATEGORY` - Filter by category
- `--since DATE` - Review period start date
- `--until DATE` - Review period end date
- `--learning-pathway PATH` - Review specific pathway
- `--recommendations` - Include actionable recommendations
- `--export FORMAT` - Export format (markdown, json, pdf)
- `--detailed` - Include detailed analysis and metrics
- `--session-length N` - Number of concepts in spaced repetition session (default: 5)
- `--retention-threshold FLOAT` - Minimum retention level for review trigger (default: 0.7)

## Analytics Provided:

### Progress Metrics
- Goal completion percentages
- Milestone achievement rates
- Learning velocity (captures per week)
- Application implementation rates
- Source utilization scores

### Content Insights
- Most frequent capture types
- Top-performing sources
- Popular tags and categories
- Connection patterns
- Knowledge clustering

### Effectiveness Measures
- Time-to-application ratios
- Retention indicators
- Cross-goal knowledge transfer
- Learning compound effects
- ROI by source and category

### Predictive Analysis
- Goal completion forecasts
- Learning bottleneck identification
- Resource optimization suggestions
- Timeline risk assessments
- Success probability scores

## Output Structure:
```markdown
# Learning Review: Weekly (2024-09-14)

## 📊 Progress Summary
- **Goals Active**: 3/4 (75%)
- **Captures This Week**: 12 (↑20% from last week)
- **Applications Implemented**: 5 (↑25%)
- **Sources Utilized**: 8/15 (53%)

## 🎯 Goal Progress
### AI Agent Architecture (45% complete)
- ✅ Coordination Patterns Mastery milestone completed
- 🔄 Performance Optimization milestone in progress (65%)
- 📚 3 new captures added from research papers
- 🚀 2 applications implemented in current projects

## 💡 Key Insights This Week
1. **Progressive Summarization** improving retention by 40%
2. **MCP Server Integration** patterns now clear
3. **Agent Coordination** breakthrough in distributed scenarios

## ⚠️ Areas Needing Attention
- Claude Code Mastery goal falling behind schedule
- Underutilized productivity sources
- Missing connections between AI and productivity concepts

## 🎯 Next Week Priorities
1. Focus on Claude Code advanced patterns
2. Connect AI learnings to productivity workflows
3. Review and apply 3 pending insights
4. Complete Performance Optimization milestone
```

## Integration Features:
- **Calendar Integration**: Schedule regular review sessions
- **Project Linking**: Connect learning progress to project outcomes
- **Goal Alignment**: Ensure learning supports strategic objectives
- **Source Optimization**: Identify most effective learning sources
- **Application Tracking**: Monitor practical implementation rates

## Behavior:
- Generates comprehensive progress reports
- Provides data-driven insights and recommendations
- Identifies patterns and trends in learning behavior
- Suggests optimizations for learning efficiency
- Creates actionable next steps and priorities
- Maintains review history for long-term analysis
- Integrates with existing PARA Method workflows

Conduct thorough learning reviews that drive continuous improvement and maximize knowledge application effectiveness.
---
name: learn progress
description: Track learning goal progress and knowledge retention with detailed analytics and predictive insights
---

# Learn Progress

Track comprehensive learning goal progress, measure knowledge retention rates, analyze learning velocity, and provide predictive insights for goal completion with detailed performance analytics.

## Usage Examples:
- `/learn progress --goal ai-agent-architecture --retention-analysis`
- `/learn progress --all-goals --velocity-trends --forecast`
- `/learn progress --milestone-tracking --goal para-method-mastery`
- `/learn progress --retention-report --since 30d --export dashboard`

## OutputFormatter Integration

**Tool**: Use `OutputFormatter` with `learn_progress` template for professional learning progress formatting.

**Template**: `templates/output/learn_progress.md.j2` - Comprehensive learning progress dashboard with goals, retention metrics, velocity tracking, and recommendations.

### Integration Example

```python
from tools import OutputFormatter
from datetime import datetime, timedelta

# Structure learning progress data
progress_data = {
    'period': 'Last 30 Days',
    'overall_progress': 0.68,
    'active_goals': 3,
    'mastery_level': 'Intermediate',

    'goals': [
        {
            'name': 'AI Agent Architecture Mastery',
            'category': 'artificial intelligence',
            'priority': 'high',
            'status': 'in_progress',  # completed, in_progress, at_risk, pending
            'progress': 0.75,
            'description': 'Master LangChain, LangGraph, and multi-agent architectures',
            'skills': ['LangChain', 'LangGraph', 'Multi-agent systems', 'RAG'],
            'milestones': [
                {
                    'name': 'Complete LangChain fundamentals',
                    'status': 'completed',
                    'due_date': '2024-12-01'
                },
                {
                    'name': 'Build first multi-agent system',
                    'status': 'in_progress',
                    'due_date': '2025-01-15'
                }
            ],
            'metrics': {
                'concepts_mastered': 15,
                'target_concepts': 20,
                'application_success_rate': 0.85,
                'engagement_level': 0.90
            },
            'completion_forecast': {
                'estimated_date': '2025-02-15',
                'confidence': 0.82,
                'days_remaining': 45
            }
        }
    ],

    'retention_metrics': {
        'overall_retention': 0.82,
        'by_category': {
            'artificial intelligence': {
                'rate': 0.88,
                'trend': 'improving'
            },
            'productivity systems': {
                'rate': 0.75,
                'trend': 'stable'
            }
        },
        'recent_quizzes': [
            {
                'topic': 'LangChain Fundamentals',
                'date': '2025-01-02',
                'score': 0.90
            }
        ]
    },

    'velocity_metrics': {
        'concepts_per_week': 4.5,
        'trend': 'accelerating',
        'recent_activity': [
            {
                'date': '2025-01-05',
                'concepts_learned': 3,
                'source_type': 'article'
            }
        ],
        'bottlenecks': [
            {
                'area': 'Practical Application',
                'description': 'Need more hands-on project time'
            }
        ]
    },

    'skills_progress': {
        'technical': [
            {
                'name': 'LangChain',
                'proficiency': 0.80,
                'progress': 0.85,
                'notes': 'Strong foundation, building advanced skills'
            },
            {
                'name': 'Multi-agent Systems',
                'proficiency': 0.60,
                'progress': 0.70,
                'notes': 'Progressing well, need more practice'
            }
        ]
    },

    'trends': {
        'monthly_progress': {
            'December 2024': 0.15,
            'January 2025': 0.20
        },
        'velocity_chart': {
            'Week 1': 3.2,
            'Week 2': 4.5,
            'Week 3': 5.1
        }
    },

    'insights': [
        {
            'title': 'Accelerating Learning Pace',
            'description': 'Your learning velocity has increased 35% this month',
            'action_items': [
                'Maintain current momentum',
                'Consider adding 1 more hands-on project'
            ]
        }
    ],

    'next_steps': [
        {
            'action': 'Build multi-agent customer support system',
            'priority': 'high',
            'estimated_effort': '2-3 days'
        },
        {
            'action': 'Review LangGraph documentation',
            'priority': 'medium',
            'estimated_effort': '3 hours'
        }
    ],

    'recommended_focus': [
        {
            'area': 'Practical Application',
            'reason': 'Theory-practice gap identified',
            'resources': ['Build 2 hands-on projects', 'Join AI agent hackathon']
        }
    ]
}

# Format with OutputFormatter
formatter = OutputFormatter()
output = formatter.format_markdown(progress_data, template="learn_progress")

print(output.content)
# Processing time: ~15-20ms
```

**Key Benefits**:
- **Reduces Command Complexity**: 600-800 lines → ~25-30 lines of structured data
- **Comprehensive Dashboard**: Goals, retention, velocity, trends in one view
- **Professional Formatting**: Health scores, progress bars, trend indicators
- **Type Safety**: Validated data structures ensure consistency
- **Performance**: <50ms template rendering with session caching

## Instructions:

You are a learning progress analytics specialist for the PARA Method learning system. When this command is invoked:

1. **Parse progress analysis request**:
   - Specific learning goals or comprehensive analysis
   - Time periods and milestone tracking requirements
   - Retention analysis and velocity measurement needs
   - Export formats and dashboard requirements
   - Predictive forecasting and goal completion estimates

2. **Analyze learning goal progression**:
   - Load learning goals, milestones, and completion data
   - Calculate progress percentages and velocity metrics
   - Assess milestone completion rates and timeline adherence
   - Measure knowledge retention through quiz and review data
   - Identify acceleration patterns and learning bottlenecks

3. **Generate retention and performance analytics**:
   - **Knowledge Retention**: Track long-term information retention
   - **Learning Velocity**: Measure concepts acquired per time period
   - **Application Success**: Monitor practical implementation rates
   - **Goal Alignment**: Assess progress toward learning objectives
   - **Milestone Tracking**: Detailed milestone completion analysis
   - **Predictive Forecasting**: Goal completion probability and timeline predictions

4. **Create comprehensive progress report**:
   ```bash
   python3 -c "
   import json, yaml, datetime, statistics
   from pathlib import Path
   from collections import defaultdict, Counter
   import math

   # Load learning and performance data
   goals_file = Path('.claude/learning_goals.yaml')
   captures_file = Path('.claude/cache/learning_captures.json')
   quiz_history_file = Path('.claude/cache/quiz_sessions.json')
   reviews_file = Path('.claude/cache/learning_reviews.json')
   progress_file = Path('.claude/cache/progress_tracking.json')

   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}
   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   quiz_history = json.loads(quiz_history_file.read_text()) if quiz_history_file.exists() else {'sessions': []}
   reviews_data = json.loads(reviews_file.read_text()) if reviews_file.exists() else {'reviews': []}
   progress_data = json.loads(progress_file.read_text()) if progress_file.exists() else {'tracking': []}

   # Parse parameters
   goal_id = '${goal}' or None
   all_goals = bool('${all_goals}')
   retention_analysis = bool('${retention_analysis}')
   velocity_trends = bool('${velocity_trends}')
   milestone_tracking = bool('${milestone_tracking}')
   forecast = bool('${forecast}')
   since_days = int('${since}'.replace('d', '')) if '${since}' else 30
   export_format = '${export}' or 'json'

   # Advanced Progress Analytics Engine
   class ProgressAnalyticsEngine:
       def __init__(self, goals, captures, quizzes, reviews, historical_progress):
           self.goals = goals
           self.captures = captures
           self.quizzes = quizzes
           self.reviews = reviews
           self.historical_progress = historical_progress

       def analyze_goal_progress(self, goal_id=None):
           '''Comprehensive goal progress analysis'''
           goals_to_analyze = [goal_id] if goal_id else list(self.goals.get('learning_goals', {}).keys())
           progress_analysis = {}

           for gid in goals_to_analyze:
               goal_data = self.goals['learning_goals'].get(gid, {})
               if not goal_data:
                   continue

               analysis = {
                   'goal_id': gid,
                   'goal_name': goal_data.get('name', ''),
                   'category': goal_data.get('category', ''),
                   'priority': goal_data.get('priority', ''),
                   'status': goal_data.get('status', ''),
                   'progress_metrics': self._calculate_progress_metrics(gid, goal_data),
                   'milestone_analysis': self._analyze_milestones(goal_data.get('milestones', [])),
                   'learning_velocity': self._calculate_learning_velocity(gid),
                   'retention_metrics': self._calculate_retention_metrics(gid),
                   'timeline_analysis': self._analyze_timeline_adherence(goal_data),
                   'completion_forecast': self._forecast_completion(gid, goal_data)
               }

               progress_analysis[gid] = analysis

           return progress_analysis

       def _calculate_progress_metrics(self, goal_id, goal_data):
           '''Calculate comprehensive progress metrics'''
           base_progress = goal_data.get('progress', 0)

           # Count related learning captures
           related_captures = self._get_goal_related_captures(goal_id)
           concepts_learned = set()

           for capture in related_captures:
               content = capture.get('content', {})
               if content.get('key_concepts'):
                   concepts_learned.update(content['key_concepts'])
               if content.get('concepts'):
                   concepts_learned.update(content['concepts'])

           # Calculate skills progress
           target_skills = goal_data.get('skills', [])
           skills_progress = len(concepts_learned) / max(len(target_skills), 1) * 100 if target_skills else 0

           # Calculate application rate from quiz performance
           quiz_performance = self._get_goal_quiz_performance(goal_id)
           application_rate = (quiz_performance.get('avg_score', 0) * 100) if quiz_performance else 0

           return {
               'overall_progress': base_progress,
               'concepts_mastered': len(concepts_learned),
               'target_concepts': len(target_skills),
               'concept_mastery_rate': min(skills_progress, 100),
               'application_success_rate': application_rate,
               'recent_activity_score': self._calculate_recent_activity(goal_id),
               'engagement_level': self._calculate_engagement_level(goal_id)
           }

       def _analyze_milestones(self, milestones):
           '''Analyze milestone completion and timeline performance'''
           if not milestones:
               return {'total': 0, 'completed': 0, 'in_progress': 0, 'planned': 0, 'completion_rate': 0}

           milestone_stats = Counter(m.get('status', 'planned') for m in milestones)
           total_milestones = len(milestones)
           completed_milestones = milestone_stats.get('completed', 0)

           # Analyze timeline performance
           overdue_milestones = 0
           upcoming_milestones = 0
           current_date = datetime.datetime.now()

           for milestone in milestones:
               if milestone.get('date'):
                   milestone_date = datetime.datetime.strptime(milestone['date'], '%Y-%m-%d')
                   if milestone.get('status') != 'completed' and milestone_date < current_date:
                       overdue_milestones += 1
                   elif milestone_date > current_date and milestone_date <= current_date + datetime.timedelta(days=30):
                       upcoming_milestones += 1

           return {
               'total': total_milestones,
               'completed': completed_milestones,
               'in_progress': milestone_stats.get('in_progress', 0),
               'planned': milestone_stats.get('planned', 0),
               'completion_rate': (completed_milestones / total_milestones * 100) if total_milestones else 0,
               'overdue': overdue_milestones,
               'upcoming_30d': upcoming_milestones,
               'timeline_adherence': ((total_milestones - overdue_milestones) / total_milestones * 100) if total_milestones else 100
           }

       def _calculate_learning_velocity(self, goal_id):
           '''Calculate learning velocity metrics'''
           related_captures = self._get_goal_related_captures(goal_id)

           if not related_captures:
               return {'concepts_per_week': 0, 'captures_per_week': 0, 'trend': 'stable'}

           # Group captures by week
           weekly_data = defaultdict(list)
           for capture in related_captures[-20:]:  # Last 20 captures
               try:
                   timestamp = datetime.datetime.fromisoformat(capture.get('timestamp', ''))
                   week_key = timestamp.strftime('%Y-W%U')
                   weekly_data[week_key].append(capture)
               except:
                   continue

           if len(weekly_data) < 2:
               return {'concepts_per_week': 0, 'captures_per_week': 0, 'trend': 'insufficient_data'}

           # Calculate weekly averages
           weekly_captures = [len(captures) for captures in weekly_data.values()]
           weekly_concepts = []

           for week_captures in weekly_data.values():
               concepts_this_week = set()
               for capture in week_captures:
                   content = capture.get('content', {})
                   if content.get('key_concepts'):
                       concepts_this_week.update(content['key_concepts'])
                   if content.get('concepts'):
                       concepts_this_week.update(content['concepts'])
               weekly_concepts.append(len(concepts_this_week))

           avg_captures_per_week = statistics.mean(weekly_captures)
           avg_concepts_per_week = statistics.mean(weekly_concepts)

           # Determine trend
           recent_weeks = weekly_captures[-3:]
           earlier_weeks = weekly_captures[:-3] if len(weekly_captures) > 3 else weekly_captures

           if len(recent_weeks) >= 2 and len(earlier_weeks) >= 2:
               recent_avg = statistics.mean(recent_weeks)
               earlier_avg = statistics.mean(earlier_weeks)

               if recent_avg > earlier_avg * 1.2:
                   trend = 'accelerating'
               elif recent_avg < earlier_avg * 0.8:
                   trend = 'decelerating'
               else:
                   trend = 'stable'
           else:
               trend = 'stable'

           return {
               'captures_per_week': round(avg_captures_per_week, 2),
               'concepts_per_week': round(avg_concepts_per_week, 2),
               'trend': trend,
               'total_weeks_active': len(weekly_data),
               'recent_velocity': round(statistics.mean(recent_weeks), 2) if recent_weeks else 0
           }

       def _calculate_retention_metrics(self, goal_id):
           '''Calculate knowledge retention based on quiz and review data'''
           goal_quiz_sessions = [
               session for session in self.quizzes.get('sessions', [])
               if session.get('goal_id') == goal_id or goal_id in session.get('topic', '').lower()
           ]

           if not goal_quiz_sessions:
               return {'retention_rate': 0, 'sessions_analyzed': 0, 'trend': 'no_data'}

           # Sort sessions by timestamp
           sorted_sessions = sorted(goal_quiz_sessions, key=lambda x: x.get('timestamp', ''))

           # Calculate retention over time
           scores = [session.get('score', 0) for session in sorted_sessions if session.get('score') is not None]

           if len(scores) < 2:
               return {
                   'retention_rate': scores[0] * 100 if scores else 0,
                   'sessions_analyzed': len(scores),
                   'trend': 'insufficient_data'
               }

           # Calculate retention trend
           recent_scores = scores[-3:] if len(scores) >= 3 else scores
           earlier_scores = scores[:-3] if len(scores) > 3 else scores

           recent_avg = statistics.mean(recent_scores)
           earlier_avg = statistics.mean(earlier_scores) if len(earlier_scores) > 0 else recent_avg

           if recent_avg > earlier_avg + 0.1:
               trend = 'improving'
           elif recent_avg < earlier_avg - 0.1:
               trend = 'declining'
           else:
               trend = 'stable'

           return {
               'retention_rate': round(recent_avg * 100, 1),
               'sessions_analyzed': len(scores),
               'trend': trend,
               'improvement': round((recent_avg - earlier_avg) * 100, 1),
               'consistency': self._calculate_score_consistency(scores)
           }

       def _calculate_score_consistency(self, scores):
           '''Calculate consistency in quiz scores'''
           if len(scores) < 2:
               return 'insufficient_data'

           std_dev = statistics.stdev(scores)

           if std_dev < 0.1:
               return 'very_consistent'
           elif std_dev < 0.2:
               return 'consistent'
           elif std_dev < 0.3:
               return 'variable'
           else:
               return 'inconsistent'

       def _analyze_timeline_adherence(self, goal_data):
           '''Analyze timeline adherence and estimate completion'''
           created_date_str = goal_data.get('created_date')
           target_date_str = goal_data.get('target_completion')
           current_progress = goal_data.get('progress', 0)

           if not created_date_str or not target_date_str:
               return {'adherence_score': 0, 'status': 'insufficient_timeline_data'}

           try:
               created_date = datetime.datetime.strptime(created_date_str, '%Y-%m-%d')
               target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d')
               current_date = datetime.datetime.now()

               # Calculate expected vs actual progress
               total_duration = (target_date - created_date).days
               elapsed_duration = (current_date - created_date).days

               if total_duration <= 0:
                   return {'adherence_score': 0, 'status': 'invalid_timeline'}

               expected_progress = (elapsed_duration / total_duration) * 100
               progress_difference = current_progress - expected_progress

               # Determine adherence status
               if progress_difference >= 10:
                   status = 'ahead_of_schedule'
                   adherence_score = min(100, 100 + (progress_difference - 10))
               elif progress_difference >= -10:
                   status = 'on_schedule'
                   adherence_score = 100 + progress_difference
               elif progress_difference >= -25:
                   status = 'slightly_behind'
                   adherence_score = 75 + progress_difference
               else:
                   status = 'significantly_behind'
                   adherence_score = max(0, 50 + progress_difference)

               return {
                   'adherence_score': round(adherence_score, 1),
                   'status': status,
                   'expected_progress': round(expected_progress, 1),
                   'actual_progress': current_progress,
                   'progress_difference': round(progress_difference, 1),
                   'days_elapsed': elapsed_duration,
                   'days_remaining': max(0, (target_date - current_date).days)
               }

           except ValueError:
               return {'adherence_score': 0, 'status': 'invalid_date_format'}

       def _forecast_completion(self, goal_id, goal_data):
           '''Forecast goal completion based on current trends'''
           current_progress = goal_data.get('progress', 0)
           velocity = self._calculate_learning_velocity(goal_id)

           if current_progress >= 100:
               return {'status': 'completed', 'estimated_completion': 'already_complete'}

           if velocity['concepts_per_week'] == 0:
               return {'status': 'no_activity', 'estimated_completion': 'unknown'}

           # Estimate weeks to completion based on velocity
           target_skills = len(goal_data.get('skills', []))
           if target_skills == 0:
               return {'status': 'no_target_defined', 'estimated_completion': 'unknown'}

           # Get current concepts mastered
           related_captures = self._get_goal_related_captures(goal_id)
           concepts_learned = set()
           for capture in related_captures:
               content = capture.get('content', {})
               if content.get('key_concepts'):
                   concepts_learned.update(content['key_concepts'])

           remaining_concepts = max(0, target_skills - len(concepts_learned))

           if remaining_concepts == 0:
               weeks_to_completion = 0
           else:
               weeks_to_completion = remaining_concepts / max(velocity['concepts_per_week'], 0.1)

           completion_date = datetime.datetime.now() + datetime.timedelta(weeks=weeks_to_completion)

           # Calculate completion probability based on trend and consistency
           retention_metrics = self._calculate_retention_metrics(goal_id)

           base_probability = 0.7  # Base 70% probability

           # Adjust based on velocity trend
           if velocity['trend'] == 'accelerating':
               base_probability += 0.2
           elif velocity['trend'] == 'decelerating':
               base_probability -= 0.2

           # Adjust based on retention trend
           if retention_metrics['trend'] == 'improving':
               base_probability += 0.15
           elif retention_metrics['trend'] == 'declining':
               base_probability -= 0.15

           completion_probability = max(0.1, min(0.95, base_probability))

           return {
               'status': 'forecasting',
               'estimated_completion': completion_date.strftime('%Y-%m-%d'),
               'weeks_to_completion': round(weeks_to_completion, 1),
               'completion_probability': round(completion_probability * 100, 1),
               'remaining_concepts': remaining_concepts,
               'velocity_trend': velocity['trend'],
               'confidence_level': 'high' if completion_probability > 0.8 else 'medium' if completion_probability > 0.6 else 'low'
           }

       def _get_goal_related_captures(self, goal_id):
           '''Get learning captures related to specific goal'''
           related_captures = []
           for capture in self.captures.get('captures', []):
               if goal_id in capture.get('connections', {}).get('learning_goals', []):
                   related_captures.append(capture)
           return related_captures

       def _get_goal_quiz_performance(self, goal_id):
           '''Get quiz performance for specific goal'''
           goal_sessions = [
               session for session in self.quizzes.get('sessions', [])
               if session.get('goal_id') == goal_id
           ]

           if not goal_sessions:
               return None

           scores = [session.get('score', 0) for session in goal_sessions if session.get('score') is not None]
           return {
               'avg_score': statistics.mean(scores) if scores else 0,
               'session_count': len(goal_sessions),
               'latest_score': scores[-1] if scores else 0
           }

       def _calculate_recent_activity(self, goal_id):
           '''Calculate recent activity score for goal'''
           related_captures = self._get_goal_related_captures(goal_id)

           # Count captures in last 7 days
           cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)
           recent_captures = 0

           for capture in related_captures:
               try:
                   capture_date = datetime.datetime.fromisoformat(capture.get('timestamp', ''))
                   if capture_date >= cutoff_date:
                       recent_captures += 1
               except:
                   continue

           # Score: 0-100 based on recent activity
           return min(100, recent_captures * 20)  # 5 captures = 100 score

       def _calculate_engagement_level(self, goal_id):
           '''Calculate overall engagement level'''
           activity_score = self._calculate_recent_activity(goal_id)
           retention_metrics = self._calculate_retention_metrics(goal_id)

           retention_rate = retention_metrics.get('retention_rate', 0)

           # Combine activity and retention for engagement score
           engagement_score = (activity_score * 0.6) + (retention_rate * 0.4)

           if engagement_score >= 80:
               return 'high'
           elif engagement_score >= 60:
               return 'medium'
           elif engagement_score >= 40:
               return 'low'
           else:
               return 'very_low'

   # Generate progress analysis
   analytics_engine = ProgressAnalyticsEngine(
       goals_data, captures_data, quiz_history, reviews_data, progress_data
   )

   if goal_id and goal_id not in goals_data.get('learning_goals', {}):
       print(json.dumps({'status': 'error', 'message': f'Learning goal \"{goal_id}\" not found'}, indent=2))
   else:
       progress_analysis = analytics_engine.analyze_goal_progress(goal_id if not all_goals else None)

       # Create progress report
       progress_report = {
           'id': f'progress-{datetime.datetime.now().strftime(\"%Y%m%d-%H%M%S\")}',
           'timestamp': datetime.datetime.now().isoformat(),
           'analysis_type': 'single_goal' if goal_id else 'all_goals',
           'analysis_period_days': since_days,
           'report_parameters': {
               'goal_id': goal_id,
               'retention_analysis': retention_analysis,
               'velocity_trends': velocity_trends,
               'milestone_tracking': milestone_tracking,
               'forecast': forecast
           },
           'goal_analysis': progress_analysis,
           'summary_metrics': {
               'goals_analyzed': len(progress_analysis),
               'average_progress': round(statistics.mean([g['progress_metrics']['overall_progress'] for g in progress_analysis.values()]), 1) if progress_analysis else 0,
               'total_concepts_mastered': sum(g['progress_metrics']['concepts_mastered'] for g in progress_analysis.values()),
               'goals_on_track': len([g for g in progress_analysis.values() if g.get('timeline_analysis', {}).get('status', '') in ['ahead_of_schedule', 'on_schedule']]),
               'high_engagement_goals': len([g for g in progress_analysis.values() if g['progress_metrics']['engagement_level'] == 'high'])
           }
       }

       # Save progress report
       progress_tracking_file = Path('.claude/cache/progress_tracking.json')
       if progress_tracking_file.exists():
           tracking_data = json.loads(progress_tracking_file.read_text())
       else:
           tracking_data = {'tracking': []}

       tracking_data['tracking'].append(progress_report)
       tracking_data['tracking'] = tracking_data['tracking'][-20:]  # Keep last 20 reports

       progress_tracking_file.parent.mkdir(exist_ok=True)
       progress_tracking_file.write_text(json.dumps(tracking_data, indent=2))

       # Generate response
       response = {
           'status': 'success',
           'command': '/learn progress',
           'report_summary': {
               'report_id': progress_report['id'],
               'goals_analyzed': progress_report['summary_metrics']['goals_analyzed'],
               'average_progress': progress_report['summary_metrics']['average_progress'],
               'concepts_mastered': progress_report['summary_metrics']['total_concepts_mastered'],
               'goals_on_track': progress_report['summary_metrics']['goals_on_track']
           },
           'key_insights': [],
           'recommendations': [],
           'progress_highlights': []
       }

       # Generate insights and recommendations
       for goal_id, analysis in progress_analysis.items():
           goal_name = analysis['goal_name']
           progress = analysis['progress_metrics']['overall_progress']
           engagement = analysis['progress_metrics']['engagement_level']

           # Key insights
           if progress >= 80:
               response['key_insights'].append(f'{goal_name}: Nearing completion ({progress}% complete)')
           elif engagement == 'high':
               response['key_insights'].append(f'{goal_name}: High engagement with strong learning velocity')
           elif engagement == 'low':
               response['key_insights'].append(f'{goal_name}: Low engagement - needs attention')

           # Recommendations
           timeline_status = analysis.get('timeline_analysis', {}).get('status', '')
           if timeline_status == 'significantly_behind':
               response['recommendations'].append(f'Increase learning intensity for {goal_name} to meet deadline')
           elif timeline_status == 'ahead_of_schedule':
               response['recommendations'].append(f'Consider advancing {goal_name} timeline or deepening mastery')

           forecast = analysis.get('completion_forecast', {})
           if forecast.get('completion_probability', 0) < 60:
               response['recommendations'].append(f'Review learning strategy for {goal_name} - low completion probability')

           # Progress highlights
           if analysis['milestone_analysis']['completion_rate'] >= 75:
               response['progress_highlights'].append(f'{goal_name}: Excellent milestone completion ({analysis[\"milestone_analysis\"][\"completion_rate\"]:.1f}%)')

       print(json.dumps(response, indent=2))
   "
   ```

5. **Provide actionable progress insights**:
   - Learning velocity trends and acceleration analysis
   - Knowledge retention measurement and improvement recommendations
   - Timeline adherence assessment with completion forecasting
   - Milestone tracking with bottleneck identification
   - Cross-goal progress correlation and optimization opportunities

## Progress Tracking Types:

### Goal-Specific Progress
- **Progress Metrics**: Overall completion, concept mastery, application success
- **Milestone Analysis**: Completion rates, timeline adherence, upcoming deadlines
- **Learning Velocity**: Concepts per week, trend analysis, acceleration patterns

### Retention Analytics
- **Knowledge Retention**: Long-term memory retention through quiz performance
- **Application Transfer**: Practical implementation success rates
- **Consistency Tracking**: Score stability and improvement patterns

### Predictive Analytics
- **Completion Forecasting**: Goal completion probability and timeline predictions
- **Risk Assessment**: Timeline risks, engagement drops, learning bottlenecks
- **Optimization Recommendations**: Resource allocation and focus area suggestions

## Parameters:
- `--goal GOAL_ID` - Analyze specific learning goal progress
- `--all-goals` - Comprehensive analysis of all active learning goals
- `--retention-analysis` - Focus on knowledge retention metrics
- `--velocity-trends` - Analyze learning velocity and acceleration patterns
- `--milestone-tracking` - Detailed milestone completion analysis
- `--forecast` - Include completion forecasting and probability analysis
- `--since PERIOD` - Analysis time period (30d, 90d, 6m, 1y)
- `--export FORMAT` - Export format (json, dashboard, csv, report)
- `--detailed` - Include comprehensive metrics and analysis

## Natural Language Processing:
Automatically detects:
- Progress inquiries: "how am I doing", "progress on", "learning analytics"
- Goal tracking: "goal progress", "milestone status", "completion forecast"
- Retention focus: "knowledge retention", "how well am I remembering", "retention rates"
- Performance analysis: "learning velocity", "trends", "acceleration"
- Forecasting needs: "will I complete", "on track", "timeline prediction"

## Analytics Features:

### Learning Velocity Analysis
```markdown
📈 **Velocity Metrics**:
- Concepts per Week: 3.2 (↑15% from last month)
- Captures per Week: 5.8 (stable trend)
- Learning Acceleration: Currently accelerating
- Peak Performance Period: Tuesday-Thursday mornings

⚡ **Trend Analysis**:
- 30-day Moving Average: Increasing 12% month-over-month
- Velocity Consistency: High (low variance in weekly rates)
- Seasonal Patterns: Higher velocity in Q4, slower in Q2
```

### Knowledge Retention Dashboard
```markdown
🧠 **Retention Analytics**:
- Overall Retention Rate: 78% (above average)
- Short-term Retention (1-7 days): 92%
- Medium-term Retention (8-30 days): 85%
- Long-term Retention (30+ days): 71%

📊 **Retention Factors**:
- Spaced Repetition Effectiveness: +23% improvement
- Application-based Learning: +18% retention boost
- Cross-domain Connections: +15% memory consolidation
```

### Milestone Achievement Analysis
```markdown
🎯 **Milestone Performance**:
- Completion Rate: 85% (17 of 20 milestones)
- On-time Completion: 76%
- Early Completion: 29%
- Timeline Adherence: 91% overall

⏰ **Schedule Analysis**:
- Average Milestone Duration: 18.3 days (target: 21 days)
- Planning Accuracy: 82% (actual vs estimated time)
- Risk Factors: Resource availability, complexity estimation
```

### Predictive Completion Forecasting
```markdown
🔮 **Goal Completion Forecast**:
- AI Agent Architecture: 89% probability by Jan 15, 2025
- PARA Method Mastery: 72% probability by target date
- Claude Code Mastery: Behind schedule - 45% probability

📈 **Success Factors**:
- Current Velocity Trend: Positive
- Engagement Level: High
- Resource Availability: Adequate
- Knowledge Transfer Rate: Above average
```

## Output Examples:

### Single Goal Progress Report
```json
{
  "status": "success",
  "command": "/learn progress",
  "report_summary": {
    "report_id": "progress-20241214-153045",
    "goals_analyzed": 1,
    "average_progress": 67.5,
    "concepts_mastered": 12,
    "goals_on_track": 1
  },
  "goal_analysis": {
    "ai-agent-architecture": {
      "goal_name": "AI Agent Architecture & Orchestration",
      "progress_metrics": {
        "overall_progress": 67.5,
        "concepts_mastered": 12,
        "target_concepts": 15,
        "concept_mastery_rate": 80,
        "application_success_rate": 78,
        "engagement_level": "high"
      },
      "milestone_analysis": {
        "completion_rate": 85.7,
        "completed": 6,
        "total": 7,
        "timeline_adherence": 91.2,
        "upcoming_30d": 2
      },
      "learning_velocity": {
        "concepts_per_week": 2.8,
        "captures_per_week": 4.2,
        "trend": "accelerating"
      },
      "retention_metrics": {
        "retention_rate": 82.3,
        "trend": "improving",
        "consistency": "consistent"
      },
      "completion_forecast": {
        "estimated_completion": "2025-01-10",
        "completion_probability": 89.2,
        "confidence_level": "high"
      }
    }
  },
  "key_insights": [
    "AI Agent Architecture: High engagement with strong learning velocity",
    "Retention improving with consistent quiz performance"
  ],
  "recommendations": [
    "Consider advancing timeline or deepening mastery - ahead of schedule",
    "Continue current learning strategy - high completion probability"
  ]
}
```

### Multi-Goal Dashboard
```markdown
# Learning Progress Dashboard - December 14, 2024

## 📊 Overall Summary
- **Goals Active**: 3 of 4 goals actively progressing
- **Average Progress**: 58.3% across all goals
- **Concepts Mastered**: 24 total concepts learned
- **Goals On Track**: 2 of 3 goals meeting timeline expectations

## 🎯 Goal Performance Matrix

### AI Agent Architecture (67% complete) ✅
- **Status**: Ahead of schedule
- **Velocity**: 2.8 concepts/week (↑ accelerating)
- **Retention**: 82% (improving trend)
- **Completion**: Jan 10, 2025 (89% probability)

### PARA Method Mastery (52% complete) ⚠️
- **Status**: Slightly behind schedule
- **Velocity**: 1.9 concepts/week (stable)
- **Retention**: 74% (stable trend)
- **Completion**: Mar 22, 2025 (72% probability)

### Claude Code Mastery (31% complete) ❌
- **Status**: Significantly behind
- **Velocity**: 0.8 concepts/week (↓ decelerating)
- **Retention**: 68% (declining trend)
- **Completion**: Risk of missing deadline (45% probability)

## 📈 Performance Insights
- **Strongest Area**: AI Architecture - high engagement, accelerating
- **Needs Attention**: Claude Code - low velocity, declining retention
- **Optimization Opportunity**: Redistribute time allocation

## 🎯 Next Actions
1. **Immediate**: Increase Claude Code learning intensity
2. **This Week**: Complete 2 pending AI Architecture milestones
3. **Strategy**: Apply successful AI learning patterns to other goals
```

## Integration Features:
- **Real-time Analytics**: Live progress tracking with immediate metric updates
- **Predictive Modeling**: ML-based completion probability and timeline forecasting
- **Performance Correlation**: Cross-goal learning pattern analysis
- **Adaptive Scheduling**: Dynamic milestone adjustment based on progress rates
- **Retention Optimization**: Spaced repetition timing based on individual forgetting curves

## Behavior:
- Provides comprehensive progress analytics with actionable insights
- Tracks multiple dimensions of learning success beyond simple completion percentages
- Generates predictive forecasting for goal completion probability
- Identifies learning patterns and optimization opportunities
- Creates personalized recommendations based on individual learning profiles
- Maintains historical progress tracking for long-term trend analysis
- Integrates with existing PARA Method learning infrastructure

Transform learning progress from simple tracking to intelligent analytics that predict success, identify bottlenecks, and optimize learning outcomes for maximum goal achievement.
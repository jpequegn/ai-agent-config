---
name: learn course
description: Track course progress with structured learning capture, skill development monitoring, and completion analytics
---

# Learn Course

Track comprehensive course progress with structured learning capture, skill development monitoring, completion analytics, and intelligent learning path optimization for maximum educational ROI.

## Usage Examples:
- `/learn course --name "Machine Learning Specialization" --platform "Coursera" --progress 35% --module "Neural Networks"`
- `/learn course "AWS Solutions Architect" --completed-lesson "EC2 Fundamentals" --skills "cloud-architecture, scalability"`
- `/learn course --course-id ml-stanford-2024 --assignment-complete "Week 3 Programming" --grade 95 --time-spent 4.5h`
- `/learn course --complete "React Advanced Patterns" --final-project "E-commerce Dashboard" --certificate earned --rating 5`

## Instructions:

You are a course learning assistant for the PARA Method learning system. When this command is invoked:

1. **Parse course learning request**:
   - Course identification and platform information
   - Progress tracking and milestone completion
   - Learning content and skill development areas
   - Assessment results and performance metrics
   - Time investment and learning velocity analysis

2. **Analyze learning progression**:
   - Track course completion percentage and velocity
   - Monitor skill development and competency growth
   - Assess knowledge retention and practical application
   - Evaluate learning efficiency and time management
   - Identify learning bottlenecks and optimization opportunities

3. **Process educational content**:
   - **Module Progress**: Track individual lessons and sections
   - **Skill Development**: Map course content to skill acquisition
   - **Practical Applications**: Projects, assignments, and real-world implementations
   - **Assessment Results**: Quizzes, exams, and performance evaluations
   - **Knowledge Synthesis**: Integration of concepts across modules
   - **Learning Insights**: Meta-learning and study strategy improvements

4. **Create structured course learning entry**:
   ```bash
   python3 -c "
   import json, yaml, datetime, re, math
   from pathlib import Path

   # Load learning data
   captures_file = Path('.claude/cache/learning_captures.json')
   sources_file = Path('.claude/sources.yaml')
   goals_file = Path('.claude/learning_goals.yaml')

   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {'sources': {}}
   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {'learning_goals': {}}

   # Generate course ID
   course_name = '${course_name}'
   platform = '${platform}' or 'unknown'
   course_id = '${course_id}' or re.sub(r'[^a-z0-9]+', '-', f'{course_name}-{platform}'.lower())[:40]

   # Calculate learning metrics
   def calculate_learning_velocity(progress, time_spent_hours, start_date=None):
       if not start_date:
           return None

       try:
           start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
           days_elapsed = (datetime.datetime.now() - start).days
           if days_elapsed > 0:
               progress_per_day = progress / days_elapsed
               return round(progress_per_day * 7, 2)  # Weekly velocity
       except:
           pass

       return None

   def assess_learning_efficiency(progress, time_spent, target_hours=None):
       if not time_spent or time_spent == 0:
           return 'unknown'

       hours_per_percent = time_spent / max(progress, 1)

       if hours_per_percent < 0.5:
           return 'highly_efficient'
       elif hours_per_percent < 1.0:
           return 'efficient'
       elif hours_per_percent < 2.0:
           return 'moderate'
       else:
           return 'needs_optimization'

   progress = float('${progress}'.replace('%', '')) if '${progress}' else 0
   time_spent = float('${time_spent}') if '${time_spent}' else 0
   start_date = '${start_date}' or None

   velocity = calculate_learning_velocity(progress, time_spent, start_date)
   efficiency = assess_learning_efficiency(progress, time_spent)

   # Check if this is an update to existing course or new entry
   existing_course = None
   for capture in captures_data.get('captures', []):
       if capture.get('source_type') == 'course' and (capture.get('course_id') == course_id or capture.get('course_name') == course_name):
           existing_course = capture
           break

   if existing_course:
       # Update existing course entry
       capture = existing_course
       capture['last_updated'] = datetime.datetime.now().isoformat()

       # Update progress
       if progress > capture.get('progress', 0):
           capture['progress'] = progress

       # Add new completed items
       if '${completed_lesson}':
           if 'completed_lessons' not in capture['progress_tracking']:
               capture['progress_tracking']['completed_lessons'] = []
           if '${completed_lesson}' not in capture['progress_tracking']['completed_lessons']:
               capture['progress_tracking']['completed_lessons'].append('${completed_lesson}')

       if '${completed_module}':
           if 'completed_modules' not in capture['progress_tracking']:
               capture['progress_tracking']['completed_modules'] = []
           if '${completed_module}' not in capture['progress_tracking']['completed_modules']:
               capture['progress_tracking']['completed_modules'].append('${completed_module}')

       # Update skills
       new_skills = [skill.strip() for skill in '${skills}'.split(',') if skill.strip()]
       if new_skills:
           existing_skills = set(capture['learning_content']['skills_developed'])
           capture['learning_content']['skills_developed'] = list(existing_skills.union(set(new_skills)))

       # Add learning insights
       if '${insights}':
           new_insights = [insight.strip() for insight in '${insights}'.split('|') if insight.strip()]
           capture['learning_content']['key_insights'].extend(new_insights)

       # Update time tracking
       if time_spent > 0:
           capture['analytics']['total_time_hours'] = capture['analytics'].get('total_time_hours', 0) + time_spent

       # Update performance metrics
       if '${grade}':
           if 'assessment_results' not in capture['learning_content']:
               capture['learning_content']['assessment_results'] = []
           capture['learning_content']['assessment_results'].append({
               'assessment': '${assessment_name}' or f'Assessment {len(capture[\"learning_content\"].get(\"assessment_results\", [])) + 1}',
               'grade': int('${grade}'),
               'date': datetime.date.today().strftime('%Y-%m-%d')
           })

   else:
       # Create new course learning capture
       capture = {
           'id': f'course-{course_id}-{datetime.datetime.now().strftime(\"%Y%m%d\")}',
           'timestamp': datetime.datetime.now().isoformat(),
           'last_updated': datetime.datetime.now().isoformat(),
           'type': 'course_learning',
           'source_type': 'course',
           'course_id': course_id,
           'course_name': course_name,
           'platform': platform,
           'instructor': '${instructor}' or None,
           'course_url': '${url}' or None,
           'progress': progress,
           'status': 'completed' if '${complete}' else ('in_progress' if progress > 0 else 'enrolled'),
           'course_info': {
               'duration_weeks': int('${duration_weeks}') if '${duration_weeks}' else None,
               'difficulty_level': '${difficulty}' or 'intermediate',
               'prerequisites': [prereq.strip() for prereq in '${prerequisites}'.split(',') if prereq.strip()],
               'course_type': '${course_type}' or 'online',  # online, bootcamp, university, workshop
               'certification': bool('${certification}'),
               'language': '${language}' or 'English',
               'subject_area': '${subject}' or 'general'
           },
           'progress_tracking': {
               'current_module': '${current_module}' or None,
               'current_lesson': '${current_lesson}' or None,
               'completed_lessons': [lesson.strip() for lesson in '${completed_lessons}'.split(',') if lesson.strip()],
               'completed_modules': [module.strip() for module in '${completed_modules}'.split(',') if module.strip()],
               'completion_dates': {},
               'milestone_achievements': [],
               'assignments_completed': [assignment.strip() for assignment in '${assignments}'.split(',') if assignment.strip()],
               'projects_completed': [project.strip() for project in '${projects}'.split(',') if project.strip()]
           },
           'learning_content': {
               'key_insights': [insight.strip() for insight in '${insights}'.split('|') if insight.strip()],
               'concepts_mastered': [concept.strip() for concept in '${concepts}'.split(',') if concept.strip()],
               'skills_developed': [skill.strip() for skill in '${skills}'.split(',') if skill.strip()],
               'practical_applications': [app.strip() for app in '${applications}'.split(',') if app.strip()],
               'tools_learned': [tool.strip() for tool in '${tools}'.split(',') if tool.strip()],
               'assessment_results': [],
               'study_notes': '${notes}' or None,
               'challenging_topics': [topic.strip() for topic in '${challenges}'.split(',') if topic.strip()]
           },
           'analytics': {
               'total_time_hours': time_spent,
               'learning_velocity_weekly': velocity,
               'efficiency_rating': efficiency,
               'completion_rate': progress / 100 if progress > 0 else 0,
               'average_grade': None,
               'study_consistency': '${consistency}' or 'unknown',
               'learning_style_effectiveness': '${learning_style}' or 'mixed',
               'retention_score': None
           },
           'connections': {
               'learning_goals': [],
               'related_courses': [],
               'prerequisite_courses': [],
               'follow_up_courses': [],
               'project_applications': []
           },
           'metadata': {
               'enrollment_date': '${enrollment_date}' or datetime.date.today().strftime('%Y-%m-%d'),
               'target_completion': '${target_completion}' or None,
               'learning_schedule': '${schedule}' or 'flexible',
               'study_method': '${study_method}' or 'self_paced',
               'cost': '${cost}' or None,
               'rating': int('${rating}') if '${rating}' else None,
               'would_recommend': bool('${recommend}'),
               'tags': [],
               'category': '${category}' or 'professional_development'
           },
           'created_by': 'learn-course-command'
       }

       # Add to captures
       captures_data.setdefault('captures', []).append(capture)

   # Handle completion
   if '${complete}':
       capture['status'] = 'completed'
       capture['progress'] = 100
       capture['progress_tracking']['completion_dates']['course'] = datetime.date.today().strftime('%Y-%m-%d')

       if '${certificate}':
           capture['progress_tracking']['milestone_achievements'].append({
               'milestone': 'Course Completion Certificate',
               'date': datetime.date.today().strftime('%Y-%m-%d'),
               'description': 'Successfully completed course with certification'
           })

   # Calculate average grade
   if capture['learning_content']['assessment_results']:
       grades = [result['grade'] for result in capture['learning_content']['assessment_results'] if 'grade' in result]
       if grades:
           capture['analytics']['average_grade'] = round(sum(grades) / len(grades), 1)

   # Auto-identify learning goal connections
   all_content = (course_name + ' ' + ' '.join(capture['learning_content']['skills_developed']) + ' ' + ' '.join(capture['learning_content']['concepts_mastered'])).lower()

   for goal_id, goal in goals_data.get('learning_goals', {}).items():
       goal_keywords = set((goal.get('name', '') + ' ' + ' '.join(goal.get('tags', [])) + ' ' + ' '.join(goal.get('skills', []))).lower().split())

       # Check for keyword matches
       keyword_matches = sum(1 for keyword in goal_keywords if len(keyword) > 3 and keyword in all_content)
       if keyword_matches >= 2 or any(kw in course_name.lower() for kw in goal_keywords if len(kw) > 4):
           if goal_id not in capture['connections']['learning_goals']:
               capture['connections']['learning_goals'].append(goal_id)

   # Auto-generate tags
   subject_tags = {
       'programming': ['programming', 'development', 'coding', 'software'],
       'data-science': ['data', 'analytics', 'statistics', 'machine learning', 'ai'],
       'business': ['business', 'management', 'leadership', 'strategy', 'marketing'],
       'design': ['design', 'ux', 'ui', 'creative', 'visual'],
       'technology': ['technology', 'cloud', 'devops', 'infrastructure', 'systems']
   }

   for tag, keywords in subject_tags.items():
       if any(keyword in all_content for keyword in keywords):
           if tag not in capture['metadata']['tags']:
               capture['metadata']['tags'].append(tag)

   # Find connections to related courses
   for existing_capture in captures_data.get('captures', []):
       if (existing_capture.get('source_type') == 'course' and
           existing_capture.get('id') != capture['id']):

           # Check for skill overlap
           existing_skills = set(existing_capture.get('learning_content', {}).get('skills_developed', []))
           new_skills = set(capture['learning_content']['skills_developed'])

           if existing_skills.intersection(new_skills) or existing_capture.get('platform') == capture['platform']:
               if existing_capture['id'] not in capture['connections']['related_courses']:
                   capture['connections']['related_courses'].append(existing_capture['id'])

   # Save updated data
   captures_file.parent.mkdir(exist_ok=True)
   captures_file.write_text(json.dumps(captures_data, indent=2))

   # Generate intelligent response
   response = {
       'status': 'success',
       'command': '/learn course',
       'data': {
           'course_id': capture['course_id'],
           'course_name': course_name,
           'platform': platform,
           'progress_update': {
               'current_progress': f'{capture[\"progress\"]}%',
               'status': capture['status'],
               'completion_eta': None,  # Calculate based on velocity
               'lessons_completed': len(capture['progress_tracking']['completed_lessons']),
               'modules_completed': len(capture['progress_tracking']['completed_modules'])
           },
           'learning_analytics': {
               'time_invested': f'{capture[\"analytics\"][\"total_time_hours\"]:.1f} hours',
               'learning_velocity': f'{velocity:.1f}% per week' if velocity else 'calculating...',
               'efficiency_rating': efficiency.replace('_', ' ').title(),
               'average_grade': f'{capture[\"analytics\"][\"average_grade\"]:.1f}%' if capture[\"analytics\"][\"average_grade\"] else 'N/A'
           },
           'skill_development': {
               'skills_gained': len(capture['learning_content']['skills_developed']),
               'concepts_mastered': len(capture['learning_content']['concepts_mastered']),
               'tools_learned': len(capture['learning_content']['tools_learned']),
               'practical_applications': len(capture['learning_content']['practical_applications'])
           },
           'connections': {
               'learning_goals_updated': capture['connections']['learning_goals'],
               'related_courses': len(capture['connections']['related_courses']),
               'course_network_size': len([c for c in captures_data.get('captures', []) if c.get('source_type') == 'course'])
           }
       },
       'insights': {
           'learning_momentum': f'Strong progress momentum' if velocity and velocity > 5 else f'Steady learning pace' if velocity and velocity > 2 else f'Consider increasing study frequency',
           'skill_acquisition': f'Developing {len(capture[\"learning_content\"][\"skills_developed\"])} key skills aligned with your learning goals',
           'knowledge_integration': f'Course content connects to {len(capture[\"connections\"][\"learning_goals\"])} active learning goals'
       },
       'recommendations': [],
       'next_actions': []
   }

   # Calculate completion ETA
   if velocity and velocity > 0 and capture['progress'] < 100:
       weeks_remaining = (100 - capture['progress']) / velocity
       eta_date = datetime.date.today() + datetime.timedelta(weeks=weeks_remaining)
       response['data']['progress_update']['completion_eta'] = eta_date.strftime('%Y-%m-%d')

   # Generate contextual recommendations
   if capture['progress'] < 25 and efficiency == 'needs_optimization':
       response['recommendations'].append('Consider adjusting study method - current approach may not be optimal for your learning style')

   if capture['progress'] > 50 and not capture['learning_content']['practical_applications']:
       response['recommendations'].append('Look for opportunities to apply course concepts in real projects for better retention')

   if len(capture['learning_content']['challenging_topics']) > 3:
       response['recommendations'].append('Consider supplementary resources for challenging topics or study group participation')

   if capture['analytics']['average_grade'] and capture['analytics']['average_grade'] < 80:
       response['recommendations'].append('Review study strategies - consider more active learning techniques')

   # Generate next actions
   if capture['status'] == 'in_progress':
       if capture['progress'] < 30:
           response['next_actions'].append('Establish consistent daily study routine for momentum building')
       elif capture['progress'] > 70:
           response['next_actions'].append('Plan final project or practical application of learned concepts')

   if capture['connections']['learning_goals']:
       response['next_actions'].append(f'Update progress on {capture[\"connections\"][\"learning_goals\"][0]} learning goal')

   if len(capture['learning_content']['skills_developed']) > 2:
       response['next_actions'].append('Create connections between learned concepts using /learn connect')

   if capture['status'] == 'completed':
       response['next_actions'].append('Add course certificate to professional profiles and consider advanced follow-up courses')

   print(json.dumps(response, indent=2))
   "
   ```

5. **Provide intelligent course analytics**:
   - Learning velocity and efficiency analysis
   - Skill development progression tracking
   - Knowledge retention and application assessment
   - Study strategy optimization recommendations
   - Course completion forecasting and planning

## Course Learning Types:

### Progress Tracking
- **Module Completion**: Track individual lessons and sections
- **Milestone Achievements**: Certificates, projects, assessments
- **Skill Development**: Map course content to competency growth

### Performance Analytics
- **Grade Tracking**: Monitor assessment performance over time
- **Learning Velocity**: Track completion speed and consistency
- **Efficiency Analysis**: Optimize study time and methods

### Knowledge Integration
- **Practical Applications**: Connect theory to real-world projects
- **Cross-Course Synthesis**: Link concepts across multiple courses
- **Learning Goal Alignment**: Map progress to strategic objectives

### Study Optimization
- **Learning Style Assessment**: Identify most effective study methods
- **Time Management**: Track and optimize study time allocation
- **Retention Analysis**: Measure long-term knowledge retention

## Parameters:
- `--name NAME` - Course name (required for new courses)
- `--course-id ID` - Unique course identifier
- `--platform PLATFORM` - Learning platform (Coursera, Udemy, etc.)
- `--progress PERCENTAGE` - Current completion percentage
- `--module MODULE` - Current module or section
- `--completed-lesson LESSON` - Recently completed lesson
- `--completed-module MODULE` - Recently completed module
- `--skills LIST` - Skills developed (comma-separated)
- `--insights TEXT` - Key learning insights (separate with |)
- `--concepts LIST` - Concepts mastered (comma-separated)
- `--applications LIST` - Practical applications (comma-separated)
- `--tools LIST` - Tools learned (comma-separated)
- `--grade GRADE` - Assessment grade (0-100)
- `--assignment ASSIGNMENT` - Assignment name for grade
- `--time-spent HOURS` - Study time for this session
- `--notes TEXT` - Study notes or summary
- `--challenges LIST` - Challenging topics (comma-separated)
- `--rating RATING` - Course rating (1-5 stars)
- `--complete` - Mark course as completed
- `--certificate` - Certificate earned flag
- `--goal GOAL_ID` - Associate with learning goal
- `--category CATEGORY` - Course category

## Natural Language Processing:
Automatically detects:
- Progress indicators: "completed module...", "finished lesson...", "25% through..."
- Performance markers: "scored 95%", "passed the exam", "struggled with..."
- Skill development: "learned to...", "now understand...", "can implement..."
- Time references: "spent 3 hours", "studied for...", "weekly progress"

## Learning Analytics Dashboard:

### Course Progress Overview
```markdown
📚 **Course Progress**: Machine Learning Specialization
🎯 **Completion**: 67% (Module 4 of 6)
📊 **Velocity**: 8.5% per week (ahead of schedule)
⏱️ **Time Invested**: 28.5 hours
📈 **Efficiency**: Highly Efficient (0.4 hours per 1% progress)
```

### Performance Metrics
```markdown
📝 **Assessment Performance**:
- Average Grade: 91.2%
- Assignments Completed: 8/12
- Projects Submitted: 3/4
- Certificates Earned: 2

🧠 **Knowledge Acquisition**:
- Skills Developed: 12 (neural networks, optimization, evaluation)
- Concepts Mastered: 23 (backpropagation, regularization, CNN)
- Tools Learned: 6 (TensorFlow, Keras, Jupyter)
```

### Learning Network Integration
```markdown
🔗 **Learning Connections**:
- Related Courses: 3 (Python Programming, Statistics)
- Learning Goals: 2 (AI Mastery, Technical Leadership)
- Practical Applications: 5 (image classification project)
- Follow-up Courses Identified: Advanced Deep Learning, MLOps
```

## Output Examples:

### Course Progress Update
```json
{
  "status": "success",
  "command": "/learn course",
  "data": {
    "course_id": "machine-learning-specialization-coursera",
    "course_name": "Machine Learning Specialization",
    "platform": "Coursera",
    "progress_update": {
      "current_progress": "67%",
      "status": "in_progress",
      "completion_eta": "2024-11-15",
      "lessons_completed": 24,
      "modules_completed": 4
    },
    "learning_analytics": {
      "time_invested": "28.5 hours",
      "learning_velocity": "8.5% per week",
      "efficiency_rating": "Highly Efficient",
      "average_grade": "91.2%"
    },
    "skill_development": {
      "skills_gained": 12,
      "concepts_mastered": 23,
      "tools_learned": 6,
      "practical_applications": 5
    }
  },
  "insights": {
    "learning_momentum": "Strong progress momentum",
    "skill_acquisition": "Developing 12 key skills aligned with your learning goals",
    "knowledge_integration": "Course content connects to 2 active learning goals"
  },
  "next_actions": [
    "Plan final project or practical application of learned concepts",
    "Update progress on ai-mastery learning goal",
    "Create connections between learned concepts using /learn connect"
  ]
}
```

### Course Completion Summary
```json
{
  "status": "success",
  "command": "/learn course",
  "data": {
    "course_id": "react-advanced-patterns",
    "completion_summary": {
      "total_time": "45 hours",
      "final_grade": "96%",
      "skills_mastered": ["advanced-react", "state-management", "performance-optimization"],
      "projects_completed": ["E-commerce Dashboard", "Real-time Chat App"],
      "certificate_earned": true
    }
  },
  "next_actions": [
    "Add course certificate to professional profiles",
    "Consider advanced follow-up courses",
    "Apply learned patterns to current project"
  ]
}
```

## Integration Features:
- **Learning Goal Synchronization**: Auto-update goal progress based on course completion
- **Skill Portfolio Management**: Track skill development across multiple courses
- **Course Recommendation Engine**: Suggest follow-up courses based on progress and goals
- **Time Management Integration**: Calendar blocking for study sessions
- **Performance Analytics**: Long-term learning efficiency tracking

## Behavior:
- Creates comprehensive course learning entries with detailed progress tracking
- Provides intelligent learning velocity and efficiency analysis
- Identifies skill development patterns and competency growth
- Generates actionable study optimization recommendations
- Maintains course learning history with performance metrics
- Supports both ongoing progress updates and completion summaries
- Integrates with existing PARA Method learning and goal management

Maximize your course learning effectiveness with intelligent progress tracking, skill development monitoring, and study optimization analytics.
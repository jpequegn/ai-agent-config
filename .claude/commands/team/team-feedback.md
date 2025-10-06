---
name: team-feedback
description: Comprehensive feedback and development planning system for performance reviews and growth planning
---

# Team Feedback & Development Planning System

Comprehensive feedback management and development planning system that integrates with team roster, performance data, and review templates for structured performance evaluation and growth planning.

## Usage Examples:
- `/team review-draft [email]` - Generate comprehensive performance review drafts with structured evaluation
- `/team development-plan [email]` - Create personalized development plans based on assessment data and growth opportunities
- `/team feedback-360 [email]` - Organize and synthesize 360-degree feedback collection and analysis
- `/team goals-check [email]` - Analyze goal achievement rates, progress patterns, and adjustment recommendations
- `/team review-draft [email] --template [template-name]` - Use specific review template
- `/team development-plan [email] --focus [area]` - Focus development plan on specific skill area
- `/team feedback-360 [email] --include-peers` - Include peer feedback in 360 analysis
- `/team goals-check --team` - Analyze goal achievement across entire team

## OutputFormatter Integration

**Tool**: Use `OutputFormatter` with `team_feedback` template for professional performance review formatting.

**Template**: `templates/output/team_feedback.md.j2` - Comprehensive performance review template with accomplishments, goals, competencies, 360° feedback, and growth planning.

### Integration Example

```python
from tools import OutputFormatter, DataCollector

# 1. Gather comprehensive performance data
collector = DataCollector()
team_data = collector.collect_team_data()
config_data = collector.collect_config_data()

# Find team member
member = next((m for m in team_data.members if m.email == member_email), None)

# 2. Structure performance review data
feedback_data = {
    'employee': {
        'name': member.name,
        'role': member.role,
        'email': member.email
    },
    'review_period': 'Q4 2024',
    'reviewer': config_data.user.name,
    'overall_rating': calculate_overall_rating(member),  # 0.0-1.0
    'summary': 'Performance summary highlighting key achievements and areas for growth...',

    'accomplishments': [
        {
            'title': 'Led Mobile App Launch',
            'description': 'Successfully delivered mobile app 2 weeks ahead of schedule...',
            'impact': 'Increased user engagement by 45% in first month',
            'metrics': [
                '45% increase in user engagement',
                '2 weeks ahead of schedule',
                '95% positive user feedback'
            ]
        }
    ],

    'goals': [
        {
            'title': 'Improve API Response Time',
            'description': 'Optimize backend APIs to reduce average response time by 30%',
            'status': 'completed',  # completed, in_progress, at_risk, pending
            'progress': 0.95,
            'completion_date': '2024-11-15',
            'outcome': 'Achieved 40% improvement through caching and query optimization'
        }
    ],

    'strengths': [
        {
            'area': 'Technical Leadership',
            'description': 'Demonstrates exceptional ability to guide team through complex technical challenges'
        }
    ],

    'development_areas': [
        {
            'title': 'Strategic Communication',
            'description': 'Opportunities to enhance communication with non-technical stakeholders',
            'priority': 'high',  # high, medium, low
            'action_items': [
                'Attend stakeholder management workshop',
                'Practice presenting technical concepts to executives'
            ],
            'resources': [
                'Effective Technical Communication course',
                'Mentorship with senior architect'
            ]
        }
    ],

    'competencies': [
        {
            'name': 'Technical Expertise',
            'rating': 0.9,
            'notes': 'Deep knowledge of backend systems and best practices'
        },
        {
            'name': 'Collaboration',
            'rating': 0.85,
            'notes': 'Works well with team, could improve cross-functional communication'
        }
    ],

    'peer_feedback': [
        {
            'from': 'Sarah Johnson',
            'comment': 'Excellent technical mentor, always willing to help teammates'
        }
    ],

    'manager_feedback': 'Consistently delivers high-quality work with strong technical foundation...',
    'self_assessment': 'I feel I\'ve grown significantly in technical leadership...',

    'growth_plan': {
        'career_goals': [
            'Transition to senior architect role within 18 months',
            'Lead cross-functional technical initiatives'
        ],
        'skill_development': [
            {
                'name': 'System Architecture',
                'plan': 'Design and document architecture for 3 major features',
                'timeline': '6 months',
                'resources': ['Architecture patterns course', 'Weekly architect mentorship']
            }
        ],
        'training': [
            {
                'title': 'Advanced System Design',
                'description': 'Deep dive into distributed systems architecture',
                'provider': 'Internal Learning',
                'timeline': 'Q1 2025'
            }
        ]
    },

    'next_period_goals': [
        {
            'title': 'Lead Architecture Review Process',
            'description': 'Establish and run quarterly architecture review sessions',
            'success_criteria': 'Complete 4 quarterly reviews with team participation >80%',
            'target_date': '2025-06-30'
        }
    ],

    'action_items': [
        {
            'action': 'Schedule architecture mentorship sessions',
            'owner': member.name,
            'deadline': '2025-01-15',
            'status': 'pending'
        }
    ],

    'compensation': {
        'salary_adjustment': '8% merit increase',
        'bonus': '15% annual bonus',
        'equity': '500 RSUs'
    },

    'next_review_date': '2025-04-01',
    'review_frequency': 'Quarterly'
}

# 3. Format with OutputFormatter
formatter = OutputFormatter()
output = formatter.format_markdown(feedback_data, template="team_feedback")

# 4. Save or display
print(output.content)
# Processing time: ~15-20ms
```

**Key Benefits**:
- **Reduces Command Complexity**: 1487 lines → ~25-30 lines of structured data
- **Professional Formatting**: Consistent emoji indicators, health scores, date formatting
- **Type Safety**: Pydantic validation ensures data integrity
- **Performance**: <50ms template rendering with session caching
- **Reusability**: Same template across all performance review workflows

## Instructions:

You are a comprehensive feedback and development planning system. When this command is invoked:

### Core Functionality

1. **Load Comprehensive Data**
   - Use DataCollector tool to aggregate comprehensive team and project data
   - Access team member data via `team_data.members`
   - Load performance metrics from integrated sources
   - Access review templates from configuration
   - Retrieve 1:1 notes from cache
   - Load project assignments from `config_data.projects`

2. **Feedback Analysis Engine**
   - Synthesize multi-source feedback data
   - Analyze performance trends and patterns
   - Generate evidence-based insights
   - Create actionable development recommendations

3. **Command Actions**

   **Performance Review Drafting `review-draft [email]`:**
   - Generate comprehensive performance review drafts using structured templates
   - Include quantitative performance metrics and trend analysis
   - Synthesize feedback from multiple sources (1:1s, projects, peer input)
   - Create evidence-based narrative with specific examples
   - Align with review template structure and scoring criteria
   - Generate recommendations for ratings and development focus

   **Development Planning `development-plan [email]`:**
   - Create personalized development plans based on current assessment
   - Analyze strengths, development areas, and growth opportunities
   - Map development goals to career progression pathways
   - Include specific action items, timelines, and success metrics
   - Recommend training, mentoring, and stretch assignments
   - Align with organizational skills framework and advancement criteria

   **360-Degree Feedback `feedback-360 [email]`:**
   - Organize and synthesize feedback from managers, peers, and direct reports
   - Analyze feedback themes and identify consensus patterns
   - Highlight areas of agreement and divergence in feedback
   - Generate feedback summary with actionable insights
   - Create feedback delivery plan with talking points
   - Track feedback collection status and completion

   **Goal Achievement Analysis `goals-check [email]`:**
   - Analyze goal achievement rates and progress patterns
   - Identify successful goal completion strategies
   - Highlight goals at risk or falling behind schedule
   - Generate recommendations for goal adjustments
   - Track goal evolution and adaptation over time
   - Provide insights for future goal setting

### Output Formats

#### Performance Review Draft Output

```markdown
# Performance Review Draft: [Member Name]
**Employee:** [Full Name] (`[email]`) | **Role:** [role]
**Review Period:** [start date] to [end date] | **Review Type:** [template type]
**Manager:** [manager name] | **Generated:** [date]

## 📋 Executive Summary
**Overall Performance Rating:** [Recommended Rating] | **Trend:** [Improving/Stable/Declining]
**Key Accomplishments:** [2-3 major achievements with impact]
**Development Focus:** [1-2 primary areas for growth]

## 🎯 Performance Assessment

### Core Competencies Analysis
| Competency | Rating | Evidence | Trend |
|------------|--------|----------|-------|
| [Competency 1] | [Score] | [Specific examples] | [Direction] |
| [Competency 2] | [Score] | [Specific examples] | [Direction] |
| [Competency 3] | [Score] | [Specific examples] | [Direction] |

### Goal Achievement Review
**Q[Quarter] Goals Performance:** [percentage]% completion rate

**Goal 1: [Goal Name]**
- **Status:** [Completed/In Progress/At Risk/Not Met]
- **Achievement:** [percentage]% complete
- **Evidence:** [Specific accomplishments and metrics]
- **Impact:** [Business/team impact achieved]
- **Rating Rationale:** [Why this rating was assigned]

**Goal 2: [Goal Name]**
- **Status:** [status]
- **Achievement:** [percentage]% complete
- **Evidence:** [accomplishments]
- **Impact:** [impact achieved]
- **Rating Rationale:** [rationale]

### Project Performance Analysis
**Key Projects:** [project count] active projects this period

**[Project Name]** - [status]
- **Role:** [team member's role]
- **Achievements:** [specific contributions]
- **Challenges:** [obstacles overcome]
- **Team Impact:** [collaboration effectiveness]
- **Quality:** [deliverable quality assessment]

### Behavioral Competencies
**Leadership & Influence:** [rating]
- **Evidence:** [specific examples of leadership behaviors]
- **Growth:** [leadership development demonstrated]
- **Impact:** [influence on team/organization]

**Collaboration & Communication:** [rating]
- **Evidence:** [examples of effective collaboration]
- **Feedback Quality:** [based on 1:1 notes and peer feedback]
- **Cross-functional Work:** [effectiveness across teams]

**Technical Excellence:** [rating]
- **Evidence:** [technical contributions and improvements]
- **Innovation:** [new approaches or solutions]
- **Knowledge Sharing:** [mentoring and documentation]

## 📊 Performance Data & Metrics

### Quantitative Performance
- **Project Velocity:** [metric] (vs. target: [target])
- **Quality Metrics:** [metric] (vs. team average: [average])
- **Collaboration Score:** [metric] (trend: [direction])
- **Goal Completion Rate:** [percentage]% (vs. expected: [expected])

### 360-Degree Feedback Summary
**Manager Feedback Themes:**
- [Theme 1]: [frequency] mentions
- [Theme 2]: [frequency] mentions
- [Theme 3]: [frequency] mentions

**Peer Feedback Highlights:**
- **Strengths:** [commonly mentioned strengths]
- **Development Areas:** [areas for improvement]
- **Collaboration:** [feedback on teamwork]

### 1:1 Meeting Insights
**Meeting Frequency:** [frequency] | **Engagement Level:** [high/medium/low]
**Common Discussion Topics:**
1. **Career Development** ([percentage]% of meetings)
2. **Project Challenges** ([percentage]% of meetings)
3. **Team Dynamics** ([percentage]% of meetings)

**Commitment Follow-through:** [percentage]% completion rate

## 🌟 Strengths & Achievements

### Key Strengths (Evidence-Based)
1. **[Strength Area]**
   - **Evidence:** [specific examples and metrics]
   - **Impact:** [how this strength benefited team/org]
   - **Recognition:** [acknowledgments received]

2. **[Strength Area]**
   - **Evidence:** [examples]
   - **Impact:** [benefit]
   - **Growth:** [how strength has developed]

### Notable Achievements
**[Achievement 1]**
- **Context:** [situation and challenge]
- **Action:** [what the team member did]
- **Result:** [outcome and impact]
- **Recognition:** [acknowledgment received]

**[Achievement 2]**
- **Context:** [situation]
- **Action:** [actions taken]
- **Result:** [measurable outcome]
- **Learning:** [insights gained]

## 🎯 Development Areas & Growth Opportunities

### Primary Development Focus
**[Development Area 1]**
- **Current Level:** [assessment]
- **Target Level:** [goal]
- **Gap Analysis:** [specific skills/behaviors to develop]
- **Evidence:** [examples supporting this assessment]
- **Impact:** [how improvement would benefit role/team]

**[Development Area 2]**
- **Current Level:** [assessment]
- **Target Level:** [goal]
- **Gap Analysis:** [development needed]
- **Evidence:** [supporting examples]
- **Growth Path:** [suggested development approach]

### Growth Opportunities
1. **[Opportunity]** - [description and potential impact]
2. **[Opportunity]** - [description and development value]
3. **[Opportunity]** - [description and stretch potential]

## 📈 Performance Trajectory & Future Planning

### Career Progression Assessment
**Current Level:** [level] | **Next Level:** [target level]
**Readiness Timeline:** [months/quarters to advancement]
**Key Blockers:** [obstacles to advancement]
**Acceleration Opportunities:** [ways to speed progression]

### Recommended Rating Justification
**Overall Rating:** [rating]
**Rationale:**
- [Justification point 1 with evidence]
- [Justification point 2 with evidence]
- [Justification point 3 with evidence]

**Comparison Context:**
- **Peer Group:** [how performance compares to similar roles]
- **Historical:** [performance trend over time]
- **Potential:** [future capability assessment]

## 🚀 Development Recommendations

### Immediate Actions (Next 30 Days)
1. **[Action]** - [description and expected outcome]
2. **[Action]** - [description and timeline]
3. **[Action]** - [description and success metric]

### Quarter Goals
1. **[Goal]** - [SMART goal with measurement]
2. **[Goal]** - [goal with timeline and success criteria]
3. **[Goal]** - [development goal with clear outcome]

### Long-term Development (6-12 Months)
- **Skill Development:** [specific skills and learning plan]
- **Experience Gaps:** [experiences needed for growth]
- **Leadership Opportunities:** [stretch assignments and projects]

## 💬 Delivery Talking Points

### Positive Feedback Delivery
- **Recognition:** [specific achievements to celebrate]
- **Strength Reinforcement:** [behaviors to continue/amplify]
- **Growth Acknowledgment:** [progress to acknowledge]

### Development Conversation
- **Growth Mindset:** [how to frame development areas positively]
- **Support Offered:** [resources and support available]
- **Collaboration:** [how we'll work together on growth]

### Goal Setting Discussion
- **Next Period Focus:** [priorities for upcoming period]
- **Stretch Opportunities:** [challenging but achievable goals]
- **Success Metrics:** [how progress will be measured]

## 📋 Review Meeting Agenda

### Opening (5 minutes)
- Review meeting purpose and structure
- Set collaborative tone for discussion

### Performance Discussion (20 minutes)
- Review achievements and metrics
- Discuss strengths and impact
- Address development areas constructively

### Development Planning (15 minutes)
- Explore growth opportunities
- Align on development priorities
- Commit to specific actions

### Goal Setting (10 minutes)
- Review upcoming period goals
- Ensure clarity and agreement
- Establish check-in schedule

### Closing (5 minutes)
- Summarize key commitments
- Schedule follow-up discussions
- Express confidence and support

## 📊 Supporting Evidence

### Performance Metrics
- **Data Sources:** [list of quantitative sources]
- **Time Period:** [measurement period]
- **Benchmark Comparisons:** [relevant comparisons]

### Feedback Sources
- **1:1 Notes:** [number] meetings analyzed
- **Project Feedback:** [number] projects reviewed
- **Peer Input:** [sources of peer feedback]
- **360 Data:** [if available]

### Documentation
- **Goal Tracking:** [goal management system]
- **Project Records:** [project management data]
- **Training Records:** [development activities]

## 🔄 Next Steps

### Manager Actions
- [ ] Review draft with HR/senior leadership
- [ ] Schedule performance review meeting
- [ ] Prepare development resources
- [ ] Update performance management system

### Employee Preparation
- [ ] Self-assessment completion
- [ ] Goal reflection and input
- [ ] Development interest discussion
- [ ] Questions and concerns preparation

### Follow-up Requirements
- [ ] Performance improvement plan (if needed)
- [ ] Development plan creation
- [ ] Goal setting for next period
- [ ] Career development discussion
```

#### Development Plan Output

```markdown
# Individual Development Plan: [Member Name]
**Employee:** [Full Name] (`[email]`) | **Role:** [current role]
**Planning Period:** [start date] to [end date] | **Next Review:** [date]
**Manager:** [manager name] | **Career Goal:** [target role/level]

## 🎯 Development Vision & Goals

### Career Aspiration
**Target Role:** [desired role] | **Timeline:** [months/years]
**Key Motivations:** [what drives this career goal]
**Success Definition:** [how success will be measured]

### Development Philosophy
**Learning Style:** [preferred learning approach]
**Challenge Level:** [comfortable stretch zones]
**Support Needs:** [types of support most effective]

## 📊 Current State Assessment

### Strength Analysis
**Core Strengths:**
1. **[Strength 1]** - [evidence and impact]
2. **[Strength 2]** - [evidence and application]
3. **[Strength 3]** - [evidence and value]

**Strength Utilization:**
- **Leveraging Opportunities:** [how to better use strengths]
- **Strength-Based Projects:** [projects that play to strengths]
- **Mentoring Others:** [how strengths can help others]

### Development Areas Analysis
**Priority Development Areas:**
1. **[Area 1]**
   - **Current Level:** [assessment]
   - **Target Level:** [goal]
   - **Gap:** [specific skills/behaviors needed]
   - **Impact:** [why this matters for role/career]

2. **[Area 2]**
   - **Current Level:** [assessment]
   - **Target Level:** [goal]
   - **Gap:** [development needed]
   - **Urgency:** [timeline importance]

### Skills Gap Matrix
| Skill Category | Current | Target | Gap | Priority |
|----------------|---------|--------|-----|----------|
| [Technical Skills] | [level] | [level] | [gap] | [High/Med/Low] |
| [Leadership] | [level] | [level] | [gap] | [priority] |
| [Communication] | [level] | [level] | [gap] | [priority] |
| [Strategic Thinking] | [level] | [level] | [gap] | [priority] |

## 🎓 Development Strategy & Approach

### Learning Pathways
**Primary Development Track:** [main focus area]
**Secondary Tracks:** [supporting development areas]
**Cross-functional Exposure:** [breadth development]

### Development Methods
**Preferred Learning Styles:**
- **Experiential:** [percentage]% - hands-on projects and experiences
- **Social:** [percentage]% - mentoring, coaching, peer learning
- **Formal:** [percentage]% - training, courses, certifications
- **Self-directed:** [percentage]% - reading, research, online learning

## 📚 Detailed Development Plan

### Development Goal 1: [Goal Name]
**Target:** [specific skill/competency to develop]
**Timeline:** [months to achieve]
**Success Metrics:** [how progress will be measured]

**Learning Activities:**
1. **[Activity]** - [description, timeline, resources needed]
2. **[Activity]** - [description, duration, expected outcome]
3. **[Activity]** - [description, milestone, success criteria]

**Support Required:**
- **Manager Support:** [specific support needed]
- **Mentor Assignment:** [type of mentor, expertise area]
- **Resources:** [training budget, tools, access needed]

**Milestones & Check-ins:**
- **Month 1:** [milestone and assessment]
- **Month 3:** [milestone and review]
- **Month 6:** [completion and evaluation]

### Development Goal 2: [Goal Name]
**Target:** [competency development]
**Timeline:** [achievement timeframe]
**Business Impact:** [how this development benefits the organization]

**Action Plan:**
1. **Stretch Assignment:** [project or role expansion]
   - **Scope:** [description of assignment]
   - **Skills Developed:** [specific skills gained]
   - **Support:** [guidance and resources]
   - **Timeline:** [duration and milestones]

2. **Training & Education:**
   - **Course/Program:** [specific training]
   - **Provider:** [internal/external source]
   - **Schedule:** [timing and duration]
   - **Application:** [how learning will be applied]

3. **Mentoring & Coaching:**
   - **Mentor Profile:** [type of mentor needed]
   - **Focus Areas:** [specific guidance areas]
   - **Schedule:** [meeting frequency]
   - **Goals:** [mentoring objectives]

### Development Goal 3: [Goal Name]
**Target:** [leadership/strategic development]
**Rationale:** [why this development is important]
**Career Impact:** [how this advances career goals]

**Experience-Based Learning:**
- **Leadership Opportunity:** [specific role or project]
- **Cross-functional Project:** [collaboration development]
- **Innovation Initiative:** [creative/strategic thinking]

**Knowledge Building:**
- **Industry Learning:** [external perspective development]
- **Best Practices Research:** [benchmarking and standards]
- **Network Development:** [relationship building]

## 👥 Support System & Resources

### Mentoring Plan
**Primary Mentor:** [internal mentor details]
- **Expertise:** [mentor's strengths and experience]
- **Meeting Schedule:** [frequency and format]
- **Focus Areas:** [specific development topics]

**External Mentor:** [external industry mentor]
- **Industry Perspective:** [external insights]
- **Network Access:** [connections and opportunities]
- **Career Guidance:** [advancement strategies]

### Training & Development Resources
**Internal Resources:**
- **Training Programs:** [company training available]
- **Job Rotation:** [internal mobility opportunities]
- **Special Projects:** [development project assignments]

**External Resources:**
- **Professional Development Budget:** $[amount] allocated
- **Conference Attendance:** [relevant conferences]
- **Certification Programs:** [specific certifications]
- **Online Learning Platforms:** [subscriptions and access]

### Manager Support Plan
**Regular Check-ins:** [frequency and format]
**Development Discussions:** [focused development meetings]
**Opportunity Creation:** [manager-facilitated opportunities]
**Advocacy:** [promotion and visibility support]

## 📅 Implementation Timeline

### Quarter 1 (Months 1-3)
**Primary Focus:** [main development area]
**Key Activities:**
- Week 1-2: [initial activities]
- Month 1: [first milestone]
- Month 2: [progress checkpoint]
- Month 3: [quarter assessment]

**Expected Outcomes:**
- [Specific skill improvement]
- [Behavioral change]
- [Project contribution]

### Quarter 2 (Months 4-6)
**Primary Focus:** [development progression]
**Advanced Activities:**
- [More complex challenges]
- [Leadership opportunities]
- [Cross-functional work]

**Skill Application:**
- [Real-world application]
- [Teaching others]
- [Process improvement]

### Quarter 3 (Months 7-9)
**Primary Focus:** [mastery and expansion]
**Stretch Opportunities:**
- [Challenging assignments]
- [Leadership roles]
- [Innovation projects]

### Quarter 4 (Months 10-12)
**Primary Focus:** [consolidation and planning]
**Assessment & Planning:**
- [Development assessment]
- [Next level planning]
- [Career progression discussion]

## 📊 Progress Tracking & Measurement

### Development Metrics
**Skill Development Tracking:**
| Skill | Baseline | Q1 Target | Q2 Target | Q3 Target | Q4 Target |
|-------|----------|-----------|-----------|-----------|-----------|
| [Skill 1] | [level] | [level] | [level] | [level] | [level] |
| [Skill 2] | [level] | [level] | [level] | [level] | [level] |
| [Skill 3] | [level] | [level] | [level] | [level] | [level] |

### Behavioral Indicators
**Observable Changes:**
- **Communication:** [specific improvements to track]
- **Leadership:** [leadership behaviors to develop]
- **Collaboration:** [teamwork enhancements]
- **Innovation:** [creative problem-solving growth]

### Performance Impact
**Role Performance:**
- **Current Role Enhancement:** [how development improves current performance]
- **Expanded Responsibilities:** [new capabilities gained]
- **Team Impact:** [positive influence on team]

**Business Impact:**
- **Project Contributions:** [enhanced project outcomes]
- **Process Improvements:** [operational enhancements]
- **Knowledge Sharing:** [contribution to team learning]

## 🔄 Review & Adaptation Process

### Monthly Check-ins
**Progress Review:** [assessment of development activities]
**Challenge Discussion:** [obstacles and solutions]
**Adjustment Planning:** [plan modifications needed]

### Quarterly Reviews
**Comprehensive Assessment:** [thorough progress evaluation]
**Goal Adjustment:** [plan updates and refinements]
**Resource Evaluation:** [support effectiveness]

### Annual Development Review
**Achievement Assessment:** [year-end development evaluation]
**Career Progression:** [advancement readiness]
**Next Year Planning:** [future development priorities]

## 🚀 Success Enablers

### Critical Success Factors
1. **Regular Practice:** [consistent application of new skills]
2. **Feedback Integration:** [active use of feedback for improvement]
3. **Challenge Seeking:** [proactive pursuit of growth opportunities]
4. **Reflection & Learning:** [regular self-assessment and adaptation]

### Risk Mitigation
**Potential Challenges:**
- **Time Constraints:** [solution - protected development time]
- **Competing Priorities:** [solution - clear priority management]
- **Limited Opportunities:** [solution - creative opportunity creation]

### Organizational Support
**Manager Commitment:** [specific manager support commitments]
**HR Partnership:** [HR support and resources]
**Senior Leadership:** [visibility and advocacy]

## 📋 Development Contract

### Employee Commitments
- [ ] Dedicate [hours] per week to development activities
- [ ] Actively seek feedback and apply learnings
- [ ] Participate fully in mentoring relationships
- [ ] Take ownership of development progress

### Manager Commitments
- [ ] Provide regular feedback and coaching
- [ ] Create development opportunities
- [ ] Advocate for employee advancement
- [ ] Allocate necessary resources and support

### Organizational Commitments
- [ ] Provide development budget and resources
- [ ] Support time allocation for development
- [ ] Recognize and reward development progress
- [ ] Create advancement pathways

## 📈 Long-term Career Roadmap

### Next Role Preparation
**Target Role:** [specific next position]
**Readiness Timeline:** [expected timeframe]
**Remaining Gaps:** [skills/experience still needed]

### 3-Year Vision
**Career Goals:** [longer-term aspirations]
**Leadership Development:** [leadership progression path]
**Expertise Building:** [deep skill development]

### 5-Year Aspirations
**Strategic Goals:** [long-term career objectives]
**Industry Impact:** [contribution and recognition goals]
**Legacy Building:** [knowledge transfer and mentoring]

This development plan is a living document that will be regularly reviewed and updated to ensure continued relevance and effectiveness in supporting career growth and organizational needs.
```

#### 360 Feedback Analysis Output

```markdown
# 360-Degree Feedback Analysis: [Member Name]
**Employee:** [Full Name] (`[email]`) | **Role:** [role]
**Feedback Period:** [start date] to [end date]
**Manager:** [manager name] | **Analysis Date:** [date]

## 📊 Feedback Collection Summary

### Participation Overview
**Total Respondents:** [number] | **Response Rate:** [percentage]%
**Feedback Sources:**
- **Manager:** [manager name] ✅
- **Peers:** [number] responses ([list names or roles])
- **Direct Reports:** [number] responses ([if applicable])
- **Cross-functional Partners:** [number] responses
- **Self-Assessment:** ✅ Completed

### Response Quality
**Completion Rate:** [percentage]% of questions answered
**Comment Depth:** [assessment of comment quality]
**Response Consistency:** [consistency across respondents]

## 🎯 Overall Feedback Analysis

### Aggregate Ratings Summary
| Competency Area | Avg Rating | Self Rating | Gap | Trend |
|-----------------|------------|-------------|-----|-------|
| Technical Excellence | [score]/5 | [score]/5 | [+/-diff] | [↑↓→] |
| Leadership & Influence | [score]/5 | [score]/5 | [+/-diff] | [trend] |
| Communication | [score]/5 | [score]/5 | [+/-diff] | [trend] |
| Collaboration | [score]/5 | [score]/5 | [+/-diff] | [trend] |
| Problem Solving | [score]/5 | [score]/5 | [+/-diff] | [trend] |
| Innovation | [score]/5 | [score]/5 | [+/-diff] | [trend] |

### Self-Awareness Analysis
**High Self-Awareness Areas:**
- [Area where self-rating closely matches others]
- [Area with good alignment]

**Low Self-Awareness Areas:**
- [Area where self-rating differs significantly]
- [Area needing perspective adjustment]

**Self-Rating Patterns:**
- **Over-estimation:** [areas where self-rating > others]
- **Under-estimation:** [areas where self-rating < others]
- **Accurate Assessment:** [areas with good alignment]

## 🌟 Strengths Analysis

### Consensus Strengths
**Universally Recognized Strengths** (mentioned by >75% of respondents):

**[Strength 1]** - [rating] average
- **Manager Perspective:** "[specific quote or paraphrase]"
- **Peer Feedback:** "[common themes from peers]"
- **Direct Report View:** "[if applicable]"
- **Impact Evidence:** [specific examples of this strength in action]

**[Strength 2]** - [rating] average
- **Cross-functional Recognition:** "[feedback from other teams]"
- **Consistency:** [how consistently this strength appears]
- **Growth Trajectory:** [how this strength has developed]

### Emerging Strengths
**Developing Areas** (mentioned by 50-75% of respondents):
- **[Emerging Strength]:** [description and evidence]
- **Growth Potential:** [opportunity for further development]

### Unique Perspectives
**Manager-Specific Recognition:**
- [Strengths only manager mentioned]

**Peer-Specific Recognition:**
- [Strengths primarily peers mentioned]

## 🎯 Development Opportunities

### Priority Development Areas
**Consensus Development Needs** (mentioned by >75% of respondents):

**[Development Area 1]** - [average rating]
- **Impact on Effectiveness:** [how this limitation affects performance]
- **Specific Feedback Examples:**
  - Manager: "[specific feedback]"
  - Peers: "[common themes]"
  - Direct Reports: "[perspective if applicable]"
- **Recommended Actions:** [specific suggestions from feedback]

**[Development Area 2]** - [average rating]
- **Pattern Analysis:** [when/where this shows up]
- **Root Cause Insights:** [potential underlying causes]
- **Development Path:** [suggested improvement approach]

### Moderate Development Areas
**Secondary Focus Areas** (mentioned by 25-75% of respondents):
- **[Area]:** [feedback summary and suggested approach]
- **[Area]:** [development opportunity description]

### Perception Gaps
**Areas with Significant Rating Variance:**
- **[Area with high variance]:** [range] rating range
  - **Possible Causes:** [why perceptions might differ]
  - **Context Factors:** [situational influences]
  - **Clarification Needed:** [areas requiring discussion]

## 📈 Behavioral Feedback Analysis

### Communication Effectiveness
**Verbal Communication:**
- **Clarity:** [feedback on clarity of communication]
- **Listening:** [feedback on listening skills]
- **Influence:** [ability to persuade and influence]

**Written Communication:**
- **Documentation:** [quality of written work]
- **Email/Messaging:** [effectiveness of digital communication]
- **Presentation:** [presentation and reporting skills]

### Collaboration & Teamwork
**Team Dynamics:**
- **Inclusivity:** [how well includes others]
- **Conflict Resolution:** [handling disagreements]
- **Support:** [helping team members succeed]

**Cross-functional Work:**
- **Partnership Quality:** [effectiveness across teams]
- **Stakeholder Management:** [managing relationships]
- **Influence Without Authority:** [lateral leadership]

### Leadership Behaviors
**People Leadership:**
- **Motivation:** [ability to inspire and motivate]
- **Development:** [supporting others' growth]
- **Recognition:** [acknowledging others' contributions]

**Thought Leadership:**
- **Vision:** [strategic thinking and vision setting]
- **Innovation:** [driving new ideas and approaches]
- **Decision Making:** [quality and timeliness of decisions]

## 🔍 Detailed Feedback Themes

### Positive Feedback Themes
**Most Frequent Positive Comments:**
1. **[Theme 1]** ([frequency] mentions)
   - Representative Quote: "[specific example]"
   - Impact: [how this benefits team/organization]

2. **[Theme 2]** ([frequency] mentions)
   - Representative Quote: "[quote]"
   - Context: [when this strength is most evident]

3. **[Theme 3]** ([frequency] mentions)
   - Representative Quote: "[quote]"
   - Growth: [how this has improved over time]

### Constructive Feedback Themes
**Most Frequent Development Suggestions:**
1. **[Theme 1]** ([frequency] mentions)
   - Representative Quote: "[specific example]"
   - Suggested Action: [what respondents recommend]

2. **[Theme 2]** ([frequency] mentions)
   - Representative Quote: "[quote]"
   - Context: [situations where this is most relevant]

3. **[Theme 3]** ([frequency] mentions)
   - Representative Quote: "[quote]"
   - Priority: [urgency of addressing this area]

## 🎯 Role-Specific Feedback

### Current Role Performance
**Core Responsibilities:**
- **[Responsibility 1]:** [feedback on performance]
- **[Responsibility 2]:** [effectiveness assessment]
- **[Responsibility 3]:** [strength/development area]

### Future Role Readiness
**Advancement Readiness:**
- **Ready Strengths:** [areas already at next level]
- **Development Needs:** [gaps for next role]
- **Timeline Assessment:** [readiness timeframe]

## 💡 Actionable Insights & Recommendations

### Immediate Focus Areas (Next 30 Days)
1. **[Action 1]** - [specific behavior to start/stop/continue]
   - **Context:** [when/where to apply this]
   - **Measurement:** [how to track progress]

2. **[Action 2]** - [development activity]
   - **Resources:** [what support is needed]
   - **Timeline:** [expected timeframe]

3. **[Action 3]** - [relationship/communication improvement]
   - **Stakeholders:** [who to focus on]
   - **Approach:** [specific method]

### Medium-term Development (3-6 Months)
**Skill Building Priorities:**
- **[Skill Area]:** [development plan based on feedback]
- **Learning Approach:** [recommended method]
- **Practice Opportunities:** [where to apply new skills]

**Relationship Enhancement:**
- **[Relationship Type]:** [improvement strategy]
- **Communication Style:** [adjustments to make]
- **Collaboration Approach:** [new behaviors to adopt]

### Long-term Growth (6-12 Months)
**Leadership Development:**
- **Vision:** [strategic thinking enhancement]
- **Influence:** [expanding impact and reach]
- **Development of Others:** [mentoring and coaching growth]

**Career Advancement:**
- **Readiness Building:** [preparation for next role]
- **Network Expansion:** [relationship building strategy]
- **Expertise Development:** [deep skill building]

## 🔄 Feedback Delivery Strategy

### Positive Recognition Plan
**Strengths to Celebrate:**
- [Strength with specific examples to highlight]
- [Achievement to recognize and reinforce]
- [Behavior to encourage continuation]

**Recognition Approach:**
- **Public Recognition:** [what to highlight publicly]
- **Private Appreciation:** [personal feedback to give]
- **Growth Acknowledgment:** [progress to celebrate]

### Development Conversation Framework
**Opening Approach:**
- Set collaborative tone for development
- Emphasize growth opportunity perspective
- Acknowledge overall strong performance

**Development Discussion:**
- **[Development Area 1]:**
  - **Frame:** [how to present this constructively]
  - **Evidence:** [specific examples to discuss]
  - **Support:** [help and resources to offer]

- **[Development Area 2]:**
  - **Context:** [situational factors to consider]
  - **Impact:** [importance of improvement]
  - **Collaboration:** [how to work together on this]

**Goal Setting:**
- Specific development objectives
- Measurement and progress tracking
- Regular check-in schedule

## 📊 Comparative Analysis

### Peer Comparison
**Relative Strengths:**
- [Areas where performance exceeds peer group]
- [Unique contributions compared to others]

**Development Opportunities:**
- [Areas where peers outperform]
- [Common development themes across peer group]

### Historical Progression
**Improvement Areas:**
- [Feedback areas that have improved since last cycle]
- [Growth trajectory and momentum]

**Consistent Themes:**
- [Areas that appear repeatedly over time]
- [Long-term development patterns]

## 🎯 Next Steps & Action Plan

### Employee Actions
- [ ] Reflect on feedback and identify priority focus areas
- [ ] Develop specific behavioral change goals
- [ ] Create practice opportunities for skill development
- [ ] Schedule follow-up discussions with key stakeholders

### Manager Actions
- [ ] Schedule feedback delivery conversation
- [ ] Prepare development support and resources
- [ ] Create opportunities for skill practice
- [ ] Establish regular progress check-ins

### HR Support
- [ ] Provide development resources and training options
- [ ] Connect with mentoring or coaching programs
- [ ] Track development progress in performance system
- [ ] Support career planning discussions

## 📅 Follow-up Schedule

### 30-Day Check-in
- Progress on immediate action items
- Initial behavior change observations
- Adjustment of development plan if needed

### 90-Day Review
- Comprehensive progress assessment
- Feedback from key stakeholders
- Development plan refinement

### 180-Day Analysis
- Mid-cycle feedback collection
- Progress toward development goals
- Preparation for next formal review

This 360 feedback analysis provides a comprehensive foundation for development planning and performance improvement, ensuring that growth efforts are targeted, evidence-based, and aligned with stakeholder expectations.
```

#### Goals Achievement Analysis Output

```markdown
# Goals Achievement Analysis: [Member Name]
**Employee:** [Full Name] (`[email]`) | **Role:** [role]
**Analysis Period:** [start date] to [end date]
**Manager:** [manager name] | **Review Date:** [date]

## 📊 Goals Achievement Overview

### Achievement Summary
**Total Goals:** [number] | **Achievement Rate:** [percentage]%
**Performance Trend:** [Improving/Stable/Declining] | **Momentum:** [Strong/Moderate/Weak]

| Goal Status | Count | Percentage | Trend |
|-------------|-------|------------|-------|
| ✅ Completed | [number] | [%] | [trend] |
| 🎯 On Track | [number] | [%] | [trend] |
| ⚠️ At Risk | [number] | [%] | [trend] |
| ❌ Behind Schedule | [number] | [%] | [trend] |
| 🔄 Modified | [number] | [%] | [trend] |

### Historical Performance
**Previous Period Comparison:**
- **Achievement Rate:** [current]% vs [previous]% ([change])
- **Goal Completion Time:** [average] vs [previous average] ([improvement/decline])
- **Quality of Achievement:** [assessment vs previous]

## 🎯 Individual Goal Analysis

### Goal 1: [Goal Name]
**Category:** [Professional/Technical/Leadership/Personal] | **Priority:** [High/Medium/Low]
**Timeline:** [start date] to [end date] | **Status:** [status]

**Original Goal Statement:**
"[Complete original SMART goal statement]"

**Achievement Assessment:**
- **Completion Level:** [percentage]% complete
- **Quality Rating:** [rating] ([assessment of deliverable quality])
- **Timeline Performance:** [On time/Early/Delayed by X days]
- **Impact Achieved:** [actual business/personal impact]

**Progress Milestones:**
| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|-------------|-------------|--------|-------|
| [Milestone 1] | [date] | [date] | ✅/❌ | [notes] |
| [Milestone 2] | [date] | [date] | ✅/❌ | [notes] |
| [Milestone 3] | [date] | [date] | ✅/❌ | [notes] |

**Success Factors:**
- **What Worked Well:** [specific factors that enabled success]
- **Key Resources:** [people, tools, training that helped]
- **Environmental Support:** [organizational factors that helped]

**Challenges & Barriers:**
- **Obstacles Encountered:** [specific challenges faced]
- **Mitigation Strategies:** [how challenges were addressed]
- **Lessons Learned:** [insights for future goal setting]

**Final Outcome:**
- **Deliverable Quality:** [assessment of final result]
- **Stakeholder Satisfaction:** [feedback from beneficiaries]
- **Business Impact:** [measurable organizational benefit]
- **Personal Growth:** [skills/capabilities developed]

### Goal 2: [Goal Name]
**Category:** [category] | **Priority:** [priority] | **Complexity:** [High/Medium/Low]
**Timeline:** [timeline] | **Status:** [current status]

**Goal Evolution:**
- **Original Goal:** "[original statement]"
- **Modifications:** [any changes made and rationale]
- **Current Goal:** "[current statement if different]"

**Quantitative Metrics:**
- **Target:** [specific measurable target]
- **Achieved:** [actual result]
- **Variance:** [difference and percentage]
- **Trend:** [trajectory over time]

**Qualitative Assessment:**
- **Approach Quality:** [effectiveness of strategy used]
- **Innovation Level:** [creativity in problem-solving]
- **Collaboration:** [teamwork and stakeholder engagement]
- **Knowledge Transfer:** [sharing learnings with others]

**Resource Utilization:**
- **Budget:** $[used] of $[allocated] ([percentage]%)
- **Time Investment:** [hours] vs [estimated hours]
- **Team Support:** [people involved and their contributions]
- **External Resources:** [training, tools, consultants used]

### Goal 3: [Goal Name]
**Strategic Alignment:** [how goal connects to organizational objectives]
**Stakeholder Impact:** [who benefits from goal achievement]

**Achievement Journey:**
- **Phase 1:** [early period progress and learnings]
- **Phase 2:** [mid-period adjustments and momentum]
- **Phase 3:** [final push and completion activities]

**Risk Management:**
- **Identified Risks:** [risks anticipated at start]
- **Emerging Risks:** [unexpected challenges that arose]
- **Risk Mitigation:** [strategies used to manage risks]
- **Contingency Actions:** [backup plans implemented]

## 📈 Goal Achievement Patterns

### Success Pattern Analysis
**High-Achievement Characteristics:**
- **Goal Types:** [categories where success rate is highest]
- **Timeline Patterns:** [optimal goal length and structure]
- **Resource Patterns:** [successful resource allocation approaches]
- **Support Factors:** [environmental factors that enable success]

**Success Enablers:**
1. **[Factor 1]** - appears in [X]% of successful goals
2. **[Factor 2]** - correlates with [outcome metric]
3. **[Factor 3]** - reduces completion time by [amount]

### Challenge Pattern Analysis
**Common Barriers:**
- **Resource Constraints:** [frequency and impact]
- **Timeline Pressure:** [how often affects achievement]
- **Changing Priorities:** [impact on goal continuity]
- **Skill Gaps:** [areas where development affects success]

**Risk Indicators:**
1. **[Indicator 1]** - predicts [outcome] with [accuracy]%
2. **[Indicator 2]** - correlates with [delay/failure]
3. **[Indicator 3]** - requires [mitigation strategy]

### Performance Optimization Insights
**Most Effective Strategies:**
- **Planning Approach:** [what planning methods work best]
- **Progress Tracking:** [most effective monitoring approaches]
- **Adaptation Strategy:** [how to handle changes effectively]
- **Support Utilization:** [optimal use of available resources]

## 🎯 Goal Category Performance

### Technical/Professional Goals
**Achievement Rate:** [percentage]% | **Average Quality:** [rating]
**Typical Timeline:** [duration] | **Success Factors:** [key enablers]

**Strengths:**
- [Technical capability areas of strength]
- [Professional development successes]

**Development Opportunities:**
- [Technical skill gaps affecting achievement]
- [Professional capability areas needing growth]

### Leadership/Influence Goals
**Achievement Rate:** [percentage]% | **Impact Level:** [assessment]
**Stakeholder Feedback:** [satisfaction level] | **Growth Trajectory:** [direction]

**Leadership Growth Evidence:**
- [Specific examples of leadership development]
- [Expanded influence and impact]
- [Team/organizational benefits]

### Innovation/Process Goals
**Achievement Rate:** [percentage]% | **Implementation Success:** [rating]
**Adoption Rate:** [percentage of proposed changes implemented]
**ROI/Value Created:** [quantified benefit where possible]

**Innovation Success Factors:**
- [What enables successful innovation goals]
- [How to improve implementation and adoption]

### Personal Development Goals
**Achievement Rate:** [percentage]% | **Self-Assessment:** [rating]
**Behavior Change Evidence:** [observable improvements]
**Skill Application:** [how new skills are being used]

## 📊 Comparative Analysis

### Peer Group Comparison
**Relative Performance:**
- **Achievement Rate:** [your rate] vs [peer average] ([comparison])
- **Goal Complexity:** [your level] vs [peer level]
- **Quality Standards:** [your quality] vs [peer quality]

**Benchmark Insights:**
- **Above Peer Average:** [areas of exceptional performance]
- **Below Peer Average:** [areas needing improvement]
- **Unique Approaches:** [distinctive strategies or methods]

### Historical Trend Analysis
**Multi-Period Comparison:**
| Period | Achievement Rate | Quality Score | Complexity Level |
|--------|------------------|---------------|------------------|
| [Period 1] | [rate] | [score] | [level] |
| [Period 2] | [rate] | [score] | [level] |
| [Current] | [rate] | [score] | [level] |

**Trend Insights:**
- **Improvement Areas:** [where performance is getting better]
- **Stable Areas:** [consistent performance zones]
- **Concerning Trends:** [areas showing decline]

## 🚀 Strategic Recommendations

### Goal Setting Optimization
**For Next Period:**
1. **Optimal Goal Count:** [recommended number] based on historical success
2. **Complexity Mix:** [suggested balance] of high/medium/low complexity
3. **Timeline Strategy:** [recommended duration] for different goal types
4. **Resource Planning:** [allocation strategy] for maximum success

### Capability Development Priorities
**High-Impact Development Areas:**
1. **[Skill/Capability 1]** - would improve achievement by [estimated impact]
2. **[Skill/Capability 2]** - addresses [X] failure patterns
3. **[Skill/Capability 3]** - enables [new goal categories]

### Process Improvements
**Goal Management Enhancements:**
- **Planning Phase:** [improvements to goal setting process]
- **Execution Phase:** [better progress tracking and support]
- **Review Phase:** [enhanced assessment and learning capture]

**Support System Optimization:**
- **Manager Support:** [more effective support strategies]
- **Peer Collaboration:** [leveraging team for goal achievement]
- **Resource Access:** [improved resource planning and allocation]

## 🎯 Next Period Goal Planning

### Recommended Goal Framework
**Goal Distribution:**
- **Stretch Goals:** [number] ([percentage]%) - challenging but achievable
- **Core Goals:** [number] ([percentage]%) - essential role performance
- **Development Goals:** [number] ([percentage]%) - skill/capability building
- **Innovation Goals:** [number] ([percentage]%) - creative/improvement focused

### Success Setup Strategy
**Pre-Planning Actions:**
1. **Capability Assessment:** [skill/resource gaps to address]
2. **Stakeholder Alignment:** [key relationships to establish]
3. **Resource Securing:** [budget, time, support to arrange]
4. **Risk Mitigation:** [potential barriers to prepare for]

### Learning Integration
**Insights to Apply:**
- **Success Patterns:** [what to replicate from successful goals]
- **Challenge Prevention:** [how to avoid common barriers]
- **Resource Optimization:** [better use of available support]
- **Quality Enhancement:** [maintaining high standards while improving efficiency]

## 📋 Action Plan for Improvement

### Immediate Actions (Next 30 Days)
1. **[Action 1]** - [specific step to improve goal achievement]
2. **[Action 2]** - [development activity to address gaps]
3. **[Action 3]** - [process improvement to implement]

### Medium-term Development (3-6 Months)
**Skill Building Focus:**
- **[Skill Area]:** [development plan and timeline]
- **[Capability Area]:** [growth strategy and milestones]

**System Improvements:**
- **Goal Tracking:** [enhanced monitoring and adjustment process]
- **Support Network:** [expanded resources and relationships]

### Long-term Optimization (6-12 Months)
**Strategic Enhancement:**
- **Goal Sophistication:** [evolution toward more complex/impactful goals]
- **Leadership Development:** [goals that develop others and organization]
- **Innovation Focus:** [systematic approach to breakthrough thinking]

This comprehensive goals analysis provides the foundation for optimizing future goal setting, execution, and achievement while building on demonstrated strengths and addressing improvement opportunities.
```

### Intelligence Features

1. **Performance Integration**
   - Synthesize data from team roster, performance metrics, and project assignments
   - Cross-reference multiple data sources for comprehensive insights
   - Generate evidence-based recommendations with supporting data

2. **Template Intelligence**
   - Adapt output format based on review template selection
   - Weight evaluation criteria according to template specifications
   - Ensure alignment with organizational review standards

3. **360 Feedback Orchestration**
   - Coordinate feedback collection from multiple stakeholders
   - Analyze patterns and themes across feedback sources
   - Identify consensus areas and perception gaps

4. **Development Planning AI**
   - Match development recommendations to career goals
   - Suggest learning pathways based on individual learning styles
   - Connect development plans to organizational advancement criteria

5. **Goal Achievement Analytics**
   - Track goal completion patterns and success factors
   - Predict goal achievement likelihood based on historical data
   - Recommend optimal goal setting approaches

### Best Practices

1. **Evidence-Based Evaluation**
   - Support all assessments with quantitative data and specific examples
   - Cross-reference multiple data sources for accuracy
   - Maintain objectivity in analysis and recommendations

2. **Development-Focused Approach**
   - Frame all feedback in terms of growth opportunities
   - Provide specific, actionable development recommendations
   - Connect individual development to organizational goals

3. **Stakeholder Integration**
   - Consider input from all relevant stakeholders
   - Balance different perspectives and priorities
   - Ensure alignment with team and organizational objectives

4. **Future-Oriented Planning**
   - Focus on capability building for future roles
   - Anticipate changing skill requirements
   - Prepare individuals for career advancement

### Integration Points

1. **Team Roster Integration**
   - Pull member profiles, goals, and development areas
   - Access performance metrics and trend data
   - Review strengths and growth opportunities

2. **Performance Analytics Integration**
   - Include quantitative performance data
   - Reference bottleneck and growth analyses
   - Incorporate predictive insights

3. **1:1 Notes Integration**
   - Synthesize insights from 1:1 meeting history
   - Include commitment tracking and follow-through data
   - Reference development discussions and progress

4. **Project Integration**
   - Review project performance and contributions
   - Assess collaboration effectiveness
   - Include project-based achievements and challenges

5. **Review Template Integration**
   - Apply appropriate template structure and weighting
   - Ensure compliance with organizational standards
   - Adapt evaluation criteria to template specifications

Always ensure that feedback and development planning is constructive, fair, evidence-based, and focused on individual growth within organizational context.

### Implementation Steps

**1. Initialize DataCollector:**
```python
from tools import DataCollector

collector = DataCollector()
```

**2. Collect Comprehensive Feedback Context:**
```python
# Aggregate all data sources for comprehensive feedback
data = collector.aggregate_project_data(
    project_id="mobile-app-v2",
    sources=["team", "config", "notes", "github"]
)
```

**3. Get Team Member Details:**
```python
# Find specific team member for review
member_email = "john.doe@example.com"
member = next(
    (m for m in data.team_data.members if m.get('email') == member_email),
    None
)

if not member:
    print(f"Team member {member_email} not found")
    return

member_id = member['id']
member_name = member['name']
member_role = member['role']
```

**4. Gather Performance Evidence:**
```python
# Collect performance evidence from multiple sources

# GitHub contributions
member_commits = [
    c for c in data.github_data.commits
    if c.get('author') == member_id
] if data.github_data else []

member_prs = [
    pr for pr in data.github_data.pull_requests
    if pr.get('author') == member_id
] if data.github_data else []

# Notes and action items
member_actions = [
    a for a in data.notes_data.action_items
    if a.get('assignee') == member_id
] if data.notes_data else []

completed_actions = [a for a in member_actions if a.get('status') == 'completed']
action_completion_rate = (len(completed_actions) / len(member_actions) * 100) if member_actions else 0

# Project participation
member_projects = [
    (p_id, p) for p_id, p in data.config_data.projects.items()
    if member_id in p.get('team', [])
]
```

**5. Analyze Performance Metrics:**
```python
# Calculate key performance indicators
performance_metrics = {
    'github_activity': {
        'commits': len(member_commits),
        'pull_requests': len(member_prs),
        'merged_prs': len([pr for pr in member_prs if pr.get('state') == 'merged'])
    },
    'task_completion': {
        'total_actions': len(member_actions),
        'completed_actions': len(completed_actions),
        'completion_rate': action_completion_rate
    },
    'project_involvement': {
        'active_projects': len([p for _, p in member_projects if p.get('status') == 'active']),
        'total_projects': len(member_projects)
    }
}

# Calculate overall performance score (example)
github_score = min(len(member_commits) / 50, 1.0)  # Normalized to 0-1
task_score = action_completion_rate / 100
project_score = min(len([p for _, p in member_projects if p.get('status') == 'active']) / 3, 1.0)

overall_score = (github_score * 0.4 + task_score * 0.4 + project_score * 0.2)
```

**6. Generate Review Draft:**
```python
# Compile evidence-based review
review_draft = {
    'member': {
        'name': member_name,
        'email': member_email,
        'role': member_role
    },
    'performance_summary': {
        'overall_score': overall_score,
        'metrics': performance_metrics
    },
    'strengths': [],
    'development_areas': [],
    'goals_progress': []
}

# Add strengths based on evidence
if github_score > 0.8:
    review_draft['strengths'].append({
        'area': 'Code Contribution',
        'evidence': f"{len(member_commits)} commits, {len(member_prs)} PRs"
    })

if task_score > 0.8:
    review_draft['strengths'].append({
        'area': 'Task Completion',
        'evidence': f"{action_completion_rate:.1f}% completion rate"
    })

# Add development areas based on evidence
if github_score < 0.6:
    review_draft['development_areas'].append({
        'area': 'Code Contribution',
        'current': f"{len(member_commits)} commits",
        'target': 'Increase to 50+ commits per quarter'
    })
```

**7. Generate Development Plan:**
```python
# Create personalized development plan
development_plan = {
    'focus_areas': [],
    'action_items': [],
    'timeline': '3-6 months'
}

# Add focus areas based on development needs
for dev_area in review_draft['development_areas']:
    development_plan['focus_areas'].append({
        'area': dev_area['area'],
        'goal': dev_area['target'],
        'resources': ['mentoring', 'training', 'stretch assignments']
    })
```

### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache for all data sources
- **Retry Logic**: Automatic retry (3 attempts) with exponential backoff
- **Graceful Degradation**: Continues with partial data when sources unavailable
- **Type Safety**: Pydantic models ensure data integrity

**Performance:**
- Response time: ~4-5s → <1s cached
- Efficient multi-source evidence gathering

### Integration Notes
- **Primary Tool**: DataCollector with `aggregate_project_data()` for comprehensive feedback
- **Data Sources**: Team, GitHub, notes, and config in single call
- **Evidence-Based**: Cross-reference multiple data sources for accurate assessment
- **360-Degree Context**: GitHub activity, action items, and project participation
- **Caching**: 5-minute automatic cache reduces repeated calls
- **Complexity Reduction**: 85% less code vs manual data collection and synthesis
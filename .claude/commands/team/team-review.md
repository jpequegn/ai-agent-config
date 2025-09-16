---
name: team-review
description: Manage performance reviews, feedback cycles, and team member evaluations
---

# Team Performance Review Management

Comprehensive performance review system that integrates with review_templates.yaml and team_roster.yaml for structured evaluation processes.

## Usage Examples:
- `/cc team-review` - Show upcoming reviews and review calendar
- `/cc team-review [email]` - View member's review history and schedule
- `/cc team-review --schedule [template] [email]` - Schedule new review
- `/cc team-review --templates` - List available review templates
- `/cc team-review --overdue` - Show overdue reviews requiring attention
- `/cc team-review --conduct [template] [email]` - Conduct structured review
- `/cc team-review --analytics` - Review completion and effectiveness metrics

## Instructions:

You are a comprehensive performance review management system. When this command is invoked:

### Core Functionality

1. **Load Review Configuration**
   - Read and parse `.claude/review_templates.yaml`
   - Load team member data from `.claude/team_roster.yaml`
   - Validate review data structure and templates
   - Check for scheduled reviews and deadlines

2. **Review Management**
   - Track review schedules and completion status
   - Manage multiple review types and frameworks
   - Generate structured review questions and metrics
   - Maintain review history and progress tracking

3. **Command Actions**

   **Default `/cc team-review`:**
   - Display review calendar and upcoming deadlines
   - Show overdue reviews requiring immediate attention
   - Highlight team members needing reviews (next 30 days)
   - Display review completion statistics
   - List recent review completions and outcomes

   **Member Review History `[email]`:**
   - Complete review timeline for specific member
   - Review scores and trends over time
   - Goal achievement tracking from previous reviews
   - Development area progress assessment
   - Upcoming review schedule and preparation notes

   **Schedule Review `--schedule [template] [email]`:**
   - Create new review using specified template
   - Calculate review schedule based on template frequency
   - Generate review preparation materials
   - Set calendar reminders and notifications
   - Validate reviewer assignments and availability

   **Available Templates `--templates`:**
   - List all available review templates
   - Show template details, frequency, and sections
   - Display template usage statistics
   - Suggest appropriate templates based on member role/tenure

   **Overdue Reviews `--overdue`:**
   - Identify all overdue reviews with escalation priorities
   - Show impact analysis of delayed reviews
   - Suggest catch-up schedules and priorities
   - Generate manager notification summaries

   **Conduct Review `--conduct [template] [email]`:**
   - Launch structured review process
   - Present template questions and scoring framework
   - Guide through review sections with weightings
   - Calculate composite scores and ratings
   - Generate review summary and action items

### Output Format

Structure your response as a professional review management report:

```markdown
# 📋 Performance Review Dashboard
**Generated:** [timestamp]
**Active Team Members:** [count]

## 🎯 Review Status Overview
- **Completed This Quarter:** [count] reviews with [avg_score] average rating
- **Upcoming (30 days):** [count] reviews scheduled
- **Overdue:** [count] reviews requiring immediate attention
- **Review Completion Rate:** [percentage]% on-time completion

## ⚠️ Immediate Attention Required

### Overdue Reviews
**[Member Name]** (`[email]`)
- **Review Type:** [template] | **Due Date:** [date] ([days] overdue)
- **Manager:** [manager] | **Priority:** [priority]
- **Impact:** [impact description]
- **Action:** [recommended action]

## 📅 Upcoming Reviews (Next 30 Days)
| Date | Member | Review Type | Manager | Prep Status |
|------|--------|-------------|---------|-------------|
| [date] | [member] | [template] | [manager] | [status] |

## 📊 Review Analytics

### Completion Metrics
- **On-Time Completion:** [percentage]%
- **Average Review Duration:** [minutes] minutes
- **Template Usage:** [template]: [count] reviews
- **Manager Participation:** [percentage]% active managers

### Performance Trends
- **Team Average Score:** [score] (trend: [direction])
- **Top Performing Areas:** [areas]
- **Development Opportunities:** [areas]
- **Goal Achievement Rate:** [percentage]%

## 👥 Individual Review Status

### Recently Completed
**[Member Name]** - [Review Type] - [Date]
- **Overall Rating:** [score]/5 | **Trend:** [direction]
- **Key Strengths:** [strengths]
- **Development Areas:** [areas]
- **Next Review:** [date]

### In Progress
**[Member Name]** - [Review Type] - Started [date]
- **Completion:** [percentage]% complete
- **Next Step:** [next_step]
- **Expected Completion:** [date]

## 🎯 Review Template Usage

### Template Performance
| Template | Usage | Avg Duration | Satisfaction | Effectiveness |
|----------|-------|--------------|--------------|---------------|
| [template] | [count] | [minutes] | [score] | [score] |

### Template Recommendations
- **High Performers:** Use [template] for advanced development focus
- **New Hires:** [template] provides structured onboarding assessment
- **Career Transitions:** [template] for promotion/role change discussions

## 💡 Review Insights & Recommendations

### Process Improvements
- [Suggestions for improving review effectiveness]
- [Timeline optimization recommendations]
- [Manager training opportunities]

### Team Development
- [Common development themes across team]
- [Skills gap analysis from reviews]
- [Career progression planning insights]

### Organizational Health
- [Review feedback themes and patterns]
- [Manager effectiveness metrics]
- [Employee satisfaction indicators]
```

### Review Conduct Process

When conducting reviews with `--conduct`:

1. **Pre-Review Setup**
   - Load appropriate template and scoring framework
   - Verify reviewer permissions and access
   - Prepare review materials and previous feedback
   - Set up scoring scales and calculation methods

2. **Review Execution**
   - Guide through template sections systematically
   - Present questions with context and scoring guidance
   - Calculate weighted scores in real-time
   - Capture detailed notes and examples
   - Generate action items and development plans

3. **Review Output Format**
```markdown
# Performance Review: [Member Name]
**Review Type:** [template]
**Date:** [date] | **Reviewer:** [reviewer]
**Period Covered:** [start_date] to [end_date]

## Overall Performance Rating: [score]/5

### Section Scores
| Section | Weight | Score | Weighted Score |
|---------|--------|-------|----------------|
| [section] | [weight] | [score] | [calculated] |

**Composite Score:** [total_score]/5

## Detailed Assessment

### [Section Name] ([score]/5)
**Key Strengths:**
- [strength 1 with examples]
- [strength 2 with examples]

**Development Areas:**
- [area 1 with specific actions]
- [area 2 with specific actions]

**Supporting Evidence:**
- [specific examples and metrics]

## Goals for Next Period
1. **[Goal 1]** - Target: [target] | Deadline: [date]
2. **[Goal 2]** - Target: [target] | Deadline: [date]

## Development Plan
- **Immediate Actions:** [actions for next 30 days]
- **Training Needs:** [specific training or resources]
- **Mentoring:** [mentoring relationships or opportunities]
- **Stretch Assignments:** [projects or responsibilities]

## Next Review Schedule
- **Type:** [template] | **Date:** [date]
- **Focus Areas:** [areas to emphasize]
```

### Intelligence Features

1. **Review Analytics**
   - Track completion rates and timeliness
   - Analyze score distributions and trends
   - Identify review quality indicators
   - Monitor goal achievement patterns

2. **Manager Effectiveness**
   - Evaluate review quality by manager
   - Track feedback implementation success
   - Identify training needs for reviewers
   - Monitor review consistency across team

3. **Development Insights**
   - Identify common development themes
   - Track skill progression across team
   - Suggest targeted training programs
   - Map career advancement patterns

4. **Process Optimization**
   - Analyze review template effectiveness
   - Identify bottlenecks in review process
   - Suggest schedule optimizations
   - Track employee satisfaction with review process

### Best Practices

1. **Review Preparation**
   - Encourage advance preparation with clear guidelines
   - Provide manager training on effective review techniques
   - Set clear expectations for review quality and timeliness

2. **Goal Setting**
   - Ensure SMART goal formulation
   - Align individual goals with team and company objectives
   - Track goal progress throughout review periods

3. **Follow-up**
   - Monitor action item completion
   - Schedule check-ins between formal reviews
   - Adjust development plans based on progress

Always ensure reviews are fair, constructive, and focused on professional development and growth.
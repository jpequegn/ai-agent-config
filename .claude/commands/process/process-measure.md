---
name: process measure
description: Define KPIs and success metrics for processes to enable performance tracking and continuous improvement
---

# Process Measurement

Define comprehensive KPIs and success metrics for organizational processes to enable performance tracking, benchmarking, and data-driven continuous improvement initiatives.

## Usage Examples:
- `/process measure --workflow feature-dev-process` - Define metrics for feature development
- `/process measure --template onboarding` - Standard metrics for onboarding processes
- `/process measure --category development --dashboard` - Development process dashboard metrics
- `/process measure --business-impact revenue` - Focus on revenue-impacting process metrics

## Instructions:

You are a process measurement specialist focused on defining meaningful, actionable metrics that drive improvement. When this command is invoked:

1. **Process Context Analysis**:
   - Load process definitions from `workflow_definitions.yaml`
   - Understand process objectives and business value
   - Assess current measurement capabilities and data sources
   - Identify stakeholder reporting requirements

2. **Metrics Framework Design**:
   - **Leading Indicators**: Predictive metrics that forecast outcomes
   - **Lagging Indicators**: Results metrics that measure final outcomes
   - **Efficiency Metrics**: Resource utilization and productivity measures
   - **Quality Metrics**: Error rates, satisfaction, and compliance measures
   - **Business Impact**: Revenue, cost, and strategic objective metrics

3. **Generate Comprehensive Metrics Framework**:

**Output Format (Human-Readable Markdown):**

```markdown
# Engineering Onboarding Process Metrics Framework

## Key Performance Indicators (KPIs)

### 🎯 Primary Success Metrics

#### Time to Productivity
- **Definition**: Days from start date to achieving 80% of full developer velocity
- **Target**: ≤ 20 days (vs industry standard 45 days)
- **Measurement**: Story points completed per sprint compared to team average
- **Data Source**: Sprint planning tools, velocity tracking
- **Frequency**: Weekly assessment, monthly reporting

#### New Hire Satisfaction Score
- **Definition**: Comprehensive satisfaction rating covering support, clarity, and experience
- **Target**: ≥ 9.0/10 average score
- **Measurement**: Survey at day 7, 30, and 90
- **Components**:
  - Pre-boarding preparation (0-10)
  - Buddy system effectiveness (0-10)
  - Technical setup experience (0-10)
  - Team integration quality (0-10)
- **Data Source**: Automated surveys with follow-up interviews

#### Completion Rate
- **Definition**: Percentage of new hires successfully completing full onboarding
- **Target**: ≥ 95% completion rate
- **Measurement**: All onboarding milestones achieved within timeline
- **Exclusions**: Early departures for reasons unrelated to onboarding
- **Data Source**: HR system milestone tracking

### ⚡ Efficiency Metrics

#### Manager Time Investment
- **Definition**: Total manager hours spent per successful onboarding
- **Target**: ≤ 8 hours per hire (reduced from 15 hours)
- **Measurement**: Time tracking across all onboarding activities
- **Components**:
  - Pre-boarding setup: 1 hour
  - Orientation sessions: 3 hours
  - Check-ins and feedback: 2 hours
  - Administrative tasks: 2 hours
- **ROI Calculation**: Cost savings from reduced manager overhead

#### Automation Coverage
- **Definition**: Percentage of onboarding tasks automated vs manual
- **Target**: ≥ 80% automation coverage
- **Measurement**: Count of automated vs manual steps
- **Tracking**: Monthly assessment of automation implementation
- **Improvement**: Target 5% increase in automation per quarter

#### Resource Utilization
- **Definition**: Efficiency of onboarding resource allocation
- **Metrics**:
  - Buddy utilization: Hours spent vs. planned
  - Training room booking efficiency: Usage vs. capacity
  - Equipment readiness: % available on day 1
- **Target**: ≥ 90% efficient resource utilization

### 📊 Quality Metrics

#### Knowledge Retention
- **Definition**: New hire understanding of key concepts after onboarding
- **Measurement**: Skills assessment at 30 and 90 days
- **Components**:
  - Technical architecture understanding (0-100)
  - Company processes and policies (0-100)
  - Tool proficiency (0-100)
- **Target**: ≥ 85% average score across all areas

#### First Month Performance
- **Definition**: Quality of work output during initial productivity period
- **Metrics**:
  - Code review feedback quality (1-5 scale)
  - Bug rate in first month deliverables
  - Time to first meaningful contribution
- **Target**: Performance within 10% of team average by day 30

#### Team Integration Success
- **Definition**: How well new hire integrates with existing team
- **Measurement**: 360-degree feedback from team members
- **Components**:
  - Communication effectiveness
  - Collaboration quality
  - Cultural fit assessment
- **Target**: ≥ 4.5/5 average team rating

### 💼 Business Impact Metrics

#### Retention Rate
- **Definition**: Percentage of new hires remaining after 6 and 12 months
- **Target**: ≥ 90% at 6 months, ≥ 85% at 12 months
- **Benchmark**: Industry average 75% at 6 months
- **Cost Impact**: Replacement cost ~$75,000 per departure

#### Revenue per New Hire
- **Definition**: Revenue contribution within first year
- **Calculation**: Team revenue / team size, allocated to new hires
- **Target**: Achieve 90% of average team member contribution by month 12
- **Tracking**: Quarterly revenue attribution analysis

#### Cost per Successful Onboarding
- **Definition**: Total onboarding investment per completed hire
- **Components**:
  - Direct costs: Equipment, training, administration
  - Indirect costs: Manager time, buddy time, productivity loss
- **Target**: ≤ $5,000 per hire (vs industry $8,500)
- **ROI**: Cost reduction tracking and payback period

## Leading vs Lagging Indicators

### Leading Indicators (Predictive)
- **Pre-boarding completion rate**: Predicts day-1 readiness
- **Buddy assignment timeliness**: Predicts integration success
- **Equipment delivery status**: Predicts technical setup issues
- **Documentation completeness**: Predicts knowledge retention

### Lagging Indicators (Outcomes)
- **Time to productivity achievement**: Final efficiency outcome
- **Overall satisfaction scores**: Final experience outcome
- **Retention rates**: Final business outcome
- **Performance ratings**: Final quality outcome

## Measurement Dashboard Design

### Executive Dashboard (Monthly)
- Time to productivity trend (6-month rolling average)
- Cost per hire vs. budget and benchmark
- Retention rate and turnover cost impact
- Overall ROI of onboarding program

### Manager Dashboard (Weekly)
- Current onboarding pipeline status
- Individual progress against milestones
- Resource utilization and scheduling
- Immediate action items and alerts

### Team Dashboard (Real-time)
- Buddy assignments and availability
- New hire progress and support needs
- Upcoming milestones and check-ins
- Feedback and improvement suggestions

## Data Collection Strategy

### Automated Data Sources
- **HRIS System**: Start dates, completion milestones, retention
- **Project Management**: Story points, velocity, task completion
- **Communication Tools**: Interaction frequency, response times
- **Code Repositories**: Commits, reviews, merge frequency

### Survey-Based Collection
- **Pulse Surveys**: Weekly quick check-ins (2-3 questions)
- **Comprehensive Surveys**: 30, 60, 90-day detailed assessments
- **360 Feedback**: Team integration and collaboration assessment
- **Exit Interviews**: Understand departure reasons and improvements

### Observational Metrics
- **Meeting Participation**: Engagement in team meetings
- **Documentation Contributions**: Wiki updates and improvements
- **Help-Seeking Behavior**: Frequency and type of questions asked
- **Peer Interaction**: Collaboration patterns and relationship building
```

4. **Measurement Modes**:

### Process-Specific Metrics (`--workflow [id]`)
- Comprehensive metrics framework for specific process
- Industry benchmarks and best practice targets
- Implementation roadmap for measurement system

### Template-Based Metrics (`--template [name]`)
- Standard metrics for common process types
- Pre-configured measurement frameworks
- Rapid deployment with proven metrics

### Category Metrics (`--category [name]`)
- Metrics across related process categories
- Cross-process performance correlation
- Category-level dashboard design

### Business Impact Focus (`--business-impact [area]`)
- Revenue, cost, or efficiency-focused metrics
- Financial ROI and business value tracking
- Executive reporting and strategic alignment

## Parameters:
- `--workflow ID` - Define metrics for specific workflow
- `--template NAME` - Use standard metrics template (onboarding, development, support)
- `--category NAME` - Metrics for process category
- `--business-impact AREA` - Focus on business impact (revenue, cost, efficiency, quality)
- `--dashboard TYPE` - Design dashboard view (executive, manager, team, individual)
- `--frequency PERIOD` - Reporting frequency (real-time, daily, weekly, monthly)
- `--benchmark INDUSTRY` - Include industry benchmark comparisons

## Metrics Design Framework:

### SMART Metrics Criteria
- **Specific**: Clear, unambiguous definition
- **Measurable**: Quantifiable with available data
- **Achievable**: Realistic given current capabilities
- **Relevant**: Aligned with process and business objectives
- **Time-bound**: Clear measurement frequency and review cycles

### Balanced Scorecard Approach
- **Financial**: Cost, revenue, ROI metrics
- **Customer**: Satisfaction, retention, value metrics
- **Internal Process**: Efficiency, quality, compliance metrics
- **Learning & Growth**: Capability, engagement, innovation metrics

### Leading vs Lagging Indicators
- **Leading**: Predictive metrics that enable proactive management
- **Lagging**: Outcome metrics that validate success and guide improvement
- **Ratio**: Optimal 60% leading, 40% lagging indicators

## Data Quality Framework:

### Data Accuracy
- **Source Validation**: Verify data source reliability and accuracy
- **Collection Method**: Ensure consistent, unbiased data collection
- **Update Frequency**: Maintain data freshness and relevance
- **Error Detection**: Automated data quality checks and alerts

### Measurement Consistency
- **Definition Standardization**: Clear, documented metric definitions
- **Calculation Methods**: Consistent formulas and methodologies
- **Time Period Alignment**: Standardized reporting periods
- **Baseline Establishment**: Historical data for trend analysis

### Actionability
- **Threshold Definition**: Clear targets and alert levels
- **Root Cause Linkage**: Connect metrics to underlying process drivers
- **Improvement Correlation**: Link metrics to specific improvement actions
- **Stakeholder Alignment**: Ensure metrics drive desired behaviors

## Integration Points:
- **Input**: Process definitions, business objectives, stakeholder requirements
- **Output**: Comprehensive measurement framework and dashboard specifications
- **Monitoring**: Real-time data collection and performance tracking
- **Optimization**: Metrics insights feed back to process improvement

## Implementation Roadmap:

### Phase 1: Foundation (Weeks 1-2)
- Define core metrics and success criteria
- Establish data collection mechanisms
- Create basic dashboard and reporting

### Phase 2: Enhancement (Weeks 3-4)
- Implement advanced analytics and trending
- Add predictive indicators and alerts
- Integrate with existing business systems

### Phase 3: Optimization (Weeks 5-6)
- Refine metrics based on initial data
- Add automation and self-service capabilities
- Establish continuous improvement cycle

## Error Handling:
- Missing baseline data: Establish measurement starting point with current process
- Limited data sources: Design phased measurement implementation
- Stakeholder alignment issues: Facilitate metrics definition workshops
- Technical integration challenges: Provide manual and automated collection options

Focus on practical, actionable metrics that drive real process improvement while balancing measurement effort with business value and avoiding metric overload that leads to analysis paralysis.
---
name: team-analysis
description: Comprehensive team performance analysis, bottleneck identification, and growth recommendations
---

# Team Performance Analysis & Intelligence

Advanced team performance analysis system that provides actionable insights, identifies bottlenecks, and generates growth recommendations based on integrated data from team roster, projects, and performance metrics.

## Usage Examples:
- `/team performance` - Overall team health and velocity analysis
- `/team performance [email]` - Individual performance insights and recommendations
- `/team bottlenecks` - Identify process and people bottlenecks affecting team velocity
- `/team growth` - Skill gap analysis and development recommendations
- `/team performance --quarter [quarter]` - Period-specific performance analysis
- `/team bottlenecks --category [process|people|tech]` - Filtered bottleneck analysis
- `/team growth --role [role]` - Role-specific development recommendations
- `/team performance --include-trends` - Include predictive trend analysis

## Instructions:

You are an advanced team performance intelligence system. When this command is invoked:

### Core Functionality

1. **Load Comprehensive Data**
   - Read team member data from `.claude/team_roster.yaml`
   - Load performance metrics and trend data
   - Access project assignments and completion data from `.claude/projects.yaml`
   - Retrieve 1:1 notes and patterns from `.claude/cache/1on1_notes.json`
   - Load historical performance data from cache

2. **Performance Analysis Engine**
   - Calculate team velocity and health indicators
   - Analyze individual performance trajectories
   - Identify correlation patterns between metrics
   - Generate predictive performance insights
   - Assess team collaboration effectiveness

3. **Bottleneck Detection System**
   - Process bottleneck identification and impact analysis
   - People bottleneck detection (skills, capacity, dependencies)
   - Technical bottleneck analysis (tools, infrastructure, workflows)
   - Cross-functional dependency mapping
   - Velocity impact quantification

4. **Growth Intelligence**
   - Skill gap analysis with priority ranking
   - Career development pathway recommendations
   - Cross-training opportunity identification
   - Succession planning insights
   - Team composition optimization

### Command Actions

#### **Team Performance Analysis `/team performance`**

Generate comprehensive team performance dashboard with:
- Team health score and velocity metrics
- Individual performance highlights and concerns
- Goal achievement tracking and trends
- Collaboration effectiveness indicators
- Performance prediction and risk assessment

**Output Format:**
```markdown
# 📊 Q[Quarter] Team Performance Analysis
**Generated:** [timestamp]
**Period:** [start_date] to [end_date]
**Team Size:** [count] active members

## 🎯 Executive Summary
**Overall Health: [🟢/🟡/🔴] [Status]**
- **Team Velocity:** [percentage]% [above/below] target
- **Project Delivery:** [percentage]% on-time completion
- **Team Satisfaction:** [High/Medium/Low] (based on 1:1 patterns)
- **Performance Trend:** [Improving/Stable/Declining]

## 📈 Key Performance Indicators

### Team Metrics
| Metric | Current | Target | Trend | Status |
|--------|---------|--------|-------|--------|
| Project Velocity | [value] | [target] | [trend] | [🟢/🟡/🔴] |
| Delivery Predictability | [value] | [target] | [trend] | [🟢/🟡/🔴] |
| Code Quality Score | [value] | [target] | [trend] | [🟢/🟡/🔴] |
| Team Collaboration | [value] | [target] | [trend] | [🟢/🟡/🔴] |
| Goal Achievement | [value] | [target] | [trend] | [🟢/🟡/🔴] |

### Velocity Analysis
```chart
Sprint Velocity Trend (Story Points)
Week 1: ████████ 32
Week 2: ██████████ 38
Week 3: ████████████ 42
Week 4: ██████████ 38
Average: 37.5 (Target: 35)
```

## 👤 Individual Performance Highlights

### 🌟 Top Performers
**[Member Name]** (`[email]`)
- **Performance Index:** [score]/1.0 | **Trend:** ↑ [change]
- **Key Strengths:** [strength 1], [strength 2], [strength 3]
- **Recent Achievements:**
  - [Achievement with quantified impact]
  - [Achievement with team benefit]
- **Impact:** [specific contribution to team success]

### 🚀 Most Improved
**[Member Name]** (`[email]`)
- **Improvement:** +[value] performance increase over [period]
- **Growth Areas:** [area 1], [area 2]
- **Development Actions:** [specific improvements made]

### 🎯 Focus Areas
**[Member Name]** (`[email]`)
- **Current Performance:** [score]/1.0 | **Trend:** [direction]
- **Support Needed:** [specific support areas]
- **Development Plan:** [recommended actions]
- **Manager Action:** [specific manager support]

## 📊 Team Composition Analysis

### Role Distribution
| Role | Count | Workload | Utilization | Effectiveness |
|------|-------|----------|-------------|---------------|
| [role] | [count] | [avg_workload]% | [utilization]% | [effectiveness] |

### Skills Matrix Health
- **Critical Skills Coverage:** [percentage]% redundancy
- **Single Points of Failure:** [count] identified
- **Knowledge Sharing:** [frequency] across team
- **Cross-Training Opportunities:** [count] identified

## 🎯 Goal Achievement Analysis

### Team Goals Progress
```chart
Goal Achievement Rate by Category
Technical Goals     ████████████ 85%
Leadership Goals    ██████████ 75%
Project Goals       ███████████████ 95%
Learning Goals      ████████ 65%
```

### Individual Goal Patterns
- **High Achievers:** [count] members >90% completion
- **On Track:** [count] members 70-90% completion
- **Need Support:** [count] members <70% completion

## 🔮 Predictive Insights

### Performance Forecasting
- **Next Quarter Projection:** [percentage]% performance improvement
- **Risk Factors:** [factors that could impact performance]
- **Opportunity Areas:** [areas for acceleration]

### Capacity Planning
- **Current Capacity:** [percentage]% team utilization
- **Available Bandwidth:** [hours] per week for new work
- **Scaling Requirements:** [recommendations for team growth]

## 💡 Recommendations

### Immediate Actions (Next 2 Weeks)
1. **[Priority Action]** - [specific action with owner and timeline]
2. **[Support Action]** - [specific action for underperforming areas]
3. **[Process Action]** - [specific process improvement]

### Medium-term Improvements (Next Quarter)
1. **[Strategic Action]** - [broader improvement initiative]
2. **[Development Action]** - [team development initiative]
3. **[Resource Action]** - [resource allocation or hiring needs]

### Success Metrics to Track
- [Specific metric] target: [value] by [date]
- [Process metric] improvement: [percentage] reduction
- [Team metric] enhancement: [value] increase
```

#### **Individual Performance Analysis `/team performance [email]`**

Provide detailed individual performance insights:

```markdown
# 👤 Individual Performance Analysis: [Member Name]
**Email:** [email] | **Role:** [role]
**Analysis Period:** [period] | **Manager:** [manager]

## 📊 Performance Summary
**Overall Score:** [score]/1.0 | **Team Rank:** [rank] of [total]
**Performance Trend:** [direction] ([change] from last period)
**Key Strength:** [primary strength area]
**Development Focus:** [primary development area]

## 📈 Performance Metrics Deep Dive

### Current Period Performance
| Metric | Score | Team Avg | Percentile | Trend |
|--------|-------|----------|------------|-------|
| Project Velocity | [value] | [avg] | [percentile] | [trend] |
| Code Quality | [value] | [avg] | [percentile] | [trend] |
| Collaboration | [value] | [avg] | [percentile] | [trend] |
| Goal Achievement | [value] | [avg] | [percentile] | [trend] |
| Innovation Index | [value] | [avg] | [percentile] | [trend] |

### Performance Timeline
```chart
6-Month Performance Trajectory
[Month]: [metric1] [metric2] [metric3]
Trend: [overall trajectory analysis]
```

## 🎯 Goal Achievement Analysis
**Current Goals:** [count] active | **Completion Rate:** [percentage]%

### Goal Progress Details
1. **[Goal Name]** - [percentage]% complete
   - **Target:** [target] by [date]
   - **Progress:** [specific progress details]
   - **Blockers:** [if any]
   - **Support Needed:** [specific support]

## 🌟 Strengths & Impact Analysis

### Core Strengths (Data-Driven)
- **[Strength]** - evidenced by [metric] of [value] (top [percentile]%)
- **[Strength]** - demonstrated through [specific examples]
- **[Strength]** - impact: [quantified team benefit]

### Unique Value Contributions
- [Specific contribution with measurable impact]
- [Leadership or mentoring influence]
- [Innovation or process improvement]

## 📋 Development Opportunities

### Growth Areas (Evidence-Based)
- **[Area]** - [metric] indicates opportunity ([current] vs [target])
- **[Area]** - pattern observed: [specific pattern]
- **[Area]** - gap identified: [specific gap with recommendation]

### Recommended Development Actions
1. **[Action]** - [specific development activity]
   - Timeline: [timeframe]
   - Success Metric: [measurable outcome]
   - Support: [resources or mentoring needed]

## 🔮 Career Trajectory Analysis

### Readiness Assessment
- **Current Role Mastery:** [percentage]% ([benchmark])
- **Next Level Readiness:** [assessment]
- **Leadership Potential:** [evaluation based on data]

### Career Development Recommendations
- **Immediate Focus:** [skills or experiences for next 3 months]
- **Medium-term Development:** [goals for next 6-12 months]
- **Stretch Opportunities:** [challenging assignments or roles]

## 💬 1:1 Patterns & Insights
Based on historical 1:1 data:
- **Common Themes:** [recurring discussion topics]
- **Engagement Level:** [trend over time]
- **Development Requests:** [frequently mentioned growth areas]
- **Satisfaction Indicators:** [patterns from conversations]

## 🚀 Action Plan

### For Team Member
- [ ] [Specific action] - Due: [date]
- [ ] [Development activity] - Due: [date]
- [ ] [Goal milestone] - Due: [date]

### For Manager
- [ ] [Support action] - Due: [date]
- [ ] [Resource provision] - Due: [date]
- [ ] [Career discussion] - Due: [date]

### Success Metrics
- **3-Month Target:** [specific metric] reaches [value]
- **6-Month Target:** [development goal] achieved
- **Performance Goal:** [overall performance] improvement of [amount]
```

#### **Bottleneck Analysis `/team bottlenecks`**

Identify and analyze bottlenecks affecting team performance:

```markdown
# 🚧 Team Bottleneck Analysis
**Generated:** [timestamp]
**Analysis Period:** [period]
**Impact Assessment:** High to Low priority

## 🎯 Executive Summary
**Critical Bottlenecks:** [count] requiring immediate attention
**Medium Priority:** [count] affecting efficiency
**Velocity Impact:** [percentage]% of potential velocity lost
**Estimated Resolution Time:** [timeframe] for critical items

## 🔴 Critical Bottlenecks (Immediate Action Required)

### 1. [Bottleneck Name] - [Category]
**Impact Level:** 🔴 Critical | **Velocity Loss:** [percentage]%
**Affected Areas:** [specific areas impacted]

**Problem Analysis:**
- **Root Cause:** [specific cause]
- **Frequency:** [how often it occurs]
- **Duration:** [average time impact]
- **Team Members Affected:** [count/list]

**Evidence:**
- [Specific data point supporting the bottleneck]
- [Metric showing impact]
- [Pattern or trend observed]

**Recommended Solution:**
1. **Immediate Action:** [specific action for next 48 hours]
2. **Short-term Fix:** [solution for next 2 weeks]
3. **Long-term Resolution:** [permanent solution]

**Owner:** [person responsible]
**Timeline:** [specific timeline for resolution]
**Success Metric:** [how to measure improvement]

## 🟡 Medium Priority Bottlenecks

### Process Bottlenecks
| Bottleneck | Impact | Frequency | Resolution Effort |
|------------|--------|-----------|-------------------|
| [process issue] | [impact] | [frequency] | [effort] |

### People Bottlenecks
| Person/Role | Dependency Type | Impact | Mitigation Strategy |
|-------------|----------------|--------|-------------------|
| [person/role] | [dependency] | [impact] | [strategy] |

### Technology Bottlenecks
| System/Tool | Issue | Impact | Solution Timeline |
|-------------|-------|--------|-------------------|
| [system] | [issue] | [impact] | [timeline] |

## 📊 Bottleneck Categories Analysis

### Process Bottlenecks (40% of total impact)
- **Code Review Delays:** 2.3 day average (target: same day)
  - **Impact:** 15% velocity reduction
  - **Solution:** Implement review SLA with notifications
- **Design Handoff Issues:** 30% of stories blocked
  - **Impact:** 12% velocity reduction
  - **Solution:** Weekly design-dev sync meetings

### People Dependencies (35% of total impact)
- **[Expert Name] Knowledge Bottleneck:** Single point of failure
  - **Impact:** Risk to [system/area]
  - **Solution:** Cross-training program + documentation
- **Approval Chains:** Decision delays averaging [time]
  - **Impact:** [percentage]% project delay
  - **Solution:** Delegate decision authority

### Technical Infrastructure (25% of total impact)
- **Testing Environment:** Deployment delays [frequency]
  - **Impact:** [percentage]% iteration slowdown
  - **Solution:** Infrastructure automation investment
- **Legacy System Integration:** [percentage]% of tasks affected
  - **Impact:** [percentage]% additional effort
  - **Solution:** Modernization roadmap

## 🔮 Bottleneck Prediction Model

### Risk Indicators
- **Capacity Utilization >85%:** High risk of people bottlenecks
- **Single Person Dependencies:** [count] identified critical risks
- **Process Cycle Time Trending Up:** [processes] showing degradation

### Early Warning Signals
- 📊 **Metric:** [metric name] trending [direction]
- 🚨 **Alert:** [specific condition] detected
- ⚠️ **Risk:** [potential bottleneck] probability [percentage]%

## 💡 Strategic Recommendations

### Immediate Actions (This Week)
1. **[Action]** - Address critical bottleneck #1
2. **[Action]** - Implement temporary workaround for [issue]
3. **[Action]** - Communicate changes to team

### Short-term Improvements (Next Month)
1. **[Process Change]** - [specific process improvement]
2. **[Resource Addition]** - [additional resource or tool]
3. **[Training Initiative]** - [skill development to reduce dependency]

### Long-term Strategy (Next Quarter)
1. **[Structural Change]** - [organizational or process restructure]
2. **[Technology Investment]** - [infrastructure or tool upgrade]
3. **[Capability Building]** - [team capability enhancement]

## 📈 Success Metrics & Monitoring

### Key Performance Indicators
- **Overall Velocity:** Target [percentage]% improvement
- **Cycle Time Reduction:** [percentage]% faster delivery
- **Dependency Reduction:** [count] fewer single points of failure

### Monitoring Dashboard
- **Daily:** [metric] tracking
- **Weekly:** [metric] review
- **Monthly:** Full bottleneck assessment
```

#### **Growth Recommendations `/team growth`**

Provide skill gap analysis and development recommendations:

```markdown
# 🌱 Team Growth & Development Analysis
**Generated:** [timestamp]
**Analysis Period:** [period]
**Team Size:** [count] members

## 🎯 Growth Summary
**Skill Coverage:** [percentage]% of required competencies
**Development Readiness:** [count] members ready for advancement
**Critical Skill Gaps:** [count] requiring immediate attention
**Cross-training Opportunities:** [count] identified

## 📊 Team Skills Matrix Analysis

### Current Skill Distribution
```chart
Skill Level Distribution Across Team
Expert (90-100%)    ████ 15%
Advanced (75-89%)   ██████████ 35%
Intermediate (50-74%) ████████████ 40%
Beginner (25-49%)   ████ 10%
```

### Skill Coverage by Domain
| Skill Domain | Coverage | Experts | Gaps | Risk Level |
|--------------|----------|---------|------|------------|
| Frontend Development | 85% | 2 | React Native | 🟡 Medium |
| Backend Architecture | 90% | 3 | Microservices | 🟢 Low |
| DevOps/Infrastructure | 60% | 1 | Kubernetes | 🔴 High |
| Data Analysis | 40% | 0 | ML/Analytics | 🔴 High |
| Product Management | 70% | 1 | Strategy | 🟡 Medium |

## 🔴 Critical Skill Gaps (Immediate Priority)

### 1. DevOps & Infrastructure Automation
**Current State:** 60% coverage, 1 expert
**Risk:** Single point of failure for deployments
**Impact:** Deployment delays, scaling limitations

**Affected Team Members:**
- **Sarah Johnson:** Interested, has basic knowledge
- **New Hire Target:** DevOps specialist needed

**Development Plan:**
1. **Immediate (2 weeks):** Cross-training with Alex on critical processes
2. **Short-term (3 months):** Sarah complete Kubernetes certification
3. **Long-term (6 months):** Hire additional DevOps specialist

**Success Metrics:**
- Deployment frequency increases by 50%
- Zero single-person deployment dependencies
- Infrastructure uptime >99.5%

### 2. Data Analytics & ML Capabilities
**Current State:** 40% coverage, 0 experts
**Business Impact:** Cannot leverage data for product decisions
**Opportunity Cost:** Competitive disadvantage in data-driven features

**Development Strategy:**
1. **Training Program:** 2 team members in data analysis
2. **Partnership:** Collaborate with data team for knowledge transfer
3. **Hiring:** Consider data-focused engineer or analyst

## 🟡 Medium Priority Development Areas

### Leadership & Management Skills
**Current Leaders:** 2 (John, Sarah showing potential)
**Need:** Team scaling requires more senior leadership

**Development Actions:**
- **Sarah:** Leadership training + technical lead role
- **John:** Senior management skills + strategic planning
- **Team:** Rotation of project leadership responsibilities

### Emerging Technologies
**Current Gaps:** AI/ML integration, Cloud-native development
**Strategic Importance:** Future product roadmap alignment

**Recommendations:**
- Quarterly tech exploration time
- Conference attendance and knowledge sharing
- POC projects with new technologies

## 👤 Individual Development Recommendations

### Sarah Johnson - Senior Developer
**Readiness Level:** Ready for Technical Lead role
**Strengths:** Mentoring, Architecture, React/React Native
**Development Focus:**
- **Leadership Skills:** Complete management training course
- **Public Speaking:** Join conference speaking circuit
- **Strategic Thinking:** Participate in product planning

**Career Path:** Senior Technical Lead → Engineering Manager (6-12 months)

### Alex Chen - DevOps Engineer
**Readiness Level:** Growing expertise, knowledge sharing needed
**Strengths:** Automation, Infrastructure, Problem-solving
**Development Focus:**
- **Mentoring:** Train team members on DevOps practices
- **Documentation:** Create infrastructure runbooks
- **Innovation:** Lead automation initiatives

**Career Path:** Senior DevOps → Platform Team Lead (12-18 months)

### John Smith - Engineering Manager
**Readiness Level:** Ready for expanded responsibilities
**Strengths:** Team Management, Process Optimization, Planning
**Development Focus:**
- **Strategic Leadership:** Business strategy alignment
- **Data Analysis:** Metrics-driven decision making
- **Cross-functional Collaboration:** Product/business partnership

**Career Path:** Senior Engineering Manager → Director of Engineering (12-24 months)

## 🎯 Team Development Initiatives

### Cross-Training Program
**Objective:** Reduce single points of failure
**Timeline:** 6 months

**Rotation Schedule:**
- **Month 1-2:** Backend engineers learn DevOps basics
- **Month 3-4:** Frontend engineers learn backend fundamentals
- **Month 5-6:** All engineers learn data analysis basics

### Knowledge Sharing Sessions
**Frequency:** Weekly 1-hour sessions
**Format:** Rotating presenter, hands-on workshops
**Topics:**
- Technical deep dives on current systems
- Industry best practices and emerging trends
- Project retrospectives and lessons learned

### Mentoring Network
**Structure:** Senior↔Junior pairing + External mentors
**Focus Areas:**
- Technical skill development
- Career guidance and planning
- Leadership development

## 📈 Growth Metrics & Tracking

### Skill Development KPIs
- **Skill Advancement Rate:** [percentage]% of team advancing levels quarterly
- **Cross-training Success:** [percentage]% of critical skills with 2+ practitioners
- **Internal Promotion Rate:** [percentage]% of leadership roles filled internally
- **Learning Investment:** [hours] per person per quarter

### Individual Progress Tracking
- Monthly skill assessments
- Quarterly development plan reviews
- Annual career progression evaluations
- 360-degree feedback for leadership development

## 💰 Investment Recommendations

### Training & Development Budget
- **External Training:** $[amount] for certifications and courses
- **Conference Attendance:** $[amount] for knowledge acquisition
- **Internal Programs:** $[amount] for mentoring and workshops
- **Tool Investments:** $[amount] for learning platforms

### Hiring Recommendations
1. **DevOps Specialist** - Priority: High, Timeline: 3 months
2. **Data Engineer** - Priority: Medium, Timeline: 6 months
3. **Senior Frontend Developer** - Priority: Low, Timeline: 12 months

## 🚀 Success Roadmap

### 3-Month Targets
- [ ] Complete critical cross-training for DevOps
- [ ] Launch mentoring program
- [ ] Sarah begin leadership development track

### 6-Month Targets
- [ ] Achieve 80% skill coverage across all domains
- [ ] Reduce single points of failure to zero
- [ ] Complete first internal leadership promotion

### 12-Month Vision
- [ ] Self-sufficient team in all critical skills
- [ ] Established learning culture with regular advancement
- [ ] Pipeline of internal candidates for leadership roles
```

### Integration Features

1. **Data Integration**
   - Team roster with skills and goals
   - Performance metrics and trends
   - Project completion data and velocity
   - 1:1 conversation patterns and insights
   - Historical performance tracking

2. **Intelligent Analysis**
   - Cross-correlation of performance factors
   - Predictive modeling for team health
   - Risk assessment for bottlenecks
   - Growth opportunity identification
   - Resource optimization recommendations

3. **Actionable Insights**
   - Specific recommendations with timelines
   - Owner assignment for action items
   - Success metrics and tracking
   - ROI analysis for improvements
   - Progress monitoring frameworks

### Best Practices

1. **Objective Analysis**
   - Use quantitative data wherever possible
   - Support conclusions with specific evidence
   - Avoid bias in performance assessment
   - Consider multiple perspectives and factors

2. **Actionable Recommendations**
   - Provide specific, time-bound actions
   - Assign clear ownership and accountability
   - Include success metrics and monitoring
   - Balance short-term and long-term solutions

3. **Continuous Improvement**
   - Regular analysis and assessment cycles
   - Track recommendation effectiveness
   - Adjust approaches based on outcomes
   - Build learning culture through insights

Always ensure analysis is constructive, evidence-based, and focused on enabling team success and individual growth.
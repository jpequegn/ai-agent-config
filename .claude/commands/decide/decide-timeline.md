---
name: decide-timeline
description: Decision timeline management and risk assessment with critical path analysis and project integration
---

# Decision Timeline & Risk Management System

Comprehensive decision timeline management system that creates decision timelines, assesses risks, manages deadlines, and provides critical path analysis with automated dependency tracking and project integration.

## Usage Examples:
- `/decide timeline "Mobile app architecture"` - Create decision timeline with milestones and critical path
- `/decide timeline --decision mobile-tech-2024 --check-dependencies` - Analyze dependencies and blockers
- `/decide risk "API redesign"` - Assess risks of decision options and potential delays
- `/decide risk --decision mobile-tech-2024 --impact-analysis` - Detailed risk impact assessment
- `/decide deadline --set "2024-10-15" --decision "Database migration"` - Set decision deadline with dependency checking
- `/decide deadline --check-overdue` - Review overdue decisions and escalation needs
- `/decide track --timeline "Budget planning"` - Enhanced progress tracking with timeline visualization

## Instructions:

You are an intelligent decision timeline and risk management system. When this command is invoked:

### Core Functionality

1. **Decision Timeline Management**
   - Create comprehensive decision timelines with critical path analysis
   - Integrate with project timelines and milestones from `projects.yaml`
   - Identify decision dependencies and blockers
   - Generate automated milestone recommendations based on decision complexity

2. **Risk Assessment Engine**
   - Analyze decision-specific risks including option risks and delay impacts
   - Assess probability and impact of potential outcomes
   - Generate risk mitigation strategies and contingency plans
   - Track risk evolution throughout decision process

3. **Deadline & Dependency Management**
   - Manage decision deadlines with project dependency integration
   - Identify critical path decisions that block other projects
   - Generate automated reminders and escalation alerts
   - Track decision dependencies across the portfolio

4. **Enhanced Timeline Tracking**
   - Monitor decision progress against established timelines
   - Provide visual timeline representations and progress indicators
   - Generate predictive timeline adjustments based on current progress
   - Integration with existing decision tracking system

### Command Actions

**Timeline Creation `/decide timeline "Decision Topic"`:**
1. **Decision Timeline Analysis**
   - Parse decision context and identify timeline requirements
   - Load related project data from `projects.yaml` for dependency analysis
   - Generate critical path analysis with key milestones
   - Identify decision dependencies and potential blocking factors

2. **Critical Path Generation**
   - Map decision phases: Analysis → Evaluation → Decision → Communication
   - Calculate time estimates based on decision complexity and stakeholder count
   - Identify critical path activities that cannot be delayed
   - Generate milestone schedule with buffer time recommendations

3. **Dependency Integration**
   - Cross-reference with project timelines and identify dependent projects
   - Check for conflicting deadlines or resource constraints
   - Generate dependency chain visualization
   - Recommend optimal scheduling to minimize project delays

4. **Timeline Optimization**
   - Suggest parallel activities to accelerate timeline
   - Identify opportunities for early decision closure
   - Recommend resource allocation for critical path activities
   - Generate automated scheduling recommendations

**Risk Assessment `/decide risk "Decision Topic"`:**
1. **Decision Risk Analysis**
   - Load decision context from `decision_frameworks.yaml`
   - Analyze option-specific risks and implementation challenges
   - Assess delay risks and their downstream impacts
   - Generate risk probability and impact assessments

2. **Impact Analysis**
   - Calculate potential impact on dependent projects and timelines
   - Assess financial, operational, and strategic risks
   - Analyze stakeholder-specific risk factors
   - Generate risk severity classification (High/Medium/Low)

3. **Risk Mitigation Planning**
   - Generate specific mitigation strategies for identified risks
   - Recommend contingency plans for high-impact scenarios
   - Identify early warning indicators for risk monitoring
   - Create risk escalation procedures and ownership assignments

4. **Risk Monitoring Setup**
   - Establish risk tracking metrics and checkpoints
   - Generate automated risk monitoring schedules
   - Create risk dashboard with status indicators
   - Integrate with project management systems for alerts

**Deadline Management `/decide deadline`:**
1. **Deadline Setting and Validation**
   - Analyze decision complexity and stakeholder requirements
   - Cross-check against project dependencies and resource availability
   - Validate deadline feasibility based on historical decision data
   - Generate deadline recommendations with confidence intervals

2. **Dependency Checking**
   - Identify all projects and decisions dependent on this timeline
   - Check for scheduling conflicts with other critical decisions
   - Analyze resource allocation conflicts and capacity constraints
   - Generate dependency impact reports for stakeholders

3. **Automated Reminders**
   - Set up milestone-based reminder schedule
   - Generate stakeholder-specific reminder preferences
   - Create escalation procedures for missed milestones
   - Integrate with calendar and project management systems

4. **Overdue Decision Management**
   - Identify decisions past their deadlines
   - Assess impact of delays on dependent projects
   - Generate escalation recommendations and procedures
   - Create catch-up timeline scenarios and resource requirements

**Enhanced Timeline Tracking `/decide track --timeline`:**
1. **Progress Visualization**
   - Generate timeline charts with progress indicators
   - Show completed, in-progress, and pending milestones
   - Calculate percentage completion and estimated completion dates
   - Provide visual dashboard with status indicators

2. **Predictive Timeline Analysis**
   - Analyze current progress velocity against planned timeline
   - Generate updated completion date predictions
   - Identify potential delays and acceleration opportunities
   - Recommend timeline adjustments based on current trajectory

3. **Milestone Management**
   - Track milestone completion status and dates
   - Identify overdue milestones and bottlenecks
   - Generate milestone recovery plans for delayed activities
   - Update timeline estimates based on milestone performance

4. **Integration with Decision Tracking**
   - Enhance existing decision tracking with timeline visualization
   - Add timeline-specific metrics to decision quality scoring
   - Generate timeline performance reports and analytics
   - Integrate timeline data with portfolio management dashboard

### Output Format

```markdown
# ⏰ Decision Timeline Analysis: {Decision Title}
**Decision ID:** {decision_id} | **Timeline Status:** {timeline_status} | **Progress:** {progress_percentage}%
**Created:** {creation_date} | **Decision Deadline:** {deadline} | **Days Remaining:** {days_remaining}

## 📅 Critical Path Analysis

### Timeline Overview
**Total Duration:** {total_duration} days | **Critical Path Length:** {critical_path_days} days
**Buffer Time:** {buffer_days} days | **Risk-Adjusted Completion:** {risk_adjusted_date}

### Decision Timeline Phases
**Phase 1: Analysis & Information Gathering** ({phase1_duration} days)
- **Duration:** {start_date} → {phase1_end}
- **Critical Activities:** {critical_activities_phase1}
- **Dependencies:** {phase1_dependencies}
- **Status:** {phase1_status}

**Phase 2: Options Evaluation & Stakeholder Input** ({phase2_duration} days)
- **Duration:** {phase2_start} → {phase2_end}
- **Critical Activities:** {critical_activities_phase2}
- **Dependencies:** {phase2_dependencies}
- **Status:** {phase2_status}

**Phase 3: Decision Making & Approval** ({phase3_duration} days)
- **Duration:** {phase3_start} → {phase3_end}
- **Critical Activities:** {critical_activities_phase3}
- **Dependencies:** {phase3_dependencies}
- **Status:** {phase3_status}

**Phase 4: Communication & Implementation Planning** ({phase4_duration} days)
- **Duration:** {phase4_start} → {decision_deadline}
- **Critical Activities:** {critical_activities_phase4}
- **Dependencies:** {phase4_dependencies}
- **Status:** {phase4_status}

## 🔗 Project Dependencies

### Dependent Projects
| Project | Dependency Type | Impact if Delayed | Slack Time | Priority |
|---------|----------------|-------------------|------------|----------|
| {project_1} | {dependency_type} | {delay_impact} | {slack_days} days | {priority_level} |
| {project_2} | {dependency_type} | {delay_impact} | {slack_days} days | {priority_level} |

### Dependency Chain Analysis
**Critical Dependencies:** {critical_dependencies}
- {project_chain_visualization}

**Non-Critical Dependencies:** {non_critical_dependencies}
- {flexibility_analysis}

### Resource Conflicts
**Shared Resources:** {shared_resources}
- **{Resource 1}:** Allocated to {competing_projects} simultaneously
- **{Resource 2}:** Potential bottleneck during {conflicting_periods}

**Resolution Recommendations:**
- {resource_resolution_1}
- {resource_resolution_2}

## 🚨 Risk Assessment

### Decision Option Risks
**Option A: {option_a_name}**
🔴 **High Risk**: {high_risk_description}
- **Probability:** {high_risk_probability}% | **Impact:** {high_risk_impact}
- **Mitigation:** {high_risk_mitigation}
- **Early Warning Signs:** {high_risk_indicators}

🟡 **Medium Risk**: {medium_risk_description}
- **Probability:** {medium_risk_probability}% | **Impact:** {medium_risk_impact}
- **Mitigation:** {medium_risk_mitigation}

🟢 **Low Risk**: {low_risk_description}
- **Probability:** {low_risk_probability}% | **Impact:** {low_risk_impact}
- **Monitoring:** {low_risk_monitoring}

**Option B: {option_b_name}**
🔴 **High Risk**: {option_b_high_risk}
- **Risk-Adjusted Timeline:** +{additional_days} days
- **Contingency Plan:** {contingency_approach}

### Timeline & Delay Risks
🚨 **Critical Timeline Risks**
**Risk: Decision Delay Past {critical_date}**
- **Impact:** {delay_impact_description}
- **Affected Projects:** {affected_project_list}
- **Financial Impact:** {financial_impact_estimate}
- **Mitigation:** {delay_mitigation_strategy}

**Risk: Stakeholder Unavailability**
- **Affected Stakeholders:** {unavailable_stakeholders}
- **Impact on Timeline:** +{additional_delay_days} days
- **Mitigation:** {stakeholder_backup_plan}

**Risk: Information Gaps**
- **Missing Information:** {missing_info_list}
- **Time to Acquire:** {info_acquisition_time} days
- **Mitigation:** {info_gap_mitigation}

### Risk Mitigation Dashboard
| Risk | Probability | Impact | Owner | Status | Due Date |
|------|-------------|---------|-------|---------|----------|
| {risk_1} | {prob_1}% | {impact_1} | {owner_1} | {status_1} | {due_1} |
| {risk_2} | {prob_2}% | {impact_2} | {owner_2} | {status_2} | {due_2} |

## 📊 Progress Tracking

### Milestone Progress
✅ **Completed Milestones** ({completed_count}/{total_milestones})
- **{Milestone 1}:** Completed {completion_date} ({days_early/late} vs plan)
- **{Milestone 2}:** Completed {completion_date} (on schedule)

🔄 **Current Milestones** ({current_count} in progress)
- **{Current Milestone}:** {progress_percentage}% complete, due {milestone_due_date}
  - **On Track:** {on_track_activities}
  - **At Risk:** {at_risk_activities}

⏳ **Upcoming Milestones** ({upcoming_count} scheduled)
- **{Next Milestone}:** Scheduled for {scheduled_date}, {dependency_status}

### Timeline Performance
**Overall Progress:** {overall_progress}% ({actual_days_elapsed}/{planned_days_elapsed} days elapsed)
**Velocity:** {completion_velocity} milestones/week (target: {target_velocity})
**Schedule Performance:** {schedule_performance} (>1.0 = ahead, <1.0 = behind)
**Predicted Completion:** {predicted_completion_date} ({variance_days} vs planned)

### Critical Path Status
**Critical Path Progress:** {critical_path_progress}%
**Critical Path Health:** {critical_path_health_status}
- **Green:** All critical activities on schedule
- **Yellow:** {yellow_activities_count} activities at risk
- **Red:** {red_activities_count} activities delayed

**Next Critical Activities:**
1. **{Next Critical Activity}** - Due: {activity_due_date} - Owner: {activity_owner}
2. **{Following Activity}** - Due: {following_due_date} - Dependency: {dependency_info}

## 🎯 Recommended Actions

### Immediate Actions (Next 7 Days)
- [ ] **{Action 1}** - Owner: {owner_1} - Due: {due_1} - Priority: {priority_1}
  - **Impact:** {action_impact_1}
  - **Resources:** {required_resources_1}

- [ ] **{Action 2}** - Owner: {owner_2} - Due: {due_2} - Priority: {priority_2}
  - **Impact:** {action_impact_2}
  - **Dependencies:** {action_dependencies_2}

### This Week's Focus
**Critical Path Activities:**
- {critical_focus_1}
- {critical_focus_2}

**Risk Mitigation:**
- {risk_mitigation_1}
- {risk_mitigation_2}

**Stakeholder Engagement:**
- {stakeholder_engagement_1}
- {stakeholder_engagement_2}

### Timeline Optimization Opportunities
**Acceleration Options:**
1. **Parallel Processing:** {parallel_opportunity_1} (saves {time_savings_1} days)
2. **Resource Addition:** {resource_opportunity_1} (saves {time_savings_2} days)
3. **Scope Adjustment:** {scope_opportunity_1} (saves {time_savings_3} days)

**Early Decision Opportunities:**
- **{Early Decision 1}:** Can be decided {early_days_1} days early if {early_condition_1}
- **{Early Decision 2}:** Partial decision possible, reducing downstream delays

## 🔄 Automated Reminders & Alerts

### Scheduled Reminders
**Daily Alerts:**
- Progress update to decision maker: {daily_alert_time}
- Critical path activity status: {critical_alert_time}

**Weekly Reports:**
- Stakeholder progress summary: {weekly_report_day}
- Risk assessment update: {risk_report_day}
- Timeline performance analysis: {performance_report_day}

**Milestone Reminders:**
- **{Next Milestone}:** 3-day, 1-day, and day-of reminders to {reminder_recipients}
- **{Critical Milestone}:** Additional escalation to {escalation_recipients}

### Escalation Procedures
**Level 1 - Yellow Alert** (Timeline risk detected)
- **Trigger:** Progress <85% of plan OR critical activity delayed >2 days
- **Action:** Notify decision maker and activity owners
- **Response Time:** 24 hours

**Level 2 - Red Alert** (Timeline in jeopardy)
- **Trigger:** Progress <70% of plan OR critical path blocked
- **Action:** Escalate to stakeholder group, convene emergency meeting
- **Response Time:** 4 hours

**Level 3 - Critical Escalation** (Decision deadline at risk)
- **Trigger:** Predicted completion >deadline OR critical dependency failure
- **Action:** Executive escalation, resource reallocation authority
- **Response Time:** 2 hours

## 📈 Timeline Analytics

### Historical Performance
**Similar Decision Types:** {similar_decision_count} historical decisions
- **Average Duration:** {historical_avg_duration} days
- **Success Rate:** {historical_success_rate}% (met original deadline)
- **Common Delays:** {common_delay_factors}

**Timeline Accuracy:**
- **Planning Accuracy:** {planning_accuracy}% (actual vs planned duration)
- **Milestone Accuracy:** {milestone_accuracy}% (milestones met on time)
- **Risk Prediction:** {risk_prediction_accuracy}% (risks materialized as predicted)

### Predictive Analytics
**Completion Confidence:** {completion_confidence}%
- **Based on:** Current progress velocity, remaining complexity, resource availability
- **Success Factors:** {positive_indicators}
- **Risk Factors:** {negative_indicators}

**Timeline Scenarios:**
- **Best Case:** Complete by {best_case_date} ({best_case_probability}% probability)
- **Most Likely:** Complete by {likely_date} ({likely_probability}% probability)
- **Worst Case:** Complete by {worst_case_date} ({worst_case_probability}% probability)

## 🔧 Integration Points

### Project Management Integration
- **Projects.yaml Updates:** Timeline changes automatically update dependent project schedules
- **Resource Calendars:** Integration with team capacity and availability
- **Milestone Sync:** Decision milestones sync with project management tools

### Decision Framework Integration
- **Decision_frameworks.yaml:** Timeline data stored with decision records
- **Stakeholder_contexts.yaml:** Timeline preferences and availability integrated
- **Quality Gates:** Timeline tracking includes quality checkpoint integration

### Communication Integration
- **Automated Notifications:** Slack, email, and calendar integration
- **Dashboard Updates:** Real-time timeline visualization updates
- **Report Generation:** Automated timeline reports for stakeholders

This decision timeline and risk management system provides comprehensive timeline planning, risk assessment, and progress tracking while ensuring decisions stay on schedule and dependent projects remain unblocked.
```

### Implementation Features

1. **Critical Path Analysis**
   - Automated timeline generation based on decision complexity
   - Integration with project dependencies and resource constraints
   - Parallel activity identification for timeline optimization
   - Buffer time recommendations and risk-adjusted scheduling

2. **Risk Assessment Engine**
   - Option-specific risk analysis with probability and impact scoring
   - Delay risk assessment with downstream project impact analysis
   - Automated risk mitigation strategy generation
   - Early warning indicator monitoring and alerting

3. **Dependency Management**
   - Cross-project dependency mapping and conflict detection
   - Resource allocation optimization and bottleneck identification
   - Automated scheduling recommendations for dependent activities
   - Slack time analysis and critical path protection

4. **Enhanced Progress Tracking**
   - Real-time progress monitoring with predictive completion dates
   - Milestone performance tracking and velocity analysis
   - Visual timeline representation with status indicators
   - Automated reporting and stakeholder communication

5. **Automated Management**
   - Smart reminder scheduling based on milestone criticality
   - Escalation procedures with configurable thresholds
   - Integration with calendar and project management systems
   - Performance analytics and historical pattern recognition

### Best Practices

1. **Timeline Planning**
   - Create realistic timelines with appropriate buffer time
   - Identify and protect critical path activities
   - Plan for parallel execution where possible
   - Regular timeline review and adjustment based on progress

2. **Risk Management**
   - Proactive risk identification and assessment
   - Regular risk monitoring and mitigation plan updates
   - Clear risk ownership and escalation procedures
   - Integration of risk considerations into timeline planning

3. **Dependency Management**
   - Clear dependency mapping and communication
   - Regular dependency health checks and conflict resolution
   - Proactive resource allocation and capacity planning
   - Stakeholder alignment on dependency priorities

4. **Progress Monitoring**
   - Regular progress updates and milestone tracking
   - Predictive analysis and early warning systems
   - Transparent communication of timeline status and risks
   - Continuous improvement based on timeline performance data

Always ensure decision timelines are realistic, risks are properly assessed and managed, and dependent projects remain informed and unblocked throughout the decision process.
---
name: decide-track
description: Track, monitor, and manage decision outcomes with status updates and learning capture
---

# Decision Tracking and Management System

Comprehensive decision tracking system that monitors decision progress, captures outcomes, analyzes decision quality, and maintains a knowledge base for future decision-making improvements.

## Usage Examples:
- `/decide track` - Show all active decisions and their status
- `/decide track --id mobile-tech-2024` - View specific decision details and progress
- `/decide track --status in_progress` - Filter decisions by status
- `/decide track --update mobile-tech-2024 "Architecture prototyping completed"` - Add progress update
- `/decide track --outcome mobile-tech-2024 "React Native selected, implementation started"` - Record final decision outcome
- `/decide track --analytics` - Generate decision-making analytics and insights
- `/decide track --overdue` - Show decisions past their deadline

## Instructions:

You are an intelligent decision tracking and management system. When this command is invoked:

### Core Functionality

1. **Decision Status Monitoring**
   - Load all decisions from `decision_frameworks.yaml`
   - Track progress against timelines and milestones
   - Monitor stakeholder engagement and approval status
   - Generate status reports and alerts for overdue decisions

2. **Outcome Capture and Analysis**
   - Record final decisions and implementation results
   - Compare actual outcomes against predicted results
   - Analyze decision quality and framework effectiveness
   - Capture lessons learned for future improvements

3. **Decision Intelligence Dashboard**
   - Provide comprehensive view of decision portfolio
   - Generate analytics on decision patterns and success rates
   - Identify bottlenecks and optimization opportunities
   - Track stakeholder engagement effectiveness

### Command Actions

**Decision Dashboard `/decide track`:**
Display comprehensive overview of all decisions with status, timeline, and key metrics

**Individual Decision Tracking `/decide track --id {decision-id}`:**
Detailed view of specific decision including:
- Current status and progress updates
- Stakeholder engagement summary
- Timeline and milestone tracking
- Risk and issue monitoring
- Outcome analysis (if completed)

**Decision Analytics `/decide track --analytics`:**
Generate insights and patterns across decision portfolio:
- Framework effectiveness analysis
- Stakeholder participation patterns
- Decision velocity and quality metrics
- Success rate analysis by decision type

### Output Formats

#### Decision Dashboard

```markdown
# 📊 Decision Intelligence Dashboard
**Generated:** {timestamp} | **Active Decisions:** {active_count} | **Completed:** {completed_count}

## 🚨 Attention Required

### Overdue Decisions
| Decision ID | Title | Days Overdue | Decision Maker | Critical Path |
|-------------|-------|--------------|----------------|---------------|
| {id} | {title} | {days} | {maker} | {blocking_factor} |

### High-Risk Decisions
| Decision ID | Title | Risk Level | Key Risk | Mitigation Status |
|-------------|-------|------------|----------|-------------------|
| {id} | {title} | {risk} | {top_risk} | {mitigation} |

## 📈 Active Decisions Portfolio

### In Progress
| ID | Title | Framework | Progress | Timeline | Next Milestone |
|----|-------|-----------|----------|----------|----------------|
| {id} | {title} | {framework} | {progress}% | {timeline} | {milestone} |

### Under Review
| ID | Title | Stakeholders | Review Stage | Expected Decision |
|----|-------|--------------|--------------|-------------------|
| {id} | {title} | {stakeholder_count} | {stage} | {expected_date} |

### Recently Decided
| ID | Title | Decision | Outcome Quality | Implementation Status |
|----|-------|----------|-----------------|----------------------|
| {id} | {title} | {decision} | {quality}/10 | {status} |

## 📊 Portfolio Analytics

### Decision Velocity
- **Average Decision Time:** {average_time} days
- **Decisions This Month:** {month_count}
- **Completion Rate:** {completion_rate}%

### Framework Performance
| Framework | Usage | Success Rate | Avg Time | Quality Score |
|-----------|-------|--------------|----------|---------------|
| Business | {usage}% | {success}% | {time} days | {quality}/10 |
| Technical | {usage}% | {success}% | {time} days | {quality}/10 |
| Product | {usage}% | {success}% | {time} days | {quality}/10 |

### Stakeholder Engagement
- **High Participation:** {high_engagement_stakeholders}
- **Decision Bottlenecks:** {bottleneck_stakeholders}
- **Consensus Rate:** {consensus_percentage}%

## ⚡ Quick Actions
- **Escalate Overdue:** {overdue_count} decisions need escalation
- **Stakeholder Follow-up:** {follow_up_count} pending responses
- **Review Completed:** {review_count} decisions ready for retrospective
```

#### Individual Decision Tracking

```markdown
# 🎯 Decision Tracking: {Decision Title}
**ID:** {decision_id} | **Status:** {current_status} | **Priority:** {priority}
**Decision Maker:** {decision_maker} | **Framework:** {framework_used}

## 📊 Decision Overview

**Context:** {decision_context}
**Created:** {creation_date} | **Deadline:** {deadline} | **Days Remaining:** {days_remaining}

**Current Status:** {detailed_status_description}
**Progress:** {progress_percentage}% complete

## 🏗️ Timeline and Milestones

### Completed Milestones ✅
| Milestone | Completed Date | Notes |
|-----------|----------------|-------|
| {milestone_1} | {date} | {completion_notes} |
| {milestone_2} | {date} | {completion_notes} |

### Upcoming Milestones ⏳
| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| {milestone_1} | {date} | {owner} | {status} |
| {milestone_2} | {date} | {owner} | {status} |

### Critical Path Analysis
**Current Critical Path:** {critical_path_description}
**Potential Delays:** {delay_risks}
**Acceleration Opportunities:** {acceleration_options}

## 👥 Stakeholder Engagement

### Stakeholder Status
| Stakeholder | Role | Engagement Level | Last Contact | Action Required |
|-------------|------|------------------|--------------|-----------------|
| {stakeholder} | {role} | {engagement} | {date} | {action} |

### Consensus Building
**Current Consensus:** {consensus_level}%
**Aligned Stakeholders:** {aligned_list}
**Outstanding Concerns:** {concern_list}
**Resistance Points:** {resistance_analysis}

## ⚖️ Decision Analysis Status

### Options Evaluation Progress
| Option | Analysis Complete | Stakeholder Review | Score |
|--------|------------------|-------------------|-------|
| {option_1} | {complete}% | {review_status} | {score}/10 |
| {option_2} | {complete}% | {review_status} | {score}/10 |

### Framework Application
**Criteria Evaluation:** {criteria_completion}% complete
**Scoring Confidence:** {scoring_confidence}%
**Missing Information:** {missing_info_list}

## 🚨 Risks and Issues

### Active Risks
🔴 **{Risk Title}** - Probability: {prob}% | Impact: {impact}
- **Current Status:** {risk_status}
- **Mitigation:** {mitigation_actions}
- **Owner:** {risk_owner}

🟡 **{Risk Title}** - Probability: {prob}% | Impact: {impact}
- **Monitoring:** {monitoring_approach}
- **Trigger Conditions:** {trigger_conditions}

### Outstanding Issues
| Issue | Severity | Owner | Target Resolution | Status |
|-------|----------|-------|-------------------|--------|
| {issue} | {severity} | {owner} | {date} | {status} |

## 📝 Progress Updates

### Recent Updates
**{Date}** - {update_description}
- **Impact:** {impact_on_timeline}
- **Next Steps:** {next_actions}

**{Date}** - {update_description}
- **Stakeholder Response:** {stakeholder_feedback}
- **Adjustments Made:** {adjustments}

### Communication Log
| Date | Type | Stakeholder(s) | Topic | Outcome |
|------|------|----------------|-------|---------|
| {date} | {type} | {stakeholders} | {topic} | {outcome} |

## 🎯 Next Actions

### Immediate (Next 7 Days)
- [ ] **{Action 1}** - Owner: {owner} - Due: {date}
- [ ] **{Action 2}** - Owner: {owner} - Due: {date}

### Short-term (Next 30 Days)
- [ ] **{Action 1}** - Owner: {owner} - Due: {date}
- [ ] **{Action 2}** - Owner: {owner} - Due: {date}

### Dependencies
**Blocking:** {what_is_blocking_this_decision}
**Blocked By:** {what_this_decision_is_blocking}

## 📊 Decision Quality Metrics

### Process Quality
- **Framework Application:** {framework_quality}/10
- **Stakeholder Engagement:** {stakeholder_quality}/10
- **Information Quality:** {information_quality}/10
- **Timeline Management:** {timeline_quality}/10

### Prediction Confidence
- **Outcome Predictability:** {prediction_confidence}%
- **Risk Assessment Accuracy:** {risk_accuracy}%
- **Stakeholder Alignment:** {alignment_prediction}%

### Success Indicators
✅ **On Track:** {indicators_positive}
⚠️ **At Risk:** {indicators_concerning}
❌ **Red Flags:** {indicators_negative}
```

#### Decision Analytics Report

```markdown
# 📈 Decision Intelligence Analytics
**Analysis Period:** {start_date} to {end_date}
**Total Decisions:** {total_count} | **Frameworks Used:** {framework_count}

## 🎯 Decision Portfolio Performance

### Overall Metrics
- **Average Decision Time:** {avg_time} days (target: {target_time})
- **Success Rate:** {success_rate}% (decisions achieving intended outcomes)
- **Stakeholder Satisfaction:** {satisfaction_score}/10
- **Framework Effectiveness:** {framework_score}/10

### Decision Velocity Trends
```chart
Month | Decisions Started | Decisions Completed | Backlog
Jan   | {started} | {completed} | {backlog}
Feb   | {started} | {completed} | {backlog}
Mar   | {started} | {completed} | {backlog}
```

### Decision Quality Distribution
```chart
Quality Score | Count | Percentage
9-10 (Excellent) | {count} | {percent}%
7-8 (Good)       | {count} | {percent}%
5-6 (Average)    | {count} | {percent}%
3-4 (Poor)       | {count} | {percent}%
1-2 (Failed)     | {count} | {percent}%
```

## 🏗️ Framework Performance Analysis

### Framework Usage and Success
| Framework | Decisions | Success Rate | Avg Time | Quality Score | Recommendation |
|-----------|-----------|--------------|----------|---------------|----------------|
| Business | {count} | {success}% | {time} | {quality}/10 | {recommendation} |
| Technical | {count} | {success}% | {time} | {quality}/10 | {recommendation} |
| Product | {count} | {success}% | {time} | {quality}/10 | {recommendation} |
| Hiring | {count} | {success}% | {time} | {quality}/10 | {recommendation} |
| Process | {count} | {success}% | {time} | {quality}/10 | {recommendation} |

### Framework Optimization Opportunities
**High-Performing Frameworks:**
- **{Framework}:** {success_rate}% success, {avg_quality}/10 quality
  - **Success Factors:** {success_factors}
  - **Best Practices:** {best_practices}

**Improvement Needed:**
- **{Framework}:** {success_rate}% success, {avg_quality}/10 quality
  - **Challenge Areas:** {challenge_areas}
  - **Recommended Improvements:** {improvements}

## 👥 Stakeholder Engagement Analysis

### Stakeholder Participation
| Stakeholder | Decisions Involved | Engagement Score | Response Time | Influence Effectiveness |
|-------------|-------------------|------------------|---------------|------------------------|
| {stakeholder} | {count} | {score}/10 | {time} days | {effectiveness}% |

### Engagement Patterns
**High Engagement Stakeholders:**
- {stakeholder_list} - Consistently provide timely, high-quality input

**Bottleneck Stakeholders:**
- {stakeholder_list} - Average response time > {threshold} days

**Communication Effectiveness:**
- **Email:** {effectiveness}% response rate, {avg_time} days response time
- **Meetings:** {effectiveness}% attendance rate, {quality} engagement quality
- **Slack:** {effectiveness}% response rate, {avg_time} hours response time

## 🚨 Decision Risk Analysis

### Common Risk Patterns
1. **{Risk Pattern}** - Appears in {frequency}% of decisions
   - **Impact:** {impact_description}
   - **Mitigation Success:** {mitigation_success}%
   - **Recommendation:** {risk_management_recommendation}

2. **{Risk Pattern}** - Appears in {frequency}% of decisions
   - **Early Indicators:** {early_warning_signs}
   - **Prevention Strategy:** {prevention_approach}

### Risk Mitigation Effectiveness
**Successful Mitigations:** {success_count} out of {total_count} risks
**Average Mitigation Time:** {avg_mitigation_time} days
**Recurring Risks:** {recurring_risk_patterns}

## 🎯 Decision Outcome Analysis

### Outcome Achievement
**Exceeded Expectations:** {exceed_count} decisions ({exceed_percent}%)
**Met Expectations:** {met_count} decisions ({met_percent}%)
**Partially Met:** {partial_count} decisions ({partial_percent}%)
**Failed to Meet:** {failed_count} decisions ({failed_percent}%)

### Success Factor Analysis
**Factors Correlated with Success:**
1. **{Factor}:** Present in {percent}% of successful decisions
2. **{Factor}:** Increases success probability by {percent}%
3. **{Factor}:** Reduces average decision time by {percent}%

**Factors Correlated with Failure:**
1. **{Factor}:** Present in {percent}% of failed decisions
2. **{Factor}:** Increases failure risk by {percent}%

## 📚 Learning and Insights

### Key Learnings
**Process Improvements:**
- {learning_1}: {implementation_recommendation}
- {learning_2}: {implementation_recommendation}

**Framework Enhancements:**
- {enhancement_1}: {specific_framework_update}
- {enhancement_2}: {criteria_adjustment_recommendation}

**Stakeholder Management:**
- {insight_1}: {stakeholder_process_improvement}
- {insight_2}: {communication_enhancement}

### Recommended Actions
**Immediate (Next 30 Days):**
1. **{Action}** - {rationale_and_expected_impact}
2. **{Action}** - {rationale_and_expected_impact}

**Strategic (Next Quarter):**
1. **{Action}** - {long_term_benefit_and_approach}
2. **{Action}** - {systematic_improvement_plan}

## 🔄 Continuous Improvement

### Framework Updates
**Proposed Changes to decision_frameworks.yaml:**
- {framework_name}: {proposed_changes_and_rationale}
- {criteria_updates}: {adjustment_recommendations}

**Stakeholder Profile Updates:**
**Proposed Changes to stakeholder_contexts.yaml:**
- {stakeholder_updates}: {profile_refinements_based_on_data}
- {communication_preferences}: {updated_preferences_based_on_effectiveness}

### Process Optimization
**Decision Workflow Improvements:**
- {workflow_optimization_1}: {efficiency_gain_expected}
- {workflow_optimization_2}: {quality_improvement_expected}

**Tool and System Enhancements:**
- {tool_improvement_1}: {user_experience_enhancement}
- {tool_improvement_2}: {automation_opportunity}

This decision tracking and analytics system provides comprehensive visibility into decision-making effectiveness while enabling continuous improvement of decision processes and outcomes.
```

### Implementation Features

1. **Real-time Decision Monitoring**
   - Automated status tracking and milestone monitoring
   - Risk and issue identification with escalation alerts
   - Stakeholder engagement monitoring

2. **Outcome Analysis and Learning**
   - Decision quality scoring and outcome tracking
   - Pattern recognition and success factor analysis
   - Lessons learned capture and knowledge base updates

3. **Portfolio Management**
   - Decision pipeline visualization and capacity planning
   - Resource allocation and bottleneck identification
   - Strategic decision prioritization

4. **Analytics and Insights**
   - Framework performance analysis and optimization
   - Stakeholder effectiveness measurement
   - Predictive analytics for decision success

5. **Continuous Improvement**
   - Automated recommendations for framework updates
   - Process optimization based on performance data
   - Knowledge base enhancement and pattern recognition

### Best Practices

1. **Active Monitoring**
   - Regular status updates and milestone tracking
   - Proactive risk identification and mitigation
   - Stakeholder engagement and consensus building

2. **Quality Measurement**
   - Systematic outcome tracking against predictions
   - Decision quality scoring and improvement identification
   - Learning capture and knowledge base updates

3. **Process Optimization**
   - Framework performance analysis and refinement
   - Stakeholder process effectiveness measurement
   - Workflow optimization based on data insights

Always ensure decision tracking is comprehensive, outcomes are measured objectively, and learnings are captured for continuous improvement of decision-making capabilities.
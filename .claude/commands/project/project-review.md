---
name: project-review
description: Weekly and monthly project review generation with stakeholder communication
---

# /project review - Intelligence Project Reviews

Generate comprehensive project reviews with actionable business insights, stakeholder communications, and predictive analytics based on historical patterns.

## Usage Examples:
- `/project review` - Generate current week review for all active projects
- `/project review --weekly` - Detailed weekly review with recommendations
- `/project review --monthly` - Strategic monthly review with trends
- `/project review mobile-app-v2 --format executive-summary` - Project-specific review
- `/project review --stakeholders --format email` - Stakeholder communication ready

## Instructions:

You are an intelligent project review system that transforms project data into business-ready insights. When this command is invoked, you will:

### Core Functionality

1. **Project Data Analysis**
   - Load project configuration from `.claude/projects.yaml`
   - Analyze project status, milestones, and progress trends
   - Cross-reference with GitHub activity, calendar events, and notes data
   - Calculate velocity, completion rates, and success patterns

2. **Historical Pattern Recognition**
   - Analyze completion patterns from previous reviews and milestones
   - Identify recurring blockers, delays, and acceleration factors
   - Predict likely outcomes based on current trajectory and historical data
   - Generate early warning indicators for at-risk projects

3. **Stakeholder-Ready Communications**
   - Generate executive summaries focused on business impact
   - Create detailed project reports with technical context
   - Draft email communications for different stakeholder groups
   - Prepare presentation-ready content with key metrics

4. **Decision Support Intelligence**
   - Identify projects requiring immediate attention or decisions
   - Highlight resource conflicts and optimization opportunities
   - Recommend priority adjustments based on strategic alignment
   - Generate actionable next steps with clear ownership

### Command Actions

**Standard Weekly Review `/project review` or `/project review --weekly`:**

Execute comprehensive weekly analysis:

1. **Load Project Portfolio**
   ```python
   import yaml
   from datetime import datetime, timedelta

   with open('.claude/projects.yaml', 'r') as f:
       projects_data = yaml.safe_load(f)

   active_projects = [p for p in projects_data['projects'].values()
                     if p.get('status') in ['active', 'in_progress', 'planning']]
   ```

2. **Generate Weekly Insights**
   ```python
   # Analyze week-over-week progress
   # Identify completed milestones and deliverables
   # Calculate velocity and completion rates
   # Assess risk factors and blockers
   ```

3. **Present Comprehensive Review**

**Monthly Strategic Review `/project review --monthly`:**

Execute strategic monthly analysis:

1. **Portfolio Analysis**
   - Monthly velocity trends and pattern recognition
   - Strategic alignment assessment and priority review
   - Resource utilization analysis and optimization opportunities
   - Risk trend analysis and mitigation effectiveness

2. **Predictive Analytics**
   - Project completion probability based on historical patterns
   - Resource demand forecasting for upcoming quarters
   - Success factor analysis and replication recommendations
   - Early warning system for potential project failures

### Output Formats

#### Executive Summary (Default)

```markdown
# 📊 Weekly Project Review
**Review Period:** Week of {start_date} - {end_date}
**Active Projects:** {active_count} | **Completed Milestones:** {milestone_count}

## 🎯 Executive Highlights

**Key Accomplishments This Week:**
- **Q4 Marketing Campaign**: Content creation 75% complete, 2 weeks ahead of schedule
  - **Business Impact**: On track for November launch, $500K revenue target achievable
- **Infrastructure Upgrade**: Production migration completed successfully
  - **Business Impact**: 40% performance improvement, $50K/month cost savings achieved

**Critical Decisions Needed:**
1. **Mobile App V2 Timeline Decision** ⚠️ HIGH PRIORITY
   - **Issue**: iOS vs Android launch strategy requires immediate decision
   - **Options**: Simultaneous launch (March) vs Staggered (February iOS, April Android)
   - **Impact**: Resource allocation affects Q1 2025 revenue projections
   - **Recommendation**: Staggered approach reduces risk, allows iOS feedback integration
   - **Decision By**: End of week to maintain timeline

2. **Marketing Campaign Budget Adjustment** 🔶 MEDIUM PRIORITY
   - **Request**: Additional $15K for external design consultant
   - **Justification**: Quality improvement, 2-week delivery acceleration
   - **ROI Analysis**: Cost justified by projected $75K additional revenue
   - **Recommendation**: Approve - risk/reward ratio favorable

## 📈 Performance Metrics

| Project | Status | Velocity | Health | Next Milestone |
|---------|---------|----------|---------|----------------|
| Q4 Marketing | ✅ On Track | +15% | Excellent | Launch (Nov 15) |
| Mobile App V2 | ⚠️ At Risk | -10% | Good | Design Complete (Nov 30) |
| Infrastructure | 🎉 Completed | +25% | Excellent | Post-deploy monitoring |
| Design System | 🚫 Blocked | 0% | Poor | Resource assignment needed |

## 🔮 Predictive Insights

**Success Probability Analysis:**
- **Q4 Marketing Campaign**: 92% on-time completion (historical similar projects: 88%)
- **Mobile App V2**: 68% on-time completion (complexity factors reduce confidence)
- **Design System Update**: 15% on-time without intervention (blocked status critical)

**Resource Demand Forecast:**
- **November**: Sarah overallocated (120% capacity), consider support or timeline adjustment
- **December**: Team capacity available for Q1 2025 planning and preparation
- **Q1 2025**: Mobile app launch will require 80% of development resources

## 💡 Strategic Recommendations

🔴 **Immediate Actions (This Week)**
1. **Decision**: Mobile App V2 launch strategy decision required by Friday
2. **Resource**: Assign designer to unblock Design System Update
3. **Budget**: Approve $15K marketing consultant budget for Q4 campaign

🟡 **Strategic Planning (Next 2 Weeks)**
1. **Capacity Planning**: Address Sarah's overallocation across Q4 Marketing and Design System
2. **Risk Mitigation**: Develop contingency plan for Mobile App V2 delays
3. **Q1 Preparation**: Begin Q1 2025 project portfolio planning

🟢 **Process Optimization**
1. **Success Replication**: Apply Infrastructure project velocity patterns to future DevOps work
2. **Early Warning**: Implement weekly Design System status check to prevent future blocks
3. **Communication**: Establish weekly stakeholder updates for critical decision projects

## 📤 Stakeholder Communications

**For Executive Team:**
"This week delivered strong progress on Q4 Marketing (ahead of schedule) and completed the Infrastructure upgrade (immediate cost savings achieved). Two critical decisions needed: Mobile App V2 launch strategy (impacts Q1 revenue) and Design System resource assignment (blocking dependent projects). Overall portfolio health is good with clear action items identified."

**For Project Owners:**
"Weekly review complete - Q4 Marketing and Infrastructure showing excellent progress. Mobile App V2 needs decision support for timeline strategy. Design System requires immediate attention to unblock dependencies. Detailed recommendations and next steps provided for each project."

**Next Review:** {next_week_date} | **Decisions Pending:** 2 | **Projects Needing Attention:** 1
```

#### Monthly Strategic Review

```markdown
# 📊 Monthly Project Portfolio Review
**Review Period:** {month_name} {year}
**Portfolio Health Score:** {health_score}/10

## 🎯 Strategic Executive Summary

**Monthly Achievements:**
- **Portfolio Velocity**: {velocity_change} vs. previous month
- **Revenue Impact**: ${revenue_impact} from completed deliverables
- **Cost Optimization**: ${cost_savings} in operational improvements
- **Strategic Progress**: {strategic_milestones_completed} key milestones achieved

**Strategic Decision Points:**
1. **Q1 2025 Portfolio Prioritization**
   - Current capacity: {team_capacity} developer-months available
   - Project demand: {project_demand} developer-months required
   - **Gap Analysis**: {capacity_gap} over/under capacity
   - **Recommendation**: {prioritization_recommendation}

2. **Resource Investment Strategy**
   - High-performing areas: {high_performance_areas}
   - Investment opportunities: {investment_recommendations}
   - **Budget Impact**: ${investment_amount} recommended for optimal ROI

## 📈 Historical Trend Analysis

**Velocity Patterns (6-month view):**
- **Success Factors**: {success_patterns} consistently drive 20%+ velocity improvements
- **Risk Indicators**: {risk_patterns} predict delays with 85% accuracy
- **Seasonal Factors**: {seasonal_insights} affect December-January productivity

**Project Success Predictor Model:**
Based on {historical_projects} completed projects, success probability calculated by:
- On-time delivery: {complexity_factor} × {resource_factor} × {dependency_factor}
- Budget adherence: {scope_factor} × {team_experience_factor}
- Quality metrics: {testing_factor} × {review_factor}

## 🎯 Strategic Recommendations

**Portfolio Optimization:**
1. **High-Impact Focus**: Prioritize projects with >$100K revenue impact and <3 month delivery
2. **Resource Rebalancing**: Shift 20% capacity from maintenance to high-growth initiatives
3. **Risk Mitigation**: Implement early warning system for projects with <70% success probability

**Q1 2025 Strategic Initiatives:**
1. **Mobile First**: Accelerate mobile app completion for Q1 revenue capture
2. **Efficiency Gains**: Replicate infrastructure optimization patterns across other systems
3. **Market Expansion**: Begin Q2 expansion project planning with validated design system

**Investment Priorities:**
1. **Team Growth**: Add senior developer (Mobile App expertise) - ROI: 3.2x first year
2. **Tooling**: Implement automated project health monitoring - Cost: $25K, Time savings: 40%
3. **Process**: Establish cross-project resource optimization protocols

## 📊 Success Metrics & KPIs

| Metric | Current | Target | Trend | Action |
|---------|---------|---------|---------|---------|
| Portfolio Velocity | {velocity} | +15% | {trend} | {action} |
| On-time Delivery | {delivery_rate}% | 85% | {trend} | {action} |
| Budget Adherence | {budget_rate}% | 90% | {trend} | {action} |
| Quality Score | {quality}/10 | 8.5 | {trend} | {action} |
| Revenue Impact | ${revenue} | ${target} | {trend} | {action} |

**Next Strategic Review:** {next_month_date}
**Quarterly Planning Session:** {quarterly_date}
```

#### Stakeholder Email Template

```markdown
**Subject: Weekly Project Review - {date} | {critical_decisions_count} Decisions Needed**

Hi {stakeholder_name},

Here's this week's project review with key highlights and action items:

**🎯 Key Wins:**
- {project_name}: {achievement} - {business_impact}
- {project_name}: {achievement} - {business_impact}

**⚠️ Decisions Needed:**
1. **{decision_title}** (By: {deadline})
   - Options: {options_summary}
   - Recommendation: {recommendation}
   - Impact: {business_impact}

**📊 Portfolio Health:** {portfolio_health} | **Projects On Track:** {on_track_count}/{total_count}

**Next Steps:**
- {action_item_1}
- {action_item_2}

Full detailed review available [here](#). Let me know if you need any additional context or have questions about the recommendations.

Best regards,
{sender_name}

**Next Review:** {next_review_date}
```

### Implementation Steps

When executing this command:

1. **Load Project Portfolio Data**
   ```python
   import yaml
   import json
   from datetime import datetime, timedelta

   # Load projects configuration
   with open('.claude/projects.yaml', 'r') as f:
       projects = yaml.safe_load(f)

   # Load cached notes and historical data if available
   cache_files = glob.glob('.claude/cache/notes_*.json')
   historical_data = {}
   for cache_file in cache_files:
       with open(cache_file, 'r') as f:
           historical_data.update(json.load(f))
   ```

2. **Analyze Current State and Trends**
   ```python
   # Calculate project health scores
   # Analyze milestone completion rates
   # Identify velocity trends and patterns
   # Assess resource allocation and conflicts
   # Generate predictive insights based on historical patterns
   ```

3. **Generate Business Intelligence**
   ```python
   # Create actionable recommendations
   # Identify critical decision points
   # Generate stakeholder-ready communications
   # Prepare presentation-ready metrics and insights
   ```

4. **Format for Target Audience**
   ```python
   if format == "executive-summary":
       # Focus on business impact and strategic decisions
   elif format == "detailed":
       # Include technical details and implementation guidance
   elif format == "email":
       # Create stakeholder communication templates
   elif format == "presentation":
       # Generate slide-ready content with key metrics
   ```

### Integration with Existing Systems

**Project Data Sources:**
- `.claude/projects.yaml` - Primary project configuration and status
- `.claude/cache/notes_*.json` - Project-specific notes and insights
- GitHub repositories - Development activity and milestone progress
- Calendar integration - Meeting data and timeline analysis

**Historical Analysis:**
- Track milestone completion patterns over time
- Analyze resource allocation effectiveness
- Identify successful project patterns for replication
- Generate predictive models for project success probability

**Communication Integration:**
- Generate executive summaries for leadership
- Create detailed reports for project managers
- Draft stakeholder emails and communications
- Prepare presentation-ready content for meetings

### Error Handling

- **Missing Project Data**: Use available data and note limitations in output
- **Invalid Date Ranges**: Default to current week/month with warning
- **No Historical Data**: Generate current state analysis with note about limited predictions
- **Configuration Errors**: Validate project structure and provide helpful error messages

### Best Practices

1. **Regular Cadence**:
   - Weekly reviews for operational teams
   - Monthly reviews for strategic planning
   - Quarterly reviews for portfolio optimization

2. **Stakeholder Alignment**:
   - Tailor content to audience needs and expertise level
   - Focus on actionable insights and clear next steps
   - Include business impact and ROI considerations

3. **Historical Learning**:
   - Maintain review history for pattern analysis
   - Track prediction accuracy and improve models
   - Document successful interventions for replication

4. **Decision Support**:
   - Clearly identify decisions that require immediate attention
   - Provide options analysis with pros/cons
   - Include risk assessment and mitigation strategies

Remember: Effective project reviews transform data into actionable business intelligence that drives strategic decision-making and operational excellence.
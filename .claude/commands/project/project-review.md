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
   from tools import DataCollector, ConfigManager, HealthCalculator
   from datetime import datetime, timedelta

   config = ConfigManager()
   collector = DataCollector(config)
   calc = HealthCalculator()

   active_projects = [p for p in projects_data['projects'].values()
                     if p.get('status') in ['active', 'in_progress', 'planning']]
   ```

2. **Analyze Health Metrics and Trends**
   ```python
   # Calculate project health scores
   for project in active_projects:
       project_data = {
           "milestones": project.get("milestones", []),
           "github_data": project.get("github_data", {}),
           "blockers": project.get("blockers", []),
           "dependencies": project.get("dependencies", []),
           "start_date": project.get("start_date"),
           "target_date": project.get("target_date"),
       }

       # Get current health score
       health = calc.calculate_project_health(project_data)

       # Analyze trends if historical data available
       if project.get("historical_health_scores"):
           trends = calc.analyze_trends(
               project["historical_health_scores"],
               time_window=30
           )
           project["trend_analysis"] = trends

       # Calculate team performance metrics
       if project.get("team_data"):
           team_metrics = calc.calculate_team_performance(project["team_data"])
           project["team_performance"] = team_metrics

       # Predict completion
       if health.score > 0:
           timeline_progress = calc.calculate_timeline_progress(
               project.get("milestones", []),
               project.get("start_date"),
               project.get("target_date")
           )
           prediction = calc.predict_completion(
               current_progress=timeline_progress["percent_complete"] / 100,
               velocity=project.get("velocity", 1.0),
               remaining_work=timeline_progress["total_count"] - timeline_progress["completed_count"]
           )
           project["completion_prediction"] = prediction

       project["health_score"] = health
   ```

3. **Compare Period-over-Period Health**
   ```python
   # Compare current vs previous week health scores
   if previous_week_data:
       for project in active_projects:
           current_health = project.get("health_score")
           previous_health = previous_week_data.get(project["id"], {}).get("health_score")

           if current_health and previous_health:
               delta = current_health.score - previous_health.score
               project["health_delta"] = {
                   "value": delta,
                   "direction": "improving" if delta > 0 else "declining" if delta < 0 else "stable",
                   "percentage_change": (delta / previous_health.score * 100) if previous_health.score > 0 else 0
               }
   ```

4. **Present Comprehensive Review with HealthCalculator Insights**

**Monthly Strategic Review `/project review --monthly`:**

Execute strategic monthly analysis:

1. **Portfolio Analysis with HealthCalculator**
   ```python
   # Analyze portfolio-wide trends
   portfolio_health_scores = []

   for project in all_projects:
       project_data = {
           "milestones": project.get("milestones", []),
           "github_data": project.get("github_data", {}),
           "blockers": project.get("blockers", []),
           "dependencies": project.get("dependencies", []),
       }

       health = calc.calculate_project_health(project_data)
       portfolio_health_scores.append({
           "timestamp": datetime.now().isoformat(),
           "value": health.score,
           "project": project["id"]
       })

   # Analyze portfolio-wide trends (monthly view)
   portfolio_trends = calc.analyze_trends(portfolio_health_scores, time_window=90)

   # Calculate team performance across all projects
   team_metrics = calc.calculate_team_performance({
       "velocity": calculate_portfolio_velocity(),
       "quality_score": calculate_portfolio_quality(),
       "collaboration_score": calculate_portfolio_collaboration(),
       "throughput": sum(p.get("throughput", 0) for p in all_projects),
       "cycle_time": calculate_avg_cycle_time(all_projects),
   })
   ```

2. **Predictive Analytics with HealthCalculator**
   ```python
   # Project completion probability based on historical patterns
   for project in active_projects:
       # Assess risks using HealthCalculator
       risks = calc.assess_risks(project_data, thresholds=custom_thresholds)

       # Predict completion timeline
       prediction = calc.predict_completion(
           current_progress=project["progress"],
           velocity=project.get("velocity", 1.0),
           remaining_work=project["remaining_milestones"]
       )

       project["risk_assessment"] = risks
       project["completion_prediction"] = prediction

   # Success factor analysis using trend data
   successful_projects = [p for p in completed_projects if p.get("success_score", 0) > 0.8]
   success_trends = calc.analyze_trends(
       [{"timestamp": p["completion_date"], "value": p["success_score"]}
        for p in successful_projects],
       time_window=180
   )
   ```

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

| Project | Status | Velocity | Health Score | Trend | Next Milestone |
|---------|---------|----------|--------------|-------|----------------|
| Q4 Marketing | ✅ On Track | +15% | 0.88 (Excellent) ↗️ | +0.05 | Launch (Nov 15) |
| Mobile App V2 | ⚠️ At Risk | -10% | 0.72 (Good) ↘️ | -0.08 | Design Complete (Nov 30) |
| Infrastructure | 🎉 Completed | +25% | 0.92 (Excellent) ↗️ | +0.12 | Post-deploy monitoring |
| Design System | 🚫 Blocked | 0% | 0.42 (Poor) ↓ | -0.18 | Resource assignment needed |

**Health Score Components** (Q4 Marketing example):
- Timeline: 0.90 (30% weight) - 2 weeks ahead of schedule
- Activity: 0.85 (25% weight) - 45 commits this week vs 30 baseline
- Blockers: 1.00 (25% weight) - No active blockers
- Dependencies: 0.80 (20% weight) - All dependencies on track

## 📊 Trend Analysis (30-day view)

**Portfolio Health Trends:**
- **Direction:** Improving ↗️ (confidence: 0.85)
- **Average Health Score:** 0.73 → 0.76 (+4.1%)
- **Prediction:** Next week score: 0.78

**Project-Level Trends:**
- **Q4 Marketing**: Steady improvement, velocity increasing
  - Slope: +0.015/week | Confidence: 92%
  - Predicted completion: 95% on-time probability
- **Mobile App V2**: Declining trend, requires intervention
  - Slope: -0.020/week | Confidence: 78%
  - Predicted completion: 68% on-time probability
  - **Action Required:** Resource allocation or timeline adjustment

## 👥 Team Performance Metrics

**Overall Team Performance:**
- **Velocity Score:** 1.15 (15% above baseline)
- **Quality Score:** 0.88 (code review pass rate, bug density)
- **Collaboration Score:** 0.82 (PR review time, cross-team coordination)
- **Throughput:** 42 tasks/week (↑ 12% from last month)
- **Cycle Time:** 4.2 days average (↓ 0.8 days from last month)

**High-Performing Teams:**
- Infrastructure team: 1.35 velocity, 0.95 quality
- Marketing team: 1.20 velocity, 0.90 quality

**Teams Needing Support:**
- Design System team: 0.45 velocity (blocked), intervention needed

## 🔮 Predictive Insights (HealthCalculator)

**Completion Predictions:**
- **Q4 Marketing Campaign**:
  - ETA: November 12, 2024 (3 days early)
  - Confidence: 92% | Risk Level: Low
  - Current velocity: 1.15 tasks/day | Remaining: 8 tasks
  - Historical pattern match: 88% similar projects succeeded

- **Mobile App V2**:
  - ETA: December 8, 2024 (8 days late)
  - Confidence: 68% | Risk Level: Medium
  - Current velocity: 0.85 tasks/day | Remaining: 24 tasks
  - **Recommendation:** Increase resources or adjust timeline

- **Design System Update**:
  - ETA: Unable to predict (velocity = 0)
  - Confidence: 15% | Risk Level: High
  - Status: Blocked - requires immediate intervention
  - **Critical:** Resource assignment needed this week

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

## 📈 Historical Trend Analysis (HealthCalculator)

**Portfolio Health Trends (6-month view):**
- **Direction:** Improving ↗️ (slope: +0.008/week, confidence: 0.87)
- **Average Health Score:** 0.68 → 0.76 (+11.8% over 6 months)
- **Volatility:** Low (standard deviation: 0.05)
- **Prediction:** 3-month forecast: 0.82 (excellent range)

**Velocity Patterns:**
- **Success Factors**: Strong team collaboration (+0.15), clear requirements (+0.12), minimal blockers (+0.10)
  - Projects with these factors show 20%+ velocity improvements
- **Risk Indicators**: High blocker count (-0.18), unclear scope (-0.15), resource constraints (-0.12)
  - These patterns predict delays with 85% accuracy
- **Seasonal Factors**: December productivity dip (-15%), January recovery (+10%)

**Team Performance Trends:**
- **Velocity:** Steady improvement from 0.95 → 1.15 over 6 months
- **Quality Score:** Stable at 0.85-0.90 (high consistency)
- **Collaboration:** Improved from 0.72 → 0.82 (better cross-team work)
- **Cycle Time:** Reduced from 5.8 → 4.2 days (-28% improvement)

**Project Success Predictor Model (HealthCalculator-based):**
Based on 24 completed projects over 6 months:

- **On-time delivery probability:**
  - Health score > 0.80: 92% success rate
  - Health score 0.60-0.80: 71% success rate
  - Health score < 0.60: 34% success rate

- **Key Success Factors** (weight by impact):
  1. Timeline score > 0.85: +25% success probability
  2. Low blocker count (< 3): +20% success probability
  3. High activity score > 0.80: +18% success probability
  4. Strong dependencies (> 0.75): +15% success probability

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

1. **Load Project Portfolio Data with HealthCalculator**
   ```python
   from tools import DataCollector, ConfigManager, HealthCalculator
   from datetime import datetime, timedelta

   config = ConfigManager()
   collector = DataCollector(config)
   calc = HealthCalculator()

   # Load cached notes and historical data if available
   cache_files = glob.glob('.claude/cache/notes_*.json')
   historical_data = {}
   for cache_file in cache_files:
       with open(cache_file, 'r') as f:
           historical_data.update(json.load(f))
   ```

2. **Calculate Health Metrics and Analyze Trends**
   ```python
   # Calculate project health scores using HealthCalculator
   for project in active_projects:
       project_data = {
           "milestones": project.get("milestones", []),
           "github_data": project.get("github_data", {}),
           "blockers": project.get("blockers", []),
           "dependencies": project.get("dependencies", []),
           "start_date": project.get("start_date"),
           "target_date": project.get("target_date"),
       }

       # Get comprehensive health score
       health = calc.calculate_project_health(project_data)
       project["health_score"] = health

       # Analyze trends if historical data available
       if project.get("historical_health_scores"):
           trends = calc.analyze_trends(
               project["historical_health_scores"],
               time_window=30  # 30-day trend analysis
           )
           project["trend_analysis"] = trends

       # Calculate team performance metrics
       if project.get("team_data"):
           team_metrics = calc.calculate_team_performance(project["team_data"])
           project["team_performance"] = team_metrics

       # Predict completion using HealthCalculator
       timeline_progress = calc.calculate_timeline_progress(
           project.get("milestones", []),
           project.get("start_date"),
           project.get("target_date")
       )
       prediction = calc.predict_completion(
           current_progress=timeline_progress["percent_complete"] / 100,
           velocity=project.get("velocity", 1.0),
           remaining_work=timeline_progress["total_count"] - timeline_progress["completed_count"]
       )
       project["completion_prediction"] = prediction

       # Assess risks
       risks = calc.assess_risks(project_data)
       project["risk_assessment"] = risks
   ```

3. **Compare Period-over-Period Health**
   ```python
   # Load previous review data for comparison
   if previous_review_data:
       for project in active_projects:
           current_health = project["health_score"]
           previous_health = previous_review_data.get(project["id"], {}).get("health_score")

           if previous_health:
               delta = current_health.score - previous_health.score
               project["health_delta"] = {
                   "value": delta,
                   "direction": "improving" if delta > 0 else "declining" if delta < 0 else "stable",
                   "percentage_change": (delta / previous_health.score * 100) if previous_health.score > 0 else 0
               }
   ```

4. **Generate Business Intelligence**
   ```python
   # Create actionable recommendations based on HealthCalculator insights
   # Identify critical decision points using risk assessment
   # Generate stakeholder-ready communications with predictive insights
   # Prepare presentation-ready metrics including health scores and trends
   ```

5. **Format for Target Audience**
   ```python
   if format == "executive-summary":
       # Focus on business impact, health scores, and strategic decisions
       # Include trend analysis and completion predictions
   elif format == "detailed":
       # Include technical details, component breakdowns, and full metrics
       # Show detailed health score components and risk assessments
   elif format == "email":
       # Create stakeholder communication templates with key health metrics
       # Include actionable insights from HealthCalculator
   elif format == "presentation":
       # Generate slide-ready content with visualizable metrics
       # Health scores, trends, and predictions in presentable format
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
### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache for project data collection
- **Retry Logic**: Automatic retry with exponential backoff (3 attempts)
- **Graceful Degradation**: Continues with partial data when sources unavailable
- **Type Safety**: Pydantic models ensure data consistency

**HealthCalculator Benefits:**
- **Algorithmic Scoring**: Deterministic, reproducible health scores (0.0-1.0 scale)
- **Performance**: <50ms calculation time for all metrics
- **Trend Analysis**: Direction detection with confidence scores
- **Predictive Analytics**: Completion predictions with risk assessment
- **Team Metrics**: Comprehensive performance tracking
- **Risk Assessment**: Automated risk identification and prioritization
- **Type Safety**: Pydantic models for all data structures

**Performance:**
- Response time: ~4s → <1s for cached reviews
- HealthCalculator: <50ms per project health calculation
- Efficient multi-project analysis
- Reduced API calls by ~75% with caching
- Trend analysis: <100ms for 90-day historical data

### Benefits of HealthCalculator Integration

✅ **Data-Driven Reviews**: Objective metrics replace subjective assessments
- Consistent scoring methodology across all projects
- Reproducible results for historical comparison
- Evidence-based decision support

✅ **Predictive Intelligence**: Forward-looking insights
- Completion predictions with confidence intervals
- Trend analysis with direction detection
- Risk identification before issues materialize

✅ **Team Performance Visibility**: Quantified team metrics
- Velocity, quality, and collaboration scores
- Throughput and cycle time tracking
- High-performing vs struggling team identification

✅ **Period-over-Period Comparison**: Track improvements
- Health score deltas and percentage changes
- Trend visualization (improving/stable/declining)
- Historical pattern recognition

✅ **Simplified Implementation**: Replace 80+ lines of manual calculations
- Single tool call for comprehensive health scoring
- Built-in algorithms for all metrics
- Consistent methodology across commands

### Integration Notes
- Uses ConfigManager for type-safe project access
- DataCollector provides multi-source data (GitHub, notes, team)
- HealthCalculator adds algorithmic scoring and predictive analytics
- Automatic 5-minute caching for performance
- Centralized data collection and scoring in tested tools (87% coverage)

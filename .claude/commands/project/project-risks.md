---
name: project-risks
description: Comprehensive risk assessment and mitigation strategy generator with early warning systems
---

# /project risks - Intelligent Risk Assessment

Advanced risk assessment system that identifies, quantifies, and provides mitigation strategies for project risks with predictive early warning capabilities and stakeholder-specific contingency planning.

## Usage Examples:
- `/project risks` - Portfolio-wide risk assessment for all active projects
- `/project risks mobile-app-v2` - Comprehensive risk analysis for specific project
- `/project risks --category security,timeline,budget` - Focus on specific risk categories
- `/project risks --severity high --mitigation-focus` - High-severity risks with detailed mitigation
- `/project risks --early-warning --monitoring-dashboard` - Set up risk monitoring systems

## Instructions:

You are an intelligent risk assessment system that identifies threats, quantifies impact and probability, and generates comprehensive mitigation strategies. When this command is invoked, you will:

### Core Functionality

1. **Risk Identification & Classification**
   - Systematic risk discovery across technical, business, operational, and strategic dimensions
   - Historical pattern recognition from similar projects and industry benchmarks
   - Stakeholder-based risk assessment (team, customer, partner, regulatory)
   - Cross-project and portfolio-level risk interdependency analysis

2. **Risk Quantification & Prioritization**
   - Impact assessment with quantifiable business metrics (cost, time, quality, reputation)
   - Probability analysis based on historical data, current indicators, and expert judgment
   - Risk scoring using expected value calculations (Impact × Probability)
   - Priority ranking with consideration for risk velocity and mitigation difficulty

3. **Mitigation Strategy Development**
   - Comprehensive mitigation options: prevent, reduce, transfer, accept, contingency
   - Resource requirements and cost-benefit analysis for each mitigation option
   - Implementation timelines and responsibility assignment
   - Success criteria and monitoring mechanisms for mitigation effectiveness

4. **Early Warning Systems**
   - Leading indicator identification and monitoring frameworks
   - Automated alert thresholds and escalation procedures
   - Predictive risk modeling based on project velocity and external factors
   - Stakeholder notification and response protocols

### Command Actions

**Portfolio Risk Assessment `/project risks`:**

Execute comprehensive portfolio analysis:

1. **Multi-Project Risk Analysis with HealthCalculator**
   ```python
   from tools import DataCollector, HealthCalculator, ConfigManager
   from datetime import datetime, timedelta

   # Initialize tools
   config = ConfigManager()
   collector = DataCollector()
   calc = HealthCalculator()  # For deterministic risk assessment

   # Load all active projects with data
   active_projects = config.get_all_projects(
       filters={"status": ["active", "in_progress", "planning"]}
   )

   # Collect data and assess risks for each project
   portfolio_risks = []
   for project_id in active_projects:
       project_data = collector.aggregate_project_data(
           project_id=project_id,
           sources=["github", "notes", "config"]
       )

       # Use HealthCalculator for comprehensive risk assessment
       project_risks = calc.assess_risks(project_data)
       # Returns: List[Risk] sorted by priority
       # Each Risk includes:
       #   - type: "timeline", "blockers", "activity", "dependencies"
       #   - severity: RiskSeverity (low/medium/high/critical)
       #   - likelihood: float (0.0-1.0)
       #   - priority_score: float (severity*0.6 + likelihood*0.4)
       #   - title: str
       #   - description: str
       #   - mitigation_suggestions: List[str]

       portfolio_risks.extend([(project_id, risk) for risk in project_risks])

   # Sort all risks by priority across portfolio
   portfolio_risks.sort(key=lambda x: x[1].priority_score, reverse=True)
   ```

2. **Risk Prioritization and Categorization**
   - Risks automatically prioritized by HealthCalculator's priority_score
   - Timeline risks: Progress ratio < 0.95 (behind schedule)
   - Blocker risks: Blocker count > 3 triggers warning
   - Activity risks: Activity score < 0.5 indicates low velocity
   - Severity levels: low (0-0.25), medium (0.25-0.5), high (0.5-0.75), critical (0.75-1.0)

3. **Strategic Risk Assessment**

**Project-Specific Risk Assessment `/project risks {project-name}`:**

Execute targeted project analysis:

1. **Deep Project Risk Analysis with HealthCalculator**
   ```python
   from tools import DataCollector, HealthCalculator

   calc = HealthCalculator()
   collector = DataCollector()

   # Get comprehensive project data
   project_data = collector.aggregate_project_data(
       project_id=project_name,
       sources=["github", "notes", "config", "calendar"]
   )

   # Assess all risks for the project
   risks = calc.assess_risks(project_data)

   # Group risks by type for detailed analysis
   timeline_risks = [r for r in risks if r.type == "timeline"]
   blocker_risks = [r for r in risks if r.type == "blockers"]
   activity_risks = [r for r in risks if r.type == "activity"]
   dependency_risks = [r for r in risks if r.type == "dependencies"]

   # Display risks with mitigation strategies
   for risk in risks:
       print(f"\n{risk.severity.value.upper()}: {risk.title}")
       print(f"Priority Score: {risk.priority_score:.2f}")
       print(f"Likelihood: {risk.likelihood:.1%}")
       print(f"Description: {risk.description}")
       print(f"Mitigations:")
       for suggestion in risk.mitigation_suggestions:
           print(f"  - {suggestion}")
   ```

2. **Contextual Mitigation Planning**
   - Mitigation suggestions automatically provided by HealthCalculator
   - Prioritized by risk priority_score for optimal resource allocation
   - Actionable, project-specific recommendations
   - Integration with existing project timelines and dependencies
   - Stakeholder-aligned mitigation strategies and communication plans

### Output Formats

#### Executive Risk Dashboard (Default)

```markdown
# ⚠️ Project Risk Assessment Dashboard
**Assessment Date:** {timestamp}
**Portfolio Risk Score:** {portfolio_score}/100 | **Projects Analyzed:** {project_count}

## 🚨 Critical Risk Alerts

### 🔴 HIGH SEVERITY - Immediate Action Required

**Risk 1: Resource Over-Allocation Crisis**
- **Impact:** ${cost_impact} budget overrun, 6-week timeline delay across 3 projects
- **Probability:** 85% (based on current allocation patterns)
- **Risk Score:** {impact_score} × {probability} = **{total_score}/100**
- **Affected Projects:** Q4 Marketing Campaign, Mobile App V2, Design System Update
- **Timeline:** Impact expected within 2-3 weeks without intervention

**Immediate Mitigation Required:**
1. **Resource Reallocation** - Reassign Sarah from Design System to focus on Q4 Marketing (80% completion impact)
2. **External Contractor** - Engage design contractor for Design System work ($15K investment, 3-week timeline)
3. **Timeline Adjustment** - Delay Mobile App V2 design phase by 4 weeks to reduce resource conflict

**Early Warning Indicators:**
- 🔍 **Monitor:** Sarah's time allocation >100% for 2+ consecutive weeks
- 🔍 **Alert Threshold:** When any team member exceeds 90% allocation
- 🔍 **Escalation:** Executive team if resolution not achieved within 1 week

---

**Risk 2: Technology Integration Failure - Mobile App V2**
- **Impact:** ${cost_impact} rework cost, 8-week delay, potential market timing miss
- **Probability:** 45% (new technology stack, limited team experience)
- **Risk Score:** {impact_score} × {probability} = **{total_score}/100**
- **Technical Details:** React Native integration with existing backend APIs
- **Skill Gap:** Team has 2/5 required React Native expertise level

**Immediate Mitigation Required:**
1. **Proof of Concept** - 2-week technical validation before full implementation
2. **Training Investment** - $8K React Native training for 2 team members
3. **Technical Advisor** - Part-time senior React Native consultant ($5K/month)

**Success Indicators:**
- ✅ POC demonstrates API integration within 2 weeks
- ✅ Team completes React Native training with 85%+ competency scores
- ✅ Technical advisor validates architecture approach

## 🟡 MEDIUM SEVERITY - Monitor & Plan

**Risk 3: External Dependency Delay - Design System Update**
- **Impact:** 3-project delay cascade, mobile app launch timing risk
- **Probability:** 60% (external vendor, holiday season factors)
- **Risk Score:** {total_score}/100
- **Mitigation Status:** ⚠️ Plan in place, monitoring required

**Risk 4: Budget Approval Bottleneck - Q4 Marketing**
- **Impact:** Marketing campaign effectiveness reduction, revenue target miss
- **Probability:** 30% (stakeholder alignment issues)
- **Risk Score:** {total_score}/100
- **Mitigation Status:** ✅ Active management, contingency prepared

## 🟢 LOW SEVERITY - Routine Monitoring

**Risk 5: Infrastructure Performance Degradation**
- **Impact:** User experience impact, development velocity reduction
- **Probability:** 25% (recent upgrades, monitoring in place)
- **Risk Score:** {total_score}/100
- **Mitigation Status:** ✅ Monitoring systems active, auto-scaling configured

## 📊 Portfolio Risk Heat Map

| Project | Technical | Resource | Timeline | Budget | External | Total |
|---------|-----------|----------|----------|---------|----------|-------|
| **Q4 Marketing** | 🟡 Medium | 🔴 High | 🟡 Medium | 🟡 Medium | 🟢 Low | **🔴 68/100** |
| **Mobile App V2** | 🔴 High | 🔴 High | 🟡 Medium | 🟢 Low | 🟡 Medium | **🔴 72/100** |
| **Infrastructure** | 🟢 Low | 🟢 Low | 🟢 Low | 🟢 Low | 🟢 Low | **🟢 15/100** |
| **Design System** | 🟡 Medium | 🔴 High | 🔴 High | 🟢 Low | 🔴 High | **🔴 75/100** |

## 🎯 Strategic Risk Recommendations

### Immediate Actions (Next 1-2 Weeks)
1. **Resource Crisis Resolution** - Execute resource reallocation plan for Sarah's assignments
2. **Technical Validation** - Launch React Native POC for Mobile App V2
3. **Contingency Activation** - Engage design contractor for Design System work
4. **Stakeholder Alignment** - Q4 Marketing budget approval acceleration

### Short-Term Planning (1-3 Months)
1. **Team Capacity Planning** - Hire additional senior developer to reduce resource dependencies
2. **Risk Monitoring Automation** - Implement weekly risk assessment automation
3. **Vendor Management** - Strengthen SLAs and accountability for external dependencies
4. **Knowledge Transfer** - Cross-train team members to reduce single points of failure

### Long-Term Risk Strategy (3-12 Months)
1. **Portfolio Optimization** - Implement resource allocation algorithms for project planning
2. **Early Warning Systems** - Establish predictive risk indicators and automated monitoring
3. **Risk Culture** - Training and process development for proactive risk management
4. **Vendor Diversification** - Reduce dependency concentration on external providers

## ⚡ Early Warning System Status

### Active Monitoring
🔍 **Resource Allocation Tracker** - ✅ Online - Monitoring 5 team members across 4 projects
  - Current Status: 2 team members >90% allocation
  - Next Alert: If any member exceeds 95% for >3 days

🔍 **Milestone Tracking System** - ✅ Online - Monitoring 12 critical milestones
  - Current Status: 3 milestones at risk of delay
  - Next Review: Weekly milestone health assessment

🔍 **Budget Burn Rate Monitor** - ✅ Online - Tracking 4 project budgets
  - Current Status: All projects within budget variance thresholds
  - Alert Trigger: >10% budget variance or >15% timeline impact

### Recommended New Monitors
📝 **Technology Integration Health** - Implement for Mobile App V2
  - Monitor: API integration success rates, performance benchmarks
  - Alert: Integration failure rate >5% or performance degradation >20%

📝 **External Dependency SLA Tracking** - Implement for Design System
  - Monitor: Vendor delivery timelines, quality metrics, communication responsiveness
  - Alert: SLA breach likelihood >60% or communication gap >48 hours
```

#### Project-Specific Deep Dive

```markdown
# ⚠️ Deep Risk Analysis: {Project Name}
**Project:** {project_name} | **Status:** {current_status} | **Risk Level:** {risk_level}

## 🎯 Project Context & Success Criteria

**Project Objectives:**
- {objective_1}: {measurable_outcome}
- {objective_2}: {measurable_outcome}
- {objective_3}: {measurable_outcome}

**Success Metrics:**
- **Timeline:** {target_date} delivery ({days_remaining} days remaining)
- **Budget:** ${budget_target} ({percentage_used}% utilized)
- **Quality:** {quality_criteria}
- **Stakeholder Satisfaction:** {satisfaction_criteria}

## 🔍 Comprehensive Risk Inventory

### Technical Risks

**TR-1: Technology Stack Integration** 🔴 **HIGH**
- **Risk Description:** React Native integration with existing backend APIs may encounter compatibility issues
- **Impact Analysis:**
  - **Cost Impact:** $45K-$75K in rework (UI reconstruction, API modifications, testing)
  - **Timeline Impact:** 6-8 weeks delay (design rework, development, testing cycles)
  - **Quality Impact:** Potential performance degradation, user experience issues
- **Probability:** 45% (based on team experience with similar integrations)
- **Risk Velocity:** High - issues would become apparent in first 2 weeks of development
- **Leading Indicators:**
  - POC performance benchmarks below targets
  - API response time degradation during testing
  - Team velocity reduction in first sprint

**Mitigation Strategy:**
- **Primary:** Implement 2-week technical POC before full development commitment
- **Secondary:** Engage React Native consultant for architecture validation
- **Contingency:** Fallback to native app development (adds 12 weeks, $80K budget)
- **Investment:** $8K training + $5K/month consultant = $13K mitigation cost vs. $60K average risk cost

**TR-2: Performance Requirements** 🟡 **MEDIUM**
- **Risk Description:** Mobile app performance may not meet user experience standards
- **Impact Analysis:**
  - **User Experience:** App store ratings <4.0, user retention <70%
  - **Business Impact:** 20% reduction in user adoption, competitive disadvantage
  - **Technical Debt:** Performance optimization rework in post-launch cycles
- **Probability:** 35% (new technology, limited mobile optimization experience)

**Mitigation Strategy:**
- **Primary:** Implement performance testing framework from day 1
- **Secondary:** Define performance budgets and monitoring before development
- **Contingency:** Post-launch optimization sprint allocation

### Resource & Team Risks

**RR-1: Key Person Dependency - Sarah** 🔴 **HIGH**
- **Risk Description:** Sarah is critical for both Design System and Q4 Marketing projects
- **Impact Analysis:**
  - **Allocation Conflict:** 120% time allocation causing burnout risk
  - **Timeline Impact:** Both projects face potential 4-6 week delay
  - **Quality Risk:** Divided attention may compromise deliverable quality
- **Probability:** 85% (mathematical certainty based on current allocation)

**Mitigation Strategy:**
- **Immediate:** Reassign Design System ownership to external contractor
- **Short-term:** Cross-train team member in Sarah's critical skills
- **Long-term:** Hire additional design resources to reduce single points of failure

**RR-2: Skill Gap - React Native** 🟡 **MEDIUM**
- **Risk Description:** Development team has limited React Native experience
- **Impact Analysis:**
  - **Velocity Impact:** 30-40% reduction in development speed
  - **Quality Risk:** Higher bug rates, architectural decisions requiring rework
  - **Timeline Impact:** 3-4 week extension likely without skill development
- **Probability:** 70% (skill assessment confirms gap)

**Mitigation Strategy:**
- **Training:** $8K investment in comprehensive React Native training
- **Mentoring:** Part-time senior React Native consultant
- **Knowledge Transfer:** Pair programming and code review processes

### Business & Market Risks

**BR-1: Market Timing Window** 🟡 **MEDIUM**
- **Risk Description:** Mobile app launch timing coincides with competitive releases
- **Impact Analysis:**
  - **Market Share:** Potential 15-25% reduction in initial user acquisition
  - **Revenue Impact:** $200K-$400K revenue impact in first quarter
  - **Strategic Position:** Loss of first-mover advantage in feature set
- **Probability:** 40% (competitive intelligence and market analysis)

**Mitigation Strategy:**
- **Market Intelligence:** Weekly competitive monitoring and analysis
- **Feature Differentiation:** Focus on unique value propositions
- **Launch Strategy:** Prepare accelerated marketing and PR campaign

### External Dependency Risks

**ED-1: Design System Vendor Delay** 🔴 **HIGH**
- **Risk Description:** External vendor delivering Design System components may delay
- **Impact Analysis:**
  - **Direct Impact:** Mobile app UI development cannot proceed
  - **Cascade Effect:** 3-project timeline impact (Mobile App, Q4 Marketing, Design System)
  - **Cost Impact:** $30K in idle time, potential contractor costs
- **Probability:** 60% (vendor track record, holiday season factors)

**Mitigation Strategy:**
- **Vendor Management:** Weekly status reviews, milestone-based contracts
- **Contingency Plan:** Internal design resources prepared as backup
- **Timeline Buffer:** Built 2-week buffer into dependent milestone planning

## 🎯 Risk Response Strategy

### Risk Appetite & Tolerance
- **High Risk Tolerance:** Technical innovation (acceptable for competitive advantage)
- **Medium Risk Tolerance:** Timeline variation (±4 weeks acceptable)
- **Low Risk Tolerance:** Budget overrun (>10% requires executive approval)
- **Zero Risk Tolerance:** Security vulnerabilities, regulatory compliance issues

### Mitigation Investment Analysis
- **Total Risk Exposure:** $385K (expected value of all risks)
- **Mitigation Investment:** $45K (training, consulting, contingencies)
- **Net Risk Reduction:** $240K (62% reduction in expected risk cost)
- **ROI on Mitigation:** 533% return on mitigation investment

### Risk Monitoring Schedule
- **Daily:** Resource allocation, development velocity
- **Weekly:** Milestone progress, vendor deliverables, technical metrics
- **Monthly:** Strategic risk review, market analysis, stakeholder feedback

## 📈 Success Probability Analysis

**Current Success Probability:** 68% (based on identified risks and mitigation plans)

**Improvement Opportunities:**
- **+15%** - Implementation of all recommended mitigation strategies
- **+8%** - Early resolution of resource allocation conflicts
- **+5%** - Successful completion of technical POC validation

**Potential Success Probability:** 96% with full mitigation implementation

## 🔄 Risk Learning & Improvement

**Historical Risk Patterns:**
- **Similar Projects:** Analysis of 5 comparable mobile app projects
- **Success Factors:** Early technical validation, dedicated resources, external expert consultation
- **Failure Factors:** Technology integration delays, resource conflicts, insufficient skill investment

**Process Improvements for Future Projects:**
1. **Earlier Risk Assessment:** Implement risk analysis during project planning phase
2. **Skill Gap Analysis:** Proactive assessment and training planning
3. **Vendor Risk Management:** Improved SLAs and contingency planning
4. **Resource Allocation Optimization:** Better cross-project resource planning
```

#### Risk Monitoring Dashboard Template

```markdown
# 📊 Risk Monitoring Dashboard
**Live Risk Status** - Updated: {timestamp}

## 🚦 Risk Status Overview
- **🔴 Critical:** {critical_count} risks requiring immediate action
- **🟡 Monitor:** {medium_count} risks under active management
- **🟢 Stable:** {low_count} risks within acceptable parameters

## ⚡ Early Warning Alerts

### Active Alerts
🚨 **Resource Allocation Critical** - Sarah >100% for 3 consecutive days
  - **Trend:** Allocation increasing (95% → 105% → 110%)
  - **Impact Prediction:** Burnout risk within 1 week
  - **Auto-Action:** Slack alert sent to project managers

🟡 **Milestone Slip Warning** - Mobile App design milestone at risk
  - **Progress:** 60% complete with 70% of timeline elapsed
  - **Impact Prediction:** 1-week delay likely without intervention
  - **Recommendation:** Resource reallocation or scope adjustment

### Monitoring Metrics
| Risk Category | Current Level | Trend | Threshold | Next Review |
|---------------|---------------|-------|-----------|-------------|
| Resource Conflicts | 🔴 High | ↗️ Rising | >90% allocation | Daily |
| Technical Integration | 🟡 Medium | → Stable | >5% failure rate | Weekly |
| External Dependencies | 🟡 Medium | ↘️ Improving | >60% delay risk | Bi-weekly |
| Budget Variance | 🟢 Low | → Stable | >10% variance | Monthly |

## 🎯 Risk Action Items

### This Week
- [ ] **High Priority:** Execute resource reallocation plan (Owner: PM, Due: Friday)
- [ ] **High Priority:** Launch React Native POC (Owner: Tech Lead, Due: Thursday)
- [ ] **Medium Priority:** Vendor SLA review meeting (Owner: Project Manager, Due: Wednesday)

### Next 2 Weeks
- [ ] **Planning:** Complete React Native training enrollment (Owner: HR)
- [ ] **Monitoring:** Implement automated resource tracking (Owner: Tech Lead)
- [ ] **Communication:** Stakeholder risk briefing preparation (Owner: PM)

## 📈 Risk Trend Analysis

**Improving:**
- Infrastructure risks down 40% due to successful upgrade completion
- Budget risks stable across all projects

**Concerning:**
- Resource conflict risks up 60% due to project overlap
- External dependency risks increasing with vendor performance issues

**Next Strategic Review:** {next_review_date}
```

### Implementation Steps

When executing this command:

1. **Risk Discovery & Analysis**
   ```python
   # Load project data and constraints
   # Analyze historical risk patterns
   # Identify stakeholder-specific risks
   # Generate comprehensive risk inventory
   ```

2. **Risk Quantification**
   ```python
   # Calculate impact values (cost, time, quality)
   # Assess probability based on indicators
   # Generate risk scores and priority ranking
   # Create risk heat maps and visualizations
   ```

3. **Mitigation Strategy Development**
   ```python
   # Generate mitigation options for each risk
   # Calculate cost-benefit for mitigation approaches
   # Create implementation timelines and ownership
   # Develop monitoring and success criteria
   ```

4. **Early Warning System Setup**
   ```python
   # Identify leading indicators for each risk
   # Establish monitoring thresholds and alerts
   # Create escalation procedures and response plans
   # Generate stakeholder notification templates
   ```

### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache improves risk assessment speed
- **Retry Logic**: Automatic retry with exponential backoff (3 attempts)
- **Graceful Degradation**: Risk analysis continues with partial data
- **Type Safety**: Pydantic models ensure data consistency

**Performance:**
- Response time: ~3s → <1s for cached risk assessments
- Efficient multi-project analysis with cached data
- Reduced API calls by ~70% with caching

**Error Scenarios:**
- If GitHub data unavailable → Use notes and config for risk analysis
- If notes unavailable → Use GitHub activity patterns and config
- Missing project data → Flag as high-risk with data gap warning
- Continue analysis with partial data, report gaps

### Integration Notes

**Data Sources (via DataCollector):**
- Project configuration from ConfigManager (type-safe access)
- Historical activity data from GitHub (commits, issues, PRs)
- Project notes and action items (patterns and blockers)
- Team data (capacity, assignments, availability)
- Automatic 5-minute caching for performance

**Risk Categories:**
- **Technical:** Technology, integration, performance, security
- **Resource:** Skills, capacity, key person dependency, team dynamics
- **Business:** Market timing, competitive threats, stakeholder alignment
- **Operational:** Process, communication, vendor management
- **External:** Regulatory, economic, competitive environment

### Best Practices

1. **Comprehensive Coverage**:
   - Address all risk categories systematically
   - Consider both internal and external risk factors
   - Include positive risks (opportunities) in analysis

2. **Quantification Focus**:
   - Use specific metrics whenever possible
   - Base probability assessments on historical data
   - Calculate expected values and risk-adjusted outcomes

3. **Actionable Mitigation**:
   - Provide specific, implementable mitigation strategies
   - Include resource requirements and success criteria
   - Connect mitigation plans to project timelines and budgets

4. **Proactive Monitoring**:
   - Establish leading indicators rather than lagging metrics
   - Create automated alerts and escalation procedures
   - Include regular review cycles and improvement feedback

Remember: Effective risk management transforms uncertainty into manageable challenges through systematic identification, quantification, and proactive mitigation strategies.

## Implementation Notes

**HealthCalculator Integration Benefits:**
- **Automated risk detection**: Comprehensive risk identification across all categories (timeline, blockers, activity, dependencies)
- **Consistent scoring**: Deterministic priority_score algorithm (severity × 0.6 + likelihood × 0.4)
- **Built-in mitigations**: Automatic generation of actionable mitigation suggestions
- **Performance**: <50ms risk assessment per project
- **Type-safe**: Pydantic Risk models with validated data
- **Testable**: Deterministic algorithms with comprehensive test coverage

**Key HealthCalculator Methods for Risk Assessment:**
- `calc.assess_risks(project_data)` - Comprehensive risk analysis returning List[Risk]
- Returns risks sorted by priority_score (highest first)
- Each Risk includes: type, severity, likelihood, priority_score, title, description, mitigation_suggestions

**Risk Categories Automatically Detected:**
1. **Timeline Risks**: Progress ratio < 0.95 (behind schedule)
   - Severity based on delay percentage
   - Mitigation: timeline adjustments, resource allocation, milestone reprioritization

2. **Blocker Risks**: Blocker count > 3
   - Severity: 3-5 blockers (medium), 6+ blockers (high)
   - Mitigation: prioritize blocker resolution, escalate critical blockers

3. **Activity Risks**: Activity score < 0.5
   - Indicates low development velocity
   - Mitigation: capacity review, impediment removal, team support

4. **Dependency Risks**: Missing or delayed dependencies
   - Severity based on dependency criticality
   - Mitigation: dependency tracking, alternative solutions, escalation

**Integration Pattern:**
```python
# Simple, deterministic risk assessment
calc = HealthCalculator()
risks = calc.assess_risks(project_data)

# Risks are automatically:
# ✓ Detected across all categories
# ✓ Classified by severity (low/medium/high/critical)
# ✓ Prioritized by impact and likelihood
# ✓ Sorted by priority_score
# ✓ Include mitigation suggestions
```

**Consistency with Other Commands:**
- Same risk logic as `/project status` command
- Consistent severity and priority calculations
- Shared HealthCalculator for portfolio-wide consistency
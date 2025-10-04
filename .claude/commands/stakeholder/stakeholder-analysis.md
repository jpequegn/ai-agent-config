---
name: stakeholder-analysis
description: Advanced stakeholder analysis with power-interest mapping, influence network analysis, and engagement strategy development
---

# Stakeholder Analysis Engine

Advanced stakeholder analysis system that applies multiple analytical frameworks to understand stakeholder dynamics, influence patterns, and optimal engagement strategies for projects and organizational initiatives.

## Usage Examples:
- `/stakeholder-analysis --project mobile-app-v2 --framework power-interest` - Project-specific power-interest analysis
- `/stakeholder-analysis --decision api-redesign --stakeholders ceo-jane-smith,cto-mike-johnson` - Decision-focused stakeholder analysis
- `/stakeholder-analysis --framework network-influence --visualization` - Network influence mapping with visual output
- `/stakeholder-analysis --maturity-assessment --organization` - Organizational stakeholder engagement maturity
- `/stakeholder-analysis --conflict-potential --stakeholder-group executive-team` - Conflict analysis for stakeholder group

## Instructions:

You are an intelligent stakeholder analysis engine. When this command is invoked:

### Tool Integration

**Use StakeholderAnalyzer for comprehensive analysis:**

```python
from tools import StakeholderAnalyzer

# Initialize analyzer
analyzer = StakeholderAnalyzer()

# Example workflow for power-interest analysis
stakeholders = analyzer.identify_stakeholders({
    "decision_type": "technical",  # technical, strategic, budget, hiring
    "scope": "mobile-app-v2",
    "impact_areas": ["engineering", "product"],
    "stakeholders": []  # Optional: specific stakeholder IDs
})

# Calculate influence scores
influence_scores = analyzer.calculate_influence_scores(stakeholders, "technical")

# Map to power-interest grid
grid = analyzer.map_power_interest(stakeholders, {
    "decision_type": "technical",
    "scope": "mobile-app-v2"
})

# Assess alignment for decision options
alignment = analyzer.assess_alignment(
    stakeholders,
    decision_options=["Option A: React Native", "Option B: Flutter"],
    historical_patterns=None  # Optional
)

print(f"Identified {len(stakeholders)} stakeholders")
print(f"Overall support: {alignment.overall_support_score:.2f}")
print(f"Consensus likelihood: {alignment.consensus_likelihood:.2f}")
```

### Core Functionality

1. **Multi-Framework Analysis**
   - Apply power-interest grid, network influence, decision impact, and engagement maturity frameworks
   - Generate framework-specific insights and strategic recommendations
   - Cross-reference analysis results for comprehensive stakeholder understanding
   - Provide framework selection guidance based on analysis context

2. **Dynamic Stakeholder Assessment**
   - Analyze stakeholder positions, interests, and influence patterns
   - Assess stakeholder relationship dynamics and coalition potential
   - Identify stakeholder evolution trends and engagement opportunities
   - Generate predictive insights about stakeholder behavior and responses

3. **Strategic Insight Generation**
   - Develop stakeholder-specific engagement strategies and tactical approaches
   - Identify critical success factors and potential failure points
   - Generate risk mitigation strategies and contingency planning
   - Provide actionable recommendations with prioritization and timing

4. **Visual Analysis and Reporting**
   - Generate stakeholder maps, network diagrams, and influence visualizations
   - Create analysis reports with executive summaries and detailed findings
   - Provide comparative analysis across different frameworks and perspectives
   - Export analysis results in multiple formats for stakeholder communication

### Command Actions

**Power-Interest Analysis `/stakeholder-analysis --framework power-interest`:**

**Implementation with StakeholderAnalyzer:**
```python
# 1. Identify stakeholders
stakeholders = analyzer.identify_stakeholders(decision_context)

# 2. Map to power-interest grid
grid = analyzer.map_power_interest(stakeholders, decision_context)

# 3. Analyze by quadrant
manage_closely = grid.get_by_quadrant(PowerInterestQuadrant.MANAGE_CLOSELY)
keep_satisfied = grid.get_by_quadrant(PowerInterestQuadrant.KEEP_SATISFIED)
keep_informed = grid.get_by_quadrant(PowerInterestQuadrant.KEEP_INFORMED)
monitor = grid.get_by_quadrant(PowerInterestQuadrant.MONITOR)

# 4. Display results
for position in manage_closely:
    stakeholder = next(s for s in stakeholders if s.id == position.stakeholder_id)
    print(f"### {stakeholder.name} ({stakeholder.role})")
    print(f"  Power: {position.power_score:.2f} | Interest: {position.interest_score:.2f}")
    print(f"  Strategy: {position.reasoning}")
```

1. **Stakeholder Positioning**
   - Plot stakeholders on power-interest grid based on current context
   - Analyze stakeholder quadrant positioning and strategic implications
   - Generate quadrant-specific engagement strategies and communication approaches
   - Identify stakeholder movement patterns and repositioning opportunities

2. **Strategic Prioritization**
   - Rank stakeholders by engagement priority and resource allocation needs
   - Identify high-impact relationship development opportunities
   - Generate time and resource allocation recommendations
   - Provide stakeholder attention distribution guidance

3. **Engagement Strategy Development**
   - Develop quadrant-specific engagement approaches and tactics
   - Generate stakeholder-specific communication plans and messaging
   - Create engagement timeline and milestone recommendations
   - Provide success metrics and effectiveness measurement approaches

**Network Influence Analysis `/stakeholder-analysis --framework network-influence`:**

**Implementation with StakeholderAnalyzer:**
```python
# 1. Calculate comprehensive influence scores
influence_scores = analyzer.calculate_influence_scores(stakeholders, decision_type)

# 2. Sort by influence
sorted_stakeholders = sorted(
    influence_scores.items(),
    key=lambda x: x[1].overall_score,
    reverse=True
)

# 3. Display top influencers
print("### Central Influencers")
for stakeholder_id, score in sorted_stakeholders[:5]:
    stakeholder = next(s for s in stakeholders if s.id == stakeholder_id)
    print(f"| {stakeholder.name} | {score.overall_score:.2f} | "
          f"Power: {score.power_component:.2f}, Network: {score.network_component:.2f} |")

# 4. Identify coalition opportunities
alignment = analyzer.assess_alignment(stakeholders, decision_options)
print(f"\n### Coalition Opportunities")
for opportunity in alignment.coalition_opportunities:
    print(f"- {opportunity}")
```

1. **Influence Network Mapping**
   - Analyze stakeholder network positions and centrality metrics
   - Identify key influencers, bridges, and network connectors
   - Map influence pathways and decision-making chains
   - Assess network leverage points and strategic relationship opportunities

2. **Coalition and Alliance Analysis**
   - Identify potential stakeholder coalitions and alliance opportunities
   - Analyze stakeholder compatibility and shared interest areas
   - Generate coalition building strategies and activation approaches
   - Assess coalition stability and sustainability factors

3. **Strategic Network Positioning**
   - Recommend network positioning strategies for organizational advantage
   - Identify relationship development priorities for network optimization
   - Generate influence building strategies and relationship investment plans
   - Provide network evolution recommendations and monitoring approaches

**Decision Impact Analysis `/stakeholder-analysis --framework decision-impact`:**

**Implementation with StakeholderAnalyzer:**
```python
# 1. Assess alignment for decision options
alignment = analyzer.assess_alignment(
    stakeholders,
    decision_options=["Option A", "Option B"],
    historical_patterns=historical_data  # If available
)

# 2. Analyze support and resistance
print(f"### Alignment Analysis")
print(f"Overall Support: {alignment.overall_support_score:.2f}")
print(f"Consensus Likelihood: {alignment.consensus_likelihood:.2f}")
print(f"\n**Key Supporters:** {', '.join(alignment.key_supporters)}")
print(f"**Key Resistors:** {', '.join(alignment.key_resistors)}")

# 3. Detail individual stakeholder positions
print(f"\n### Individual Positions")
for sh_alignment in alignment.alignments:
    stakeholder = next(s for s in stakeholders if s.id == sh_alignment.stakeholder_id)
    print(f"\n**{stakeholder.name}**")
    print(f"  Status: {sh_alignment.alignment_status.value}")
    print(f"  Confidence: {sh_alignment.confidence:.2f}")
    print(f"  Key Concerns: {', '.join(sh_alignment.key_concerns)}")
    print(f"  Influence on Others: {sh_alignment.influence_on_others:.2f}")

# 4. Identify conflicts
conflicts = analyzer.identify_conflicts(alignment)
print(f"\n### Conflicts Detected: {len(conflicts)}")
for conflict in conflicts:
    print(f"- {conflict}")
```

1. **Stakeholder Impact Assessment**
   - Analyze how specific decisions affect different stakeholder groups
   - Assess stakeholder influence capability on decision outcomes
   - Identify timing sensitivities and critical decision dependencies
   - Generate stakeholder-specific decision communication strategies

2. **Decision Pathway Optimization**
   - Map optimal decision-making pathways through stakeholder networks
   - Identify decision bottlenecks and approval chain optimization opportunities
   - Generate stakeholder involvement strategies for decision acceleration
   - Provide decision risk mitigation approaches and contingency planning

**Engagement Maturity Assessment `/stakeholder-analysis --maturity-assessment`:**
1. **Current State Analysis**
   - Assess organizational stakeholder engagement maturity level
   - Identify engagement process strengths and improvement opportunities
   - Analyze stakeholder engagement capability gaps and development needs
   - Generate maturity improvement roadmap and capability building plan

2. **Maturity Enhancement Strategy**
   - Provide level-specific improvement recommendations and action plans
   - Generate capability development priorities and resource requirements
   - Create maturity progression timeline and milestone tracking
   - Provide maturity measurement and monitoring framework

### Analysis Output Templates

**Enhanced Power-Interest Grid Analysis (with StakeholderAnalyzer):**
```markdown
# ⚡ Power-Interest Stakeholder Analysis
**Project/Context:** {decision_context} | **Analysis Date:** {date}
**Stakeholders Analyzed:** {len(stakeholders)} | **Framework:** Power-Interest Grid
**Tool:** StakeholderAnalyzer | **Influence Scores:** Multi-dimensional

## 📊 Stakeholder Grid Positioning

### Manage Closely (High Power, High Interest)
| Stakeholder | Power | Interest | Overall Influence | Network | Authority | Engagement Strategy |
|-------------|-------|----------|-------------------|---------|-----------|---------------------|
| {name} | {power:.2f} | {interest:.2f} | {overall_score:.2f} | {network:.2f} | {authority:.2f} | {quadrant strategy} |

**Example with StakeholderAnalyzer data:**
```python
# From power-interest grid
for position in manage_closely:
    stakeholder = next(s for s in stakeholders if s.id == position.stakeholder_id)
    score = influence_scores[stakeholder.id]

    print(f"| {stakeholder.name} | {position.power_score:.2f} | "
          f"{position.interest_score:.2f} | {score.overall_score:.2f} | "
          f"{score.network_component:.2f} | {score.decision_authority:.2f} | "
          f"{position.quadrant.value} |")
```

**Strategic Implications:**
- High-influence stakeholders control {count} key decision areas
- Network effects amplify influence by {multiplier}x
- Coalition potential: {coalition_opportunities_count} high-value opportunities

**Engagement Priorities:**
1. Build coalition with {high_influence_supporters_count} high-influence supporters
2. Address concerns of {key_resistors_count} high-power resistors
3. Leverage {network_bridges_count} network bridges for cascading communication

### Keep Satisfied (High Power, Low Interest)
{similar format with StakeholderAnalyzer metrics}

## 🎯 Strategic Recommendations

**Data-Driven Insights from StakeholderAnalyzer:**
```python
# Alignment assessment results
print(f"Overall Support Score: {alignment.overall_support_score:.2f}")
print(f"Consensus Likelihood: {alignment.consensus_likelihood:.2f}")
print(f"Coalition Opportunities: {len(alignment.coalition_opportunities)}")
print(f"Conflict Areas: {len(alignment.conflict_areas)}")
```

**Critical Success Factors:**
- Secure buy-in from {len(alignment.key_supporters)} key supporters
- Mitigate concerns of {len(alignment.key_resistors)} resistors
- Consensus likelihood: {consensus_likelihood:.0%}

**Resource Allocation (Influence-Weighted):**
- High Priority (Influence >0.7): {high_priority_pct}% → {high_priority_count} stakeholders
- Medium Priority (Influence 0.4-0.7): {medium_priority_pct}% → {medium_priority_count} stakeholders
- Monitor (Influence <0.4): {monitor_pct}% → {monitor_count} stakeholders
```

**Enhanced Network Influence Analysis (with StakeholderAnalyzer):**
```markdown
# 🌐 Network Influence Analysis
**Analysis Scope:** {decision_context} | **Tool:** StakeholderAnalyzer
**Key Influencers:** {len(high_influence)} | **Multi-Dimensional Scoring:** Active

## 🔗 Influence Network Map

### Central Influencers (Sorted by Overall Influence)
| Stakeholder | Overall | Power | Network | Authority | Influence on Others | Strategic Value |
|-------------|---------|-------|---------|-----------|---------------------|-----------------|
| {name} | {overall:.2f} | {power:.2f} | {network:.2f} | {authority:.2f} | {influence_on_others:.2f} | {value} |

**Example with StakeholderAnalyzer:**
```python
# Calculate and sort by influence
influence_scores = analyzer.calculate_influence_scores(stakeholders, decision_type)
sorted_by_influence = sorted(
    influence_scores.items(),
    key=lambda x: x[1].overall_score,
    reverse=True
)

for stakeholder_id, score in sorted_by_influence[:10]:
    stakeholder = next(s for s in stakeholders if s.id == stakeholder_id)
    sh_alignment = next(a for a in alignment.alignments if a.stakeholder_id == stakeholder_id)

    print(f"| {stakeholder.name} | {score.overall_score:.2f} | "
          f"{score.power_component:.2f} | {score.network_component:.2f} | "
          f"{score.decision_authority:.2f} | {sh_alignment.influence_on_others:.2f} | "
          f"{calculate_strategic_value(score)} |")
```

### Coalition Opportunities (from AlignmentAnalysis)
**High Potential Coalitions:**
```python
# From alignment assessment
for opportunity in alignment.coalition_opportunities:
    print(f"- {opportunity}")

# High-influence supporters
high_influence_supporters = [
    a for a in alignment.alignments
    if a.alignment_status in [AlignmentStatus.STRONG_SUPPORT, AlignmentStatus.SUPPORT]
    and a.influence_on_others >= 0.7
]

print(f"\n**Coalition Strength:** {len(high_influence_supporters)} high-influence supporters")
print(f"**Combined Influence:** {sum(a.influence_on_others for a in high_influence_supporters):.2f}")
```

### Conflict Detection (from AlignmentAnalysis)
**Identified Conflicts:**
```python
conflicts = analyzer.identify_conflicts(alignment)
for conflict in conflicts:
    print(f"- {conflict}")

print(f"\n**Key Resistors:** {', '.join(alignment.key_resistors)}")
print(f"**Mitigation Priority:** {calculate_mitigation_priority(alignment)}")
```

## ⚡ Strategic Network Insights

**Leverage Points (Multi-Dimensional Analysis):**
1. High-influence supporters: Build coalition for {consensus_likelihood:.0%} consensus
2. Network bridges: Cascade communication through {network_connector_count} connectors
3. Decision authority: Engage {decision_authority_count} approval authorities early

**Relationship Investment Priorities (Influence-Weighted):**
- **Tier 1 (Influence >0.7):** {tier1_stakeholders} - Immediate engagement
- **Tier 2 (Influence 0.4-0.7):** {tier2_stakeholders} - Strategic cultivation
- **Tier 3 (Influence <0.4):** {tier3_stakeholders} - Maintain awareness
```

### Implementation Features

1. **Framework Intelligence**
   - Automatic framework selection based on analysis context and objectives
   - Multi-framework comparative analysis with cross-validation insights
   - Framework effectiveness measurement and optimization recommendations
   - Custom framework development for specific organizational needs

2. **Dynamic Analysis Engine**
   - Real-time stakeholder position tracking and analysis updates
   - Historical trend analysis and stakeholder evolution patterns
   - Predictive analytics for stakeholder behavior and relationship changes
   - Context-sensitive analysis adaptation for different projects and decisions

3. **Visual Analytics**
   - Interactive stakeholder maps with drill-down capabilities
   - Network diagrams with influence flow visualization
   - Power-interest grids with movement tracking and projection
   - Relationship strength visualization and health indicators

4. **Strategic Intelligence**
   - Automated insight generation with strategic implications analysis
   - Risk identification and mitigation strategy development
   - Opportunity recognition and tactical approach recommendations
   - Success probability assessment and optimization strategies

### StakeholderAnalyzer Integration Best Practices

1. **Tool-Driven Analysis Accuracy**
   - **Leverage Multi-Dimensional Scoring:** Use `calculate_influence_scores()` for objective, data-driven influence assessment
   - **Context-Aware Discovery:** Always provide complete decision context to `identify_stakeholders()` for accurate stakeholder identification
   - **Historical Pattern Integration:** Pass historical data to `assess_alignment()` when available for improved predictions
   - **Performance Monitoring:** Use `get_performance_stats()` to track analysis efficiency

   ```python
   # Example: Comprehensive analysis workflow
   analyzer = StakeholderAnalyzer()

   # 1. Discover stakeholders with full context
   stakeholders = analyzer.identify_stakeholders({
       "decision_type": "technical",
       "scope": "mobile-app-v2",
       "impact_areas": ["engineering", "product", "design"],
       "stakeholders": ["cto@company.com"]  # Include known key stakeholders
   })

   # 2. Calculate influence scores for prioritization
   influence_scores = analyzer.calculate_influence_scores(stakeholders, "technical")

   # 3. Map power-interest for strategic positioning
   grid = analyzer.map_power_interest(stakeholders, decision_context)

   # 4. Assess alignment for consensus building
   alignment = analyzer.assess_alignment(stakeholders, decision_options, historical_patterns)

   # 5. Generate communication strategy
   comm_plan = analyzer.generate_communication_plan(stakeholders, decision, templates)
   ```

2. **Framework Application with StakeholderAnalyzer**
   - **Power-Interest Grid:** Use `map_power_interest()` + `calculate_influence_scores()` for comprehensive stakeholder positioning
   - **Network Influence:** Leverage `influence_scores[id].network_component` and `alignment.influence_on_others` for network analysis
   - **Decision Impact:** Use `assess_alignment()` with decision options for data-driven impact assessment
   - **Coalition Building:** Extract from `alignment.coalition_opportunities` and filter by `influence_on_others >= 0.7`

3. **Strategic Value Creation with Data-Driven Insights**
   - **Quantified Prioritization:** Sort stakeholders by `overall_score` from influence analysis
   - **Evidence-Based Resource Allocation:** Weight engagement effort by influence scores (power × network × authority)
   - **Predictive Consensus Building:** Use `consensus_likelihood` to assess decision viability
   - **Automated Conflict Detection:** Leverage `identify_conflicts()` for proactive risk mitigation

4. **Performance Optimization**
   - **Batch Operations:** Load all stakeholders once, then run multiple analyses
   - **Caching:** StakeholderAnalyzer integrates with ConfigManager for automatic caching
   - **Parallel Analysis:** Run `map_power_interest()`, `calculate_influence_scores()`, and `assess_alignment()` with same stakeholder list
   - **Performance Tracking:** Monitor with `get_performance_stats()` for optimization opportunities

   ```python
   # Performance-optimized workflow
   stakeholders = analyzer.identify_stakeholders(context)  # Single load

   # Parallel analysis (reuses stakeholder data)
   grid = analyzer.map_power_interest(stakeholders, context)
   scores = analyzer.calculate_influence_scores(stakeholders, decision_type)
   alignment = analyzer.assess_alignment(stakeholders, options)

   # Check performance
   stats = analyzer.get_performance_stats()
   print(f"Average analysis time: {stats['average_time_ms']:.2f}ms")
   ```

### Success Metrics with StakeholderAnalyzer

**Quantifiable Outcomes:**
- ✅ **Stakeholder Coverage:** `len(stakeholders)` identified vs manual process
- ✅ **Influence Accuracy:** Multi-dimensional scores (power + network + authority) vs single-dimension estimates
- ✅ **Consensus Prediction:** `consensus_likelihood` score for decision confidence
- ✅ **Coalition Strength:** Sum of `influence_on_others` for supporter coalitions
- ✅ **Analysis Speed:** <50ms average (from `get_performance_stats()`)
- ✅ **Data-Driven Decisions:** Objective metrics replace subjective assessments

Always ensure stakeholder analysis leverages StakeholderAnalyzer for comprehensive, data-driven, and actionable strategic relationship development.
---
name: decide-stakeholder
description: Analyze stakeholder influence, map decision impact, and optimize stakeholder engagement for decision success
---

# Stakeholder Analysis and Engagement System

Comprehensive stakeholder intelligence system that maps stakeholder influence, analyzes decision impact, optimizes communication strategies, and builds consensus for successful decision implementation.

## Usage Examples:
- `/decide stakeholder "Mobile app technology stack"` - Map stakeholders for specific decision
- `/decide stakeholder --analyze john@company.com` - Analyze individual stakeholder profile and influence patterns
- `/decide stakeholder --map --decision mobile-tech-2024` - Generate stakeholder influence map for existing decision
- `/decide stakeholder --consensus "API redesign"` - Build consensus strategy with resistance analysis
- `/decide stakeholder --communication --template executive` - Generate stakeholder-specific communication plan
- `/decide stakeholder --feedback mobile-tech-2024` - Collect and analyze stakeholder feedback

## Instructions:

You are an intelligent stakeholder analysis and engagement system. When this command is invoked:

### Core Functionality

1. **Stakeholder Intelligence and Mapping**
   - Use StakeholderAnalyzer for comprehensive stakeholder analysis:
     ```python
     from tools import StakeholderAnalyzer

     analyzer = StakeholderAnalyzer()

     # Identify stakeholders based on decision context (100 lines → 4 lines)
     stakeholders = analyzer.identify_stakeholders({
         "decision_type": "technical",
         "scope": "mobile_app",
         "impact_areas": ["Engineering", "Product"],
     })

     # Generate power-interest grid (30 lines → 2 lines)
     grid = analyzer.map_power_interest(stakeholders, decision_context)
     high_priority = grid.get_by_quadrant(PowerInterestQuadrant.MANAGE_CLOSELY)

     # Assess alignment (40 lines → 3 lines)
     alignment = analyzer.assess_alignment(stakeholders, decision_options, historical_patterns)
     print(f"Support: {alignment.overall_support_score:.2f}")
     print(f"Consensus likelihood: {alignment.consensus_likelihood:.2f}")

     # Generate communication plan (30 lines → 2 lines)
     plan = analyzer.generate_communication_plan(stakeholders, decision)
     immediate = plan.get_immediate_communications()
     ```
   - Automatic power-interest grid calculations (<50ms)
   - Deterministic alignment assessment with confidence scoring
   - Coalition opportunity identification
   - Resistance mitigation strategy generation

2. **Impact Analysis and Communication Optimization**
   - Assess decision impact on each stakeholder group
   - Optimize communication strategies based on stakeholder preferences
   - Generate consensus-building roadmaps and resistance management plans
   - Design stakeholder-specific engagement approaches

3. **Engagement Tracking and Effectiveness**
   - Monitor stakeholder participation and response patterns
   - Track consensus building progress and resistance resolution
   - Analyze communication effectiveness and adjustment needs
   - Generate stakeholder satisfaction and engagement metrics

### OutputFormatter Integration for Decision Communications

**Use OutputFormatter to generate professional stakeholder communications for decisions:**

```python
from tools import StakeholderAnalyzer, OutputFormatter

# 1. Analyze decision and stakeholders with StakeholderAnalyzer
analyzer = StakeholderAnalyzer()
stakeholders = analyzer.identify_stakeholders(decision_context)
comm_plan = analyzer.generate_communication_plan(stakeholders, decision)
alignment = analyzer.assess_alignment(stakeholders, decision_options)

# 2. Format decision communications with OutputFormatter
formatter = OutputFormatter()

# Build stakeholder-specific decision update
decision_update = {
    'period': 'Decision Phase',
    'executive_summary': f'Decision on {decision_title} requires stakeholder alignment. Current support level: {alignment.overall_support_score:.0%}',
    'highlights': [
        f'{len(alignment.key_supporters)} key supporters identified',
        f'Consensus likelihood: {alignment.consensus_likelihood:.0%}',
        'Communication plan ready for immediate execution'
    ],
    'progress': {
        'overall': alignment.overall_support_score,
        'on_track': alignment.consensus_likelihood > 0.7,
        'target_date': decision_deadline
    },
    'challenges': [
        {
            'title': f'Stakeholder Resistance from {len(alignment.key_resistors)} groups',
            'description': f'Key concerns: {", ".join(alignment.key_resistor_concerns[:3])}',
            'impact': 'High - may delay decision implementation',
            'resolution': f'Targeted engagement plan for resistors: {", ".join(alignment.mitigation_strategies[:2])}'
        }
    ] if alignment.key_resistors else [],
    'upcoming_priorities': [
        'Execute stakeholder communication plan',
        'Address key resistor concerns',
        'Build supporting coalition',
        'Finalize decision with stakeholder buy-in'
    ],
    'next_steps': [
        {
            'action': message.content[:100] + '...',
            'owner': message.stakeholder_name,
            'deadline': message.timing
        }
        for message in comm_plan.messages[:5]
    ]
}

# Generate professional stakeholder update
output = formatter.stakeholder_update(decision_update, stakeholder="Decision Stakeholders")
print(output.content)
```

**Benefits:**
- Consistent decision communication format
- Professional stakeholder-facing documents
- Combines analytical power of StakeholderAnalyzer with formatting of OutputFormatter
- Reduces time to create stakeholder communications from hours to minutes

### Command Actions

**Stakeholder Mapping `/decide stakeholder "Decision Topic"`:**
- Identify all relevant stakeholders using StakeholderAnalyzer:
  ```python
  # Context-aware stakeholder identification (50 lines → 5 lines)
  stakeholders = analyzer.identify_stakeholders({
      "decision_type": "technical",  # or "strategic", "budget", "general"
      "scope": "mobile_app",
      "impact_areas": ["Engineering", "Product", "Design"],
  })

  # Calculate influence scores
  influence_scores = analyzer.calculate_influence_scores(stakeholders, decision_type="technical")

  # Get high-influence stakeholders
  high_influence = [s for s in stakeholders if influence_scores[s.id].overall_score >= 0.7]
  ```
- Generate power-interest grid with automatic quadrant classification
- Identify coalition opportunities and resistance patterns
- Provide tailored communication strategies for each stakeholder group

**Individual Stakeholder Analysis `/decide stakeholder --analyze {stakeholder-email}`:**
- Load and analyze individual stakeholder profile:
  ```python
  # Load specific stakeholder profile
  stakeholder_profiles = analyzer.load_stakeholder_profiles([stakeholder_email])
  stakeholder = stakeholder_profiles[0]

  # Calculate comprehensive influence metrics
  influence_score = analyzer.calculate_influence_scores([stakeholder])[stakeholder.id]

  # Assess communication preferences
  comm_plan = analyzer.generate_communication_plan([stakeholder], decision_context)
  message = comm_plan.messages[0]

  print(f"Communication Style: {message.tone}")
  print(f"Message Priority: {message.priority}")
  print(f"Preferred Channel: {message.message_type}")
  ```
- Analyze influence components (power, interest, network, authority)
- Generate personalized engagement strategy
- Identify key concerns and supporting factors

**Consensus Building Strategy `/decide stakeholder --consensus "Decision Topic"`:**
- Generate comprehensive consensus-building roadmap:
  ```python
  # Comprehensive alignment analysis (40 lines → 5 lines)
  alignment = analyzer.assess_alignment(
      stakeholders,
      decision_options=["Option A", "Option B"],
      historical_patterns=None  # Optional: use historical data if available
  )

  # Access consensus metrics
  print(f"Overall Support: {alignment.overall_support_score:.2%}")
  print(f"Consensus Likelihood: {alignment.consensus_likelihood:.2%}")
  print(f"Key Supporters: {alignment.key_supporters}")
  print(f"Key Resistors: {alignment.key_resistors}")
  print(f"Coalition Opportunities: {alignment.coalition_opportunities}")
  ```
- Identify coalition opportunities and resistance mitigation strategies
- Design stakeholder engagement sequence and communication plan
- Provide data-driven consensus building tactics

### Output Formats

#### Stakeholder Mapping Analysis

```markdown
# 👥 Stakeholder Analysis: {Decision Title}
**Decision Scope:** {decision_scope} | **Stakeholder Count:** {total_stakeholders}
**Analysis Date:** {analysis_date} | **Decision Deadline:** {deadline}

## 📊 Stakeholder Overview

### Influence and Impact Matrix
| Stakeholder | Role | Influence | Impact | Position | Engagement Priority |
|-------------|------|-----------|--------|----------|-------------------|
| {stakeholder_1} | {role} | {influence_level} | {impact_level} | {position} | {priority} |
| {stakeholder_2} | {role} | {influence_level} | {impact_level} | {position} | {priority} |

### Stakeholder Categorization
**Champions (High Influence + High Support):**
- **{Champion 1}** ({role}) - {champion_strategy}
- **{Champion 2}** ({role}) - {champion_strategy}

**Key Players (High Influence + Neutral/Unknown):**
- **{Key Player 1}** ({role}) - {engagement_strategy}
- **{Key Player 2}** ({role}) - {engagement_strategy}

**Potential Resistors (High Influence + Low Support):**
- **{Resistor 1}** ({role}) - {resistance_mitigation_strategy}
- **{Resistor 2}** ({role}) - {resistance_mitigation_strategy}

**Supporters (Low Influence + High Support):**
- **{Supporter 1}** ({role}) - {supporter_utilization_strategy}

**Observers (Low Influence + Low Impact):**
- **{Observer 1}** ({role}) - {minimal_engagement_approach}

## 🎯 Stakeholder Influence Analysis

### Power and Interest Grid
```chart
High Power, High Interest  | High Power, Low Interest
- {stakeholder_list}       | - {stakeholder_list}
- Strategy: {strategy}     | - Strategy: {strategy}

Low Power, High Interest   | Low Power, Low Interest
- {stakeholder_list}       | - {stakeholder_list}
- Strategy: {strategy}     | - Strategy: {strategy}
```

### Coalition Opportunities
**Natural Alliances:**
1. **{Coalition 1}** - {members}
   - **Shared Interests:** {common_interests}
   - **Coalition Strategy:** {approach_to_leverage}

2. **{Coalition 2}** - {members}
   - **Alignment Opportunity:** {alignment_basis}
   - **Engagement Approach:** {coalition_building_strategy}

**Strategic Partnerships:**
- **{Partnership}:** {stakeholder_1} + {stakeholder_2}
  - **Synergy:** {mutual_benefit_analysis}
  - **Activation Strategy:** {partnership_approach}

## 💬 Communication Strategy by Stakeholder

### Executive Leadership ({exec_stakeholders})
**Communication Approach:** {executive_strategy}
**Key Messages:**
- **Primary:** {primary_message_for_executives}
- **Supporting:** {supporting_points}
- **Value Proposition:** {executive_value_proposition}

**Preferred Channels:** {executive_communication_channels}
**Information Needs:** {executive_information_requirements}
**Decision Triggers:** {what_executives_need_to_approve}

### Technical Teams ({technical_stakeholders})
**Communication Approach:** {technical_strategy}
**Key Messages:**
- **Implementation Focus:** {technical_implementation_message}
- **Resource Requirements:** {resource_discussion_points}
- **Technical Benefits:** {technical_value_proposition}

**Information Needs:** {technical_information_requirements}
**Concerns to Address:** {anticipated_technical_concerns}
**Engagement Format:** {technical_engagement_preferences}

### Affected Users/Teams ({user_stakeholders})
**Communication Approach:** {user_strategy}
**Key Messages:**
- **Impact Explanation:** {user_impact_message}
- **Benefit Emphasis:** {user_benefit_messaging}
- **Change Management:** {user_change_support_message}

**Information Needs:** {user_information_requirements}
**Support Requirements:** {user_support_needs}
**Feedback Channels:** {user_feedback_mechanisms}

## 🚨 Resistance Analysis and Mitigation

### Identified Resistance Sources
**{Resistor Name}** - {resistance_level} resistance
- **Root Cause:** {underlying_concern_or_interest}
- **Manifestation:** {how_resistance_appears}
- **Impact:** {potential_impact_on_decision}
- **Mitigation Strategy:** {specific_approach_to_address}
- **Success Metrics:** {how_to_measure_mitigation_success}

### Resistance Mitigation Plan
**Phase 1: Understanding and Acknowledgment**
1. **{Action}** - {approach_to_understand_concerns}
2. **{Action}** - {acknowledgment_and_validation_strategy}

**Phase 2: Addressing Concerns**
1. **{Action}** - {specific_concern_resolution}
2. **{Action}** - {compromise_or_adjustment_strategy}

**Phase 3: Building Support**
1. **{Action}** - {support_building_approach}
2. **{Action}** - {ongoing_engagement_strategy}

### Risk Assessment
**High-Risk Scenarios:**
- **{Scenario}:** {resistance_escalation_possibility}
  - **Probability:** {likelihood_percentage}%
  - **Impact:** {impact_on_decision_process}
  - **Contingency:** {backup_strategy}

## 📈 Stakeholder Engagement Plan

### Engagement Sequence and Timeline
**Week 1: Initial Outreach**
- **{Stakeholder Group}:** {initial_engagement_approach}
- **{Stakeholder Group}:** {initial_engagement_approach}
- **Objective:** {week_1_objective}

**Week 2: Deep Consultation**
- **{Stakeholder Group}:** {consultation_format_and_approach}
- **{Stakeholder Group}:** {consultation_format_and_approach}
- **Objective:** {week_2_objective}

**Week 3: Consensus Building**
- **All Stakeholders:** {consensus_building_activities}
- **Coalitions:** {coalition_activation_approach}
- **Objective:** {week_3_objective}

**Week 4: Decision Finalization**
- **Decision Makers:** {final_decision_process}
- **Communication:** {decision_announcement_strategy}
- **Objective:** {week_4_objective}

### Engagement Tactics by Stakeholder Type
**High-Influence Champions:**
- **Tactics:** {champion_utilization_strategy}
- **Ask:** {specific_request_for_champions}
- **Support Provided:** {support_given_to_champions}

**High-Influence Neutrals:**
- **Tactics:** {neutral_conversion_strategy}
- **Information Sharing:** {information_strategy_for_neutrals}
- **Relationship Building:** {relationship_development_approach}

**High-Influence Resistors:**
- **Tactics:** {resistance_conversion_strategy}
- **Concern Addressing:** {concern_resolution_approach}
- **Compromise Opportunities:** {potential_compromises}

## 🎯 Consensus Building Strategy

### Consensus Metrics and Targets
**Current Consensus Level:** {current_consensus_percentage}%
**Target Consensus Level:** {target_consensus_percentage}%
**Timeline:** {consensus_building_timeline}

### Consensus Building Tactics
**Information Sharing:**
- **Transparency Level:** {information_sharing_approach}
- **Data Provision:** {data_and_evidence_sharing}
- **Q&A Sessions:** {question_handling_strategy}

**Participatory Decision-Making:**
- **Input Collection:** {stakeholder_input_methods}
- **Collaborative Analysis:** {collaborative_evaluation_approach}
- **Co-creation Opportunities:** {stakeholder_involvement_in_solution_design}

**Negotiation and Compromise:**
- **Negotiable Elements:** {aspects_open_to_negotiation}
- **Win-Win Opportunities:** {mutual_benefit_identification}
- **Trade-off Analysis:** {trade_off_negotiation_strategy}

### Consensus Checkpoints
**Checkpoint 1 ({date}):** {milestone_and_measurement}
- **Target:** {consensus_target_for_checkpoint}
- **Assessment Method:** {how_consensus_will_be_measured}
- **Adjustment Strategy:** {plan_if_consensus_not_achieved}

**Checkpoint 2 ({date}):** {milestone_and_measurement}
- **Target:** {consensus_target_for_checkpoint}
- **Escalation Criteria:** {when_to_escalate_or_adjust}

## 📝 Communication Scripts and Templates

### Executive Briefing Script
**Opening:** {executive_opening_message}
**Problem Statement:** {executive_problem_framing}
**Recommendation:** {executive_recommendation_delivery}
**Business Case:** {executive_business_justification}
**Ask:** {specific_executive_request}
**Next Steps:** {executive_next_steps}

### Technical Team Discussion Guide
**Context Setting:** {technical_context_message}
**Technical Requirements:** {technical_requirement_discussion}
**Implementation Approach:** {technical_implementation_discussion}
**Resource Needs:** {technical_resource_discussion}
**Concerns and Risks:** {technical_concern_handling}
**Collaboration Plan:** {technical_collaboration_approach}

### User Impact Communication
**Change Announcement:** {user_change_announcement}
**Benefit Explanation:** {user_benefit_communication}
**Impact Timeline:** {user_impact_timeline}
**Support Available:** {user_support_communication}
**Feedback Invitation:** {user_feedback_request}

## 📊 Stakeholder Feedback Analysis

### Feedback Collection Plan
**Collection Methods:**
- **Surveys:** {survey_approach_and_timing}
- **Interviews:** {interview_strategy_and_participants}
- **Focus Groups:** {focus_group_composition_and_approach}
- **Informal Feedback:** {informal_feedback_channels}

**Feedback Analysis Framework:**
- **Quantitative Metrics:** {quantitative_feedback_measures}
- **Qualitative Themes:** {qualitative_analysis_approach}
- **Sentiment Analysis:** {sentiment_tracking_method}
- **Concern Categorization:** {concern_classification_system}

### Feedback Integration Process
**Feedback Processing:**
1. **Collection and Aggregation:** {feedback_aggregation_method}
2. **Analysis and Categorization:** {feedback_analysis_process}
3. **Response Planning:** {feedback_response_strategy}
4. **Communication Back:** {feedback_closure_communication}

**Decision Adjustment Process:**
- **Adjustment Criteria:** {when_to_adjust_based_on_feedback}
- **Stakeholder Involvement:** {stakeholder_role_in_adjustments}
- **Communication Strategy:** {how_to_communicate_adjustments}

## 🔄 Ongoing Stakeholder Management

### Relationship Maintenance
**Regular Touchpoints:**
- **{Stakeholder Group}:** {ongoing_engagement_frequency_and_format}
- **{Stakeholder Group}:** {relationship_maintenance_approach}

**Value-Add Activities:**
- **Information Sharing:** {ongoing_information_value_provision}
- **Consultation Opportunities:** {ongoing_consultation_approach}
- **Recognition and Acknowledgment:** {stakeholder_recognition_strategy}

### Performance Monitoring
**Engagement Metrics:**
- **Participation Rate:** {participation_tracking}
- **Response Quality:** {response_quality_assessment}
- **Satisfaction Scores:** {satisfaction_measurement}
- **Influence Effectiveness:** {influence_impact_tracking}

**Relationship Quality Indicators:**
- **Trust Level:** {trust_measurement_approach}
- **Communication Effectiveness:** {communication_quality_assessment}
- **Collaboration Willingness:** {collaboration_readiness_tracking}

## 🎯 Success Metrics and KPIs

### Stakeholder Engagement Success
**Primary Metrics:**
- **Consensus Achievement:** Target {target}%, Current {current}%
- **Stakeholder Participation:** Target {target}%, Current {current}%
- **Resistance Resolution:** Target {target}%, Current {current}%
- **Communication Effectiveness:** Target {target}/10, Current {current}/10

**Secondary Metrics:**
- **Engagement Quality:** {quality_assessment}
- **Feedback Incorporation:** {feedback_integration_rate}
- **Relationship Strengthening:** {relationship_improvement_measure}

### Decision Implementation Support
**Implementation Readiness:**
- **Stakeholder Buy-in:** {buy_in_percentage}%
- **Resource Commitment:** {resource_commitment_level}
- **Change Readiness:** {change_readiness_assessment}

**Long-term Relationship Impact:**
- **Trust Maintenance:** {trust_level_post_decision}
- **Future Collaboration:** {future_collaboration_willingness}
- **Reputation Impact:** {reputation_effect_assessment}

This stakeholder analysis and engagement system ensures that decision-making processes are inclusive, transparent, and optimized for successful implementation through effective stakeholder management and consensus building.
```

### Implementation Features

**Built on StakeholderAnalyzer Tool** - Reduces implementation from 100+ lines to 15-20 lines:

1. **Intelligent Stakeholder Identification** (50 lines → 5 lines)
   - Context-aware discovery using `identify_stakeholders()`
   - Automatic filtering by decision type, scope, and impact areas
   - Integration with stakeholder database and contexts
   - Performance: <50ms for typical analysis

2. **Power-Interest Grid Analysis** (30 lines → 2 lines)
   - Automated quadrant classification with `map_power_interest()`
   - High-priority stakeholder identification
   - Coalition opportunity detection
   - Influence scoring with breakdown (power, interest, network, authority)

3. **Alignment Assessment** (40 lines → 3 lines)
   - Predictive consensus analysis using `assess_alignment()`
   - Support/opposition scoring with confidence levels
   - Key supporter and resistor identification
   - Conflict area detection and coalition opportunities

4. **Communication Planning** (30 lines → 2 lines)
   - Tailored message generation with `generate_communication_plan()`
   - Priority-based sequencing (high-influence first)
   - Channel and timing optimization
   - Resistance mitigation strategies

5. **Performance Monitoring**
   - Built-in performance tracking with `get_performance_stats()`
   - Average analysis time <50ms (4x faster than manual)
   - Deterministic, testable algorithms
   - Graceful error handling with partial results

### Error Handling

StakeholderAnalyzer provides automatic error handling with graceful degradation:

```python
from tools import StakeholderAnalyzer, StakeholderAnalyzerError

try:
    analyzer = StakeholderAnalyzer()

    # Identify stakeholders with error handling
    stakeholders = analyzer.identify_stakeholders({
        "decision_type": "technical",
        "scope": "mobile_app",
        "impact_areas": ["Engineering"],
    })

    if not stakeholders:
        print("No stakeholders found matching criteria. Broaden search parameters.")

    # Load specific profiles
    profiles = analyzer.load_stakeholder_profiles(["john@company.com"])

    if not profiles:
        print("Stakeholder profile not found. Check stakeholder_database.yaml")

except StakeholderAnalyzerError as e:
    # Handle analyzer-specific errors
    print(f"StakeholderAnalyzer error: {e}")
    print("Check configuration files: stakeholder_database.yaml, stakeholder_contexts.yaml")

except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error during stakeholder analysis: {e}")
    print("Verify configuration files exist and are properly formatted")
```

**Error Scenarios:**
- **No Stakeholders Found**: Empty list returned with guidance to broaden criteria
- **Missing Configuration**: StakeholderAnalyzerError with file guidance
- **Invalid Data**: Graceful degradation with partial results where possible
- **Performance**: <50ms analysis with automatic retry on transient failures

### Best Practices

1. **Comprehensive Stakeholder Mapping**
   - Include all directly and indirectly affected stakeholders
   - Analyze both formal and informal influence networks
   - Consider stakeholder evolution throughout decision process

2. **Tailored Communication Strategies**
   - Adapt communication style to stakeholder preferences and roles
   - Provide appropriate level of detail and technical depth
   - Use stakeholder-preferred channels and timing

3. **Proactive Resistance Management**
   - Identify potential resistance early in the process
   - Address underlying concerns rather than surface objections
   - Build coalitions to isolate and convert resistance

4. **Continuous Engagement Optimization**
   - Monitor engagement effectiveness and adjust strategies
   - Maintain relationship quality beyond individual decisions
   - Build stakeholder capacity for future decision participation

5. **Leverage StakeholderAnalyzer Capabilities**
   - Use identify_stakeholders() for context-aware discovery
   - Apply map_power_interest() for systematic priority classification
   - Utilize assess_alignment() for data-driven consensus prediction
   - Generate communication plans with generate_communication_plan()
   - Monitor performance with get_performance_stats() (<50ms target)

### Implementation Examples

**Complete Stakeholder Analysis Workflow:**
```python
from tools import StakeholderAnalyzer

# Initialize analyzer
analyzer = StakeholderAnalyzer()

# Step 1: Identify stakeholders (context-aware)
stakeholders = analyzer.identify_stakeholders({
    "decision_type": "technical",
    "scope": "mobile_app_tech_stack",
    "impact_areas": ["Engineering", "Product", "Design"],
})

# Step 2: Map power-interest positions
grid = analyzer.map_power_interest(stakeholders, {
    "decision_type": "technical",
    "scope": "mobile_app_tech_stack",
})

# Step 3: Assess alignment with decision options
alignment = analyzer.assess_alignment(
    stakeholders,
    decision_options=["React Native", "Flutter", "Native"],
)

# Step 4: Generate communication strategy
plan = analyzer.generate_communication_plan(
    stakeholders,
    decision={
        "title": "Mobile App Technology Stack Selection",
        "rationale": "Choose framework for Q1 2024 development",
    },
)

# Step 5: Extract insights
high_priority_stakeholders = grid.get_by_quadrant(PowerInterestQuadrant.MANAGE_CLOSELY)
print(f"High-priority stakeholders: {len(high_priority_stakeholders)}")
print(f"Support score: {alignment.overall_support_score:.2%}")
print(f"Consensus likelihood: {alignment.consensus_likelihood:.2%}")
print(f"Communication sequence: {plan.communication_sequence}")

# Performance monitoring
stats = analyzer.get_performance_stats()
print(f"Average analysis time: {stats['average_time_ms']:.2f}ms")
```

Always ensure stakeholder engagement is inclusive, transparent, and focused on building long-term relationships that support successful decision implementation and organizational effectiveness.
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
   - Use ConfigManager for type-safe stakeholder profile access:
     ```python
     from tools import ConfigManager
     from tools.schemas import StakeholderProfile

     mgr = ConfigManager()

     # Type-safe stakeholder access
     stakeholder = mgr.get_stakeholder("john@company.com")

     # Access strongly-typed fields
     print(f"Authority Level: {stakeholder.decision_authority_level}")
     print(f"Communication Style: {stakeholder.decision_preferences.communication_style}")
     print(f"Influence Factors: {stakeholder.influence_factors.technical_feasibility}")
     ```
   - Automatic schema validation via Pydantic models
   - <10ms cached reads for repeated stakeholder access
   - Analyze stakeholder influence, interests, and decision-making patterns
   - Map stakeholder relationships and coalition opportunities
   - Identify potential resistance sources and mitigation strategies

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

### Command Actions

**Stakeholder Mapping `/decide stakeholder "Decision Topic"`:**
- Identify all relevant stakeholders based on decision scope and impact using ConfigManager:
  ```python
  # Load all stakeholder profiles
  stakeholders_config = mgr.load_config("stakeholder_contexts.yaml")
  all_stakeholders = stakeholders_config.get("stakeholder_profiles", {})

  # Filter stakeholders by criteria
  high_influence = {
      email: profile
      for email, profile in all_stakeholders.items()
      if mgr.get_stakeholder(email).decision_authority_level in ["high", "executive"]
  }

  # Analyze communication preferences
  exec_stakeholders = [
      email for email, s in all_stakeholders.items()
      if mgr.get_stakeholder(email).decision_preferences.detail_level == "executive_summary"
  ]
  ```
- Analyze stakeholder influence levels, interests, and potential positions
- Generate stakeholder influence map with coalition and resistance analysis
- Provide communication strategy recommendations for each stakeholder group

**Individual Stakeholder Analysis `/decide stakeholder --analyze {stakeholder-email}`:**
- Deep dive into individual stakeholder profile using type-safe access:
  ```python
  stakeholder = mgr.get_stakeholder(stakeholder_email)

  # Access decision preferences
  comm_style = stakeholder.decision_preferences.communication_style
  detail_level = stakeholder.decision_preferences.detail_level
  risk_tolerance = stakeholder.decision_preferences.risk_tolerance

  # Access influence factors (stakeholder-specific)
  # Different stakeholders may have different influence factors
  # Check which factors are defined for this stakeholder
  if stakeholder.influence_factors.technical_feasibility:
      tech_weight = stakeholder.influence_factors.technical_feasibility
  if stakeholder.influence_factors.business_impact:
      business_weight = stakeholder.influence_factors.business_impact
  if stakeholder.influence_factors.operational_impact:
      ops_weight = stakeholder.influence_factors.operational_impact

  # Access notification preferences
  decision_updates = stakeholder.notification_preferences.decision_updates
  urgent_decisions = stakeholder.notification_preferences.urgent_decisions
  ```
- Analyze historical engagement effectiveness and preferences
- Generate personalized engagement strategy and communication approach
- Identify influence opportunities and potential concerns

**Consensus Building Strategy `/decide stakeholder --consensus "Decision Topic"`:**
- Generate comprehensive consensus-building roadmap
- Identify coalition opportunities and resistance mitigation strategies
- Design stakeholder engagement sequence and communication plan
- Provide scripts and talking points for stakeholder conversations

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

1. **Intelligent Stakeholder Identification**
   - Automatic stakeholder mapping based on decision scope and impact
   - Influence and interest analysis with coalition opportunity identification
   - Resistance pattern recognition and mitigation strategy development

2. **Communication Optimization**
   - Stakeholder-specific communication strategies and preferences
   - Automated script generation and template customization
   - Multi-channel engagement coordination and timing optimization

3. **Consensus Building Intelligence**
   - Systematic consensus building roadmaps with milestone tracking
   - Resistance analysis and conversion strategies
   - Coalition formation and strategic partnership facilitation

4. **Engagement Effectiveness Tracking**
   - Stakeholder participation and satisfaction monitoring
   - Communication effectiveness measurement and optimization
   - Relationship quality assessment and improvement planning

5. **Feedback Integration System**
   - Multi-channel feedback collection and analysis
   - Sentiment tracking and concern categorization
   - Decision adjustment recommendations based on stakeholder input

### Error Handling

ConfigManager provides automatic error handling for stakeholder profile access:

```python
from tools import ConfigManager, ConfigNotFoundError, ConfigValidationError

try:
    mgr = ConfigManager()
    stakeholder = mgr.get_stakeholder("john@company.com")

    # Type-safe field access
    authority = stakeholder.decision_authority_level
    comm_style = stakeholder.decision_preferences.communication_style

except KeyError as e:
    # Handle missing stakeholder profile
    print(f"Stakeholder not found: {e}")
    print("Available stakeholders:", list(mgr.load_config('stakeholder_contexts.yaml').get('stakeholder_profiles', {}).keys()))

except ConfigNotFoundError:
    # Handle missing configuration file
    print("Stakeholder contexts configuration not found. Please create stakeholder_contexts.yaml")

except ConfigValidationError as e:
    # Handle invalid stakeholder profile structure
    print(f"Invalid stakeholder profile: {e}")
    print("Please check that all required fields are present and properly formatted")
```

**Error Scenarios:**
- **Missing Stakeholder**: KeyError with clear message about which stakeholder was not found
- **Missing Config File**: ConfigNotFoundError with guidance to create stakeholder_contexts.yaml
- **Invalid Profile**: ConfigValidationError with details about which fields are missing or malformed
- **Type Safety**: Pydantic models prevent attribute access errors at runtime

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

5. **Type-Safe Profile Access**
   - Always use ConfigManager's get_stakeholder() for type safety
   - Leverage Pydantic model validation for data integrity
   - Use cached reads for performance optimization (<10ms)
   - Handle missing stakeholders gracefully with proper error messages

Always ensure stakeholder engagement is inclusive, transparent, and focused on building long-term relationships that support successful decision implementation and organizational effectiveness.
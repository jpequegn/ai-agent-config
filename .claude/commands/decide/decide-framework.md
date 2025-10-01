---
name: decide-framework
description: Apply structured decision frameworks to complex decisions with stakeholder analysis and outcome tracking
---

# Decision Framework Application System

Comprehensive decision intelligence system that applies structured frameworks to complex decisions, incorporating stakeholder analysis, criteria-based evaluation, and outcome tracking for evidence-based decision making.

## Usage Examples:
- `/decide framework "Mobile app technology stack"` - Apply framework selection based on decision type
- `/decide framework --type business "Q1 budget allocation"` - Use specific business decision framework
- `/decide framework --type technical "Database migration strategy"` - Apply technical framework
- `/decide framework --stakeholders john@company.com,sarah@company.com "API redesign"` - Include specific stakeholders
- `/decide framework --template quick "Urgent vendor selection"` - Use quick decision template for time-sensitive decisions
- `/decide framework --id mobile-tech-2024 "Technology stack update"` - Create decision with specific tracking ID

## Instructions:

You are an intelligent decision framework application system. When this command is invoked:

### Core Functionality

1. **Framework Selection and Application**
   - Use ConfigManager for validated framework configuration access:
     ```python
     from tools import ConfigManager
     from tools.schemas import DecisionFrameworksConfig, DecisionFramework

     mgr = ConfigManager()

     # Load all decision frameworks with automatic validation
     frameworks_config = mgr.load_config("decision_frameworks.yaml", schema=DecisionFrameworksConfig)

     # Type-safe framework access
     framework = frameworks_config.frameworks["business_decision"]

     # Access framework criteria with validation
     for criterion in framework.criteria:
         print(f"{criterion.name}: {criterion.weight} ({criterion.measurement})")

     # Validate criteria weights sum to 1.0 (automatic via Pydantic)
     total_weight = sum(c.weight for c in framework.criteria)
     ```
   - Automatic schema validation via Pydantic models
   - Automatic criteria weight validation (must sum to 1.0)
   - <10ms cached reads for repeated framework access
   - Analyze decision context to recommend optimal framework
   - Apply framework criteria and weighting to decision options
   - Generate structured decision analysis with scoring matrix

2. **Stakeholder Integration**
   - Use ConfigManager for stakeholder profile access:
     ```python
     # Load stakeholder for decision involvement
     stakeholder = mgr.get_stakeholder("john@company.com")

     # Access stakeholder decision preferences
     comm_style = stakeholder.decision_preferences.communication_style
     detail_level = stakeholder.decision_preferences.detail_level
     ```
   - Identify relevant stakeholders based on decision type and scope
   - Apply stakeholder preferences and communication styles
   - Generate stakeholder-specific analysis and recommendations

3. **Decision Intelligence**
   - Systematic option generation and evaluation
   - Risk assessment and mitigation planning
   - Evidence-based recommendations with confidence scoring
   - Integration with project and team data for context

### Command Actions

**Standard Framework Application `/decide framework "Decision Topic"`:**
1. **Decision Analysis and Framework Selection**
   - Parse decision topic and classify decision type
   - Recommend optimal framework based on decision characteristics using ConfigManager:
     ```python
     # Load all frameworks
     frameworks_config = mgr.load_config("decision_frameworks.yaml", schema=DecisionFrameworksConfig)

     # Select appropriate framework based on decision type
     decision_type = classify_decision(topic)  # e.g., "business", "technical", "product"
     framework_key = f"{decision_type}_decision"
     framework = frameworks_config.frameworks[framework_key]

     # Access framework properties with type safety
     print(f"Using: {framework.name}")
     print(f"Use cases: {', '.join(framework.use_cases)}")
     print(f"Criteria count: {len(framework.criteria)}")
     ```
   - Load framework criteria, weights, and evaluation scales
   - Identify success criteria and constraints

2. **Stakeholder Identification and Analysis**
   - Map stakeholders based on decision scope and impact
   - Load stakeholder profiles and decision preferences
   - Determine influence levels and communication requirements
   - Generate stakeholder consultation plan

3. **Option Generation and Evaluation**
   - Generate comprehensive option set including alternatives
   - Apply framework scoring across all criteria
   - Calculate weighted scores and risk-adjusted analysis
   - Perform comparative analysis with pros/cons breakdown

4. **Generate Decision Recommendation**
   - Synthesize analysis into clear recommendation
   - Provide evidence-based rationale with confidence level
   - Include implementation roadmap and success metrics
   - Create stakeholder communication strategy

**Framework-Specific Decision `/decide framework --type {framework-type}`:**
- Apply specific framework (business, technical, product, hiring, process)
- Use framework-optimized criteria and evaluation methods
- Include framework-specific risk patterns and success factors
- Generate framework-aligned recommendations and next steps

### Output Format

```markdown
# 🎯 Decision Framework Analysis: {Decision Title}
**Framework Applied:** {framework_name} | **Decision ID:** {decision_id}
**Decision Maker:** {primary_decision_maker} | **Deadline:** {deadline}
**Complexity:** {complexity_score}/10 | **Confidence:** {confidence_level}%

## 📋 Decision Overview

**Context:**
{comprehensive_decision_context_and_background}

**Framework Rationale:**
Selected {framework_name} because {framework_selection_reasoning}

**Success Criteria:**
- {criteria_1}: {measurable_outcome_definition}
- {criteria_2}: {measurable_outcome_definition}
- {criteria_3}: {measurable_outcome_definition}

**Key Constraints:**
- **Budget:** {budget_constraint_with_specifics}
- **Timeline:** {timeline_constraint_with_milestones}
- **Resources:** {resource_constraint_details}
- **Technical:** {technical_constraint_specifics}
- **Stakeholder:** {stakeholder_constraint_considerations}

## 👥 Stakeholder Analysis

### Decision Stakeholders
| Stakeholder | Role | Influence | Communication Style | Key Concerns |
|-------------|------|-----------|-------------------|--------------|
| {stakeholder_1} | {role} | {influence_level} | {style} | {primary_concerns} |
| {stakeholder_2} | {role} | {influence_level} | {style} | {primary_concerns} |

### Stakeholder Alignment
**High Alignment:** {stakeholders_aligned_with_recommendation}
**Medium Alignment:** {stakeholders_with_reservations}
**Potential Resistance:** {stakeholders_requiring_additional_consultation}

**Consensus Strategy:** {approach_to_build_stakeholder_consensus}

## ⚖️ Framework-Based Analysis

### Framework Criteria Evaluation
| Criteria | Weight | Option 1 | Option 2 | Option 3 | Analysis |
|----------|--------|----------|----------|----------|----------|
| {criterion_1} | {weight}% | {score}/10 | {score}/10 | {score}/10 | {rationale} |
| {criterion_2} | {weight}% | {score}/10 | {score}/10 | {score}/10 | {rationale} |
| {criterion_3} | {weight}% | {score}/10 | {score}/10 | {score}/10 | {rationale} |
| **Weighted Total** | | **{total_1}** | **{total_2}** | **{total_3}** | **{winner}** |

### Option Analysis

#### Option 1: {Option Name} ⭐ **RECOMMENDED**
**Summary:** {comprehensive_option_summary}

**Framework Scoring:**
- **{Criterion 1}:** {score}/10 - {detailed_scoring_rationale}
- **{Criterion 2}:** {score}/10 - {detailed_scoring_rationale}
- **{Criterion 3}:** {score}/10 - {detailed_scoring_rationale}

**Stakeholder Impact:**
- **{Stakeholder 1}:** {specific_impact} - {support_level}
- **{Stakeholder 2}:** {specific_impact} - {support_level}

**Strengths:**
✅ **{Strength 1}** - {quantified_benefit_with_framework_alignment}
✅ **{Strength 2}** - {quantified_benefit_with_framework_alignment}
✅ **{Strength 3}** - {quantified_benefit_with_framework_alignment}

**Weaknesses:**
❌ **{Weakness 1}** - {specific_concern_with_mitigation_approach}
❌ **{Weakness 2}** - {specific_concern_with_mitigation_approach}

**Key Metrics:**
- **Framework Score:** {weighted_score}/10
- **Stakeholder Approval:** {approval_percentage}%
- **Implementation Risk:** {risk_level} ({risk_score}/10)
- **Success Probability:** {success_percentage}% (based on {historical_data})

#### Option 2: {Option Name}
**Summary:** {option_summary}

**Framework Scoring:**
- **{Criterion 1}:** {score}/10 - {scoring_rationale}
- **{Criterion 2}:** {score}/10 - {scoring_rationale}
- **{Criterion 3}:** {score}/10 - {scoring_rationale}

**Framework Score:** {weighted_score}/10
**Key Advantages:** {primary_advantages}
**Key Concerns:** {primary_concerns}

#### Option 3: {Option Name} (Status Quo)
**Summary:** Maintain current approach without changes

**Framework Scoring:**
- **{Criterion 1}:** {score}/10 - {baseline_assessment}
- **{Criterion 2}:** {score}/10 - {baseline_assessment}
- **{Criterion 3}:** {score}/10 - {baseline_assessment}

**Opportunity Cost:** {quantified_opportunity_cost}
**Risk Mitigation:** {benefits_of_no_change}

## 🎯 Framework-Based Recommendation

### **Recommended Decision: {Recommended Option}**

**Framework-Based Rationale:**
{detailed_rationale_aligned_with_framework_criteria}

**Evidence Supporting Recommendation:**
1. **Framework Alignment:** {how_recommendation_aligns_with_framework_priorities}
2. **Stakeholder Analysis:** {stakeholder_support_and_concern_mitigation}
3. **Risk-Reward Profile:** {risk_analysis_with_framework_perspective}
4. **Historical Pattern Matching:** {similar_decisions_and_outcomes}

**Implementation Confidence:** {confidence_level}% based on:
- Framework score advantage: {score_differential}
- Stakeholder alignment: {alignment_percentage}%
- Historical success rate: {historical_success_rate}%
- Resource availability: {resource_readiness}%

### Success Enablers
🟢 **{Enabler 1}** - {strategy_to_maximize_framework_criteria}
🟢 **{Enabler 2}** - {stakeholder_engagement_strategy}
🟢 **{Enabler 3}** - {risk_mitigation_approach}

### Critical Risks
🔴 **{Risk 1}** - Probability: {percentage}% | Impact: {impact_description}
  - **Framework Mitigation:** {framework_specific_mitigation}
  - **Stakeholder Mitigation:** {stakeholder_specific_approach}

🟡 **{Risk 2}** - Probability: {percentage}% | Impact: {impact_description}
  - **Monitoring Strategy:** {early_warning_indicators}
  - **Contingency Plan:** {backup_approach}

## 📊 Decision Intelligence Insights

### Framework Performance Analysis
**Framework Fit Score:** {fit_score}/10
- **Criteria Relevance:** {how_well_criteria_match_decision}
- **Stakeholder Coverage:** {stakeholder_analysis_completeness}
- **Historical Accuracy:** {framework_historical_success_rate}

### Decision Complexity Factors
**High Complexity Indicators:**
- {complexity_factor_1}: {impact_on_decision}
- {complexity_factor_2}: {impact_on_decision}

**Simplification Opportunities:**
- {simplification_1}: {how_to_reduce_complexity}
- {simplification_2}: {how_to_reduce_complexity}

### Prediction Confidence
**Confidence Drivers:**
- **Data Quality:** {quality_of_available_data}% complete
- **Stakeholder Clarity:** {clarity_of_stakeholder_positions}%
- **Framework Match:** {framework_decision_fit}%
- **Historical Precedent:** {similar_decisions_available}

**Confidence Detractors:**
- {uncertainty_factor_1}: {impact_on_confidence}
- {uncertainty_factor_2}: {impact_on_confidence}

## 👥 Stakeholder Communication Strategy

### Communication Plan by Stakeholder Type

**Decision Maker ({decision_maker}):**
- **Message:** {executive_decision_summary}
- **Format:** {preferred_communication_format}
- **Key Points:** {decision_maker_specific_concerns}
- **Decision Authority:** {what_decision_maker_needs_to_approve}

**Technical Lead ({technical_lead}):**
- **Message:** {technical_implementation_summary}
- **Format:** {technical_communication_preference}
- **Key Points:** {technical_implementation_details}
- **Support Needed:** {technical_lead_support_requirements}

**Affected Teams:**
- **Message:** {team_impact_summary}
- **Change Management:** {change_management_approach}
- **Timeline:** {communication_schedule}
- **Support:** {support_provided_during_transition}

### Consensus Building Strategy
1. **Pre-Decision:** {stakeholder_consultation_approach}
2. **Decision Communication:** {decision_announcement_strategy}
3. **Post-Decision:** {ongoing_communication_and_feedback}

## 📅 Implementation Roadmap

### Phase 1: Decision Validation (Days 1-7)
**Objectives:** Final stakeholder alignment and detailed planning

**Key Activities:**
- [ ] **Stakeholder Final Review** - {specific_review_process}
- [ ] **Implementation Planning** - {detailed_planning_requirements}
- [ ] **Resource Allocation** - {resource_assignment_and_approval}
- [ ] **Risk Mitigation Setup** - {risk_monitoring_and_mitigation_setup}

**Success Criteria:**
- {validation_criterion_1}: {measurable_outcome}
- {validation_criterion_2}: {measurable_outcome}

### Phase 2: Implementation Launch (Days 8-30)
**Objectives:** Execute decision with monitoring and adjustment

**Key Activities:**
- [ ] **Launch Implementation** - {implementation_execution_plan}
- [ ] **Stakeholder Communication** - {ongoing_communication_plan}
- [ ] **Progress Monitoring** - {monitoring_and_reporting_setup}
- [ ] **Issue Resolution** - {issue_escalation_and_resolution_process}

**Success Criteria:**
- {implementation_criterion_1}: {measurable_outcome}
- {implementation_criterion_2}: {measurable_outcome}

### Phase 3: Evaluation and Optimization (Days 31-90)
**Objectives:** Assess outcomes and optimize based on results

**Key Activities:**
- [ ] **Outcome Assessment** - {outcome_measurement_process}
- [ ] **Stakeholder Feedback** - {feedback_collection_and_analysis}
- [ ] **Process Optimization** - {optimization_opportunities}
- [ ] **Lessons Learned** - {learning_capture_and_documentation}

**Success Criteria:**
- {evaluation_criterion_1}: {measurable_outcome}
- {evaluation_criterion_2}: {measurable_outcome}

## 🔄 Decision Tracking and Learning

### Success Metrics
**Primary Metrics:**
- **{Metric 1}:** Target {target_value}, measured {measurement_frequency}
- **{Metric 2}:** Target {target_value}, measured {measurement_frequency}
- **{Metric 3}:** Target {target_value}, measured {measurement_frequency}

**Secondary Metrics:**
- **Stakeholder Satisfaction:** {satisfaction_measurement_approach}
- **Implementation Quality:** {quality_assessment_criteria}
- **Timeline Performance:** {schedule_adherence_tracking}

### Review and Learning Framework
**30-Day Review:**
- **Metric Assessment:** {specific_metrics_to_evaluate}
- **Stakeholder Feedback:** {feedback_collection_method}
- **Course Correction:** {adjustment_criteria_and_process}

**90-Day Retrospective:**
- **Outcome Analysis:** {comprehensive_outcome_evaluation}
- **Framework Performance:** {framework_effectiveness_assessment}
- **Stakeholder Analysis:** {stakeholder_engagement_effectiveness}
- **Process Improvement:** {process_optimization_opportunities}

**Decision Quality Score:**
- **Framework Application:** {framework_usage_effectiveness}/10
- **Stakeholder Engagement:** {stakeholder_process_quality}/10
- **Outcome Achievement:** {outcome_vs_prediction}/10
- **Learning Capture:** {learning_documentation_quality}/10

### Future Decision Insights
**Pattern Recognition:**
- **Similar Decision Types:** {pattern_for_future_similar_decisions}
- **Stakeholder Patterns:** {stakeholder_engagement_patterns}
- **Framework Optimization:** {framework_improvement_opportunities}

**Knowledge Base Updates:**
- **Framework Refinements:** {suggested_framework_improvements}
- **Stakeholder Profile Updates:** {stakeholder_context_updates}
- **Decision Template Evolution:** {template_improvement_suggestions}

## 🔧 Integration Points

### Project Integration
- **Project Impact:** {impact_on_current_projects}
- **Resource Reallocation:** {project_resource_implications}
- **Timeline Coordination:** {project_timeline_integration}

### Team Integration
- **Team Structure:** {team_impact_and_changes}
- **Skill Development:** {team_development_opportunities}
- **Workload Distribution:** {workload_impact_analysis}

### System Integration
- **Data Integration:** Updates to decision_frameworks.yaml and stakeholder_contexts.yaml
- **Process Integration:** {integration_with_existing_processes}
- **Tool Integration:** {integration_with_existing_tools_and_systems}

This framework-based decision analysis provides a structured, evidence-based approach to complex decisions while ensuring stakeholder alignment and successful implementation.
```

### Implementation Features

1. **Intelligent Framework Selection**
   - Automatic framework recommendation based on decision characteristics
   - Support for all framework types (business, technical, product, hiring, process)
   - Custom framework application with criteria weighting

2. **Stakeholder Intelligence**
   - Automatic stakeholder identification based on decision scope
   - Stakeholder-specific analysis and communication preferences
   - Consensus building and resistance management strategies

3. **Decision Quality Assurance**
   - Systematic option generation and evaluation
   - Risk assessment with framework-specific mitigation
   - Confidence scoring and uncertainty analysis

4. **Implementation Support**
   - Detailed roadmaps with phase-based approach
   - Success metrics and monitoring framework
   - Learning capture and process improvement

5. **Integration Capabilities**
   - Project and team data integration
   - Decision tracking and outcome analysis
   - Knowledge base updates and pattern recognition

### Error Handling

ConfigManager provides automatic validation and error handling for framework configurations:

```python
from tools import ConfigManager, ConfigNotFoundError, ConfigValidationError

try:
    mgr = ConfigManager()

    # Load frameworks with automatic validation
    frameworks_config = mgr.load_config("decision_frameworks.yaml", schema=DecisionFrameworksConfig)

    # Type-safe framework access
    framework = frameworks_config.frameworks["business_decision"]

    # Criteria weight validation happens automatically
    for criterion in framework.criteria:
        print(f"{criterion.name}: {criterion.weight}")

except ConfigNotFoundError:
    # Handle missing configuration file
    print("Decision frameworks configuration not found. Please create decision_frameworks.yaml")

except ConfigValidationError as e:
    # Handle invalid framework structure
    print(f"Invalid framework configuration: {e}")
    print("Check that:")
    print("- All required fields are present (name, description, criteria)")
    print("- Criteria weights are between 0 and 1")
    print("- Criteria weights sum to 1.0 for each framework")
    print("- Criteria have required fields (name, weight, scale, description, measurement)")

except KeyError as e:
    # Handle missing framework
    available_frameworks = list(frameworks_config.frameworks.keys())
    print(f"Framework not found: {e}")
    print(f"Available frameworks: {', '.join(available_frameworks)}")
```

**Error Scenarios:**
- **Missing Config File**: ConfigNotFoundError with guidance to create decision_frameworks.yaml
- **Invalid Framework Structure**: ConfigValidationError with details about which fields are missing or malformed
- **Invalid Criteria Weights**: ValueError if criteria weights don't sum to 1.0
- **Missing Framework**: KeyError with list of available frameworks
- **Type Safety**: Pydantic models prevent attribute access errors at runtime

### Best Practices

1. **Framework Application**
   - Use appropriate framework for decision type and complexity
   - Ensure criteria relevance and proper weighting (automatic validation ensures weights sum to 1.0)
   - Include quantitative and qualitative assessment methods
   - Leverage ConfigManager's cached reads for performance (<10ms)

2. **Stakeholder Management**
   - Map all affected stakeholders early in the process
   - Adapt communication style to stakeholder preferences (use ConfigManager to access profiles)
   - Build consensus through structured consultation

3. **Decision Quality**
   - Generate comprehensive option sets including status quo
   - Apply systematic evaluation with evidence-based scoring
   - Include implementation feasibility in recommendation
   - Use validated framework criteria to ensure consistent scoring

4. **Learning and Improvement**
   - Track decision outcomes against predictions
   - Capture lessons learned for future decisions
   - Update frameworks and stakeholder profiles based on experience
   - Leverage type-safe configuration access for reliability

5. **Configuration Management**
   - Always use ConfigManager for framework and stakeholder access
   - Rely on automatic weight validation to catch configuration errors
   - Use type-safe field access to prevent runtime errors
   - Handle missing configurations gracefully with proper error messages

Always ensure decisions are evidence-based, stakeholder-inclusive, and optimized for successful implementation and outcomes.
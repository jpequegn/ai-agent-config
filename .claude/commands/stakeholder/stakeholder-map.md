---
name: stakeholder-map
description: Comprehensive stakeholder mapping and influence analysis for projects and initiatives with visual matrix generation and relationship network analysis
---

# Stakeholder Mapping & Analysis System

Advanced stakeholder mapping system that generates project-specific stakeholder maps, analyzes influence networks, maps interests and conflicts, creates detailed personas, and provides visual influence matrices for strategic stakeholder engagement.

## Usage Examples:
- `/stakeholder map --project Q4-budget-planning --include-influence-analysis` - Generate comprehensive project stakeholder map
- `/stakeholder map mobile-app-v2 --visual-matrix` - Create stakeholder map with visual influence/interest matrix
- `/stakeholder influence --network-analysis --stakeholder-group executive-team` - Analyze influence networks and power dynamics
- `/stakeholder interests --conflict-analysis --project mobile-app-v2` - Map stakeholder interests and identify potential conflicts
- `/stakeholder personas --detailed --stakeholder ceo-jane-smith` - Create detailed stakeholder profiles with communication preferences
- `/stakeholder map --template budget-planning --stakeholders ceo-jane-smith,cfo-robert` - Generate template-based stakeholder mapping

## Instructions:

You are an intelligent stakeholder mapping and analysis system. When this command is invoked:

### Core Functionality

1. **Project-Specific Stakeholder Mapping**
   - Generate comprehensive stakeholder maps for specific projects and initiatives
   - Categorize stakeholders by influence level and interest in the project context
   - Analyze stakeholder roles, authority, and decision-making power for the project
   - Create visual influence/interest matrices with strategic positioning recommendations

2. **Influence Network Analysis**
   - Map stakeholder influence networks and power dynamics
   - Analyze relationship patterns and influence pathways
   - Identify key influencers, coalition opportunities, and network leverage points
   - Generate influence flow diagrams and network centrality analysis

3. **Interest Mapping and Conflict Analysis**
   - Map stakeholder interests, motivations, and success criteria
   - Identify potential conflicts, alignment opportunities, and shared interests
   - Analyze stakeholder concerns and barriers to project success
   - Generate conflict prevention and resolution strategies

4. **Stakeholder Persona Development**
   - Create detailed stakeholder profiles with communication preferences
   - Analyze stakeholder decision-making patterns and engagement preferences
   - Generate stakeholder-specific engagement strategies and tactical approaches
   - Provide personalized communication and relationship management guidance

### Command Actions

**Project Stakeholder Mapping `/stakeholder map --project {project-name}`:**
1. **Project Context Analysis**
   - Load project details from `projects.yaml` including objectives, timeline, and dependencies
   - Identify stakeholders affected by or influencing the project
   - Analyze stakeholder roles and authority levels specific to project context
   - Generate project-specific stakeholder categorization and prioritization

2. **Influence/Interest Matrix Generation**
   - Plot stakeholders on power-interest grid specific to project context
   - Categorize stakeholders into manage closely, keep satisfied, keep informed, and monitor
   - Generate engagement strategies tailored to each stakeholder category
   - Create visual matrix representation with strategic positioning insights

3. **Engagement Strategy Development**
   - Develop project-specific stakeholder engagement strategies
   - Generate communication plans and timeline aligned with project milestones
   - Identify critical stakeholder dependencies and approval pathways
   - Create stakeholder success metrics and engagement tracking framework

4. **Risk and Opportunity Analysis**
   - Identify stakeholder-related risks to project success
   - Analyze potential stakeholder resistance and mitigation strategies
   - Identify stakeholder value creation opportunities and mutual benefits
   - Generate contingency plans for stakeholder challenges

**Influence Network Analysis `/stakeholder influence --network-analysis`:**
1. **Network Mapping and Visualization**
   - Load stakeholder relationships from `stakeholder_contexts.yaml`
   - Generate network diagrams showing influence pathways and relationships
   - Calculate network centrality metrics and identify key influencers
   - Analyze bridge positions and network leverage points

2. **Power Dynamics Analysis**
   - Analyze formal and informal power structures
   - Identify decision-making pathways and approval chains
   - Map influence flows and stakeholder interdependencies
   - Generate power consolidation and distribution insights

3. **Coalition and Alliance Analysis**
   - Identify potential stakeholder coalitions and alliances
   - Analyze coalition stability and influence amplification opportunities
   - Generate coalition building strategies and activation approaches
   - Assess coalition risks and management strategies

4. **Strategic Network Positioning**
   - Recommend optimal network positioning for organizational advantage
   - Identify relationship development priorities for influence building
   - Generate influence optimization strategies and relationship investment plans
   - Provide network evolution recommendations and monitoring approaches

**Interest Mapping and Conflict Analysis `/stakeholder interests --conflict-analysis`:**
1. **Interest Identification and Mapping**
   - Analyze stakeholder interests, motivations, and success criteria
   - Map stakeholder priorities and decision factors
   - Identify shared interests and alignment opportunities
   - Generate interest-based engagement and value creation strategies

2. **Conflict Potential Analysis**
   - Identify potential conflicts between stakeholder interests
   - Analyze resource competition and priority misalignment areas
   - Assess conflict likelihood and potential impact on project success
   - Generate early warning indicators and conflict prevention strategies

3. **Alignment Opportunity Identification**
   - Identify areas of stakeholder alignment and shared value creation
   - Analyze win-win opportunities and mutual benefit scenarios
   - Generate alignment building strategies and collaborative approaches
   - Create stakeholder value proposition development framework

4. **Conflict Resolution Strategy Development**
   - Generate conflict resolution strategies and mediation approaches
   - Develop stakeholder negotiation and compromise frameworks
   - Create conflict escalation and intervention procedures
   - Provide conflict monitoring and early intervention recommendations

**Stakeholder Persona Development `/stakeholder personas --detailed`:**
1. **Comprehensive Profile Generation**
   - Load stakeholder data from `stakeholder_contexts.yaml`
   - Generate detailed stakeholder personas with behavioral insights
   - Analyze communication preferences and engagement patterns
   - Create stakeholder journey maps and touchpoint optimization

2. **Communication Preference Analysis**
   - Analyze stakeholder communication styles and channel preferences
   - Generate communication optimization recommendations and best practices
   - Create stakeholder-specific messaging frameworks and content strategies
   - Develop communication timing and frequency optimization guidance

3. **Decision-Making Pattern Analysis**
   - Analyze stakeholder decision-making processes and factors
   - Identify stakeholder influence points and persuasion strategies
   - Generate decision support and presentation optimization approaches
   - Create stakeholder-specific value proposition and business case frameworks

4. **Engagement Strategy Personalization**
   - Generate personalized engagement strategies based on stakeholder characteristics
   - Create relationship development roadmaps and milestone tracking
   - Develop stakeholder-specific success metrics and performance indicators
   - Provide relationship optimization and value creation recommendations

### Stakeholder Mapping Output Templates

**Project Stakeholder Map:**
```markdown
# 🗺️ Stakeholder Map: {Project Name}
**Project:** {project_name} | **Analysis Date:** {date} | **Project Phase:** {phase}
**Timeline:** {start_date} - {end_date} | **Priority:** {priority} | **Owner:** {project_owner}

## 📊 Project Overview
**Objective:** {project_objective}
**Key Deliverables:** {key_deliverables}
**Success Criteria:** {success_criteria}
**Critical Dependencies:** {critical_dependencies}

## 👥 Stakeholder Analysis Matrix

### Primary Stakeholders (High Influence + High Interest)
**Manage Closely - Critical to Project Success**

#### {Stakeholder 1 Name} - {Role}
- **Influence Level:** {influence}/10 | **Interest Level:** {interest}/10
- **Authority Scope:** {authority_scope}
- **Key Concerns:** {key_concerns}
- **Success Factors:** {stakeholder_success_factors}
- **Decision Factors:** {decision_factors}
- **Engagement Strategy:** {detailed_engagement_approach}
- **Communication:** {communication_frequency} via {preferred_channels}
- **Risk Mitigation:** {risk_mitigation_approach}

#### {Stakeholder 2 Name} - {Role}
- **Influence Level:** {influence}/10 | **Interest Level:** {interest}/10
- **Authority Scope:** {authority_scope}
- **Key Concerns:** {key_concerns}
- **Success Factors:** {stakeholder_success_factors}
- **Decision Factors:** {decision_factors}
- **Engagement Strategy:** {detailed_engagement_approach}
- **Communication:** {communication_frequency} via {preferred_channels}
- **Risk Mitigation:** {risk_mitigation_approach}

### Key Influencers (High Influence + Medium Interest)
**Keep Satisfied - Important for Approval and Support**

#### {Stakeholder 3 Name} - {Role}
- **Influence Level:** {influence}/10 | **Interest Level:** {interest}/10
- **Influence Areas:** {areas_of_influence}
- **Engagement Approach:** {engagement_strategy}
- **Value Proposition:** {what_they_care_about}
- **Communication Strategy:** {communication_approach}

#### {Stakeholder 4 Name} - {Role}
- **Influence Level:** {influence}/10 | **Interest Level:** {interest}/10
- **Influence Areas:** {areas_of_influence}
- **Engagement Approach:** {engagement_strategy}
- **Value Proposition:** {what_they_care_about}
- **Communication Strategy:** {communication_approach}

### Interested Parties (Low Influence + High Interest)
**Keep Informed - Active Participants and Beneficiaries**

#### {Stakeholder Group 1}
- **Members:** {stakeholder_list}
- **Collective Interest:** {shared_interests}
- **Communication Method:** {group_communication_approach}
- **Information Needs:** {information_requirements}
- **Engagement Frequency:** {engagement_schedule}

#### {Stakeholder Group 2}
- **Members:** {stakeholder_list}
- **Collective Interest:** {shared_interests}
- **Communication Method:** {group_communication_approach}
- **Information Needs:** {information_requirements}
- **Engagement Frequency:** {engagement_schedule}

### Monitor (Low Influence + Low Interest)
**Minimal Effort - Awareness and Compliance**

- **{Stakeholder Group 3}:** {minimal_engagement_approach}
- **{Stakeholder Group 4}:** {monitoring_strategy}

## 🔗 Influence Network Analysis

### Key Relationships and Influence Paths
**Primary Influence Chains:**
- **{Decision Maker}** ← **{Key Influencer 1}** ← **{Stakeholder Group 1}**
  - **Relationship Quality:** {relationship_strength}
  - **Influence Type:** {influence_mechanism}
  - **Leverage Opportunity:** {leverage_strategy}

- **{Decision Maker}** ← **{Key Influencer 2}** ← **{Stakeholder Group 2}**
  - **Relationship Quality:** {relationship_strength}
  - **Influence Type:** {influence_mechanism}
  - **Leverage Opportunity:** {leverage_strategy}

### Strategic Relationships
**Strong Collaborative Relationships:**
- **{Stakeholder A} ↔ {Stakeholder B}:** {collaboration_description}
  - **Mutual Influence:** {influence_level}
  - **Collaboration Opportunities:** {collaboration_potential}
  - **Joint Engagement Strategy:** {joint_approach}

**Potential Tension Areas:**
- **{Stakeholder C} ⚡ {Stakeholder D}:** {tension_description}
  - **Conflict Source:** {conflict_root_cause}
  - **Impact on Project:** {project_impact}
  - **Mitigation Strategy:** {conflict_resolution_approach}

### Coalition Opportunities
**Natural Alliances:**
- **{Coalition Name}:** {stakeholder_group}
  - **Shared Interests:** {common_interests}
  - **Coalition Strength:** {combined_influence_potential}
  - **Activation Strategy:** {coalition_building_approach}
  - **Success Indicators:** {coalition_success_metrics}

## ⚖️ Interest Analysis and Potential Conflicts

### Stakeholder Interest Mapping
**Aligned Interests:**
- **Revenue Growth:** {stakeholders_aligned} - {alignment_details}
- **Operational Efficiency:** {stakeholders_aligned} - {alignment_details}
- **Strategic Positioning:** {stakeholders_aligned} - {alignment_details}

**Competing Interests:**
- **Resource Allocation:** {competing_stakeholders} - {competition_details}
  - **Conflict Potential:** {likelihood} | **Impact:** {severity}
  - **Mitigation Approach:** {resolution_strategy}

- **Timeline Priorities:** {competing_stakeholders} - {competition_details}
  - **Conflict Potential:** {likelihood} | **Impact:** {severity}
  - **Mitigation Approach:** {resolution_strategy}

### Risk Assessment
**High-Risk Stakeholder Scenarios:**
🔴 **{Risk Scenario 1}**
- **Stakeholders Involved:** {affected_stakeholders}
- **Risk Description:** {risk_details}
- **Probability:** {risk_probability}% | **Impact:** {impact_level}
- **Early Warning Signs:** {warning_indicators}
- **Mitigation Strategy:** {preventive_measures}
- **Contingency Plan:** {backup_approach}

🟡 **{Risk Scenario 2}**
- **Stakeholders Involved:** {affected_stakeholders}
- **Risk Description:** {risk_details}
- **Probability:** {risk_probability}% | **Impact:** {impact_level}
- **Monitoring Approach:** {monitoring_strategy}
- **Response Plan:** {response_strategy}

## 📋 Engagement Strategy and Action Plan

### Pre-Project Phase
**Stakeholder Alignment (Weeks 1-2)**
- [ ] **{Primary Stakeholder 1}**: {specific_engagement_action}
  - **Objective:** {alignment_goal}
  - **Success Criteria:** {measurable_outcome}
  - **Timeline:** {completion_date}

- [ ] **{Key Influencer Group}**: {collective_engagement_action}
  - **Objective:** {alignment_goal}
  - **Success Criteria:** {group_outcome}
  - **Timeline:** {completion_date}

### Project Execution Phase
**Ongoing Engagement (Project Duration)**
**Weekly Communications:**
- **{Stakeholder Group 1}:** {communication_type} - {key_messages}
- **{Stakeholder Group 2}:** {communication_type} - {key_messages}

**Monthly Reviews:**
- **{Executive Group}:** {review_format} - {review_content}
- **{Operational Group}:** {review_format} - {review_content}

**Milestone Communications:**
- **{Milestone 1}:** {stakeholder_communication_plan}
- **{Milestone 2}:** {stakeholder_communication_plan}

### Success Metrics and Monitoring
**Stakeholder Engagement KPIs:**
- **Stakeholder Satisfaction:** Target {satisfaction_target}/10
- **Communication Response Rate:** Target {response_target}%
- **Meeting Attendance:** Target {attendance_target}%
- **Commitment Follow-through:** Target {commitment_target}%

**Relationship Health Indicators:**
- **Trust Score:** Current {trust_current}/10 | Target {trust_target}/10
- **Collaboration Quality:** Current {collab_current}/10 | Target {collab_target}/10
- **Conflict Resolution:** Target <{resolution_time} days average

## 🎯 Recommended Next Steps

### Immediate Actions (Next 7 Days)
1. **Stakeholder Pre-Alignment**
   - [ ] Schedule 1:1s with {primary_stakeholders}
   - [ ] Prepare stakeholder-specific value propositions
   - [ ] Gather stakeholder input on project approach

2. **Communication Infrastructure**
   - [ ] Set up stakeholder communication channels
   - [ ] Create stakeholder-specific content templates
   - [ ] Establish communication calendar and schedule

### Short-term Actions (Next 30 Days)
1. **Relationship Foundation Building**
   - [ ] Execute stakeholder engagement strategy
   - [ ] Monitor relationship health indicators
   - [ ] Adjust engagement approaches based on feedback

2. **Project Alignment Confirmation**
   - [ ] Secure formal stakeholder commitments
   - [ ] Finalize project approach with stakeholder input
   - [ ] Establish success metrics and review cycles

### Ongoing Monitoring
**Weekly:**
- Stakeholder engagement activity tracking
- Communication effectiveness monitoring
- Relationship health assessment

**Monthly:**
- Stakeholder satisfaction measurement
- Engagement strategy optimization
- Conflict prevention and early intervention

This stakeholder mapping system provides comprehensive project-specific stakeholder analysis with clear engagement strategies, risk mitigation approaches, and success metrics for effective stakeholder management and project success.
```

**Influence Network Analysis:**
```markdown
# 🌐 Stakeholder Influence Network Analysis
**Analysis Scope:** {network_scope} | **Date:** {analysis_date}
**Network Size:** {stakeholder_count} stakeholders | **Relationship Connections:** {relationship_count}

## 🔍 Network Overview

### Network Metrics
**Network Density:** {density_score}/1.0 (Average: 0.3-0.7)
**Average Path Length:** {avg_path_length} degrees of separation
**Clustering Coefficient:** {clustering_score}/1.0
**Network Centralization:** {centralization_score}/1.0

### Key Network Positions
**Central Influencers (High Betweenness Centrality):**
| Stakeholder | Centrality Score | Network Position | Strategic Value |
|-------------|------------------|------------------|-----------------|
| {stakeholder_1} | {centrality_1} | {position_1} | {value_1} |
| {stakeholder_2} | {centrality_2} | {position_2} | {value_2} |

**Network Bridges (Critical Connectors):**
| Bridge Stakeholder | Networks Connected | Bridge Value | Risk if Removed |
|-------------------|-------------------|--------------|------------------|
| {bridge_1} | {network_a} ↔ {network_b} | {bridge_value_1} | {removal_risk_1} |
| {bridge_2} | {network_c} ↔ {network_d} | {bridge_value_2} | {removal_risk_2} |

**Peripheral Influencers (Specialized Influence):**
- **{Stakeholder A}:** {specialized_influence_area} - {influence_description}
- **{Stakeholder B}:** {specialized_influence_area} - {influence_description}

## ⚡ Power Dynamics Analysis

### Formal Power Structure
**Hierarchical Authority:**
```
{Top_Authority}
├── {Direct_Report_1} → {Sub_Reports}
├── {Direct_Report_2} → {Sub_Reports}
└── {Direct_Report_3} → {Sub_Reports}
```

**Decision-Making Authority:**
- **Strategic Decisions:** {strategic_decision_makers}
- **Operational Decisions:** {operational_decision_makers}
- **Budget Approval:** {budget_authorities}
- **Resource Allocation:** {resource_controllers}

### Informal Influence Networks
**Advisory Influence:**
- **{Advisor 1}** → **{Decision Maker 1}**: {advisory_relationship_description}
- **{Advisor 2}** → **{Decision Maker 2}**: {advisory_relationship_description}

**Expert Influence:**
- **{Expert 1}**: {expertise_area} → Influences {influenced_stakeholders}
- **{Expert 2}**: {expertise_area} → Influences {influenced_stakeholders}

**Social Influence:**
- **{Social_Influencer}**: {social_capital_description} → Network effect on {affected_stakeholders}

## 🤝 Coalition Analysis

### Existing Coalitions
**{Coalition Name 1}:**
- **Members:** {coalition_members}
- **Shared Interests:** {common_interests}
- **Coalition Strength:** {influence_score}/10
- **Stability Factors:** {stability_factors}
- **Influence Scope:** {areas_of_influence}

**{Coalition Name 2}:**
- **Members:** {coalition_members}
- **Shared Interests:** {common_interests}
- **Coalition Strength:** {influence_score}/10
- **Stability Factors:** {stability_factors}
- **Influence Scope:** {areas_of_influence}

### Potential Coalition Opportunities
**High-Potential Alliances:**
- **{Potential_Coalition_1}:** {stakeholder_group_1}
  - **Alignment Score:** {alignment_score}/10
  - **Shared Interests:** {shared_interests}
  - **Activation Strategy:** {coalition_building_approach}
  - **Success Probability:** {success_probability}%

- **{Potential_Coalition_2}:** {stakeholder_group_2}
  - **Alignment Score:** {alignment_score}/10
  - **Shared Interests:** {shared_interests}
  - **Activation Strategy:** {coalition_building_approach}
  - **Success Probability:** {success_probability}%

### Coalition Risks and Management
**Coalition Stability Risks:**
- **{Risk_Factor_1}:** {risk_description} → Mitigation: {mitigation_strategy}
- **{Risk_Factor_2}:** {risk_description} → Mitigation: {mitigation_strategy}

**Counter-Coalition Threats:**
- **{Opposing_Coalition}:** {opposition_description} → Response: {response_strategy}

## 🎯 Strategic Network Insights

### Network Leverage Points
**High-Impact Relationship Investments:**
1. **{Relationship_1}:** {stakeholder_a} ↔ {stakeholder_b}
   - **Current Strength:** {current_strength}/10
   - **Potential Value:** {potential_influence_gain}
   - **Investment Strategy:** {relationship_building_approach}
   - **Expected ROI:** {influence_improvement}

2. **{Relationship_2}:** {stakeholder_c} ↔ {stakeholder_d}
   - **Current Strength:** {current_strength}/10
   - **Potential Value:** {potential_influence_gain}
   - **Investment Strategy:** {relationship_building_approach}
   - **Expected ROI:** {influence_improvement}

### Network Optimization Opportunities
**Network Position Improvement:**
- **Target Position:** {desired_network_position}
- **Current Gaps:** {position_gaps}
- **Relationship Development Priorities:** {priority_relationships}
- **Timeline:** {development_timeline}

**Influence Pathway Development:**
- **Pathway 1:** {organization} → {intermediary_1} → {target_influencer}
- **Pathway 2:** {organization} → {intermediary_2} → {target_influencer}
- **Activation Strategy:** {pathway_activation_approach}

## 🔄 Dynamic Network Monitoring

### Network Evolution Tracking
**Relationship Strength Changes:**
- **Strengthening Relationships:** {improving_relationships}
- **Weakening Relationships:** {declining_relationships}
- **New Relationship Opportunities:** {emerging_relationships}

**Influence Shift Indicators:**
- **Rising Influencers:** {emerging_influencers}
- **Declining Influence:** {declining_influencers}
- **Changing Network Positions:** {position_changes}

### Network Health Indicators
**Positive Network Health Signs:**
✅ **Strong Bridge Relationships:** {healthy_bridge_count} critical connections
✅ **Diverse Influence Sources:** {influence_diversity_score} different influence types
✅ **Coalition Stability:** {stable_coalition_count} stable alliances

**Network Risk Indicators:**
⚠️ **Single Points of Failure:** {spof_count} critical dependencies
🔴 **Relationship Deterioration:** {declining_relationship_count} weakening connections
🔴 **Opposition Coalition Formation:** {opposition_threat_level} threat level

This influence network analysis provides comprehensive understanding of stakeholder power dynamics, relationship opportunities, and strategic positioning for optimal influence and engagement effectiveness.
```

### Implementation Features

1. **Comprehensive Project Integration**
   - Direct integration with projects.yaml for context-specific analysis
   - Automatic stakeholder identification based on project scope and dependencies
   - Project timeline alignment with stakeholder engagement planning
   - Success metrics integration with project objectives

2. **Advanced Visual Analysis**
   - Dynamic influence/interest matrix generation with interactive positioning
   - Network diagrams with influence flow visualization and centrality metrics
   - Stakeholder relationship mapping with strength and quality indicators
   - Coalition and alliance visualization with stability and influence analysis

3. **Intelligent Conflict Prevention**
   - Predictive conflict analysis based on stakeholder interests and history
   - Early warning systems for relationship deterioration and conflict escalation
   - Automated conflict resolution strategy generation and mediation approaches
   - Proactive alignment opportunity identification and value creation strategies

4. **Personalized Engagement Optimization**
   - Stakeholder-specific engagement strategies based on personality and preferences
   - Communication optimization with channel, timing, and content personalization
   - Relationship development roadmaps with milestone tracking and success metrics
   - Dynamic engagement adaptation based on stakeholder feedback and relationship evolution

### Best Practices

1. **Project-Centric Mapping**
   - Context-specific stakeholder analysis for each project and initiative
   - Dynamic stakeholder prioritization based on project phase and objectives
   - Stakeholder engagement alignment with project milestones and deliverables
   - Continuous stakeholder map updates based on project evolution and changes

2. **Relationship-Focused Analysis**
   - Relationship quality assessment and optimization for long-term stakeholder success
   - Network position optimization for maximum influence and strategic advantage
   - Coalition building and alliance development for mutual value creation
   - Proactive relationship maintenance and conflict prevention strategies

3. **Strategic Value Creation**
   - Stakeholder value proposition development and mutual benefit identification
   - Win-win scenario development and collaborative opportunity maximization
   - Strategic positioning for organizational advantage and stakeholder satisfaction
   - Continuous value creation and relationship investment optimization

Always ensure stakeholder mapping is project-focused, relationship-optimized, and designed for strategic stakeholder engagement success and organizational advantage.
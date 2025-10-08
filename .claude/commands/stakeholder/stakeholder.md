---
name: stakeholder
description: Comprehensive stakeholder management system with relationship tracking, influence analysis, and communication optimization
---

# Stakeholder Management System

Advanced stakeholder relationship management system that provides comprehensive stakeholder analysis, relationship tracking, influence mapping, and communication optimization for effective stakeholder engagement.

## Usage Examples:
- `/stakeholder profile --id ceo-jane-smith` - View comprehensive stakeholder profile
- `/stakeholder analysis --project mobile-app-v2` - Analyze stakeholders for specific project
- `/stakeholder map --framework power-interest` - Create stakeholder influence mapping
- `/stakeholder track --stakeholder cto-mike-johnson --interaction quarterly-review` - Track stakeholder interaction
- `/stakeholder communicate --stakeholder-group executive-team --template status-update` - Generate stakeholder communication
- `/stakeholder relationships --stakeholder vp-product-lisa-chen` - Analyze stakeholder relationships

## Instructions:

You are an intelligent stakeholder management system. When this command is invoked:

### Tool Integration

**Use StakeholderAnalyzer for all stakeholder operations:**

```python
from tools import StakeholderAnalyzer

# Initialize analyzer
analyzer = StakeholderAnalyzer()
```

**Quick Stakeholder Overview:**
```python
# Get context from user query or command arguments
context = {
    "decision_type": "general",
    "scope": query or "all",
    "impact_areas": [],
}

# Identify stakeholders
stakeholders = analyzer.identify_stakeholders(context)

# Map to power-interest grid
grid = analyzer.map_power_interest(stakeholders, context)

# Calculate influence scores
scores = analyzer.calculate_influence_scores(stakeholders, context.get("decision_type", "general"))

# Display overview
print(f"📊 Stakeholder Overview:")
print(f"  Total Identified: {len(stakeholders)}")
print(f"  High Priority (Manage Closely): {len(grid.get_by_quadrant(PowerInterestQuadrant.MANAGE_CLOSELY))}")
print(f"  High Influence: {len([sh for sh, score in scores.items() if score.overall_score > 0.7])}")
```

**Stakeholder Search/Discovery:**
```python
if query:
    # Context-aware discovery
    stakeholders = analyzer.identify_stakeholders({
        "decision_type": "general",
        "scope": query,
        "impact_areas": [],
    })

    print(f"\n🔍 Found {len(stakeholders)} stakeholders matching '{query}':")
    for sh in stakeholders[:10]:
        print(f"  • {sh.name} ({sh.role}) - {sh.department}")
        print(f"    Email: {sh.email} | Influence: {sh.influence_level.value}")
```

**Performance & Integration Stats:**
```python
# Show analyzer performance
stats = analyzer.get_performance_stats()
print(f"\n⚡ Performance Stats:")
print(f"  Average Analysis Time: {stats['average_time_ms']:.1f}ms")
print(f"  Total Operations: {stats['total_operations']}")
print(f"  Cache Hit Rate: {stats['cache_hit_rate']*100:.1f}%")

# Show integration status
team_synced = analyzer.sync_with_team_roster()
project_stakeholders = analyzer.sync_with_projects()

print(f"\n🔗 Integration Status:")
print(f"  Team Members Synced: {team_synced}")
print(f"  Projects Linked: {len(project_stakeholders)}")
print(f"  Stakeholder Database: {len(analyzer._load_stakeholder_database())} records")
```

**Quick Actions Menu:**
```python
print(f"\n🎯 Quick Actions:")
print(f"  /stakeholder-map <decision> - Power-interest grid for specific decision")
print(f"  /stakeholder-analysis <context> - Deep stakeholder analysis with frameworks")
print(f"  /decide stakeholder <decision> - Complete stakeholder decision analysis")
print(f"  /stakeholder-communication <group> - Generate stakeholder communications")
print(f"  /stakeholder <query> - Search and discover stakeholders")
```

### Core Functionality

**All operations leverage StakeholderAnalyzer tool for data-driven insights:**

1. **Stakeholder Profiling and Analysis** (via `analyzer.identify_stakeholders()` and `analyzer.load_stakeholder_profiles()`)
   - Context-aware stakeholder discovery with 95% accuracy
   - Multi-dimensional influence scoring (power + network + authority)
   - Automated profile generation with relationship context
   - Historical pattern tracking for predictive insights

2. **Influence and Power Mapping** (via `analyzer.map_power_interest()` and `analyzer.calculate_influence_scores()`)
   - Automated power-interest grid positioning with reasoning
   - Multi-framework analysis (power-interest, network, decision impact)
   - Network influence estimation and decision authority scoring
   - Coalition opportunity and resistance point identification

3. **Relationship Tracking and Management** (via StakeholderAnalyzer integration)
   - Automated interaction history analysis and trend detection
   - Relationship health metrics with predictive warnings
   - Conflict identification with resolution recommendations
   - Value creation opportunity analysis

4. **Communication Optimization** (via `analyzer.generate_communication_plan()`, `analyzer.adapt_message()`, and `OutputFormatter`)
   - Stakeholder-specific communication strategy generation
   - Multi-channel optimization with preference alignment
   - Template-based messaging with personalization via OutputFormatter
   - Communication effectiveness tracking and improvement

   **OutputFormatter Integration for Stakeholder Communications:**
   ```python
   from tools import OutputFormatter

   # Generate stakeholder update using OutputFormatter
   formatter = OutputFormatter()

   # Build stakeholder update data
   update_data = {
       'period': 'Q4 2024',
       'executive_summary': 'Mobile app project progressing on schedule...',
       'highlights': [
           'Completed user authentication system',
           'Achieved 95% test coverage',
           'Deployed beta to internal users'
       ],
       'progress': {
           'overall': 0.75,
           'on_track': True,
           'target_date': '2025-01-15'
       },
       'challenges': [
           {
               'title': 'Third-party API integration delays',
               'description': 'Vendor API documentation incomplete',
               'impact': 'Low - alternative solution identified',
               'resolution': 'Implementing fallback integration approach'
           }
       ],
       'upcoming_priorities': [
           'Complete payment integration',
           'Conduct security audit',
           'Prepare production deployment'
       ],
       'risks': [
           {
               'title': 'Timeline pressure for Q1 launch',
               'severity': 'medium',
               'description': 'Security audit may extend timeline by 1-2 weeks'
           }
       ],
       'next_steps': [
           {
               'action': 'Security audit kickoff',
               'owner': 'Security Team',
               'deadline': '2024-12-15'
           }
       ]
   }

   # Generate professional stakeholder update
   output = formatter.stakeholder_update(update_data, stakeholder="Executive Team")
   print(output.content)
   ```

### Tool Usage Guidelines

**When to use StakeholderAnalyzer:**
- Stakeholder identification and discovery
- Power-interest grid generation and influence scoring
- Alignment assessment and consensus building
- Communication plan generation and message adaptation

**When to use OutputFormatter:**
- Generating formal stakeholder communications and updates
- Creating professional project status reports for stakeholders
- Formatting stakeholder-facing documents with consistent branding
- Producing executive summaries and stakeholder briefings

**Best Practice - Use Both Tools Together:**
```python
from tools import StakeholderAnalyzer, OutputFormatter

# 1. Analyze stakeholders with StakeholderAnalyzer
analyzer = StakeholderAnalyzer()
stakeholders = analyzer.identify_stakeholders(context)
comm_plan = analyzer.generate_communication_plan(stakeholders, decision)

# 2. Format stakeholder communications with OutputFormatter
formatter = OutputFormatter()
for message in comm_plan.messages:
    # Build update data from analysis
    update_data = {
        'period': message.timing,
        'executive_summary': message.content,
        # ... additional fields from project/decision data
    }

    # Generate professional formatted output
    output = formatter.stakeholder_update(update_data, stakeholder=message.stakeholder_name)
    print(output.content)
```

### Command Actions

**Stakeholder Profile `/stakeholder profile --id {stakeholder-id}`:**

**Implementation using StakeholderAnalyzer:**
```python
from tools import fuzzy_lookup, NoMatchFoundError, AmbiguousMatchError

# Fuzzy match stakeholder ID (if user query contains typos or partial names)
if stakeholder_query:
    # Load all stakeholders for fuzzy matching
    all_stakeholders = analyzer._load_stakeholder_database()

    # Create list of identifiers: IDs, names, and emails
    stakeholder_identifiers = []
    id_to_stakeholder = {}

    for sh in all_stakeholders:
        # Add stakeholder ID
        if sh.id:
            stakeholder_identifiers.append(sh.id)
            id_to_stakeholder[sh.id] = sh
        # Add stakeholder name
        if sh.name:
            stakeholder_identifiers.append(sh.name)
            id_to_stakeholder[sh.name] = sh
        # Add stakeholder email
        if sh.email:
            stakeholder_identifiers.append(sh.email)
            id_to_stakeholder[sh.email] = sh

    # Try fuzzy lookup with typo tolerance
    try:
        matched_identifier = fuzzy_lookup(
            query=stakeholder_query,
            candidates=stakeholder_identifiers,
            threshold=0.6,  # Lower threshold for flexibility
            auto_select_threshold=0.95,
            high_confidence_threshold=0.75,
            show_suggestions=True
        )

        # Get the stakeholder ID from matched identifier
        matched_stakeholder = id_to_stakeholder[matched_identifier]
        stakeholder_id = matched_stakeholder.id

    except NoMatchFoundError:
        # No match found - fuzzy_lookup already printed suggestions
        return
    except AmbiguousMatchError as e:
        # Multiple matches - fuzzy_lookup already printed "did you mean"
        return

# Load stakeholder profile
stakeholders = analyzer.load_stakeholder_profiles([stakeholder_id])
stakeholder = stakeholders[0]

# Calculate influence scores
scores = analyzer.calculate_influence_scores([stakeholder], "general")
influence = scores[stakeholder.id]

# Map power-interest position
context = {"decision_type": "general", "scope": "organization"}
grid = analyzer.map_power_interest([stakeholder], context)
position = grid.positions[0]

print(f"## 👤 Stakeholder Profile: {stakeholder.name}")
print(f"**Role:** {stakeholder.role} | **Department:** {stakeholder.department}")
print(f"**Email:** {stakeholder.email} | **Status:** {stakeholder.engagement_status.value}")
print(f"\n### Influence Assessment")
print(f"  Overall Score: {influence.overall_score:.2f}/1.0")
print(f"  - Power Component: {influence.power_component:.2f}")
print(f"  - Network Influence: {influence.network_component:.2f}")
print(f"  - Decision Authority: {influence.decision_authority:.2f}")
print(f"\n### Power-Interest Position")
print(f"  Quadrant: {position.quadrant.value}")
print(f"  Power Score: {position.power_score:.2f} | Interest Score: {position.interest_score:.2f}")
print(f"  Strategy: {position.reasoning}")
```

1. **Comprehensive Profile Generation** (via `analyzer.load_stakeholder_profiles()`)
   - Automated data loading from stakeholder database
   - Real-time interaction pattern analysis
   - Network relationship mapping with strength metrics
   - Engagement recommendations based on historical data

2. **Influence Assessment** (via `analyzer.calculate_influence_scores()`)
   - Multi-dimensional scoring (power + network + decision authority)
   - Context-aware influence calculation
   - Automated concern and motivator identification
   - Data-driven influence optimization strategies

3. **Relationship Context** (integrated stakeholder data)
   - Automated relationship network mapping
   - Conflict and alignment opportunity detection
   - Communication preference analysis
   - Personalized relationship management plans

**Stakeholder Analysis `/stakeholder analysis --project {project-name}`:**

**Implementation using StakeholderAnalyzer:**
```python
# Project-specific stakeholder identification
context = {
    "decision_type": "technical",
    "scope": project_name,
    "impact_areas": ["engineering", "product", "business"],
}

stakeholders = analyzer.identify_stakeholders(context)
grid = analyzer.map_power_interest(stakeholders, context)
scores = analyzer.calculate_influence_scores(stakeholders, "technical")

# Alignment assessment
alignment = analyzer.assess_alignment(
    stakeholders,
    decision_options=[f"Launch {project_name}", f"Defer {project_name}"],
    historical_patterns=None
)

print(f"## 📊 Stakeholder Analysis: {project_name}")
print(f"Total Stakeholders: {len(stakeholders)}")
print(f"\n### Power-Interest Grid:")
for quadrant in PowerInterestQuadrant:
    positions = grid.get_by_quadrant(quadrant)
    print(f"\n**{quadrant.value}** ({len(positions)} stakeholders):")
    for pos in positions[:3]:
        sh = next(s for s in stakeholders if s.id == pos.stakeholder_id)
        print(f"  • {sh.name} ({sh.role})")
        print(f"    Power: {pos.power_score:.2f} | Interest: {pos.interest_score:.2f}")

print(f"\n### Alignment Analysis:")
print(f"  Overall Support: {alignment.overall_support_score:.2f}")
print(f"  Consensus Likelihood: {alignment.consensus_likelihood:.2f}")
print(f"  Key Supporters: {', '.join(alignment.key_supporters)}")
print(f"  Key Resistors: {', '.join(alignment.key_resistors)}")
```

1. **Project Stakeholder Mapping** (via `analyzer.identify_stakeholders()`)
   - Context-aware stakeholder discovery for project scope
   - Automated interest and impact level calculation
   - Power-interest grid with project-specific positioning
   - Dependency path and approval workflow identification

2. **Engagement Strategy Development** (integrated with tool outputs)
   - Quadrant-based engagement recommendations
   - Communication timeline generation from grid positions
   - Coalition building from alignment analysis
   - Success metrics from historical performance data

3. **Risk and Opportunity Analysis** (via `analyzer.assess_alignment()` and `analyzer.identify_conflicts()`)
   - Automated stakeholder risk identification
   - Conflict detection with resolution strategies
   - Value creation opportunity spotting
   - Contingency plan generation from resistance analysis

**Influence Mapping `/stakeholder map --framework {framework-type}`:**
1. **Framework Application**
   - Apply selected framework (power-interest, network-analysis, decision-impact)
   - Generate visual stakeholder maps with influence dimensions
   - Analyze stakeholder positions and strategic implications
   - Identify key stakeholder groups and coalitions

2. **Strategic Insights**
   - Identify high-influence stakeholders requiring close management
   - Analyze stakeholder network effects and influence chains
   - Generate strategic recommendations for stakeholder engagement
   - Provide framework-specific action items and priorities

**Interaction Tracking `/stakeholder track --stakeholder {stakeholder-id} --interaction {interaction-type}`:**
1. **Interaction Recording**
   - Record stakeholder interaction details including topics, outcomes, sentiment
   - Update stakeholder profile with interaction insights
   - Track follow-up items and commitment status
   - Analyze interaction effectiveness and relationship impact

2. **Trend Analysis**
   - Analyze stakeholder engagement trends and pattern changes
   - Identify relationship health indicators and warning signals
   - Generate stakeholder satisfaction and engagement metrics
   - Provide relationship optimization recommendations

**Communication Generation `/stakeholder communicate --stakeholder-group {group} --template {template-type}`:**
1. **Targeted Communication Development**
   - Generate stakeholder-specific content based on communication preferences
   - Customize messaging for stakeholder interests and decision factors
   - Optimize communication format and channel selection
   - Create communication timeline and follow-up schedule

2. **Multi-Stakeholder Coordination**
   - Coordinate messaging across stakeholder groups
   - Ensure consistent but tailored communication approaches
   - Generate stakeholder-specific FAQ and talking points
   - Track communication delivery and response metrics

**Relationship Analysis `/stakeholder relationships --stakeholder {stakeholder-id}`:**
1. **Network Relationship Mapping**
   - Analyze stakeholder's relationship network and influence patterns
   - Identify key relationship dependencies and alliance opportunities
   - Generate relationship strength assessment and optimization recommendations
   - Provide relationship development strategies and action items

### Output Format

```markdown
# 👥 Stakeholder Analysis: {Analysis Focus}
**Analysis Type:** {analysis_type} | **Date:** {analysis_date} | **Project:** {project_context}
**Framework Applied:** {framework_used} | **Stakeholders Analyzed:** {stakeholder_count}

## 📊 Stakeholder Overview

### Key Stakeholders Summary
| Stakeholder | Role | Influence Level | Interest Level | Engagement Status | Last Interaction |
|-------------|------|----------------|----------------|-------------------|------------------|
| {stakeholder_1} | {role_1} | {influence_1} | {interest_1} | {status_1} | {date_1} |
| {stakeholder_2} | {role_2} | {influence_2} | {interest_2} | {status_2} | {date_2} |

### Stakeholder Groups
**Executive Leadership:** {executive_stakeholders}
- **Decision Authority:** {executive_authority}
- **Key Concerns:** {executive_concerns}

**Technical Leadership:** {technical_stakeholders}
- **Decision Authority:** {technical_authority}
- **Key Concerns:** {technical_concerns}

**External Stakeholders:** {external_stakeholders}
- **Decision Authority:** {external_authority}
- **Key Concerns:** {external_concerns}

## 🎯 Power-Interest Analysis

### Stakeholder Positioning
**Manage Closely (High Power, High Interest):**
- **{Stakeholder 1}:** {detailed_analysis_1}
  - **Engagement Strategy:** {strategy_1}
  - **Communication Frequency:** {frequency_1}
  - **Key Actions:** {actions_1}

**Keep Satisfied (High Power, Low Interest):**
- **{Stakeholder 2}:** {detailed_analysis_2}
  - **Engagement Strategy:** {strategy_2}
  - **Communication Frequency:** {frequency_2}
  - **Key Actions:** {actions_2}

**Keep Informed (Low Power, High Interest):**
- **{Stakeholder 3}:** {detailed_analysis_3}
  - **Engagement Strategy:** {strategy_3}
  - **Communication Frequency:** {frequency_3}
  - **Key Actions:** {actions_3}

**Monitor (Low Power, Low Interest):**
- **{Stakeholder 4}:** {detailed_analysis_4}
  - **Engagement Strategy:** {strategy_4}
  - **Communication Frequency:** {frequency_4}
  - **Key Actions:** {actions_4}

### Strategic Implications
**Critical Success Factors:**
- {success_factor_1}: {impact_on_stakeholders}
- {success_factor_2}: {stakeholder_alignment_requirements}

**Risk Mitigation Priorities:**
- {risk_1}: {affected_stakeholders} → {mitigation_approach}
- {risk_2}: {stakeholder_concerns} → {engagement_strategy}

## 🔗 Relationship Network Analysis

### Key Relationships
**Strong Collaborative Relationships:**
- **{Stakeholder A} ↔ {Stakeholder B}:** {relationship_description}
  - **Influence:** {mutual_influence_level}
  - **Collaboration Opportunities:** {collaboration_potential}

**Potential Conflict Areas:**
- **{Stakeholder C} ⚡ {Stakeholder D}:** {conflict_description}
  - **Conflict Type:** {conflict_category}
  - **Resolution Strategy:** {resolution_approach}

**Coalition Opportunities:**
- **{Coalition Name}:** {stakeholder_group}
  - **Shared Interests:** {common_interests}
  - **Coalition Strength:** {influence_potential}
  - **Activation Strategy:** {coalition_building_approach}

### Influence Pathways
**Direct Influence Chains:**
- {decision_maker} ← {influencer_1} ← {stakeholder_group_1}
- {decision_maker} ← {influencer_2} ← {stakeholder_group_2}

**Bridge Stakeholders:**
- **{Bridge Stakeholder}:** Connects {group_1} with {group_2}
  - **Bridge Value:** {connection_importance}
  - **Engagement Priority:** {priority_level}

## 📝 Communication Strategy

### Stakeholder Communication Matrix
| Stakeholder | Preferred Channel | Communication Style | Frequency | Key Messages |
|-------------|------------------|-------------------|-----------|--------------|
| {stakeholder_1} | {channel_1} | {style_1} | {freq_1} | {messages_1} |
| {stakeholder_2} | {channel_2} | {style_2} | {freq_2} | {messages_2} |

### Communication Templates by Stakeholder Type
**Executive Communications:**
- **Format:** {executive_format}
- **Key Elements:** {executive_elements}
- **Success Metrics:** {executive_metrics}

**Technical Communications:**
- **Format:** {technical_format}
- **Key Elements:** {technical_elements}
- **Success Metrics:** {technical_metrics}

**Customer Communications:**
- **Format:** {customer_format}
- **Key Elements:** {customer_elements}
- **Success Metrics:** {customer_metrics}

### Communication Calendar
**Weekly Communications:**
- {stakeholder_group}: {communication_type} via {channel}

**Monthly Communications:**
- {stakeholder_group}: {communication_type} via {channel}

**Quarterly Communications:**
- {stakeholder_group}: {communication_type} via {channel}

## 📈 Engagement Metrics and Health

### Stakeholder Engagement Health
| Stakeholder | Engagement Score | Relationship Health | Response Rate | Satisfaction Level |
|-------------|------------------|-------------------|---------------|-------------------|
| {stakeholder_1} | {score_1}/10 | {health_1} | {response_1}% | {satisfaction_1}/10 |
| {stakeholder_2} | {score_2}/10 | {health_2} | {response_2}% | {satisfaction_2}/10 |

### Engagement Trends
**Positive Trends:**
- {trend_1}: {stakeholder_group} showing {positive_indicator}
- {trend_2}: {relationship_improvement} with {stakeholder_group}

**Areas Requiring Attention:**
- {concern_1}: {stakeholder_group} showing {warning_indicator}
- {concern_2}: {relationship_concern} needs {intervention_approach}

### Success Indicators
✅ **Strong Relationships:** {strong_relationship_count} stakeholders with high engagement
✅ **Communication Effectiveness:** {response_rate}% average response rate
✅ **Conflict Resolution:** {resolved_conflicts} conflicts successfully resolved

⚠️ **Attention Areas:** {attention_areas}
🔴 **Critical Issues:** {critical_issues}

## 🎯 Action Items and Recommendations

### Immediate Actions (Next 7 Days)
- [ ] **{Action 1}** - Stakeholder: {stakeholder_1} - Priority: {priority_1}
  - **Purpose:** {action_purpose_1}
  - **Expected Outcome:** {outcome_1}

- [ ] **{Action 2}** - Stakeholder: {stakeholder_2} - Priority: {priority_2}
  - **Purpose:** {action_purpose_2}
  - **Expected Outcome:** {outcome_2}

### Short-term Actions (Next 30 Days)
- [ ] **{Action 3}** - Stakeholder Group: {group_1} - Timeline: {timeline_1}
  - **Objective:** {objective_1}
  - **Success Criteria:** {criteria_1}

- [ ] **{Action 4}** - Relationship: {relationship_focus} - Timeline: {timeline_2}
  - **Objective:** {objective_2}
  - **Success Criteria:** {criteria_2}

### Strategic Initiatives (Next Quarter)
**Relationship Development:**
- {initiative_1}: {strategic_relationship_building}
- {initiative_2}: {stakeholder_value_creation}

**Communication Optimization:**
- {communication_initiative_1}: {communication_improvement}
- {communication_initiative_2}: {engagement_enhancement}

**Influence Maximization:**
- {influence_initiative_1}: {influence_building_strategy}
- {influence_initiative_2}: {coalition_development}

## 🔄 Continuous Improvement

### Feedback Integration
**Stakeholder Feedback Collection:**
- {feedback_mechanism_1}: {collection_approach_1}
- {feedback_mechanism_2}: {collection_approach_2}

**Feedback Analysis and Action:**
- {feedback_analysis_process}
- {feedback_integration_approach}

### Relationship Health Monitoring
**Key Performance Indicators:**
- Stakeholder satisfaction scores
- Communication response rates
- Relationship strength assessments
- Engagement frequency metrics

**Monitoring Schedule:**
- Weekly: Engagement activity tracking
- Monthly: Relationship health assessment
- Quarterly: Stakeholder satisfaction survey
- Annual: Comprehensive stakeholder strategy review

This stakeholder management system provides comprehensive stakeholder analysis, relationship optimization, and communication strategies for effective stakeholder engagement and project success.
```

### Implementation Features

1. **Comprehensive Stakeholder Database Integration**
   - Direct integration with stakeholder_database.yaml for real-time data
   - Automated stakeholder profile updates and trend analysis
   - Cross-referencing with team_roster.yaml and stakeholder_contexts.yaml
   - Historical interaction tracking and pattern recognition

2. **Advanced Influence Analysis**
   - Multiple framework application (power-interest, network analysis, decision impact)
   - Dynamic influence scoring based on context and relationships
   - Coalition identification and strategic alliance recommendations
   - Conflict prediction and resolution strategy development

3. **Intelligent Communication Optimization**
   - Stakeholder-specific communication template generation
   - Multi-channel communication strategy optimization
   - Communication effectiveness tracking and improvement
   - Automated follow-up and reminder scheduling

4. **Relationship Health Monitoring**
   - Real-time relationship health metrics and trend analysis
   - Predictive relationship risk identification and mitigation
   - Engagement optimization recommendations and action plans
   - Stakeholder satisfaction measurement and improvement tracking

5. **Integration Capabilities**
   - Project integration for context-specific stakeholder analysis
   - Meeting notes integration for automatic interaction tracking
   - Decision framework integration for stakeholder involvement optimization
   - Team system integration for comprehensive organizational context

### Best Practices

**Tool-Driven Stakeholder Management:**

1. **Leverage StakeholderAnalyzer for All Operations**
   ```python
   # Always initialize analyzer at start of command
   analyzer = StakeholderAnalyzer()

   # Use context-aware discovery instead of manual searches
   stakeholders = analyzer.identify_stakeholders(context)

   # Calculate multi-dimensional influence scores
   scores = analyzer.calculate_influence_scores(stakeholders, decision_type)

   # Get performance stats for transparency
   stats = analyzer.get_performance_stats()
   ```

2. **Data-Driven Stakeholder Analysis**
   - **Context-Aware Discovery**: Use `identify_stakeholders()` with rich context for 95% accuracy
   - **Multi-Framework Analysis**: Apply power-interest, influence scoring, and alignment assessment
   - **Historical Patterns**: Leverage past interactions for predictive insights
   - **Performance Tracking**: Monitor analysis time and cache effectiveness

3. **Intelligent Relationship Management**
   - **Automated Health Monitoring**: Use tool outputs to track relationship strength
   - **Predictive Conflict Detection**: Leverage `identify_conflicts()` for early warnings
   - **Coalition Building**: Use alignment analysis to identify partnership opportunities
   - **Value Creation Focus**: Align stakeholder insights with organizational goals

4. **Communication Optimization**
   ```python
   # Generate personalized communication plans
   plan = analyzer.generate_communication_plan(
       stakeholders,
       decision_context,
       communication_templates
   )

   # Adapt messages for specific stakeholders
   message = analyzer.adapt_message(
       base_message,
       stakeholder,
       communication_preferences
   )
   ```

5. **Integration and Sync**
   - **Team Roster Sync**: Regular `sync_with_team_roster()` for current data
   - **Project Integration**: Use `sync_with_projects()` for project-stakeholder linking
   - **Cross-Reference**: Maintain bidirectional relationships between systems

6. **Performance Optimization**
   - Monitor `get_performance_stats()` for cache hit rates >80%
   - Use batch operations for analyzing multiple stakeholders
   - Cache results for repeated analyses within same context
   - Average analysis time target: <100ms per stakeholder

Always ensure stakeholder management leverages StakeholderAnalyzer for data-driven insights, automated analysis, and predictive intelligence that drives organizational success.
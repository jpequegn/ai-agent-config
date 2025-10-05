---
name: project-decide
description: Decision analysis framework with pros/cons evaluation and stakeholder impact assessment
---

# /project decide - Intelligent Decision Analysis

Comprehensive decision support system that analyzes options, evaluates trade-offs, assesses stakeholder impacts, and provides evidence-based recommendations for project-related decisions.

## Usage Examples:
- `/project decide "Mobile App launch strategy"` - Analyze decision with available options
- `/project decide --project mobile-app-v2 --options "simultaneous,staggered"` - Project-specific decision
- `/project decide "Budget allocation Q1" --stakeholders --impact-analysis` - Stakeholder-focused analysis
- `/project decide --template timeline-decision --factors "resource,budget,risk"` - Template-based analysis
- `/project decide "Technology stack" --format executive-brief --decision-by 2024-12-15` - Executive decision brief

## Instructions:

You are an intelligent decision analysis system that transforms complex business decisions into structured, evidence-based recommendations. When this command is invoked, you will:

### Core Functionality

1. **Decision Framing and Context**
   - Define the decision clearly with success criteria
   - Identify key stakeholders and their interests
   - Establish decision timeline and constraints
   - Map dependencies and related project impacts

2. **Option Generation and Analysis**
   - Generate comprehensive option sets (including hybrid approaches)
   - Analyze feasibility, cost, timeline, and risk for each option
   - Identify hidden costs and long-term implications
   - Consider do-nothing scenarios and opportunity costs

3. **Evidence-Based Evaluation**
   - Apply decision frameworks (cost-benefit, risk-adjusted NPV, strategic fit)
   - Use historical data and pattern recognition for predictions
   - Quantify impacts using project metrics and success indicators
   - Validate assumptions with available data and expert insights

4. **Stakeholder Impact Assessment**
   - Analyze impact on each stakeholder group
   - Identify potential conflicts and alignment opportunities
   - Assess communication and change management requirements
   - Generate stakeholder-specific messaging and rationales

### Command Actions

**Standard Decision Analysis `/project decide "Decision Topic"`:**

Execute comprehensive decision framework:

1. **Decision Structuring**
   ```python
   from tools import OutputFormatter

   decision_data = {
       'decision': {
           'title': decision_topic,
           'description': extract_description(),
           'urgency': assess_urgency(),  # critical, high, medium, low
           'deadline': determine_deadline()
       },
       'options': [
           {
               'name': option_name,
               'description': option_description,
               'score': calculate_overall_score(),
               'pros': list_of_pros,
               'cons': list_of_cons,
               'criteria_scores': {
                   'strategic_impact': 0.0-1.0,
                   'cost_efficiency': 0.0-1.0,
                   'implementation_risk': 0.0-1.0,
                   # Additional criteria as needed
               },
               'estimated_cost': cost_estimate,
               'estimated_time': time_estimate
           }
           # Generate multiple options including status quo
       ],
       'recommendation': {
           'option': recommended_option_name,
           'reasoning': detailed_rationale,
           'confidence': 0.0-1.0
       },
       'stakeholder_impact': {
           'stakeholder_name': {
               'description': impact_description,
               'sentiment': 'positive' | 'neutral' | 'negative'
           }
       },
       'risks': [
           {
               'title': risk_title,
               'severity': 'critical' | 'high' | 'medium' | 'low',
               'likelihood': 'high' | 'medium' | 'low',
               'description': risk_description,
               'mitigation': mitigation_strategy
           }
       ],
       'next_steps': [
           {
               'action': action_description,
               'owner': owner_name,
               'deadline': deadline_date
           }
       ]
   }

   formatter = OutputFormatter()
   output = formatter.format_markdown(decision_data, template="decision_analysis")
   print(output.content)
   ```

2. **Present Structured Recommendation**
   - Use OutputFormatter with decision_analysis template
   - Template automatically handles formatting, emojis, and health scores
   - Consistent presentation across all decision analyses

**Project-Specific Decision `/project decide --project {project-name}`:**

Execute project-contextualized analysis:

1. **Project Context Integration**
   - Load project data, milestones, and current status using ConfigManager
   - Analyze decision impact on project timeline and success
   - Consider resource allocation and dependency effects
   - Evaluate alignment with project goals and constraints

2. **Cross-Project Impact Analysis**
   - Assess ripple effects on other projects in portfolio
   - Identify resource conflicts and optimization opportunities
   - Consider strategic portfolio alignment and priorities

### Output Format

The command now uses the **OutputFormatter** tool with the `decision_analysis.md.j2` template for consistent, professional output. The template automatically handles:

- **Decision Overview**: Title, description, urgency, and deadline
- **Options Analysis**: Pros/cons with emoji indicators, scoring, costs, and timelines
- **Criteria Evaluation**: Health scores for each option across evaluation criteria
- **Recommendations**: Clear recommendation with confidence level and reasoning
- **Stakeholder Impact**: Impact analysis by stakeholder group with sentiment indicators
- **Risk Assessment**: Risk identification with severity/likelihood and mitigation strategies
- **Next Steps**: Action items with owners and deadlines

**Example Output Structure** (generated by template):

```markdown
## 🎯 Decision Overview

**Decision**: Technology Stack Selection

Modern web framework selection for new product line...

**Urgency**: 🔴 High
**Deadline**: Dec 15, 2024

## 📊 Options Analysis

### Option 1: React with TypeScript

Modern web framework with strong ecosystem...

**Overall Score**: 🟢 85.0%

#### Pros
- ✅ Strong ecosystem and community support
- ✅ Team already experienced with React
- ✅ Excellent tooling and development experience

#### Cons
- ⚠️ Higher learning curve for TypeScript
- ⚠️ Requires additional build tooling

#### Criteria Evaluation
- 🟢 Strategic Impact: 90.0%
- 🟢 Cost Efficiency: 80.0%
- 🟡 Implementation Risk: 70.0%

**Estimated Cost**: $50,000
**Estimated Time**: 3 months

---

### Option 2: Vue.js

Progressive framework with gentle learning curve...

**Overall Score**: 🟡 72.0%

[Additional options...]

## 🎓 Recommendation

ℹ️ **Recommended Option**: React with TypeScript

**Reasoning**:
Based on team experience, ecosystem maturity, and long-term maintainability...

**Confidence**: 🟢 85.0%

## 👥 Stakeholder Impact

- **Engineering Team**: Positive alignment with existing skills (🟢 positive)
- **Product Management**: Faster time-to-market capabilities (🟢 positive)

## ⚠️ Risks & Mitigation

### ⚠️ Learning Curve for TypeScript

**Severity**: Medium | **Likelihood**: Medium

Team will need training on TypeScript patterns...

**Mitigation Strategy**:
Allocate 2 weeks for team training and pair programming...

## 📅 Next Steps

1. Approve framework selection and budget allocation (Owner: CTO) - Due: Dec 1, 2024
2. Schedule TypeScript training for team (Owner: Engineering Manager) - Due: Dec 5, 2024
```

### Implementation Steps

When executing this command:

1. **Decision Context Analysis**
   ```python
   # Parse decision topic and identify key elements
   # Load relevant project data using ConfigManager if --project specified
   # Identify stakeholders and their interests
   # Establish success criteria and evaluation framework
   ```

2. **Option Generation**
   ```python
   # Generate comprehensive option set
   # Include hybrid and creative alternatives
   # Consider do-nothing and status quo scenarios
   # Validate option feasibility against constraints
   # Calculate overall scores (0.0-1.0) for each option
   ```

3. **Structure Decision Data**
   ```python
   from tools import OutputFormatter

   # Build decision data structure matching template requirements
   decision_data = {
       'decision': {...},
       'options': [...],
       'recommendation': {...},
       'stakeholder_impact': {...},
       'risks': [...],
       'next_steps': [...]
   }
   ```

4. **Generate Output**
   ```python
   # Use OutputFormatter for consistent formatting
   formatter = OutputFormatter()
   output = formatter.format_markdown(
       decision_data,
       template="decision_analysis"
   )
   print(output.content)
   ```

### Decision Analysis Best Practices

**Comprehensive Option Analysis:**
- Always include status quo/do-nothing option for comparison
- Generate at least 2-3 viable alternatives
- Calculate realistic scores (0.0-1.0) based on evidence
- Consider both short-term and long-term implications

**Stakeholder Consideration:**
- Map all affected stakeholder groups
- Assess sentiment realistically (positive/neutral/negative)
- Tailor communication strategies to stakeholder concerns
- Build consensus through transparent analysis

**Risk Management:**
- Identify high-impact risks with realistic probability/severity
- Provide specific, actionable mitigation strategies
- Include contingency plans for critical risks
- Balance optimism with practical risk assessment

**Project Integration:**
- Use ConfigManager to load project context when --project specified
- Analyze decision impact on project milestones and timeline
- Consider resource allocation and dependency effects
- Evaluate cross-project portfolio implications

### Error Handling

- **Insufficient Information**: Request critical missing details before analysis
- **Conflicting Constraints**: Identify and highlight constraint conflicts
- **Unclear Decision Topic**: Provide structured questions to clarify scope
- **Missing Stakeholder Data**: Use available information and note limitations
- **Template Rendering Errors**: Validate decision_data structure matches template expectations

### Tool Integration Benefits

**OutputFormatter Integration:**
- **Consistency**: 250+ lines of manual template → 10-15 lines of structured data
- **Maintainability**: Template changes apply to all decision analyses automatically
- **Features**: Automatic emoji indicators, health score formatting, date formatting
- **Performance**: <50ms template rendering, cached for session reuse
- **Quality**: Type-safe data structure prevents formatting errors

**ConfigManager Integration:**
- **Project Context**: Load project data for project-specific decision analysis
- **Type Safety**: Pydantic validation ensures data integrity
- **Performance**: <10ms cached configuration reads
- **Error Handling**: Clear error messages for missing/invalid configurations

Remember: Great decisions come from structured analysis, stakeholder consideration, and evidence-based reasoning. OutputFormatter ensures this analysis is presented consistently and professionally.

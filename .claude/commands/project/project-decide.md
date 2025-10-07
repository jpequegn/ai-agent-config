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
- `/project decide --template framework-analysis --factors "resource,budget,risk"` - Framework-based analysis
- `/project decide "Technology stack" --format executive-brief --decision-by 2024-12-15` - Executive decision brief

## Instructions:

You are an intelligent decision analysis system that transforms complex business decisions into structured, evidence-based recommendations using the **DecisionAnalyzer tool**.

### Tool-Based Implementation

**Standard Decision Analysis** `/project decide "Decision Topic"`:

```python
from tools import DecisionAnalyzer

# Initialize analyzer
analyzer = DecisionAnalyzer()

# Define decision and options
decision_title = "{extracted_from_user_input}"
description = "{comprehensive_decision_context}"
options = [
    {
        "name": "Option 1 Name",
        "description": "Detailed option description",
        "pros": ["Advantage 1", "Advantage 2", "Advantage 3"],
        "cons": ["Disadvantage 1", "Disadvantage 2"],
        # Criterion scores (0.0-1.0)
        "strategic_impact_score": 0.85,
        "cost_efficiency_score": 0.70,
        "implementation_risk_score": 0.60,
        "timeline_score": 0.75,
        "estimated_cost": "$50,000",
        "estimated_time": "3 months"
    },
    {
        "name": "Option 2 Name",
        "description": "Alternative approach description",
        "pros": ["Different advantage 1", "Different advantage 2"],
        "cons": ["Different concern 1", "Different concern 2"],
        "strategic_impact_score": 0.70,
        "cost_efficiency_score": 0.85,
        "implementation_risk_score": 0.75,
        "timeline_score": 0.80,
        "estimated_cost": "$30,000",
        "estimated_time": "2 months"
    },
    # Include status quo / do-nothing option for comparison
    {
        "name": "Status Quo",
        "description": "Maintain current approach",
        "pros": ["No change risk", "Zero implementation cost"],
        "cons": ["Missed opportunity", "Continued problems"],
        "strategic_impact_score": 0.40,
        "cost_efficiency_score": 0.90,
        "implementation_risk_score": 0.95,
        "timeline_score": 0.95,
        "estimated_cost": "$0",
        "estimated_time": "0 months"
    }
]

# Apply decision framework
analysis = analyzer.apply_framework(
    decision_title=decision_title,
    options=options,
    framework_type="business",  # or "technical", "strategic", "general"
    description=description,
    urgency="high",  # "critical", "high", "medium", "low"
    deadline="2024-12-15",  # Optional deadline
    output_format="markdown"
)

# Output formatted analysis
print(analysis.formatted_output)
```

**Project-Specific Decision** `/project decide --project {project-name}`:

```python
from tools import DecisionAnalyzer, ConfigManager

analyzer = DecisionAnalyzer()
config_mgr = ConfigManager()

# Load project context
project_data = config_mgr.get_project(project_name)

# Enhance decision analysis with project context
decision_title = f"{decision_topic} for {project_name}"
description = f"""
Decision context: {decision_description}

Project: {project_name}
Current Status: {project_data.status}
Timeline Impact: Decision affects project milestone {relevant_milestone}
Resource Constraints: {project_resource_constraints}
"""

# Generate options considering project constraints
options = generate_project_aware_options(project_data, decision_context)

# Apply framework
analysis = analyzer.apply_framework(
    decision_title=decision_title,
    options=options,
    framework_type="business",
    description=description,
    urgency=assess_project_urgency(project_data),
    deadline=project_data.get("next_milestone_date")
)

print(analysis.formatted_output)
```

**Stakeholder Impact Analysis** `--stakeholders --impact-analysis`:

```python
from tools import DecisionAnalyzer

analyzer = DecisionAnalyzer()

# First, apply decision framework
analysis = analyzer.apply_framework(
    decision_title=decision_title,
    options=options,
    framework_type="strategic"
)

# Then, analyze stakeholder impact
stakeholder_impact = analyzer.analyze_stakeholder_impact(
    decision_title=decision_title,
    options=options,
    stakeholders=["engineering", "product", "executive"],  # Or None for auto-detection
    decision_type="strategic"
)

# Update analysis with stakeholder data
analysis.stakeholder_impact = stakeholder_impact

# Generate stakeholder-focused report
output = analyzer.generate_decision_report(
    analysis=analysis,
    template="stakeholder_impact",
    include_stakeholders=True
)

print(output)
```

**Framework-Specific Analysis** `--template framework-analysis`:

```python
from tools import DecisionAnalyzer

analyzer = DecisionAnalyzer()

# Apply specific framework (technical, business, strategic, etc.)
analysis = analyzer.apply_framework(
    decision_title=decision_title,
    options=options,
    framework_type="technical",  # Framework determines criteria and weights
    description=description,
    urgency="medium",
    output_format="markdown"
)

# Generate framework-focused report with scoring matrix
output = analyzer.generate_decision_report(
    analysis=analysis,
    template="framework_analysis",
    include_stakeholders=False
)

print(output)
```

**Option Comparison** `--compare-options`:

```python
from tools import DecisionAnalyzer

analyzer = DecisionAnalyzer()

# Define custom criteria for comparison
criteria = [
    {"name": "strategic_impact", "weight": 0.30},
    {"name": "cost_efficiency", "weight": 0.25},
    {"name": "implementation_risk", "weight": 0.20},
    {"name": "timeline", "weight": 0.15},
    {"name": "team_capability", "weight": 0.10}
]

# Compare options using multi-criteria analysis
comparison = analyzer.compare_options(
    options=options,
    criteria=criteria
)

# Generate comparison report
analysis = analyzer.apply_framework(
    decision_title=decision_title,
    options=options,
    framework_type="general",
    description=description
)

output = analyzer.generate_decision_report(
    analysis=analysis,
    template="option_comparison"
)

print(output)
```

### Output Templates

The DecisionAnalyzer tool integrates with OutputFormatter and supports multiple templates:

- **decision_analysis** (default): Comprehensive decision analysis with all components
- **framework_analysis**: Framework-focused analysis with detailed scoring matrices
- **stakeholder_impact**: Stakeholder-centric analysis with impact assessment
- **option_comparison**: Side-by-side option comparison with rankings

### Decision Analysis Best Practices

**Comprehensive Option Analysis:**
- Always include status quo/do-nothing option for comparison
- Generate at least 2-3 viable alternatives
- Calculate realistic scores (0.0-1.0) based on evidence and analysis
- Consider both short-term and long-term implications
- Include concrete cost and timeline estimates when available

**Criterion Scoring Guidelines:**
- **Strategic Impact** (0.0-1.0): Alignment with goals, competitive advantage, market positioning
- **Cost Efficiency** (0.0-1.0): Total cost of ownership, ROI, budget fit
- **Implementation Risk** (0.0-1.0): Technical complexity, team capability, external dependencies
- **Timeline** (0.0-1.0): Speed to value, deadline feasibility, resource availability

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

### Tool Integration Benefits

**DecisionAnalyzer Integration:**
- **Simplification**: 323 lines → ~150 lines (53% reduction) through tool delegation
- **Consistency**: Standardized decision methodology across all decision commands
- **Performance**: <50ms framework application with automatic caching
- **Testability**: Centralized decision logic with comprehensive unit tests
- **Reusability**: Same tool used across /decide, /decide-framework, /decide-stakeholder

**OutputFormatter Integration:**
- **Templates**: Professional template-based output with automatic formatting
- **Consistency**: Uniform presentation across all decision analyses
- **Features**: Automatic emoji indicators, health score formatting, date formatting
- **Performance**: <50ms template rendering with session-based caching
- **Quality**: Type-safe data structures prevent formatting errors

### Error Handling

- **Insufficient Information**: Request critical missing details before analysis
- **Invalid Options**: Validate option structure and provide clear error messages
- **Framework Loading Errors**: Gracefully fall back to default framework
- **Template Errors**: DecisionAnalyzer handles template validation and fallbacks automatically

Remember: Great decisions come from structured analysis, stakeholder consideration, and evidence-based reasoning. DecisionAnalyzer ensures this analysis is presented consistently and professionally.

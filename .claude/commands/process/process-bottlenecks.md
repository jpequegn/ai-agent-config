---
name: process bottlenecks
description: Cross-process bottleneck identification with impact analysis and ROI-prioritized recommendations
---

# Process Bottlenecks

Identify and analyze bottlenecks across all organizational processes with quantified impact analysis, root cause investigation, and ROI-prioritized improvement recommendations.

## Usage Examples:
- `/process bottlenecks` - Cross-process bottleneck analysis
- `/process bottlenecks --critical-only` - Show only critical bottlenecks (>2 days impact)
- `/process bottlenecks --category development` - Focus on development process bottlenecks
- `/process bottlenecks --include-root-cause` - Include detailed root cause analysis

## Instructions:

You are a bottleneck analysis specialist focused on identifying the highest-impact process constraints. When this command is invoked:

1. **Load and Analyze Process Data**:
   - Access `.claude/workflow_definitions.yaml` for current process definitions
   - Load project performance data from `projects.yaml`
   - Integrate team capacity data from `team_roster.yaml`
   - Pull meeting efficiency data for decision velocity analysis

2. **Bottleneck Detection Algorithm**:
   - **Statistical Analysis**: Identify stages with highest variance and longest durations
   - **Frequency Analysis**: Calculate how often each bottleneck affects processes
   - **Impact Quantification**: Measure delay impact in days/hours lost per month
   - **Critical Path Analysis**: Identify bottlenecks that affect overall process completion

3. **Generate Bottleneck Analysis Report**:

**Output Format (Human-Readable Markdown):**

```markdown
# Development Process Bottleneck Analysis

**Critical Bottlenecks (Impact > 2 days average delay):**

## 1. Code Review Process 🔴
- **Average Delay**: 2.3 days (target: same day)
- **Frequency**: 75% of features affected
- **Root Cause Analysis**:
  - Only 2 people qualified for architecture reviews
  - Reviews queued behind urgent bug fixes
  - No clear SLA or prioritization system
- **Impact**: 17.25 days lost per month across team

## 2. Testing Environment Access 🟡
- **Average Delay**: 1.8 days (target: immediate)
- **Frequency**: 40% of features affected
- **Root Cause**: Environment conflicts, unclear booking system
- **Impact**: 14.4 days lost per month

## 3. Requirements Clarification 🟡
- **Average Delay**: 1.2 days (target: 0.5 days)
- **Frequency**: 60% of features affected
- **Root Cause**: Product manager availability, unclear initial specs
- **Impact**: 14.4 days lost per month

**Process Performance Trends:**
- **Cycle Time**: Increased from 7 to 9 days over last quarter
- **Throughput**: Decreased from 4.1 to 3.2 features/week
- **Defect Rate**: Improved from 0.12 to 0.08 (code reviews helping quality)

**Improvement Recommendations (ROI Prioritized):**

### High Impact, Low Effort:
1. **Implement Code Review SLA**: 24-hour review commitment + notification system
   - *Expected Impact*: Reduce cycle time by 1.5 days
   - *Implementation*: 1 week (GitHub automation + team process)

### Medium Impact, Medium Effort:
2. **Testing Environment Automation**: Self-service environment provisioning
   - *Expected Impact*: Reduce delays by 1.2 days per feature
   - *Implementation*: 3 weeks (DevOps work)

3. **Requirements Template**: Structured PRD template with acceptance criteria
   - *Expected Impact*: Reduce clarification cycles by 50%
   - *Implementation*: 2 weeks (template + training)

**Projected Results if Implemented:**
- Cycle time: 9 → 6.3 days (30% improvement)
- Throughput: 3.2 → 4.5 features/week (40% improvement)
- Team satisfaction: Reduced context switching and waiting
```

4. **Analysis Modes**:

### Cross-Process Analysis (Default)
- Analyze bottlenecks across all organizational processes
- Identify system-wide constraint patterns
- Quantify cumulative impact on organizational throughput
- Prioritize improvements by global ROI

### Critical Only (`--critical-only`)
- Focus on bottlenecks with >2 days average delay
- High-frequency issues affecting >50% of processes
- Critical path bottlenecks that block multiple processes

### Category Focus (`--category [name]`)
- Deep dive into specific process category bottlenecks
- Category-specific improvement recommendations
- Resource optimization within category

### Root Cause Analysis (`--include-root-cause`)
- Detailed root cause investigation using 5 whys
- Fishbone analysis for complex bottlenecks
- Correlation analysis between bottlenecks and external factors

## Parameters:
- `--critical-only` - Show only critical bottlenecks (>2 days impact)
- `--category NAME` - Focus on specific process category
- `--include-root-cause` - Include detailed root cause analysis
- `--time-period PERIOD` - Analysis period (30d, 90d, 1y)
- `--threshold DAYS` - Custom threshold for critical bottlenecks
- `--format markdown|json` - Output format (default: markdown)

## Bottleneck Classification:

### 🔴 Critical (Red)
- **Criteria**: >2 days average delay OR >50% frequency OR blocks critical path
- **Priority**: Immediate attention required
- **Escalation**: Executive visibility needed

### 🟡 Warning (Yellow)
- **Criteria**: 0.5-2 days average delay OR 25-50% frequency
- **Priority**: Plan improvement within current quarter
- **Resource**: Team-level resolution

### 🟢 Monitor (Green)
- **Criteria**: <0.5 days average delay OR <25% frequency
- **Priority**: Track for trends, improve when convenient
- **Action**: Process optimization backlog

## Impact Calculation:

### Quantified Impact Formula
```
Monthly Impact = (Average Delay × Frequency × Items per Month)
ROI Score = (Monthly Impact × Cost per Delay Day) / Implementation Cost
```

### Cost Factors
- **Developer Time**: $500/day (loaded cost)
- **Opportunity Cost**: Lost features, delayed releases
- **Quality Impact**: Defect costs, rework time
- **Team Morale**: Context switching, frustration costs

## Root Cause Analysis Framework:

### 5 Whys Investigation
- Systematic drilling down to underlying causes
- Document each level of "why" with evidence
- Identify systemic vs. symptomatic issues

### Fishbone Categories
- **People**: Skills, availability, training, motivation
- **Process**: Procedures, handoffs, approvals, communication
- **Technology**: Tools, systems, automation, integration
- **Environment**: Physical/virtual workspace, culture, policies

### Correlation Analysis
- Statistical correlation between bottlenecks and:
  - Team workload and capacity
  - External dependencies and vendor performance
  - Seasonal patterns and business cycles
  - Tool performance and system reliability

## Integration Points:
- **Input**: Workflow definitions, project data, team metrics
- **Output**: Prioritized improvement roadmap for `/process optimize`
- **Monitoring**: Integration with `/process metrics` for trend tracking
- **Visualization**: Support for `/process map` bottleneck highlighting

## Success Metrics:
- **Bottleneck Resolution Time**: Time to resolve identified bottlenecks
- **Impact Reduction**: Measured decrease in delay days per month
- **Process Velocity**: Improvement in overall cycle times
- **Team Satisfaction**: Reduced frustration with process delays

## Error Handling:
- Missing performance data: Use estimation models based on team input
- Insufficient historical data: Focus on current state with future monitoring setup
- Integration failures: Graceful fallback to manual data entry
- Complex root causes: Escalate for expert analysis

Provide actionable, quantified insights that enable data-driven process improvement decisions with clear ROI justification for all recommendations.
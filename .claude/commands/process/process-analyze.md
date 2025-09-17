---
name: process analyze
description: Comprehensive process analysis with bottleneck identification and improvement opportunities
---

# Process Analysis

Analyze organizational processes using workflow definitions to identify bottlenecks, inefficiencies, and optimization opportunities.

## Usage Examples:
- `/process analyze --workflow feature-dev-process` - Analyze feature development process
- `/process analyze --category development` - Analyze all development processes
- `/process analyze --comprehensive` - Full organizational process analysis
- `/process analyze --bottlenecks` - Focus on bottleneck identification

## Instructions:

You are a process analysis specialist focused on identifying inefficiencies and optimization opportunities. When this command is invoked:

1. **Load Process Data** from workflow definitions:
   - Access `.claude/workflow_definitions.yaml` for current process definitions
   - Access `.claude/optimization_frameworks.yaml` for improvement methodologies
   - Integrate with project data from `projects.yaml` and team data from `team_roster.yaml`

2. **Analyze Process Performance**:
   - Calculate actual vs. target metrics (cycle time, throughput, quality)
   - Identify processes exceeding benchmark thresholds
   - Map dependencies and handoff points between stages
   - Assess resource utilization and capacity constraints

3. **Bottleneck Identification**:
   - Analyze stage duration variances and identify constraint points
   - Calculate bottleneck impact on overall process flow
   - Identify recurring delay patterns and root causes
   - Assess resource conflicts and scheduling issues

4. **Generate Analysis Report**:
   ```json
   {
     "process_health_summary": {
       "total_processes_analyzed": N,
       "processes_meeting_targets": N,
       "processes_requiring_attention": N,
       "overall_efficiency_score": "X.X/10"
     },
     "critical_bottlenecks": [
       {
         "process": "process_name",
         "stage": "stage_name",
         "impact": "high|medium|low",
         "delay_factor": "X.X",
         "root_causes": ["cause1", "cause2"],
         "recommended_actions": ["action1", "action2"]
       }
     ],
     "performance_gaps": [
       {
         "process": "process_name",
         "metric": "cycle_time|throughput|quality",
         "current": "X units",
         "target": "Y units",
         "gap_percentage": "Z%",
         "trend": "improving|stable|declining"
       }
     ],
     "optimization_opportunities": [
       {
         "process": "process_name",
         "opportunity": "description",
         "framework": "lean|six_sigma|agile|toc|bpr",
         "estimated_impact": "high|medium|low",
         "implementation_effort": "low|medium|high"
       }
     ]
   }
   ```

5. **Analysis Modes**:

### Comprehensive Analysis (`--comprehensive`)
- Full organizational process assessment
- Cross-process dependency analysis
- Resource allocation optimization
- Strategic improvement roadmap

### Bottleneck Focus (`--bottlenecks`)
- Constraint identification across all processes
- Impact analysis and prioritization
- Root cause analysis for critical delays
- Immediate action recommendations

### Category Analysis (`--category [name]`)
- Deep dive into specific process categories
- Category-specific metrics and benchmarks
- Inter-process coordination within category
- Category optimization recommendations

### Single Process Analysis (`--workflow [id]`)
- Detailed analysis of specific workflow
- Stage-by-stage performance assessment
- Historical trend analysis if data available
- Specific improvement recommendations

## Parameters:
- `--workflow ID` - Analyze specific workflow by ID
- `--category NAME` - Analyze processes in specific category (development, maintenance, people, planning, governance)
- `--comprehensive` - Full organizational process analysis
- `--bottlenecks` - Focus on bottleneck identification and impact analysis
- `--metrics` - Include detailed performance metrics and trends
- `--recommendations` - Include specific improvement recommendations with frameworks
- `--format json|markdown` - Output format (default: json for Claude Code integration)

## Integration Points:

**Data Sources**:
- `workflow_definitions.yaml` - Current process definitions and metrics
- `optimization_frameworks.yaml` - Improvement methodologies and techniques
- `projects.yaml` - Project performance data and timelines
- `team_roster.yaml` - Team capacity and workload information
- `meeting_notes` - Decision velocity and action item completion

**Output Integration**:
- Results feed into `/process optimize` for improvement planning
- Metrics integration with `/process metrics` for tracking
- Workflow visualization support for `/process map`

## Analysis Framework:

### Performance Assessment
- **Efficiency Metrics**: Cycle time, processing time, wait time, utilization rate
- **Quality Metrics**: Defect rate, first pass yield, customer satisfaction, rework rate
- **Productivity Metrics**: Throughput, resource productivity, value-added ratio, cost per unit
- **Flexibility Metrics**: Changeover time, response time, adaptability score

### Bottleneck Analysis
- **Constraint Identification**: Statistical analysis of stage durations and capacity
- **Impact Measurement**: Quantified effect on overall process performance
- **Root Cause Analysis**: Systematic investigation using 5 whys, fishbone, Pareto
- **Solution Prioritization**: Impact vs. effort matrix for improvement actions

### Trend Analysis
- **Historical Performance**: Track metrics over time for improvement/degradation patterns
- **Seasonal Patterns**: Identify cyclical variations in process performance
- **Correlation Analysis**: Relationship between different metrics and external factors
- **Predictive Insights**: Early warning indicators for process degradation

## Error Handling:
- Missing workflow data: Provide template for data collection
- Insufficient metrics: Recommend measurement implementation
- No historical data: Focus on current state analysis with baseline establishment
- Integration failures: Graceful fallback to available data sources

Be systematic, data-driven, and provide actionable insights for process improvement using the established optimization frameworks.
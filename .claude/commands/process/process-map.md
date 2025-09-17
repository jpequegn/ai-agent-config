---
name: process map
description: Visualize and map process workflows with dependencies, handoffs, and value stream analysis
---

# Process Mapping

Create visual representations of organizational processes with workflow mapping, dependency analysis, and value stream visualization for better process understanding and optimization.

## Usage Examples:
- `/process map --workflow feature-dev-process` - Map feature development workflow
- `/process map --category development --dependencies` - Show development processes with dependencies
- `/process map --value-stream` - Create value stream map with waste identification
- `/process map --handoffs` - Focus on handoff points and transitions

## Instructions:

You are a process mapping specialist focused on visual workflow representation and dependency analysis. When this command is invoked:

1. **Load Process Data**:
   - Access workflow definitions from `workflow_definitions.yaml`
   - Load optimization insights from `optimization_frameworks.yaml`
   - Integrate team structure from `team_roster.yaml`
   - Pull project dependencies from `projects.yaml`

2. **Process Visualization Strategy**:
   - **Workflow Diagrams**: Step-by-step process visualization
   - **Value Stream Maps**: End-to-end value flow with waste identification
   - **Swimlane Diagrams**: Cross-functional process responsibility mapping
   - **Dependency Maps**: Process interdependencies and critical paths

3. **Generate Process Map**:
   ```json
   {
     "process_map_summary": {
       "map_type": "workflow|value_stream|swimlane|dependency",
       "process_name": "process_name",
       "total_stages": N,
       "critical_path_length": "X days",
       "value_added_percentage": "Y%",
       "handoff_points": N
     },
     "process_flow": [
       {
         "stage_id": "stage_identifier",
         "stage_name": "stage_name",
         "sequence": N,
         "type": "value_adding|non_value_adding|business_required",
         "duration": {
           "min": "X hours",
           "avg": "Y hours",
           "max": "Z hours"
         },
         "inputs": ["input1", "input2"],
         "outputs": ["output1", "output2"],
         "responsible_role": "role_name",
         "supporting_roles": ["role1", "role2"],
         "tools_systems": ["tool1", "tool2"],
         "decision_points": [
           {
             "decision": "decision_description",
             "criteria": "decision_criteria",
             "outcomes": ["outcome1", "outcome2"]
           }
         ],
         "bottleneck_indicators": {
           "is_bottleneck": true|false,
           "constraint_type": "resource|capacity|policy|knowledge",
           "impact_factor": "X.X",
           "frequency": "always|often|sometimes|rarely"
         },
         "waste_analysis": {
           "waste_types": ["waiting", "overproduction", "transportation", "inappropriate_processing", "unnecessary_inventory", "unnecessary_motion", "defects", "unused_creativity"],
           "waste_time": "X hours",
           "improvement_opportunity": "description"
         }
       }
     ],
     "handoff_analysis": [
       {
         "from_stage": "stage_name",
         "to_stage": "stage_name",
         "handoff_type": "information|material|responsibility|approval",
         "handoff_method": "email|meeting|system|document",
         "typical_delay": "X hours",
         "failure_rate": "Y%",
         "improvement_suggestions": ["suggestion1", "suggestion2"]
       }
     ],
     "dependency_mapping": [
       {
         "process": "process_name",
         "depends_on": ["process1", "process2"],
         "dependency_type": "sequential|parallel|conditional",
         "critical_path": true|false,
         "risk_level": "high|medium|low",
         "coordination_mechanism": "meetings|systems|documents"
       }
     ],
     "visual_representation": {
       "ascii_diagram": "text-based process flow",
       "mermaid_syntax": "mermaid diagram code",
       "graphviz_dot": "graphviz diagram code",
       "flowchart_json": "structured flowchart data"
     },
     "optimization_insights": [
       {
         "insight_type": "bottleneck|waste|handoff|dependency",
         "description": "insight_description",
         "impact": "high|medium|low",
         "recommendation": "specific_action",
         "framework": "lean|six_sigma|agile|toc|bpr"
       }
     ]
   }
   ```

4. **Mapping Modes**:

### Workflow Mapping (`--workflow [id]`)
Standard process flow visualization:
- Sequential step representation
- Decision points and branching
- Role responsibilities and handoffs
- Time and resource allocation
- Quality gates and checkpoints

### Value Stream Mapping (`--value-stream`)
Lean-focused value flow analysis:
- Current state mapping with all activities
- Value-adding vs. non-value-adding identification
- Lead time and processing time analysis
- Waste identification and quantification
- Future state design opportunities

### Swimlane Mapping (`--swimlane`)
Cross-functional responsibility mapping:
- Role-based activity organization
- Clear responsibility boundaries
- Communication and handoff visualization
- Accountability and ownership clarity
- Cross-functional coordination points

### Dependency Mapping (`--dependencies`)
Process interdependency analysis:
- Critical path identification
- Parallel vs. sequential dependencies
- Resource sharing and conflicts
- Coordination requirements
- Risk and bottleneck propagation

## Parameters:
- `--workflow ID` - Map specific workflow by ID
- `--category NAME` - Map all processes in category
- `--value-stream` - Create value stream map with waste analysis
- `--swimlane` - Generate cross-functional swimlane diagram
- `--dependencies` - Focus on process dependencies and critical paths
- `--handoffs` - Highlight handoff points and transitions
- `--bottlenecks` - Emphasize constraint points and bottlenecks
- `--format ascii|mermaid|graphviz|json` - Output format preference
- `--detail high|medium|low` - Level of detail in visualization

## Visualization Formats:

### ASCII Diagram
Text-based flowchart for quick viewing:
```
[Start] -> [Stage 1] -> [Decision] -> [Stage 2] -> [End]
             |             |            |
             v             v            v
        [Support]    [Alternative]  [Review]
```

### Mermaid Syntax
Modern diagram syntax for web rendering:
```mermaid
graph TD
    A[Start] --> B[Stage 1]
    B --> C{Decision}
    C -->|Yes| D[Stage 2]
    C -->|No| E[Alternative]
    D --> F[End]
    E --> F
```

### Graphviz DOT
Professional diagram language:
```dot
digraph process {
    rankdir=TD;
    start -> stage1 -> decision;
    decision -> stage2 [label="yes"];
    decision -> alternative [label="no"];
    stage2 -> end;
    alternative -> end;
}
```

### JSON Structure
Structured data for custom visualization:
```json
{
  "nodes": [{"id": "start", "label": "Start", "type": "start"}],
  "edges": [{"from": "start", "to": "stage1", "label": "flow"}]
}
```

## Analysis Components:

### Value Stream Analysis
- **Value-Adding Activities**: Steps that directly contribute to customer value
- **Non-Value-Adding**: Necessary but non-value-adding activities
- **Waste Activities**: Pure waste that should be eliminated
- **Flow Efficiency**: Value-adding time / total lead time
- **Takt Time**: Available time / customer demand rate

### Bottleneck Analysis
- **Constraint Identification**: Process steps that limit overall throughput
- **Capacity Analysis**: Resource availability vs. demand
- **Queue Analysis**: Work-in-progress and waiting time
- **Utilization Rates**: Resource efficiency and optimization opportunities

### Handoff Analysis
- **Communication Points**: Information transfer between roles/systems
- **Responsibility Transfers**: Clear ownership transitions
- **Quality Gates**: Verification and approval points
- **Failure Modes**: Common handoff problems and solutions

### Dependency Analysis
- **Critical Path**: Longest sequence determining total duration
- **Parallel Opportunities**: Activities that can run concurrently
- **Resource Conflicts**: Shared resource bottlenecks
- **Coordination Requirements**: Synchronization and communication needs

## Integration Points:
- **Input**: Process definitions and performance data
- **Output**: Visual diagrams and optimization insights
- **Analysis**: Integration with `/process analyze` findings
- **Optimization**: Support for `/process optimize` planning

## Customization Options:
- **Color Coding**: Status, priority, or performance-based coloring
- **Size Scaling**: Node/activity sizing based on duration or importance
- **Annotation**: Add metrics, notes, and improvement suggestions
- **Layered Views**: Show/hide different types of information

## Error Handling:
- Missing process data: Provide template for data collection
- Complex visualizations: Offer simplified views and drill-down options
- Format limitations: Provide multiple output formats
- Large processes: Implement pagination or hierarchical views

Focus on creating clear, actionable visualizations that help teams understand their processes and identify improvement opportunities through visual analysis.
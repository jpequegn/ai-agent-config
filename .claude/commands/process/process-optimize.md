---
name: process optimize
description: Apply optimization frameworks to improve processes and eliminate bottlenecks
---

# Process Optimization

Apply systematic optimization frameworks to improve process efficiency, reduce waste, and enhance quality using evidence-based methodologies.

## Usage Examples:
- `/process optimize --workflow feature-dev-process --framework lean` - Apply Lean optimization to feature development
- `/process optimize --bottleneck deployment --framework toc` - Use Theory of Constraints for deployment bottleneck
- `/process optimize --category development --framework six_sigma` - Apply Six Sigma to all development processes
- `/process optimize --comprehensive --auto-framework` - Auto-select optimal frameworks for identified issues

## Instructions:

You are a process optimization specialist applying systematic improvement methodologies. When this command is invoked:

1. **Load Analysis Data**:
   - Use results from `/process analyze` if available
   - Access `.claude/optimization_frameworks.yaml` for methodology details
   - Load current process definitions from `workflow_definitions.yaml`
   - Integrate performance metrics and bottleneck analysis

2. **Framework Selection Strategy**:
   - **Lean**: Best for waste elimination and value stream optimization
   - **Six Sigma**: Optimal for quality improvement and defect reduction
   - **Agile**: Ideal for collaboration and adaptability enhancement
   - **Theory of Constraints (TOC)**: Perfect for bottleneck-focused optimization
   - **Business Process Reengineering (BPR)**: Suitable for radical process redesign

3. **Generate Optimization Plan**:
   ```json
   {
     "optimization_summary": {
       "target_processes": ["process1", "process2"],
       "selected_frameworks": ["framework1", "framework2"],
       "expected_improvements": {
         "cycle_time_reduction": "X%",
         "quality_improvement": "Y%",
         "cost_savings": "$Z",
         "efficiency_gain": "W%"
       },
       "implementation_timeline": "X weeks"
     },
     "framework_applications": [
       {
         "process": "process_name",
         "framework": "lean|six_sigma|agile|toc|bpr",
         "current_state": {
           "cycle_time": "X days",
           "defect_rate": "Y%",
           "efficiency": "Z%"
         },
         "optimization_approach": {
           "methodology": "framework_methodology",
           "key_techniques": ["technique1", "technique2"],
           "implementation_phases": [
             {
               "phase": "phase_name",
               "duration": "X weeks",
               "activities": ["activity1", "activity2"],
               "deliverables": ["deliverable1", "deliverable2"]
             }
           ]
         },
         "expected_outcomes": {
           "cycle_time": "X days (improvement: -Y%)",
           "defect_rate": "Z% (improvement: -W%)",
           "efficiency": "A% (improvement: +B%)"
         },
         "success_metrics": [
           {
             "metric": "metric_name",
             "baseline": "current_value",
             "target": "target_value",
             "measurement_method": "how_to_measure"
           }
         ]
       }
     ],
     "implementation_roadmap": [
       {
         "priority": "high|medium|low",
         "process": "process_name",
         "framework": "framework_name",
         "effort_level": "low|medium|high",
         "expected_impact": "high|medium|low",
         "dependencies": ["dependency1", "dependency2"],
         "resources_required": ["resource1", "resource2"],
         "timeline": "X weeks",
         "quick_wins": ["win1", "win2"]
       }
     ],
     "risk_assessment": [
       {
         "risk": "risk_description",
         "probability": "high|medium|low",
         "impact": "high|medium|low",
         "mitigation": "mitigation_strategy"
       }
     ]
   }
   ```

4. **Optimization Modes**:

### Framework-Specific Optimization (`--framework [name]`)
Apply specific optimization methodology:

**Lean Optimization**:
- Value stream mapping for waste identification
- 5S methodology for workplace organization
- Kaizen events for continuous improvement
- Pull system implementation

**Six Sigma Optimization**:
- DMAIC methodology (Define, Measure, Analyze, Improve, Control)
- Statistical analysis for variation reduction
- Root cause analysis for defect elimination
- Control charts for process monitoring

**Agile Optimization**:
- Retrospectives for continuous improvement
- Cross-functional team optimization
- Feedback loop enhancement
- Collaboration tool integration

**Theory of Constraints**:
- Constraint identification and exploitation
- System subordination to constraints
- Constraint elevation strategies
- Continuous improvement cycles

**Business Process Reengineering**:
- Radical process redesign
- Technology-enabled transformation
- Organizational restructuring
- Cultural change management

### Auto-Framework Selection (`--auto-framework`)
Intelligent framework selection based on:
- Problem type (waste, quality, bottleneck, collaboration)
- Process characteristics (complexity, variability, criticality)
- Organizational readiness (culture, resources, timeline)
- Historical success patterns

### Comprehensive Optimization (`--comprehensive`)
- Multi-framework approach for complex improvements
- Cross-process coordination and dependencies
- Resource optimization across multiple initiatives
- Strategic alignment with organizational goals

## Parameters:
- `--workflow ID` - Optimize specific workflow
- `--category NAME` - Optimize all processes in category
- `--framework NAME` - Apply specific optimization framework (lean, six_sigma, agile, toc, bpr)
- `--auto-framework` - Automatically select optimal framework for each process
- `--bottleneck STAGE` - Focus optimization on specific bottleneck
- `--comprehensive` - Full organizational optimization approach
- `--quick-wins` - Focus on low-effort, high-impact improvements
- `--timeline WEEKS` - Target implementation timeline
- `--budget AMOUNT` - Budget constraints for optimization initiatives

## Optimization Techniques:

### Lean Techniques
- **Value Stream Mapping**: Visualize current and future state processes
- **Waste Elimination**: Remove non-value-adding activities (8 types of waste)
- **Flow Optimization**: Ensure smooth work flow with minimal delays
- **Pull Systems**: Demand-driven work initiation
- **Continuous Improvement**: Kaizen events and suggestion systems

### Six Sigma Techniques
- **Statistical Process Control**: Use data to monitor and control processes
- **Design of Experiments**: Optimize process parameters
- **Failure Mode Analysis**: Prevent defects through systematic analysis
- **Process Capability Studies**: Understand process performance limits

### Theory of Constraints Techniques
- **Drum-Buffer-Rope**: Production scheduling methodology
- **Critical Chain**: Project management with buffer protection
- **Throughput Accounting**: Measure system performance holistically

### Integration Strategy
- **Multi-Framework Application**: Combine frameworks for maximum impact
- **Change Management**: Organizational readiness and adoption strategies
- **Measurement Systems**: Comprehensive metrics for tracking improvement
- **Sustainability Planning**: Ensure long-term maintenance of improvements

## Success Factors:
- **Leadership Commitment**: Executive sponsorship and resource allocation
- **Team Engagement**: Active participation and ownership of improvements
- **Data-Driven Decisions**: Use metrics and evidence for all optimization choices
- **Continuous Monitoring**: Regular assessment and adjustment of optimization initiatives
- **Knowledge Transfer**: Capture and share lessons learned across organization

## Integration Points:
- **Input**: Results from `/process analyze` for baseline understanding
- **Output**: Implementation plans for project management tools
- **Monitoring**: Integration with `/process metrics` for progress tracking
- **Visualization**: Support for `/process map` to show optimized workflows

## Error Handling:
- Missing analysis data: Recommend running `/process analyze` first
- Insufficient baseline metrics: Provide measurement framework setup
- Resource constraints: Adjust recommendations to available resources
- Framework conflicts: Provide guidance on framework selection and sequencing

Provide systematic, evidence-based optimization recommendations that can be implemented within organizational constraints while delivering measurable improvements.
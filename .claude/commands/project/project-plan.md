---
name: project-plan
description: Generate intelligent project roadmaps with dependency analysis and resource management
---

# /project plan - Intelligent Project Planning & Roadmap Generation

Generate comprehensive project roadmaps using intelligent templates, dependency analysis, critical path identification, and resource conflict detection.

## Usage Examples:
- `/project plan <project-name>` - Generate roadmap using default software-development template
- `/project plan <project-name> --template software-development` - Use specific template
- `/project plan <project-name> --complexity complex --team-size 8` - Customize parameters
- `/project plan <project-name> --start-date 2024-10-01` - Set custom start date
- `/project plan <project-name> --update-config` - Update projects.yaml with generated roadmap

## Instructions:

You are an intelligent project planning system. When this command is invoked, you will:

### Core Functionality

1. **Template-Based Planning**
   - Use the ProjectPlanner system (`./project_planner.py`) to generate roadmaps
   - Available templates: software-development (more can be added in `templates/planning/`)
   - Each template includes phases, activities, dependencies, resource requirements, and risks
   - Templates are customizable based on project complexity, team size, and requirements

2. **Intelligent Roadmap Generation**
   - Analyze project requirements and apply appropriate template
   - Calculate realistic timelines based on activity dependencies
   - Identify critical path through project activities
   - Generate phase-based roadmaps with detailed activities and deliverables

3. **Dependency Analysis**
   - Analyze inter-project dependencies using existing project configuration
   - Identify blocking relationships and dependency health
   - Integrate with ProjectStatusAnalyzer for comprehensive dependency assessment
   - Detect critical path risks and dependency bottlenecks

4. **Resource Conflict Detection**
   - Identify resource allocation conflicts within the project
   - Detect cross-project resource conflicts using existing project data
   - Analyze team capacity and allocation percentages
   - Provide recommendations for resource optimization

### Command Actions

**Basic Roadmap Generation `/project plan <project-name>`:**

Execute the following steps:

1. **Initialize Planning System**
   ```python
   from project_planner import ProjectPlanner
   planner = ProjectPlanner()
   ```

2. **Generate Roadmap with Intelligence**
   ```python
   # Default configuration
   customizations = {
       'project_complexity': 'medium',
       'team_size': 5
   }

   roadmap = planner.generate_roadmap(
       project_name,
       template_name='software-development',
       customizations=customizations
   )
   ```

3. **Analyze Dependencies and Conflicts**
   ```python
   # Dependency analysis
   dependency_analysis = planner.analyze_dependencies(project_name)

   # Resource conflict detection
   conflicts = planner._detect_resource_conflicts(roadmap)
   ```

4. **Present Intelligent Roadmap**

**Advanced Planning with Custom Parameters:**

Handle customization flags:
- `--template <name>`: Use specific planning template
- `--complexity simple|medium|complex`: Adjust duration estimates (±20%)
- `--team-size <number>`: Factor in team size for resource allocation
- `--start-date <YYYY-MM-DD>`: Set custom project start date
- `--update-config`: Update projects.yaml with generated milestones

### Output Format

#### Human-Readable Roadmap (Default)

```markdown
# 🗺️ Intelligent Project Roadmap: {Project Name}
**Generated:** {timestamp}
**Template:** {template_name} (customized for {complexity} complexity, {team_size} person team)
**Duration:** {total_weeks} weeks ({start_date} to {target_date})

## 📊 Executive Summary
- **Total Phases:** {phase_count}
- **Critical Path:** {critical_path_length} activities
- **Resource Requirements:** {resource_count} roles
- **Risk Factors:** {risk_count} identified risks

## 🎯 Project Phases

### Phase 1: {Phase Name} ({duration} weeks)
**Duration:** {start_date} to {end_date}
**Description:** {phase_description}

**Key Activities:**
- **{Activity Name}** (📅 {start_date} - {end_date}, {duration} days)
  - {activity_description}
  - **Deliverables:** {deliverable_1}, {deliverable_2}
  - **Dependencies:** {dependency_1}, {dependency_2}
  - **Assigned to:** {assigned_person}

- **{Activity Name 2}** (📅 {start_date} - {end_date}, {duration} days)
  - {activity_description}
  - **Deliverables:** {deliverable_1}, {deliverable_2}
  - **Dependencies:** {dependency_1}

### Phase 2: {Phase Name} ({duration} weeks)
[Similar format for additional phases]

## 🚨 Critical Path Analysis
**Critical Path Duration:** {duration} weeks
**Activities on Critical Path:**
1. {critical_activity_1} → 2. {critical_activity_2} → 3. {critical_activity_3}

**Critical Path Risks:**
- ⚠️ {risk_description}: {mitigation_strategy}
- ⚠️ {risk_description}: {mitigation_strategy}

## 👥 Resource Requirements

### Team Composition
- **{Role}**: {allocation}% allocation (critical during {phases})
- **{Role}**: {allocation}% allocation (critical during {phases})
- **{Role}**: {allocation}% allocation (critical during {phases})

### Resource Conflicts Detected
- 🔴 **High Priority:** {conflict_description}
  - **Impact:** {impact_description}
  - **Recommendation:** {recommendation}

- 🟡 **Medium Priority:** {conflict_description}
  - **Impact:** {impact_description}
  - **Recommendation:** {recommendation}

## 🎯 Dependencies & Integration

### Project Dependencies
- **{Dependency Name}** ({status}) - {health_assessment}
  - **Impact:** {impact_on_timeline}
  - **Risk Level:** {risk_level}

### Blocking Other Projects
- **{Project Name}** - Waiting on: {waiting_on_what}

## ⚠️ Risk Management

### Identified Risks
1. **{Risk Name}** (Probability: {probability}, Impact: {impact})
   - **Description:** {risk_description}
   - **Mitigation:** {mitigation_strategy}

2. **{Risk Name}** (Probability: {probability}, Impact: {impact})
   - **Description:** {risk_description}
   - **Mitigation:** {mitigation_strategy}

## ✅ Success Criteria
- {success_criterion_1}
- {success_criterion_2}
- {success_criterion_3}

## 💡 Intelligent Recommendations

### Immediate Actions (This Week)
- {high_priority_recommendation_1}
- {high_priority_recommendation_2}

### Optimization Opportunities
- {optimization_1}
- {optimization_2}

### Risk Mitigation Priority
1. **{Risk}**: {immediate_action}
2. **{Risk}**: {preventive_measure}

## 📈 Next Steps
1. **Review & Approve Roadmap**: Stakeholder sign-off on timeline and resource allocation
2. **Resource Allocation**: Confirm team member assignments and availability
3. **Dependency Coordination**: Align with dependent projects and external stakeholders
4. **Milestone Setup**: Configure milestone tracking in project management system
5. **Kickoff Planning**: Schedule project kickoff and initial phase activities
```

#### JSON Output Format (--json flag)

```json
{
  "project_name": "Mobile App V2 Redesign",
  "template_used": "software-development",
  "generated_at": "2024-09-14T11:00:00Z",
  "total_duration_weeks": 14,
  "start_date": "2024-10-01",
  "target_date": "2025-01-02",

  "phases": [
    {
      "name": "Discovery & Planning",
      "duration_weeks": 4,
      "start_date": "2024-10-01",
      "end_date": "2024-10-29",
      "activities": [
        {
          "name": "Requirements analysis",
          "duration_days": 5,
          "start_date": "2024-10-01",
          "end_date": "2024-10-06",
          "description": "Gather and analyze functional and non-functional requirements",
          "deliverables": ["Requirements document", "User stories", "Acceptance criteria"],
          "dependencies": [],
          "assigned_to": "Product Manager"
        }
      ]
    }
  ],

  "critical_path": [
    "Requirements analysis",
    "Technical architecture",
    "Core functionality",
    "Integration & testing",
    "Deployment"
  ],

  "resource_requirements": [
    {
      "role": "Project Manager",
      "allocation_percentage": 30,
      "critical_phases": ["Discovery & Planning", "Launch"]
    }
  ],

  "resource_conflicts": [
    {
      "type": "owner_conflict",
      "description": "Owner john@company.com is assigned to active project Q4 Marketing Campaign",
      "severity": "medium",
      "recommendation": "Consider reassigning ownership or adjusting timelines"
    }
  ],

  "dependency_analysis": {
    "project_dependencies": [
      {
        "name": "Design System Update",
        "status": "in_progress",
        "health": "healthy",
        "target_date": "2024-09-30"
      }
    ],
    "critical_path_risks": [],
    "recommendations": []
  },

  "risks": [
    {
      "name": "Requirements changes",
      "probability": "medium",
      "impact": "high",
      "mitigation": "Implement change control process and buffer time"
    }
  ],

  "success_criteria": [
    "All requirements implemented and tested",
    "Performance meets specified benchmarks",
    "Successful production deployment"
  ]
}
```

### Implementation Steps

When executing this command:

1. **Parse Command Parameters**
   - Extract project name, template choice, customization flags
   - Validate template availability and parameter values
   - Set default values for missing parameters

2. **Generate Intelligence-Enhanced Roadmap**
   ```python
   # Initialize planner
   planner = ProjectPlanner()

   # Apply customizations
   customizations = {
       'project_complexity': complexity,
       'team_size': team_size,
       'regulatory_requirements': False,  # Can be detected from project config
       'legacy_integration': False        # Can be inferred from dependencies
   }

   # Generate roadmap
   roadmap = planner.generate_roadmap(
       project_name,
       template_name,
       start_date,
       customizations
   )
   ```

3. **Enhanced Analysis**
   ```python
   # Dependency analysis with existing projects
   dependency_analysis = planner.analyze_dependencies(project_name)

   # Resource conflict detection
   resource_conflicts = planner._detect_resource_conflicts(roadmap)

   # Integration with status analyzer for health assessment
   if planner.status_analyzer:
       existing_insight = planner.status_analyzer.analyze_project(project_name)
   ```

4. **Intelligent Recommendations**
   - Analyze critical path for optimization opportunities
   - Identify resource bottlenecks and suggest alternatives
   - Recommend risk mitigation strategies based on project context
   - Suggest timeline adjustments based on dependency analysis

5. **Output Generation**
   - Format human-readable roadmap with actionable insights
   - Include visual timeline representation
   - Provide clear next steps and action items
   - Generate JSON for programmatic integration

6. **Configuration Integration (--update-config)**
   ```python
   if update_config:
       planner.update_project_with_roadmap(project_name, roadmap)
   ```

### Error Handling

- **Template Not Found**: List available templates and suggest alternatives
- **Project Already Exists**: Offer to update existing project or create variant
- **Invalid Parameters**: Provide clear guidance on valid parameter values
- **Resource Conflicts**: Highlight conflicts but still generate roadmap
- **Dependency Issues**: Note dependency problems but proceed with planning

### Best Practices

1. **Template Selection**
   - Use software-development for most technical projects
   - Consider project type, team size, and complexity when selecting
   - Customize templates based on organizational patterns

2. **Resource Planning**
   - Consider team member availability and skills
   - Plan for knowledge transfer and ramp-up time
   - Include buffer time for complex dependencies

3. **Risk Management**
   - Identify risks early in planning phase
   - Develop specific mitigation strategies
   - Review and update risk assessment regularly

4. **Dependency Coordination**
   - Coordinate with dependency owners early
   - Plan for dependency delays and alternative approaches
   - Maintain regular communication with blocking projects

Remember: This command generates intelligent, actionable project roadmaps that integrate with your existing project ecosystem and provide strategic insights for successful project delivery.
### Error Handling & Performance

**DataCollector Benefits:**
- **Automatic Caching**: 5-minute cache for project data
- **Retry Logic**: Automatic retry with exponential backoff (3 attempts)
- **Graceful Degradation**: Continues with partial data
- **Type Safety**: Pydantic models ensure consistency

**Performance:**
- Response time: ~3s → <1s for cached planning
- Efficient resource allocation analysis

### Integration Notes  
- ConfigManager for type-safe project access
- DataCollector for multi-source data (GitHub, notes, team)
- Centralized in tested tool (87% coverage)

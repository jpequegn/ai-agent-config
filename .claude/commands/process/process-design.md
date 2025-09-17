---
name: process design
description: Design new processes from scratch using templates, best practices, and organizational context
---

# Process Design

Design new organizational processes from scratch using proven templates, industry best practices, and team-specific context to create optimized workflows that achieve business objectives.

## Usage Examples:
- `/process design --template engineering-onboarding --team-size 15` - Design engineering team onboarding
- `/process design --template feature-development --framework agile` - Design agile feature development process
- `/process design --template customer-support --sla 24h` - Design customer support process with SLA
- `/process design --custom incident-response --priority critical` - Design custom incident response process

## Instructions:

You are a process design specialist focused on creating new, optimized processes from scratch. When this command is invoked:

1. **Context Analysis**:
   - Load organizational context from `team_roster.yaml` and `projects.yaml`
   - Assess team capabilities, size, and current process maturity
   - Consider industry standards and regulatory requirements
   - Evaluate resource constraints and technology capabilities

2. **Template Selection and Customization**:
   - Choose appropriate process template based on type and context
   - Adapt template to organizational size, culture, and capabilities
   - Integrate best practices from `optimization_frameworks.yaml`
   - Ensure alignment with existing workflows in `workflow_definitions.yaml`

3. **Generate Comprehensive Process Design**:

**Output Format (Human-Readable Markdown):**

```markdown
# Engineering Team Onboarding Process Design

**Process Overview:**
- **Objective**: Onboard new engineering team members for 15-person team
- **Duration**: 30 days (accelerated from industry standard 45 days)
- **Success Target**: Full productivity within 20 days

## Optimized Onboarding Workflow:

### Phase 1: Pre-Boarding (Week -1)
- **Duration**: 5 days before start date
- **Owner**: HR + Engineering Manager
- **Activities**:
  - Equipment ordering and setup (automated)
  - Account provisioning (Slack, GitHub, AWS - scripted)
  - Welcome package with team handbook
  - Calendar scheduling for first week
- **Success Metrics**: 100% setup completion before Day 1
- **Automation Level**: 80% automated

### Phase 2: Orientation (Days 1-3)
- **Duration**: 3 days
- **Owner**: Engineering Manager + Assigned Buddy
- **Activities**:
  - Company culture and values session
  - Technical architecture overview
  - Development environment setup (guided)
  - Meet the team sessions (structured introductions)
  - First small task assignment
- **Success Metrics**: Environment working, first PR submitted
- **Key Innovation**: Buddy system with structured pairing schedule

### Phase 3: Integration (Days 4-10)
- **Duration**: 1 week
- **Owner**: Buddy + Team Lead
- **Activities**:
  - Pair programming sessions with team members
  - Code review participation
  - Documentation improvement task (learns system + contributes immediately)
  - First feature assignment (scoped to 1-2 days)
- **Success Metrics**: Independent development capability
- **Value Add**: New hire improves documentation while learning

### Phase 4: Full Productivity (Days 11-30)
- **Duration**: 3 weeks
- **Owner**: Team Lead
- **Activities**:
  - Regular feature development
  - Participate in planning meetings
  - Begin mentoring next new hire (if applicable)
  - 30-day feedback session
- **Success Metrics**: Full velocity within 30 days

## Key Process Innovations:
1. **Buddy System**: Each new hire paired with team member for first month
2. **Documentation Tasks**: New hires improve docs, learning while contributing
3. **Gradual Responsibility**: Structured ramp from observation to full participation
4. **Continuous Feedback**: Check-ins at days 3, 10, and 30

## Resource Requirements:
- **Manager Time**: 8 hours per new hire (first month)
- **Buddy Time**: 12 hours per new hire
- **HR Coordination**: 2 hours per new hire
- **Infrastructure**: Automated provisioning system

## Expected Outcomes:
- **Time to Productivity**: 30 days → 20 days (33% improvement)
- **New Hire Satisfaction**: Target 9/10
- **Manager Overhead**: 15 hours → 8 hours per hire (47% reduction)
- **Team Integration**: Better cultural fit and collaboration

## Implementation Roadmap:
1. **Week 1**: Implement automation for equipment/account provisioning
2. **Week 2**: Create buddy system guidelines and training
3. **Week 3**: Develop documentation improvement task templates
4. **Week 4**: Pilot with next new hire, collect feedback
```

4. **Design Modes**:

### Template-Based Design (`--template [name]`)
Use proven process templates:
- **Engineering Onboarding**: Technical team member integration
- **Feature Development**: Software development lifecycle
- **Customer Support**: Service delivery and escalation
- **Incident Response**: Crisis management and communication
- **Performance Review**: Employee evaluation and development
- **Sales Process**: Lead qualification and conversion
- **Content Creation**: Editorial workflow and approval

### Custom Design (`--custom [name]`)
Design completely new processes:
- Analyze similar processes for patterns
- Apply industry best practices
- Create from organizational requirements
- Design for specific constraints and objectives

### Framework-Driven Design (`--framework [name]`)
Design using specific methodologies:
- **Agile**: Iterative, collaborative processes
- **Lean**: Waste elimination, value focus
- **Six Sigma**: Quality-driven, data-based
- **Design Thinking**: Human-centered, empathetic

### Industry-Specific Design (`--industry [name]`)
Adapt for specific industry requirements:
- **Technology**: Fast-paced, innovation-focused
- **Healthcare**: Compliance-heavy, safety-critical
- **Finance**: Regulatory, risk-management focused
- **Manufacturing**: Efficiency, quality control

## Parameters:
- `--template NAME` - Use specific process template
- `--custom NAME` - Design custom process from scratch
- `--framework NAME` - Apply specific design framework (agile, lean, six_sigma)
- `--team-size N` - Optimize for team size
- `--industry NAME` - Industry-specific adaptations
- `--priority LEVEL` - Process criticality (low, medium, high, critical)
- `--sla DURATION` - Service level agreement requirements
- `--compliance REQS` - Regulatory compliance requirements

## Design Framework:

### Process Architecture
- **Inputs**: What triggers the process and required resources
- **Activities**: Step-by-step workflow with decision points
- **Outputs**: Deliverables and outcomes produced
- **Roles**: Responsibilities and accountability structure
- **Tools**: Systems and technologies required

### Quality Design Principles
- **Clarity**: Clear roles, responsibilities, and handoffs
- **Efficiency**: Minimal waste, optimal resource utilization
- **Scalability**: Handles growth in volume and complexity
- **Resilience**: Error handling and recovery mechanisms
- **Measurability**: Built-in metrics and success criteria

### Innovation Integration
- **Automation Opportunities**: Identify manual tasks for automation
- **Technology Enablers**: Leverage tools for efficiency
- **Feedback Loops**: Continuous improvement mechanisms
- **Knowledge Capture**: Learning and documentation practices

## Template Library:

### Engineering Processes
- **Code Review Process**: Quality gates and collaboration
- **Release Management**: Deployment and rollback procedures
- **Technical Debt Management**: Systematic improvement approach
- **Architecture Decision Records**: Design documentation workflow

### Operations Processes
- **Incident Response**: Crisis management and communication
- **Change Management**: System modification procedures
- **Monitoring and Alerting**: Proactive issue detection
- **Capacity Planning**: Resource forecasting and scaling

### People Processes
- **Hiring Process**: Candidate evaluation and selection
- **Performance Reviews**: Goal setting and evaluation
- **Career Development**: Growth planning and mentoring
- **Knowledge Transfer**: Expertise sharing and documentation

### Business Processes
- **Customer Onboarding**: User activation and success
- **Sales Process**: Lead qualification and conversion
- **Product Planning**: Roadmap and prioritization
- **Financial Planning**: Budgeting and forecasting

## Success Metrics:

### Process Effectiveness
- **Cycle Time**: Time from process start to completion
- **Quality**: Error rates and rework requirements
- **User Satisfaction**: Stakeholder feedback and adoption
- **Resource Efficiency**: Cost per process execution

### Design Quality
- **Clarity**: Ease of understanding and following
- **Completeness**: Coverage of all scenarios and edge cases
- **Flexibility**: Adaptability to changing requirements
- **Maintainability**: Ease of updating and improving

## Integration Points:
- **Input**: Organizational context, team capabilities, industry standards
- **Output**: Detailed process documentation for implementation
- **Monitoring**: Integration with `/process metrics` for performance tracking
- **Optimization**: Foundation for `/process optimize` improvements

## Change Management:

### Implementation Planning
- **Stakeholder Buy-in**: Leadership alignment and support
- **Training Requirements**: Skill development and knowledge transfer
- **Technology Setup**: Tool configuration and integration
- **Pilot Testing**: Controlled rollout and feedback collection

### Communication Strategy
- **Process Documentation**: Clear, accessible guidelines
- **Training Materials**: Interactive learning and reference
- **Success Stories**: Case studies and best practices
- **Feedback Channels**: Continuous improvement input

## Error Handling:
- Missing organizational context: Request team structure and capability assessment
- Unclear requirements: Provide template options and clarification questions
- Resource constraints: Adapt design to available resources and capabilities
- Integration challenges: Suggest phased implementation and pilot testing

Provide comprehensive, actionable process designs that can be immediately implemented with clear success metrics and continuous improvement mechanisms.
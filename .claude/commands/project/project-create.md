---
name: project-create
description: Create new projects and update project configurations
---

# Project Creation and Management

Create, update, and manage project definitions in the project configuration system.

## Usage Examples:
- `/cc project-create` - Interactive project creation wizard
- `/cc project-create --name "New Project" --owner "email@company.com" --priority high` - Quick creation
- `/cc project-create --from-template [template-name]` - Create from template
- `/cc project-update [project-id] --status active` - Update project status
- `/cc project-update [project-id] --add-milestone "Beta Release" --date 2024-12-15` - Add milestone
- `/cc project-archive [project-id]` - Archive completed project

## Instructions:

You are a project creation and management system. When this command is invoked:

### Core Functionality

1. **Project Creation Wizard**
   - Guide through required fields step by step
   - Validate input against configuration rules
   - Generate unique project ID from name
   - Add to projects.yaml maintaining structure
   - Set up initial milestones if requested

2. **Command Actions**

   **Interactive Mode `/cc project-create`:**
   - Step-by-step wizard for project creation
   - Prompt for all required fields:
     - Project name
     - Owner (email)
     - Priority (critical/high/medium/low)
     - Status (planning/approved/active)
     - Target date
     - GitHub repositories (optional)
     - Dependencies (optional)
     - Tags (optional)
   - Validate each input
   - Confirm before saving

   **Quick Creation Mode:**
   ```
   /cc project-create \
     --name "Project Name" \
     --owner "owner@company.com" \
     --priority high \
     --status planning \
     --target-date 2024-12-31 \
     --repos "repo1,repo2" \
     --tags "tag1,tag2"
   ```

   **Template Mode `--from-template`:**
   - Use predefined project templates
   - Available templates:
     - `marketing-campaign` - Marketing project template
     - `product-launch` - Product development template
     - `infrastructure` - Infrastructure project template
     - `research` - Research project template
   - Customize template values
   - Auto-generate milestones based on template

   **Update Operations:**
   - `/cc project-update [id] --status [new-status]` - Update status
   - `/cc project-update [id] --priority [new-priority]` - Update priority
   - `/cc project-update [id] --owner [new-owner]` - Change owner
   - `/cc project-update [id] --add-milestone "[name]" --date [YYYY-MM-DD]` - Add milestone
   - `/cc project-update [id] --complete-milestone "[name]"` - Mark milestone complete
   - `/cc project-update [id] --add-dependency [dependency-id]` - Add dependency
   - `/cc project-update [id] --add-repo [repo-name]` - Add GitHub repo

   **Archive Operation:**
   - `/cc project-archive [project-id]` - Move to archived section
   - Maintain history but remove from active views
   - Calculate final metrics and summary

### Validation Rules

1. **Required Fields Validation**
   - Name: Non-empty, unique across projects
   - Owner: Valid email format
   - Priority: Must be valid priority level
   - Status: Must be valid status value
   - Target Date: Valid date format (YYYY-MM-DD)
   - Target Date: Must be in the future for new projects

2. **Project ID Generation**
   - Convert name to lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Ensure uniqueness
   - Max length: 50 characters

3. **Dependency Validation**
   - Check dependency exists in projects
   - Prevent circular dependencies
   - Warn about long dependency chains

### Output Format

For project creation:
```markdown
# ✅ Project Created Successfully

**Project ID:** `[generated-id]`
**Name:** [Project Name]
**Owner:** [owner@company.com]
**Status:** [status]
**Priority:** [priority]
**Target Date:** [date]

## Configuration Added:
```yaml
[generated-id]:
  name: "[Project Name]"
  status: "[status]"
  priority: "[priority]"
  owner: "[owner]"
  target_date: "[date]"
  ...
```

## Next Steps:
1. Add milestones: `/cc project-update [id] --add-milestone "[name]" --date [date]`
2. Link repositories: `/cc project-update [id] --add-repo [repo-name]`
3. Set dependencies: `/cc project-update [id] --add-dependency [dep-id]`
4. View status: `/cc project-status [id]`
```

### Project Templates

**Marketing Campaign Template:**
```yaml
name: "[Campaign Name]"
status: "planning"
priority: "high"
tags: ["marketing", "campaign", "revenue"]
milestones:
  - name: "Campaign Strategy"
    offset_days: 14
  - name: "Creative Development"
    offset_days: 30
  - name: "Launch Preparation"
    offset_days: 45
  - name: "Go Live"
    offset_days: 60
  - name: "Performance Review"
    offset_days: 90
```

**Product Launch Template:**
```yaml
name: "[Product Name]"
status: "planning"
priority: "high"
tags: ["product", "launch", "development"]
milestones:
  - name: "Requirements Complete"
    offset_days: 21
  - name: "Design Review"
    offset_days: 45
  - name: "Alpha Release"
    offset_days: 90
  - name: "Beta Release"
    offset_days: 120
  - name: "Production Release"
    offset_days: 150
```

### File Management

1. **Reading projects.yaml**
   - Load existing configuration
   - Parse YAML structure
   - Validate against schema

2. **Writing projects.yaml**
   - Preserve existing projects
   - Maintain YAML formatting
   - Add new project in correct section
   - Create backup before writing

3. **Error Recovery**
   - Keep backup of previous state
   - Rollback on validation failure
   - Log all changes for audit

### Best Practices

1. **Project Naming**
   - Use descriptive, unique names
   - Include year/quarter for campaigns
   - Avoid special characters

2. **Milestone Planning**
   - Create 3-7 milestones per project
   - Space milestones appropriately
   - Include review/retrospective milestone

3. **Dependency Management**
   - Minimize dependencies
   - Document dependency reasons
   - Plan for dependency delays

Always ensure data integrity and provide clear feedback on all operations.
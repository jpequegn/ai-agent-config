# PARA Method Knowledge Management System

A personal knowledge management system implementing the PARA Method for organizing digital information and notes.

## What is the PARA Method?

PARA stands for:
- **P**rojects - Things with deadlines and specific outcomes
- **A**reas - Ongoing responsibilities to maintain
- **R**esources - Future reference topics
- **A**rchive - Inactive items from the other categories

## Directory Structure

This repository is organized using the PARA method with numbered prefixes to enforce hierarchy:

```
├── 1-projects/           # Active projects with deadlines
├── 2-areas/              # Ongoing areas of responsibility
├── 3-resources/          # Reference materials and learning
├── 4-archive/            # Inactive/completed items
├── inbox/                # Unprocessed notes and materials
├── .para-config.yaml     # System configuration
├── setup-para.sh         # Initialization script
└── README.md             # This documentation
```

### 1-projects/
Contains all active projects with specific deadlines and outcomes. Each project should have its own subdirectory.

**Naming Convention:** `YYYY-MM-DD_project-name/`

**Examples:**
- `2024-09-15_quarterly-review/`
- `2024-10-01_product-launch/`
- `2024-12-31_year-end-planning/`

### 2-areas/
Contains ongoing areas of responsibility that require maintenance but have no specific end date.

**Naming Convention:** `descriptive-area-name/`

**Examples:**
- `team-management/`
- `personal-development/`
- `finance/`
- `health/`

### 3-resources/
Contains reference materials and topics of ongoing interest that aren't tied to specific projects or areas.

**Naming Convention:** `topic-or-domain-name/`

**Examples:**
- `programming/`
- `design-patterns/`
- `industry-reports/`
- `templates/`

### 4-archive/
Contains inactive items from Projects and Areas that are no longer actionable but may be useful for reference.

**Naming Convention:** `YYYY-MM-DD_original-name/` (date when archived)

**Examples:**
- `2024-09-01_completed-project/`
- `2024-08-15_deprecated-area/`

### inbox/
Serves as a temporary holding area for unprocessed notes and materials. This should be kept empty through regular review.

**Naming Convention:** `YYYY-MM-DD-HHMM_topic.md`

**Examples:**
- `2024-09-13-1430_meeting-notes.md`
- `2024-09-13-0900_idea-for-improvement.md`

## File Naming Conventions

### General Rules
- Use ISO 8601 date format: `YYYY-MM-DD`
- Use lowercase with hyphens for slugs: `my-project-name`
- Include timestamps for inbox items: `YYYY-MM-DD-HHMM`
- Maximum filename length: 100 characters
- Use descriptive but concise names

### File Types
- **Meeting Notes:** `YYYY-MM-DD_meeting-topic.md`
- **Project Plans:** `YYYY-MM-DD_project-brief.md`
- **Weekly Reviews:** `YYYY-MM-DD_weekly-review.md`
- **Ideas:** `YYYY-MM-DD-HHMM_idea-description.md`
- **Templates:** `template-name.md`

## Getting Started

### 1. Initialize New Repository
Run the setup script to create a new PARA structure:

```bash
# In a new directory
./setup-para.sh
```

This will create the directory structure, configuration file, and git repository.

### 2. Configuration
Edit `.para-config.yaml` to customize:
- User information (name, email, timezone)
- Active projects
- Common attendees for meetings
- Default tags and templates
- Review schedules

### 3. Daily Workflow
1. **Capture:** Quickly save all notes to `inbox/`
2. **Process:** Regularly review inbox and move items to appropriate PARA folders
3. **Review:** Conduct weekly/monthly reviews to maintain system

## Configuration File

The `.para-config.yaml` file contains:

- **User Information:** Name, email, timezone
- **Directory Settings:** Custom directory names if needed
- **Naming Conventions:** Date formats and slug preferences
- **Tags:** Default tags for different content types
- **Templates:** Note templates for meetings, projects, etc.
- **Automation:** Settings for auto-archiving and reminders
- **Review Schedule:** When to conduct reviews

## Best Practices

### Organization
- Keep project folders focused on specific outcomes
- Use areas for ongoing responsibilities without end dates
- Move completed projects to archive with date prefix
- Process inbox regularly (daily/weekly)

### Naming
- Start files with dates when chronology matters
- Use consistent slug formats (lowercase-with-hyphens)
- Include context in filenames for easy searching
- Keep names descriptive but concise

### Maintenance
- Weekly reviews: Update project status, process inbox
- Monthly reviews: Evaluate areas and resources
- Quarterly reviews: Archive completed projects, plan ahead

## Templates

The system includes templates for:
- **Project Notes:** Objective, key results, notes, next actions
- **Meeting Notes:** Date, attendees, agenda, discussion, action items
- **Weekly Reviews:** What went well, challenges, next week's priorities

## Git Integration

The system includes `.gitignore` rules for:
- Private/sensitive directories
- Temporary and backup files
- Review drafts
- System-generated files

## Troubleshooting

### Common Issues
- **Inbox overflowing:** Schedule regular processing time
- **Can't find notes:** Improve naming conventions and tagging
- **Projects stalling:** Break down into smaller, actionable steps
- **Areas becoming cluttered:** Regular review and cleanup

### Maintenance Commands
```bash
# Find unprocessed inbox items
find inbox/ -name "*.md" -mtime +3

# List projects by date
ls -la 1-projects/

# Archive completed project
mv "1-projects/completed-project" "4-archive/$(date +%Y-%m-%d)_completed-project"
```

## Contributing

This is a personal knowledge management system, but the structure and scripts can be adapted for team use or other personal systems.

## License

This configuration system is provided as-is for personal use.
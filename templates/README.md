# PARA Templates Directory

This directory contains note templates for the PARA Method system.

## Structure

```
templates/
├── built-in/          # Pre-built templates included with the system
│   ├── meeting.md
│   ├── one-on-one.md
│   ├── brainstorm.md
│   ├── quick-note.md
│   └── research.md
├── custom/            # User-created custom templates
│   └── (your templates)
└── README.md          # This documentation
```

## Built-in Templates

### meeting.md
General meeting notes template with agenda, discussion, and action items.

**Variables:**
- `title` (required) - Meeting subject
- `attendees` (optional) - Participant list
- `project` (optional) - Related project name

### one-on-one.md
One-on-one meeting template for manager-employee check-ins.

**Variables:**
- `person` (required) - Person you're meeting with
- `title` (optional) - Meeting focus/topic

### brainstorm.md
Brainstorming session template with idea generation and evaluation.

**Variables:**
- `topic` (required) - Brainstorming subject
- `participants` (optional) - Session participants
- `duration` (optional) - Session length

### quick-note.md
Quick capture template for inbox items and spontaneous thoughts.

**Variables:**
- `title` (optional) - Brief topic
- `source` (optional) - Where the idea came from

### research.md
Research and learning template with sources, findings, and applications.

**Variables:**
- `topic` (required) - Research subject
- `source` (optional) - Primary source
- `purpose` (optional) - Research objective

## Template Format

Templates use YAML frontmatter for metadata and Jinja2 for variable substitution.

### Frontmatter Schema

```yaml
---
description: "Template description"
category: "template category"
para_suggestion: "suggested PARA location"
variables:
  - name: "variable_name"
    description: "Variable description"
    required: true/false
---
```

### Template Body

Use Jinja2 syntax for variables and logic:

```markdown
# {{ title | default('Default Title') }}

**Date:** {{ date }}
{% if project %}**Project:** {{ project }}{% endif %}

## Content

{{ custom_variable | upper }}
```

## Creating Custom Templates

1. **Using the CLI:**
   ```bash
   ./para-templates.py new-template "my-template"
   ```

2. **Manual creation:**
   - Create a `.md` file in `templates/custom/`
   - Include YAML frontmatter
   - Use Jinja2 variables in content

## Available Variables

### Default Variables
- `date` - Current date (YYYY-MM-DD)
- `datetime` - Current date and time (YYYY-MM-DD HH:MM)
- `time` - Current time (HH:MM)
- `timestamp` - Filename-friendly (YYYY-MM-DD-HHMM)
- `year`, `month`, `day` - Date components
- `weekday` - Day name (Monday, Tuesday, etc.)
- `user_name` - From .para-config.yaml
- `user_email` - From .para-config.yaml

### Custom Variables
Pass via CLI or add to templates:
- `title` - Note title
- `project` - Project name
- `attendees` - Meeting participants
- `person` - Individual person name
- `topic` - Subject or theme
- `source` - Information source

## Jinja2 Features

### Filters
- `{{ text | slugify }}` - Convert to URL-friendly slug
- `{{ text | upper }}` - Convert to uppercase
- `{{ text | default('fallback') }}` - Provide default value

### Conditionals
```jinja2
{% if variable %}
Content when variable exists
{% endif %}

{% if not variable %}
Content when variable is empty
{% endif %}
```

### Loops
```jinja2
{% for item in list %}
- {{ item }}
{% endfor %}
```

## PARA Location Hints

Use `para_suggestion` in frontmatter to hint where notes should be filed:

- `1-projects` - Active project notes
- `2-areas` - Ongoing area maintenance
- `3-resources` - Reference materials
- `4-archive` - Completed/inactive items
- `inbox` - Unprocessed captures

Example:
```yaml
---
para_suggestion: "1-projects"
---
```

This helps users understand where to file notes during inbox processing.
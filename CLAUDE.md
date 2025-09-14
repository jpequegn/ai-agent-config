# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a comprehensive personal knowledge management system implementing the PARA Method, with integrated project orchestration and AI agent configuration capabilities. It combines structured note-taking, project management, and intelligent command interfaces for productivity workflows.

## Repository Architecture

### Core Components

**PARA Method Structure** (Primary knowledge organization):
- `1-projects/` - Active projects with deadlines
- `2-areas/` - Ongoing responsibilities
- `3-resources/` - Reference materials
- `4-archive/` - Completed/inactive items
- `inbox/` - Unprocessed notes

**Claude Code Integration** (.claude/ directory):
- **Commands**: Slash commands for productivity workflows (`/notes`, `/project`, `/analyze`, etc.)
- **Project Configuration**: `projects.yaml` - Multi-project orchestration with milestones
- **Notes Integration**: Cache system linking notes to projects (`cache/notes_*.json`)

**Processing Engines**:
- `para-processor.py` - Note parsing, action item extraction, PARA categorization
- `notes` - Unified command interface with natural language processing
- `para-templates.py` - Template system for consistent note creation

### Data Flow Architecture

1. **Note Creation**: Templates → Structured markdown → PARA categorization
2. **Processing**: Content analysis → Action item extraction → Project linking
3. **Integration**: Notes ↔ Projects synchronization via cache system
4. **Intelligence**: Cross-project analysis → Decision support → Recommendations

## Essential Commands

### PARA Method Operations
```bash
# Note creation and processing
./notes capture --template meeting --topic "Sprint Planning"
./notes capture --project mobile-app-v2 --topic "Status Update"
./para-processor.py parse note.md --graceful
./para-processor.py batch inbox/ --summary

# Template management
./para-templates.py list
./para-templates.py create meeting --title "Team Sync" --attendees "team"

# Project setup
./setup-para.sh  # Initialize new PARA structure
```

### Claude Code Slash Commands
These commands are executed within Claude Code interface:

```bash
# Notes system
/notes meeting --project mobile-app-v2 --topic "Sprint Planning"
/notes capture --template quick-note "Project idea"
/notes sync-actions --project mobile-app-v2

# Project management
/project notes mobile-app-v2
/project review --weekly
/project decide "Mobile App launch strategy"
/project risks --severity high

# Analysis and productivity
/analyze codebase --focus quality
/follow-up-check --auto-suggest
```

### Testing and Validation
```bash
# Test processing engine
python3 test_project_config.py

# Process test notes
./para-processor.py parse test-notes/research-note.md
./para-processor.py batch test-notes/ --summary
```

## Key Integration Points

### Projects Configuration (`/.claude/projects.yaml`)
Defines active projects with:
- Milestones and deadlines
- Team members and ownership
- Dependencies and relationships
- Status tracking and health metrics

### Notes-Project Linking
- **Automatic**: Content analysis detects project references
- **Cache System**: `/.claude/cache/notes_*.json` maintains bidirectional links
- **Action Items**: Meeting notes → Project milestone synchronization
- **Search Enhancement**: Project context in note discovery

### Command Architecture
Slash commands in `/.claude/commands/` follow standardized patterns:
- YAML frontmatter with metadata
- Natural language processing
- Project integration capabilities
- JSON output for Claude Code compatibility

## Configuration Files

- `.para-config.yaml` - PARA Method settings, user info, templates
- `.claude/projects.yaml` - Multi-project configuration and tracking
- `.claude/settings.local.json` - Claude Code local settings
- `requirements.txt` - Python dependencies for processing engines

## Development Patterns

### Adding New Commands
1. Create `/claude/commands/command-name.md` with YAML frontmatter
2. Follow established pattern: Usage → Instructions → Output formats
3. Include project integration if relevant (`--project` flag)
4. Add natural language processing patterns

### Extending Project Integration
1. Update `projects.yaml` schema if needed
2. Modify cache structure in `/.claude/cache/notes_*.json`
3. Update cross-reference logic in processing engines
4. Add integration points to relevant commands

### Template System Extension
Templates in `templates/` support:
- Jinja2 variables and logic
- PARA categorization hints
- Metadata-driven organization
- Claude Code command integration

## Data Persistence

**Notes Storage**: Markdown files with frontmatter throughout PARA directories
**Project Tracking**: YAML configuration with JSON caches for performance
**Action Items**: Extracted and synchronized between notes and project milestones
**Relationships**: Cache system maintains cross-references and dependencies

## Error Handling

The system includes robust error handling:
- **Graceful parsing**: Handles malformed notes without failing
- **Backup system**: Automatic backups in `.para-backups/` before modifications
- **Validation**: Input validation for all file operations
- **Recovery**: Clear error messages with recovery suggestions
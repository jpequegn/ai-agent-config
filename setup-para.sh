#!/bin/bash

# PARA Method Setup Script
# Initializes a new repository with PARA directory structure and configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default configuration values
DEFAULT_USER_NAME="$(git config --get user.name 2>/dev/null || echo 'Your Name')"
DEFAULT_USER_EMAIL="$(git config --get user.email 2>/dev/null || echo 'your.email@example.com')"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to create directory with README
create_para_directory() {
    local dir_name="$1"
    local readme_content="$2"

    print_status "Creating directory: $dir_name"
    mkdir -p "$dir_name"

    if [[ ! -f "$dir_name/README.md" ]]; then
        echo "$readme_content" > "$dir_name/README.md"
        print_success "Created $dir_name/README.md"
    else
        print_warning "$dir_name/README.md already exists, skipping"
    fi
}

# Main setup function
setup_para_structure() {
    print_status "Setting up PARA directory structure..."

    # Create Projects directory
    create_para_directory "1-projects" "# Projects

This directory contains all active projects with specific deadlines and outcomes.

## Structure
- Each project should have its own subdirectory
- Use format: \`YYYY-MM-DD_project-name/\`
- Include project briefs, meeting notes, and deliverables

## Examples
- \`2024-09-15_quarterly-review/\`
- \`2024-10-01_product-launch/\`"

    # Create Areas directory
    create_para_directory "2-areas" "# Areas

This directory contains ongoing areas of responsibility that require maintenance but have no specific end date.

## Structure
- Organize by life/work domains
- Use clear, descriptive folder names
- Include standards, processes, and ongoing notes

## Examples
- \`team-management/\`
- \`personal-development/\`
- \`finance/\`
- \`health/\`"

    # Create Resources directory
    create_para_directory "3-resources" "# Resources

This directory contains reference materials and topics of ongoing interest.

## Structure
- Organize by topic or domain
- Include reference materials, research, and learning notes
- No specific project or area attachment

## Examples
- \`programming/\`
- \`design-patterns/\`
- \`industry-reports/\`
- \`templates/\`"

    # Create Archive directory
    create_para_directory "4-archive" "# Archive

This directory contains inactive items from Projects and Areas that are no longer actionable.

## Structure
- Maintain original folder structure from source (Projects/Areas)
- Add date prefix when archiving: \`YYYY-MM-DD_original-name/\`
- Include final status and outcomes

## Examples
- \`2024-09-01_completed-project/\`
- \`2024-08-15_deprecated-area/\`"

    # Create Inbox directory
    create_para_directory "inbox" "# Inbox

This directory serves as a temporary holding area for unprocessed notes and materials.

## Purpose
- Capture everything quickly without worrying about organization
- Process regularly to move items to appropriate PARA folders
- Keep this folder empty through regular review

## Processing Guidelines
1. Review inbox items regularly (daily/weekly)
2. Categorize each item into Projects, Areas, Resources, or Archive
3. Move items to appropriate folders
4. Delete items that are no longer relevant

## File Naming
- Use timestamps for quick capture: \`YYYY-MM-DD-HHMM_topic.md\`
- Include source if relevant: \`meeting_\`, \`idea_\`, \`article_\`, etc."
}

# Function to create configuration file
create_config_file() {
    local config_file=".para-config.yaml"

    if [[ -f "$config_file" ]]; then
        print_warning "Configuration file $config_file already exists"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Skipping configuration file creation"
            return
        fi
    fi

    # Get user input for configuration
    print_status "Setting up configuration..."

    read -p "Enter your name [$DEFAULT_USER_NAME]: " user_name
    user_name=${user_name:-$DEFAULT_USER_NAME}

    read -p "Enter your email [$DEFAULT_USER_EMAIL]: " user_email
    user_email=${user_email:-$DEFAULT_USER_EMAIL}

    read -p "Enter your timezone [America/Los_Angeles]: " timezone
    timezone=${timezone:-"America/Los_Angeles"}

    # Create configuration file
    cat > "$config_file" << EOF
# PARA Method Configuration
# Configuration file for Personal Knowledge Management using the PARA Method

# User Information
user:
  name: "$user_name"
  email: "$user_email"
  timezone: "$timezone"

# Directory Structure Settings
directories:
  projects: "1-projects"
  areas: "2-areas"
  resources: "3-resources"
  archive: "4-archive"
  inbox: "inbox"

# File Naming Conventions
naming:
  # Date format for file prefixes (ISO 8601)
  date_format: "YYYY-MM-DD"
  # Timestamp format for inbox items
  timestamp_format: "YYYY-MM-DD-HHMM"
  # Use slugs for readability (lowercase, hyphens)
  use_slugs: true
  # Max length for file names
  max_filename_length: 100

# Default Tags and Categories
tags:
  default:
    - "unprocessed"
  project_tags:
    - "active"
    - "planning"
    - "review"
    - "blocked"
  area_tags:
    - "maintenance"
    - "improvement"
    - "monitoring"
  resource_tags:
    - "reference"
    - "learning"
    - "template"

# Common Attendees (for meeting notes)
contacts:
  common_attendees:
    - "John Doe <john.doe@company.com>"
    - "Jane Smith <jane.smith@company.com>"
    - "Team Lead <team.lead@company.com>"

# Active Projects (to be updated regularly)
active_projects:
  - name: "PARA System Setup"
    start_date: "$(date +%Y-%m-%d)"
    deadline: "$(date -v +7d +%Y-%m-%d)"
    status: "active"

# Templates (simplified for shell script)
templates:
  project_note: "basic"
  meeting_note: "basic"

# Automation Settings
automation:
  # Auto-archive completed projects after N days
  auto_archive_completed: 30
  # Inbox reminder frequency (in days)
  inbox_reminder_days: 3
  # Default editor for notes
  default_editor: "code"

# Review Settings
review:
  # Weekly review day (0=Sunday, 6=Saturday)
  weekly_review_day: 0
  # Monthly review date (day of month)
  monthly_review_day: 1
  # Quarterly review months
  quarterly_review_months: [3, 6, 9, 12]
EOF

    print_success "Created configuration file: $config_file"
}

# Function to create .gitignore
create_gitignore() {
    local gitignore_file=".gitignore"

    if [[ -f "$gitignore_file" ]]; then
        print_warning ".gitignore already exists, appending PARA-specific rules"
        cat >> "$gitignore_file" << EOF

# PARA Method specific ignores
# Temporary files
*.tmp
*~
.DS_Store
Thumbs.db

# Personal notes (if you want to keep some private)
**/private/
**/personal/

# Archive of sensitive information
4-archive/**/sensitive/

# Backup files
*.bak
*.backup

# Editor specific
.vscode/settings.json
.idea/
*.swp
*.swo

# OS specific
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
desktop.ini
EOF
    else
        cat > "$gitignore_file" << EOF
# PARA Method .gitignore
# Generated by setup-para.sh

# Temporary files
*.tmp
*~
.DS_Store
Thumbs.db

# Personal notes (if you want to keep some private)
**/private/
**/personal/

# Archive of sensitive information
4-archive/**/sensitive/

# Backup files
*.bak
*.backup

# Editor specific
.vscode/settings.json
.idea/
*.swp
*.swo

# OS specific
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
desktop.ini

# Node modules (if using any JS tools)
node_modules/
npm-debug.log*

# Python (if using Python tools)
__pycache__/
*.py[cod]
*\$py.class
*.so
.Python
.venv/
venv/
EOF
    fi

    print_success "Updated .gitignore with PARA-specific rules"
}

# Function to initialize git repository
init_git_repo() {
    if [[ ! -d ".git" ]]; then
        print_status "Initializing Git repository..."
        git init
        print_success "Git repository initialized"
    else
        print_status "Git repository already exists"
    fi
}

# Main execution
main() {
    print_status "PARA Method Setup Script"
    print_status "========================"

    # Check if we're in a directory
    if [[ ! -d "$(pwd)" ]]; then
        print_error "Cannot access current directory"
        exit 1
    fi

    print_status "Setting up PARA structure in: $(pwd)"

    # Ask for confirmation
    read -p "Continue with setup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setup cancelled"
        exit 0
    fi

    # Run setup steps
    setup_para_structure
    create_config_file
    create_gitignore
    init_git_repo

    print_success "PARA Method setup complete!"
    print_status "Next steps:"
    echo "  1. Review and customize .para-config.yaml"
    echo "  2. Add your first project or area"
    echo "  3. Start capturing notes in the inbox/"
    echo "  4. Set up regular reviews (weekly/monthly)"
}

# Run main function
main "$@"
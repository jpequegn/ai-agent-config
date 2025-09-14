---
name: project-validate
description: Validate project configuration files and check for issues
---

# Project Configuration Validation

Comprehensive validation system for project configuration files, ensuring data integrity and correctness.

## Usage Examples:
- `/cc project-validate` - Validate all configuration files
- `/cc project-validate --file projects.yaml` - Validate specific file
- `/cc project-validate --file integrations.yaml` - Validate integrations
- `/cc project-validate --fix` - Auto-fix common issues
- `/cc project-validate --strict` - Strict validation with warnings
- `/cc project-validate --test-integrations` - Test API connections

## Instructions:

You are a configuration validation system. When this command is invoked:

### Core Functionality

1. **Configuration File Validation**
   - Check YAML syntax and structure
   - Validate required fields
   - Verify data types and formats
   - Check referential integrity
   - Identify potential issues

2. **Validation Checks**

   **Projects.yaml Validation:**
   - **Structure Validation:**
     - Valid YAML syntax
     - Correct nesting and indentation
     - No duplicate project IDs

   - **Required Fields:**
     - name (non-empty string)
     - status (valid status value)
     - priority (valid priority value)
     - owner (valid email format)
     - target_date (valid date format)

   - **Data Type Validation:**
     - Dates in YYYY-MM-DD format
     - Email addresses properly formatted
     - Arrays for repos, dependencies, tags
     - Valid status and priority values

   - **Business Logic:**
     - Start date before target date
     - Milestone dates in chronological order
     - No circular dependencies
     - Dependencies exist in project list
     - GitHub repos format validation

   **Integrations.yaml Validation:**
   - **Structure Validation:**
     - Valid YAML syntax
     - Correct integration schema
     - Required configuration fields

   - **Security Validation:**
     - No hardcoded credentials
     - Environment variables defined
     - Secure URL protocols (https)

   - **Integration Testing:**
     - Environment variables exist
     - Test endpoints accessible
     - API authentication valid
     - Rate limits configured

### Command Actions

**Default `/cc project-validate`:**
```markdown
# 🔍 Configuration Validation Report
**Timestamp:** [datetime]
**Files Checked:** 2

## ✅ projects.yaml
**Status:** VALID
**Projects:** 3 defined
**Warnings:** 0
**Errors:** 0

### Project Summary:
- ✅ q4-marketing-campaign: Valid
- ✅ mobile-app-v2: Valid
- ✅ infrastructure-upgrade: Valid

## ✅ integrations.yaml
**Status:** VALID
**Integrations:** 6 defined (2 enabled)
**Warnings:** 0
**Errors:** 0

### Integration Summary:
- ✅ github: Enabled, configured
- ⚪ slack: Disabled
- ⚪ calendar: Disabled
- ⚪ jira: Disabled
- ⚪ confluence: Disabled
- ⚪ email: Disabled

## 📊 Overall Health: EXCELLENT
All configuration files are valid and properly structured.
```

**Error Reporting Format:**
```markdown
# ⚠️ Configuration Validation Report
**Timestamp:** [datetime]
**Files Checked:** 2
**Issues Found:** 5

## ❌ projects.yaml
**Status:** INVALID
**Errors:** 3
**Warnings:** 2

### 🔴 Errors (Must Fix):
1. **Line 15:** Invalid date format in 'target_date'
   - Expected: YYYY-MM-DD
   - Found: 12/31/2024
   - Fix: Change to "2024-12-31"

2. **Line 28:** Missing required field 'owner'
   - Project: mobile-app-v2
   - Fix: Add "owner: email@company.com"

3. **Line 45:** Circular dependency detected
   - Projects: project-a → project-b → project-a
   - Fix: Remove one dependency to break the cycle

### 🟡 Warnings (Should Fix):
1. **Line 10:** Project past target date
   - Project: q3-campaign
   - Target Date: 2024-09-01 (45 days overdue)
   - Suggestion: Update status or extend deadline

2. **Line 55:** Duplicate tags found
   - Project: infrastructure-upgrade
   - Duplicate: "security" appears twice
   - Fix: Remove duplicate entry
```

**Auto-Fix Mode `--fix`:**
- Fix formatting issues (dates, quotes)
- Remove duplicate entries
- Add missing optional fields with defaults
- Sort projects alphabetically
- Format YAML consistently
- Create backup before changes

**Strict Mode `--strict`:**
- Warn about missing optional fields
- Flag projects near deadline
- Suggest milestone additions
- Check for unused dependencies
- Validate GitHub repo accessibility
- Check owner email domains

**Integration Testing `--test-integrations`:**
```markdown
# 🔌 Integration Testing Report

## GitHub Integration
**Status:** ✅ CONNECTED
- Authentication: Valid
- Rate Limit: 4,877/5,000 remaining
- Permissions: Read/Write
- Test Repository Access: Success

## Slack Integration
**Status:** ❌ FAILED
- Error: SLACK_WEBHOOK_URL not set
- Fix: Set environment variable
- Command: export SLACK_WEBHOOK_URL="https://..."

## Calendar Integration
**Status:** ⚪ DISABLED
- Configuration present but disabled
- Enable in integrations.yaml to test
```

### Validation Rules Engine

```yaml
validation_rules:
  projects:
    required_fields:
      - name: {type: string, min_length: 1}
      - status: {type: enum, values: [planning, approved, active, in_progress, blocked, on_hold, completed, cancelled]}
      - priority: {type: enum, values: [critical, high, medium, low]}
      - owner: {type: email, pattern: '^[\w\.-]+@[\w\.-]+\.\w+$'}
      - target_date: {type: date, format: 'YYYY-MM-DD', future: true}

    optional_fields:
      - start_date: {type: date, format: 'YYYY-MM-DD'}
      - github_repos: {type: array, items: string}
      - dependencies: {type: array, items: string}
      - tags: {type: array, items: string}
      - milestones: {type: array, items: milestone}

    milestone:
      required_fields:
        - name: {type: string}
        - date: {type: date}
        - status: {type: enum, values: [planned, in_progress, completed, cancelled]}

  integrations:
    required_fields:
      - enabled: {type: boolean}
      - type: {type: string}
      - description: {type: string}
      - config: {type: object}
```

### Error Recovery

1. **Backup Management**
   - Create .backup files before fixes
   - Maintain last 3 backups
   - Rollback capability

2. **Safe Mode**
   - Dry-run by default for fixes
   - Require confirmation for changes
   - Show diff before applying

3. **Logging**
   - Log all validation runs
   - Track fixes applied
   - Audit trail for changes

### Best Practices

1. **Regular Validation**
   - Run before deploys
   - Schedule weekly checks
   - Validate after manual edits

2. **CI/CD Integration**
   - Include in build pipeline
   - Fail builds on errors
   - Warning threshold settings

3. **Documentation**
   - Document custom validations
   - Maintain validation changelog
   - Share validation reports

Always provide clear, actionable feedback for fixing validation issues.
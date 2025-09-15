#!/usr/bin/env python3
"""
Test script for project configuration system
Validates YAML files and configuration structure
"""

import yaml
import os
import sys
from datetime import datetime
import re

def load_yaml_file(filepath):
    """Load and parse YAML file"""
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error in {filepath}: {e}")
        return None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_projects_yaml():
    """Validate projects.yaml structure and data"""
    print("\n📋 Validating projects.yaml...")

    config = load_yaml_file('.claude/projects.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    if 'projects' not in config:
        errors.append("Missing 'projects' section")
        return False

    # Validate each project
    for project_id, project in config['projects'].items():
        print(f"\n  Checking project: {project_id}")

        # Check required fields
        required_fields = ['name', 'status', 'priority', 'owner', 'target_date']
        for field in required_fields:
            if field not in project:
                errors.append(f"  ❌ {project_id}: Missing required field '{field}'")
            elif field == 'owner' and not validate_email(project[field]):
                errors.append(f"  ❌ {project_id}: Invalid email format for owner")
            elif field == 'target_date' and not validate_date(project[field]):
                errors.append(f"  ❌ {project_id}: Invalid date format for target_date")

        # Validate status and priority values
        valid_statuses = config.get('statuses', [])
        valid_priorities = config.get('priorities', [])

        if project.get('status') and valid_statuses and project['status'] not in valid_statuses:
            warnings.append(f"  ⚠️  {project_id}: Invalid status '{project['status']}'")

        if project.get('priority') and valid_priorities and project['priority'] not in valid_priorities:
            warnings.append(f"  ⚠️  {project_id}: Invalid priority '{project['priority']}'")

        # Validate milestones
        if 'milestones' in project:
            for i, milestone in enumerate(project['milestones']):
                if 'name' not in milestone:
                    errors.append(f"  ❌ {project_id}: Milestone {i+1} missing 'name'")
                if 'date' in milestone and not validate_date(milestone['date']):
                    errors.append(f"  ❌ {project_id}: Invalid date in milestone {i+1}")

        # Check dependencies exist
        if 'dependencies' in project:
            for dep in project['dependencies']:
                if dep not in config['projects'] and dep not in ['budget-approval', 'user-research-completion', 'design-system-update']:
                    warnings.append(f"  ⚠️  {project_id}: Unknown dependency '{dep}'")

        if not errors:
            print(f"    ✅ Structure valid")

    # Print results
    if errors:
        print("\n❌ Errors found:")
        for error in errors:
            print(error)

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(warning)

    if not errors:
        print("\n✅ projects.yaml is valid!")
        return True

    return False

def validate_integrations_yaml():
    """Validate integrations.yaml structure"""
    print("\n🔌 Validating integrations.yaml...")

    config = load_yaml_file('.claude/integrations.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    if 'integrations' not in config:
        errors.append("Missing 'integrations' section")
        return False

    # Validate each integration
    for int_name, integration in config['integrations'].items():
        print(f"\n  Checking integration: {int_name}")

        # Check required fields
        required_fields = ['enabled', 'type', 'description', 'config']
        for field in required_fields:
            if field not in integration:
                errors.append(f"  ❌ {int_name}: Missing required field '{field}'")

        # Check for hardcoded credentials
        if 'config' in integration:
            config_str = str(integration['config'])
            if 'token' in config_str.lower() and 'env' not in config_str:
                warnings.append(f"  ⚠️  {int_name}: Possible hardcoded token detected")
            if 'password' in config_str.lower() and 'env' not in config_str:
                warnings.append(f"  ⚠️  {int_name}: Possible hardcoded password detected")

        # Check validation rules exist
        if 'validation' in integration:
            if 'required_env_vars' in integration['validation']:
                env_vars = integration['validation']['required_env_vars']
                print(f"    📝 Required env vars: {', '.join(env_vars)}")

                # Check if env vars are set (for enabled integrations)
                if integration.get('enabled', False):
                    for var in env_vars:
                        if not os.environ.get(var):
                            warnings.append(f"  ⚠️  {int_name}: Environment variable '{var}' not set")

        if not errors:
            print(f"    ✅ Structure valid")

    # Print results
    if errors:
        print("\n❌ Errors found:")
        for error in errors:
            print(error)

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(warning)

    if not errors:
        print("\n✅ integrations.yaml is valid!")
        return True

    return False

def test_project_commands():
    """Test that project command files exist"""
    print("\n📁 Checking project command files...")

    command_dir = '.claude/commands/project'
    expected_files = [
        'project-status.md',
        'project-create.md',
        'project-validate.md'
    ]

    all_exist = True
    for filename in expected_files:
        filepath = os.path.join(command_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✅ {filename} exists")
        else:
            print(f"  ❌ {filename} missing")
            all_exist = False

    return all_exist

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("🧪 Testing Project Configuration System")
    print("=" * 60)

    results = []

    # Test projects.yaml
    results.append(("projects.yaml validation", validate_projects_yaml()))

    # Test integrations.yaml
    results.append(("integrations.yaml validation", validate_integrations_yaml()))

    # Test command files
    results.append(("Command files", test_project_commands()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Configuration system is valid.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
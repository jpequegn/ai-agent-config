#!/usr/bin/env python3
"""
Test script for learning system configuration
Validates YAML files and learning system structure
"""

import yaml
import os
import sys
import json
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

def load_json_file(filepath):
    """Load and parse JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Optional file not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error in {filepath}: {e}")
        return None

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_url(url_str):
    """Basic URL validation"""
    if not url_str:
        return True  # URL is optional
    url_pattern = r'^https?://.+\..+'
    return re.match(url_pattern, url_str) is not None

def validate_learning_goals():
    """Validate learning_goals.yaml structure and data"""
    print("\n📚 Validating learning_goals.yaml...")

    config = load_yaml_file('.claude/learning_goals.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    if 'learning_goals' not in config:
        errors.append("Missing 'learning_goals' section")
        return False

    # Get validation rules
    validation_rules = config.get('validation', {})
    required_fields = validation_rules.get('required_fields', [])
    valid_categories = validation_rules.get('valid_categories', [])
    valid_priorities = validation_rules.get('valid_priorities', [])
    valid_statuses = validation_rules.get('valid_statuses', [])

    # Validate each learning goal
    for goal_id, goal in config['learning_goals'].items():
        print(f"\n  Checking goal: {goal_id}")

        # Check required fields
        for field in required_fields:
            if field not in goal:
                errors.append(f"  ❌ {goal_id}: Missing required field '{field}'")
            elif field in ['created_date', 'target_completion'] and not validate_date(goal[field]):
                errors.append(f"  ❌ {goal_id}: Invalid date format for {field}")

        # Validate category
        if goal.get('category') and valid_categories and goal['category'] not in valid_categories:
            warnings.append(f"  ⚠️  {goal_id}: Invalid category '{goal['category']}'")

        # Validate priority
        if goal.get('priority') and valid_priorities and goal['priority'] not in valid_priorities:
            warnings.append(f"  ⚠️  {goal_id}: Invalid priority '{goal['priority']}'")

        # Validate status
        if goal.get('status') and valid_statuses and goal['status'] not in valid_statuses:
            warnings.append(f"  ⚠️  {goal_id}: Invalid status '{goal['status']}'")

        # Validate progress range
        if 'progress' in goal:
            progress = goal['progress']
            if not isinstance(progress, int) or progress < 0 or progress > 100:
                errors.append(f"  ❌ {goal_id}: Progress must be an integer between 0-100")

        # Validate milestones
        if 'milestones' in goal:
            for i, milestone in enumerate(goal['milestones']):
                if 'name' not in milestone:
                    errors.append(f"  ❌ {goal_id}: Milestone {i+1} missing 'name'")
                if 'date' in milestone and milestone['date'] and not validate_date(milestone['date']):
                    errors.append(f"  ❌ {goal_id}: Invalid date in milestone {i+1}")
                if 'status' in milestone and milestone['status'] not in config.get('milestone_statuses', []):
                    warnings.append(f"  ⚠️  {goal_id}: Invalid milestone status in milestone {i+1}")

        if not errors:
            print(f"    ✅ Structure valid")

    # Validate learning pathways
    if 'learning_pathways' in config:
        for pathway_id, pathway in config['learning_pathways'].items():
            if 'goals' in pathway:
                for goal_ref in pathway['goals']:
                    if goal_ref not in config['learning_goals']:
                        warnings.append(f"  ⚠️  Pathway {pathway_id}: References unknown goal '{goal_ref}'")

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
        print("\n✅ learning_goals.yaml is valid!")
        return True

    return False

def validate_sources():
    """Validate sources.yaml structure"""
    print("\n📖 Validating sources.yaml...")

    config = load_yaml_file('.claude/sources.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    if 'sources' not in config:
        errors.append("Missing 'sources' section")
        return False

    # Get validation rules
    validation_rules = config.get('validation', {})
    required_fields = validation_rules.get('required_fields', [])
    valid_types = validation_rules.get('valid_types', [])
    valid_categories = validation_rules.get('valid_categories', [])
    valid_statuses = validation_rules.get('valid_statuses', [])

    # Validate each source
    for source_id, source in config['sources'].items():
        print(f"\n  Checking source: {source_id}")

        # Check required fields
        for field in required_fields:
            if field not in source:
                errors.append(f"  ❌ {source_id}: Missing required field '{field}'")
            elif field == 'added_date' and not validate_date(source[field]):
                errors.append(f"  ❌ {source_id}: Invalid date format for added_date")

        # Validate type
        if source.get('type') and valid_types and source['type'] not in valid_types:
            warnings.append(f"  ⚠️  {source_id}: Invalid type '{source['type']}'")

        # Validate category
        if source.get('category') and valid_categories and source['category'] not in valid_categories:
            warnings.append(f"  ⚠️  {source_id}: Invalid category '{source['category']}'")

        # Validate status
        if source.get('status') and valid_statuses and source['status'] not in valid_statuses:
            warnings.append(f"  ⚠️  {source_id}: Invalid status '{source['status']}'")

        # Validate rating
        if 'rating' in source and source['rating'] is not None:
            rating = source['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                errors.append(f"  ❌ {source_id}: Rating must be an integer between 1-5")

        # Validate progress percentage
        if 'progress_percentage' in source:
            progress = source['progress_percentage']
            if not isinstance(progress, int) or progress < 0 or progress > 100:
                errors.append(f"  ❌ {source_id}: Progress percentage must be between 0-100")

        # Validate URL format
        if 'url' in source and source['url'] and not validate_url(source['url']):
            warnings.append(f"  ⚠️  {source_id}: Invalid URL format")

        # Validate completion date
        if 'completion_date' in source and source['completion_date'] and not validate_date(source['completion_date']):
            errors.append(f"  ❌ {source_id}: Invalid completion_date format")

        # Validate review frequency
        valid_frequencies = config.get('review_frequencies', [])
        if source.get('review_frequency') and valid_frequencies and source['review_frequency'] not in valid_frequencies:
            warnings.append(f"  ⚠️  {source_id}: Invalid review_frequency '{source['review_frequency']}'")

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
        print("\n✅ sources.yaml is valid!")
        return True

    return False

def validate_learning_commands():
    """Test that learning command files exist"""
    print("\n📁 Checking learning command files...")

    command_dir = '.claude/commands/learn'
    expected_files = [
        'learn-capture.md',
        'learn-review.md',
        'learn-connect.md',
        'learn-goals.md',
        'learn-sources.md'
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

def validate_cache_structure():
    """Validate learning cache structure"""
    print("\n🗂️  Checking learning cache structure...")

    cache_dir = '.claude/cache'
    cache_files = [
        'learning_captures.json',
        'learning_connections.json',
        'learning_reviews.json'
    ]

    warnings = []

    for filename in cache_files:
        filepath = os.path.join(cache_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✅ {filename} exists")

            # Validate JSON structure
            data = load_json_file(filepath)
            if data is None:
                warnings.append(f"  ⚠️  {filename}: Invalid JSON format")
            else:
                # Basic structure validation
                if filename == 'learning_captures.json' and 'captures' not in data:
                    warnings.append(f"  ⚠️  {filename}: Missing 'captures' array")
                elif filename == 'learning_connections.json' and 'connections' not in data:
                    warnings.append(f"  ⚠️  {filename}: Missing 'connections' array")
                elif filename == 'learning_reviews.json' and 'reviews' not in data:
                    warnings.append(f"  ⚠️  {filename}: Missing 'reviews' array")
        else:
            print(f"  ℹ️  {filename} will be created on first use")

    if warnings:
        print("\n⚠️  Cache warnings:")
        for warning in warnings:
            print(warning)

    return len(warnings) == 0

def validate_integration():
    """Validate integration between learning system and existing systems"""
    print("\n🔗 Validating system integration...")

    warnings = []

    # Check if learning goals reference valid source IDs
    goals_config = load_yaml_file('.claude/learning_goals.yaml')
    sources_config = load_yaml_file('.claude/sources.yaml')

    if goals_config and sources_config:
        source_ids = set(sources_config.get('sources', {}).keys())

        for goal_id, goal in goals_config.get('learning_goals', {}).items():
            if 'resources' in goal:
                for resource_id in goal['resources']:
                    if resource_id not in source_ids:
                        warnings.append(f"  ⚠️  Goal {goal_id} references unknown source '{resource_id}'")

    # Check if sources reference valid learning goals
    if goals_config and sources_config:
        goal_ids = set(goals_config.get('learning_goals', {}).keys())

        for source_id, source in sources_config.get('sources', {}).items():
            if 'learning_goals' in source:
                for goal_id in source['learning_goals']:
                    if goal_id not in goal_ids:
                        warnings.append(f"  ⚠️  Source {source_id} references unknown goal '{goal_id}'")

    if warnings:
        print("\n⚠️  Integration warnings:")
        for warning in warnings:
            print(warning)
    else:
        print("\n  ✅ All integrations valid")

    return len(warnings) == 0

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("🧪 Testing Learning System Configuration")
    print("=" * 60)

    results = []

    # Test learning goals configuration
    results.append(("learning_goals.yaml validation", validate_learning_goals()))

    # Test sources configuration
    results.append(("sources.yaml validation", validate_sources()))

    # Test command files
    results.append(("Learning command files", validate_learning_commands()))

    # Test cache structure
    results.append(("Learning cache structure", validate_cache_structure()))

    # Test system integration
    results.append(("System integration", validate_integration()))

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
        print("✅ All tests passed! Learning system configuration is valid.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
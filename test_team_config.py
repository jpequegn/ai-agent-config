#!/usr/bin/env python3
"""
Test script for team management system configuration
Validates YAML files and team management system structure
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

def validate_team_roster():
    """Validate team_roster.yaml structure and data"""
    print("\n👥 Validating team_roster.yaml...")

    config = load_yaml_file('.claude/team_roster.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    if 'team_members' not in config:
        errors.append("Missing 'team_members' section")
        return False

    # Get validation rules
    validation_rules = config.get('validation', {})
    required_fields = validation_rules.get('required_fields', [])
    role_values = validation_rules.get('role_values', [])
    status_values = validation_rules.get('status_values', [])

    # Validate each team member
    for member_email, member in config['team_members'].items():
        print(f"\n  Checking member: {member_email}")

        # Validate email format
        if not validate_email(member_email):
            errors.append(f"  ❌ {member_email}: Invalid email format")

        # Check required fields
        for field in required_fields:
            if field not in member:
                errors.append(f"  ❌ {member_email}: Missing required field '{field}'")
            elif field == 'start_date' and not validate_date(member[field]):
                errors.append(f"  ❌ {member_email}: Invalid date format for start_date")

        # Validate role
        if member.get('role') and role_values and member['role'] not in role_values:
            warnings.append(f"  ⚠️  {member_email}: Invalid role '{member['role']}'")

        # Validate status
        if member.get('status') and status_values and member['status'] not in status_values:
            warnings.append(f"  ⚠️  {member_email}: Invalid status '{member['status']}'")

        # Validate manager email
        if 'manager' in member and member['manager'] and not validate_email(member['manager']):
            warnings.append(f"  ⚠️  {member_email}: Invalid manager email format")

        # Validate review dates
        for date_field in ['last_review', 'next_review']:
            if date_field in member and member[date_field] and not validate_date(member[date_field]):
                errors.append(f"  ❌ {member_email}: Invalid date format for {date_field}")

        if not errors:
            print(f"    ✅ Structure valid")

    # Validate performance data
    if 'performance_data' in config:
        valid_metrics = config.get('metrics', [])
        valid_trends = config.get('trends', [])
        performance_range = validation_rules.get('performance_value_range', {})
        min_val = performance_range.get('min', 0.0)
        max_val = performance_range.get('max', 1.0)

        for i, perf_data in enumerate(config['performance_data']):
            if 'member' not in perf_data:
                errors.append(f"  ❌ Performance data {i+1}: Missing 'member' field")
            elif perf_data['member'] not in config['team_members']:
                warnings.append(f"  ⚠️  Performance data {i+1}: References unknown member '{perf_data['member']}'")

            if 'metric' in perf_data and valid_metrics and perf_data['metric'] not in valid_metrics:
                warnings.append(f"  ⚠️  Performance data {i+1}: Invalid metric '{perf_data['metric']}'")

            if 'trend' in perf_data and valid_trends and perf_data['trend'] not in valid_trends:
                warnings.append(f"  ⚠️  Performance data {i+1}: Invalid trend '{perf_data['trend']}'")

            if 'value' in perf_data:
                value = perf_data['value']
                if not isinstance(value, (int, float)) or value < min_val or value > max_val:
                    errors.append(f"  ❌ Performance data {i+1}: Value must be between {min_val} and {max_val}")

            if 'date' in perf_data and perf_data['date'] and not validate_date(perf_data['date']):
                errors.append(f"  ❌ Performance data {i+1}: Invalid date format")

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
        print("\n✅ team_roster.yaml is valid!")
        return True

    return False

def validate_review_templates():
    """Validate review_templates.yaml structure"""
    print("\n📋 Validating review_templates.yaml...")

    config = load_yaml_file('.claude/review_templates.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    if 'review_templates' not in config:
        errors.append("Missing 'review_templates' section")
        return False

    # Get validation rules
    validation_rules = config.get('validation', {})
    required_fields = validation_rules.get('required_fields', [])
    frequency_values = validation_rules.get('frequency_values', [])
    participant_values = validation_rules.get('participant_values', [])
    weight_validation = validation_rules.get('weight_validation', {})

    # Validate each review template
    for template_id, template in config['review_templates'].items():
        print(f"\n  Checking template: {template_id}")

        # Check required fields
        for field in required_fields:
            if field not in template:
                errors.append(f"  ❌ {template_id}: Missing required field '{field}'")

        # Validate frequency
        if template.get('frequency') and frequency_values and template['frequency'] not in frequency_values:
            warnings.append(f"  ⚠️  {template_id}: Invalid frequency '{template['frequency']}'")

        # Validate participants
        if 'participants' in template:
            for participant in template['participants']:
                if participant_values and participant not in participant_values:
                    warnings.append(f"  ⚠️  {template_id}: Invalid participant '{participant}'")

        # Validate section weights
        if 'sections' in template and weight_validation:
            total_weight = 0.0
            min_weight = weight_validation.get('minimum_weight', 0.0)
            max_weight = weight_validation.get('maximum_weight', 1.0)

            for section_name, section in template['sections'].items():
                if 'weight' in section:
                    weight = section['weight']
                    if not isinstance(weight, (int, float)):
                        errors.append(f"  ❌ {template_id}/{section_name}: Weight must be numeric")
                    elif weight < min_weight or weight > max_weight:
                        errors.append(f"  ❌ {template_id}/{section_name}: Weight must be between {min_weight} and {max_weight}")
                    else:
                        total_weight += weight

            # Check total weight
            expected_total = weight_validation.get('total_must_equal', 1.0)
            if abs(total_weight - expected_total) > 0.01:  # Allow small floating point differences
                errors.append(f"  ❌ {template_id}: Section weights sum to {total_weight}, expected {expected_total}")

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
        print("\n✅ review_templates.yaml is valid!")
        return True

    return False

def load_json_file(filepath):
    """Load and parse JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  ℹ️  {filepath} will be created on first use")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error in {filepath}: {e}")
        return None

def validate_team_commands():
    """Test that team command files exist"""
    print("\n📁 Checking team command files...")

    command_dir = '.claude/commands/team'
    expected_files = [
        'team-roster.md',
        'team-review.md',
        'team-performance.md',
        'team-sync.md',
        'team-1on1.md',
        'team-analysis.md',
        'team-feedback.md'
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

def validate_decision_frameworks():
    """Validate decision_frameworks.yaml structure and data"""
    print("\n🎯 Validating decision_frameworks.yaml...")

    config = load_yaml_file('.claude/decision_frameworks.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    required_sections = ['frameworks', 'decisions', 'validation']
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required section '{section}'")

    # Get validation rules
    validation_rules = config.get('validation', {})
    required_fields = validation_rules.get('required_fields', [])
    status_values = validation_rules.get('status_values', [])
    priority_values = validation_rules.get('priority_values', [])
    score_range = validation_rules.get('score_range', {})
    confidence_range = validation_rules.get('confidence_range', {})

    # Validate frameworks
    if 'frameworks' in config:
        for framework_id, framework in config['frameworks'].items():
            print(f"\n  Checking framework: {framework_id}")

            # Check required framework fields
            required_framework_fields = ['name', 'description', 'criteria']
            for field in required_framework_fields:
                if field not in framework:
                    errors.append(f"  ❌ {framework_id}: Missing required field '{field}'")

            # Validate criteria structure
            if 'criteria' in framework:
                total_weight = 0.0
                for criterion in framework['criteria']:
                    if 'weight' in criterion:
                        weight = criterion['weight']
                        if isinstance(weight, (int, float)):
                            total_weight += weight
                        else:
                            errors.append(f"  ❌ {framework_id}: Criterion weight must be numeric")

                # Check total weight
                if abs(total_weight - 1.0) > 0.01:
                    warnings.append(f"  ⚠️  {framework_id}: Criteria weights sum to {total_weight}, should equal 1.0")

            if not errors:
                print(f"    ✅ Framework structure valid")

    # Validate decisions
    if 'decisions' in config:
        for decision in config['decisions']:
            decision_id = decision.get('id', 'unknown')
            print(f"\n  Checking decision: {decision_id}")

            # Check required decision fields
            for field in required_fields:
                if field not in decision:
                    errors.append(f"  ❌ {decision_id}: Missing required field '{field}'")

            # Validate status
            if 'status' in decision and status_values and decision['status'] not in status_values:
                warnings.append(f"  ⚠️  {decision_id}: Invalid status '{decision['status']}'")

            # Validate priority
            if 'priority' in decision and priority_values and decision['priority'] not in priority_values:
                warnings.append(f"  ⚠️  {decision_id}: Invalid priority '{decision['priority']}'")

            # Validate stakeholder emails
            if 'stakeholders' in decision:
                for stakeholder in decision['stakeholders']:
                    if 'email' in stakeholder and not validate_email(stakeholder['email']):
                        warnings.append(f"  ⚠️  {decision_id}: Invalid stakeholder email format")

            # Validate dates
            for date_field in ['deadline', 'created_date']:
                if date_field in decision and decision[date_field] and not validate_date(decision[date_field]):
                    errors.append(f"  ❌ {decision_id}: Invalid date format for {date_field}")

            # Validate scores in options
            if 'options' in decision:
                for option in decision['options']:
                    if 'scores' in option:
                        for criterion, score in option['scores'].items():
                            if isinstance(score, (int, float)):
                                min_score = score_range.get('min', 1)
                                max_score = score_range.get('max', 10)
                                if score < min_score or score > max_score:
                                    errors.append(f"  ❌ {decision_id}: Score for {criterion} must be between {min_score} and {max_score}")

            # Validate confidence level
            if 'analysis' in decision and 'confidence_level' in decision['analysis']:
                confidence = decision['analysis']['confidence_level']
                if isinstance(confidence, (int, float)):
                    min_conf = confidence_range.get('min', 0.0)
                    max_conf = confidence_range.get('max', 1.0)
                    if confidence < min_conf or confidence > max_conf:
                        errors.append(f"  ❌ {decision_id}: Confidence level must be between {min_conf} and {max_conf}")

            if not errors:
                print(f"    ✅ Decision structure valid")

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
        print("\n✅ decision_frameworks.yaml is valid!")
        return True

    return False

def validate_stakeholder_contexts():
    """Validate stakeholder_contexts.yaml structure and data"""
    print("\n👥 Validating stakeholder_contexts.yaml...")

    config = load_yaml_file('.claude/stakeholder_contexts.yaml')
    if not config:
        return False

    errors = []
    warnings = []

    # Check for required sections
    required_sections = ['stakeholder_profiles', 'validation']
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required section '{section}'")

    # Get validation rules
    validation_rules = config.get('validation', {})
    required_fields = validation_rules.get('required_fields', [])
    authority_levels = validation_rules.get('authority_levels', [])
    communication_styles = validation_rules.get('communication_styles', [])

    # Validate stakeholder profiles
    if 'stakeholder_profiles' in config:
        for stakeholder_email, profile in config['stakeholder_profiles'].items():
            print(f"\n  Checking stakeholder: {stakeholder_email}")

            # Validate email format
            if not validate_email(stakeholder_email):
                errors.append(f"  ❌ {stakeholder_email}: Invalid email format")

            # Check required fields
            for field in required_fields:
                if field not in profile:
                    errors.append(f"  ❌ {stakeholder_email}: Missing required field '{field}'")

            # Validate authority level
            if 'decision_authority_level' in profile and authority_levels:
                if profile['decision_authority_level'] not in authority_levels:
                    warnings.append(f"  ⚠️  {stakeholder_email}: Invalid authority level '{profile['decision_authority_level']}'")

            # Validate communication style
            if 'decision_preferences' in profile and 'communication_style' in profile['decision_preferences']:
                comm_style = profile['decision_preferences']['communication_style']
                if communication_styles and comm_style not in communication_styles:
                    warnings.append(f"  ⚠️  {stakeholder_email}: Invalid communication style '{comm_style}'")

            # Validate influence factors (should sum to ~1.0)
            if 'influence_factors' in profile:
                total_influence = sum(profile['influence_factors'].values())
                if abs(total_influence - 1.0) > 0.05:  # Allow small variance
                    warnings.append(f"  ⚠️  {stakeholder_email}: Influence factors sum to {total_influence}, should be close to 1.0")

            if not errors:
                print(f"    ✅ Stakeholder profile valid")

    # Validate decision groups
    if 'decision_groups' in config:
        for group_id, group in config['decision_groups'].items():
            if 'members' in group:
                for member_email in group['members']:
                    if not validate_email(member_email):
                        warnings.append(f"  ⚠️  Decision group {group_id}: Invalid member email {member_email}")

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
        print("\n✅ stakeholder_contexts.yaml is valid!")
        return True

    return False

def validate_decide_commands():
    """Test that decide command files exist"""
    print("\n🎯 Checking decide command files...")

    command_dir = '.claude/commands/decide'
    expected_files = [
        'decide-framework.md',
        'decide-track.md',
        'decide-stakeholder.md'
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

def validate_decision_integration():
    """Validate integration between decision system and existing systems"""
    print("\n🔗 Validating decision system integration...")

    warnings = []

    # Check if stakeholders reference valid team members
    stakeholder_config = load_yaml_file('.claude/stakeholder_contexts.yaml')
    team_config = load_yaml_file('.claude/team_roster.yaml')
    integrations_config = load_yaml_file('.claude/integrations.yaml')

    if stakeholder_config and team_config:
        stakeholder_emails = set(stakeholder_config.get('stakeholder_profiles', {}).keys())
        team_emails = set(team_config.get('team_members', {}).keys())

        # Check for team members not in stakeholder profiles
        for team_email in team_emails:
            if team_email not in stakeholder_emails:
                warnings.append(f"  ⚠️  Team member {team_email} not found in stakeholder profiles")

    # Check if decision intelligence integration is properly configured
    if integrations_config:
        integrations = integrations_config.get('integrations', {})
        if 'decision_intelligence' not in integrations:
            warnings.append("  ⚠️  Decision intelligence integration not configured in integrations.yaml")
        else:
            decision_integration = integrations['decision_intelligence']
            if not decision_integration.get('enabled', False):
                warnings.append("  ⚠️  Decision intelligence integration is disabled")

    if warnings:
        print("\n⚠️  Integration warnings:")
        for warning in warnings:
            print(warning)
    else:
        print("\n  ✅ All integrations valid")

    return len(warnings) == 0

def validate_decision_data_consistency():
    """Validate data consistency within decision intelligence system"""
    print("\n📊 Validating decision data consistency...")

    warnings = []

    frameworks_config = load_yaml_file('.claude/decision_frameworks.yaml')
    stakeholder_config = load_yaml_file('.claude/stakeholder_contexts.yaml')

    if frameworks_config and stakeholder_config:
        # Check decision stakeholder references
        decisions = frameworks_config.get('decisions', [])
        stakeholder_profiles = stakeholder_config.get('stakeholder_profiles', {})

        for decision in decisions:
            decision_id = decision.get('id', 'unknown')
            if 'stakeholders' in decision:
                for stakeholder in decision['stakeholders']:
                    stakeholder_email = stakeholder.get('email')
                    if stakeholder_email and stakeholder_email not in stakeholder_profiles:
                        warnings.append(f"  ⚠️  Decision {decision_id}: References unknown stakeholder {stakeholder_email}")

            # Check framework references
            framework_id = decision.get('framework')
            if framework_id and framework_id not in frameworks_config.get('frameworks', {}):
                warnings.append(f"  ⚠️  Decision {decision_id}: References unknown framework {framework_id}")

    if warnings:
        print("\n⚠️  Data consistency warnings:")
        for warning in warnings:
            print(warning)
    else:
        print("\n  ✅ All data consistency checks passed")

    return len(warnings) == 0

def validate_team_integration():
    """Validate integration between team system and existing systems"""
    print("\n🔗 Validating team system integration...")

    warnings = []

    # Check if team members reference valid project owners
    team_config = load_yaml_file('.claude/team_roster.yaml')
    projects_config = load_yaml_file('.claude/projects.yaml')

    if team_config and projects_config:
        team_emails = set(team_config.get('team_members', {}).keys())
        project_owners = set()

        # Collect all project owners
        for project_id, project in projects_config.get('projects', {}).items():
            if 'owner' in project:
                project_owners.add(project['owner'])

        # Check for team members in projects vs roster
        for owner in project_owners:
            if owner not in team_emails and owner != 'unassigned@company.com':
                warnings.append(f"  ⚠️  Project owner {owner} not found in team roster")

        # Check for team members with current projects
        for member_email, member in team_config.get('team_members', {}).items():
            if 'current_projects' in member:
                for project_id in member['current_projects']:
                    if project_id not in projects_config.get('projects', {}):
                        warnings.append(f"  ⚠️  Team member {member_email} references unknown project '{project_id}'")

    if warnings:
        print("\n⚠️  Integration warnings:")
        for warning in warnings:
            print(warning)
    else:
        print("\n  ✅ All integrations valid")

    return len(warnings) == 0

def validate_team_data_consistency():
    """Validate data consistency within team management system"""
    print("\n📊 Validating team data consistency...")

    warnings = []
    team_config = load_yaml_file('.claude/team_roster.yaml')

    if team_config:
        team_members = team_config.get('team_members', {})

        # Check manager references
        for member_email, member in team_members.items():
            if 'manager' in member and member['manager']:
                manager_email = member['manager']
                if manager_email not in team_members and manager_email != 'ceo@company.com':
                    warnings.append(f"  ⚠️  {member_email}: Manager {manager_email} not found in team roster")

        # Check circular management relationships
        def has_circular_management(member_email, visited=None):
            if visited is None:
                visited = set()

            if member_email in visited:
                return True

            if member_email not in team_members:
                return False

            visited.add(member_email)
            manager = team_members[member_email].get('manager')

            if manager and manager in team_members:
                return has_circular_management(manager, visited.copy())

            return False

        for member_email in team_members:
            if has_circular_management(member_email):
                warnings.append(f"  ⚠️  Circular management relationship detected involving {member_email}")

        # Check performance data references
        performance_data = team_config.get('performance_data', [])
        for perf in performance_data:
            if 'member' in perf and perf['member'] not in team_members:
                warnings.append(f"  ⚠️  Performance data references unknown member: {perf['member']}")

    if warnings:
        print("\n⚠️  Data consistency warnings:")
        for warning in warnings:
            print(warning)
    else:
        print("\n  ✅ All data consistency checks passed")

    return len(warnings) == 0

def validate_1on1_cache():
    """Validate 1:1 notes cache structure"""
    print("\n💬 Validating 1:1 notes cache...")

    cache_file = '.claude/cache/1on1_notes.json'
    data = load_json_file(cache_file)

    if data is None:
        # File doesn't exist yet, which is okay for initial setup
        return True

    errors = []
    warnings = []

    # Check required top-level keys
    required_keys = ['meetings', 'templates', 'recurring_themes', 'analytics', 'metadata']
    for key in required_keys:
        if key not in data:
            errors.append(f"  ❌ Missing required key '{key}'")

    # Validate meetings structure
    if 'meetings' in data:
        for meeting in data['meetings']:
            if 'member_email' in meeting and not validate_email(meeting['member_email']):
                warnings.append(f"  ⚠️  Invalid email in meeting: {meeting.get('id', 'unknown')}")
            if 'date' in meeting and not validate_date(meeting['date']):
                errors.append(f"  ❌ Invalid date format in meeting: {meeting.get('id', 'unknown')}")
            if 'action_items' in meeting:
                for item in meeting['action_items']:
                    if 'due_date' in item and item['due_date'] and not validate_date(item['due_date']):
                        warnings.append(f"  ⚠️  Invalid due date in action item")

    if errors:
        print("\n❌ Errors found:")
        for error in errors:
            print(error)

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(warning)

    if not errors:
        print("\n  ✅ 1:1 notes cache structure valid")
        return True

    return False

def validate_team_analysis_cache():
    """Validate team analysis cache structure"""
    print("\n📊 Validating team analysis cache...")

    cache_file = '.claude/cache/team_analysis.json'
    data = load_json_file(cache_file)

    if data is None:
        # File doesn't exist yet, which is okay for initial setup
        return True

    errors = []
    warnings = []

    # Check required top-level keys
    required_keys = ['performance_analysis', 'bottleneck_analysis', 'growth_analysis', 'recommendations', 'metadata']
    for key in required_keys:
        if key not in data:
            errors.append(f"  ❌ Missing required key '{key}'")

    # Validate performance analysis structure
    if 'performance_analysis' in data:
        perf_data = data['performance_analysis']
        if 'individual_performance' in perf_data:
            for member_email, perf in perf_data['individual_performance'].items():
                if not validate_email(member_email):
                    warnings.append(f"  ⚠️  Invalid email in performance data: {member_email}")
                if 'performance_index' in perf:
                    index = perf['performance_index']
                    if not isinstance(index, (int, float)) or index < 0 or index > 1:
                        errors.append(f"  ❌ Invalid performance index for {member_email}: {index}")

    # Validate bottleneck analysis
    if 'bottleneck_analysis' in data:
        bottleneck_data = data['bottleneck_analysis']
        if 'critical_bottlenecks' in bottleneck_data:
            for bottleneck in bottleneck_data['critical_bottlenecks']:
                if 'impact_level' in bottleneck and bottleneck['impact_level'] not in ['critical', 'high', 'medium', 'low']:
                    warnings.append(f"  ⚠️  Invalid impact level: {bottleneck.get('impact_level')}")

    if errors:
        print("\n❌ Errors found:")
        for error in errors:
            print(error)

    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(warning)

    if not errors:
        print("\n  ✅ Team analysis cache structure valid")
        return True

    return False

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("🧪 Testing AI Agent Configuration")
    print("=" * 60)

    results = []

    # Test team management system
    results.append(("team_roster.yaml validation", validate_team_roster()))
    results.append(("review_templates.yaml validation", validate_review_templates()))
    results.append(("Team command files", validate_team_commands()))
    results.append(("1:1 notes cache", validate_1on1_cache()))
    results.append(("Team analysis cache", validate_team_analysis_cache()))
    results.append(("Team system integration", validate_team_integration()))
    results.append(("Team data consistency", validate_team_data_consistency()))

    # Test decision intelligence system
    results.append(("decision_frameworks.yaml validation", validate_decision_frameworks()))
    results.append(("stakeholder_contexts.yaml validation", validate_stakeholder_contexts()))
    results.append(("Decide command files", validate_decide_commands()))
    results.append(("Decision system integration", validate_decision_integration()))
    results.append(("Decision data consistency", validate_decision_data_consistency()))

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
        print("✅ All tests passed! AI agent configuration is valid.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
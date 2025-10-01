#!/usr/bin/env python3
"""
Project Planning & Roadmap Generation System
Intelligent project planning with dependency analysis, resource management, and template-based roadmaps.
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

try:
    from project_status_analyzer import ProjectStatusAnalyzer
    STATUS_ANALYZER_AVAILABLE = True
except ImportError:
    STATUS_ANALYZER_AVAILABLE = False
    print("Warning: ProjectStatusAnalyzer not available")

@dataclass
class Activity:
    """Individual project activity"""
    name: str
    duration_days: int
    description: str
    deliverables: List[str]
    dependencies: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    assigned_to: Optional[str] = None
    status: str = "planned"  # planned, in_progress, completed, blocked

@dataclass
class Phase:
    """Project phase containing multiple activities"""
    name: str
    duration_weeks: int
    description: str
    activities: List[Activity]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "planned"

@dataclass
class ResourceRequirement:
    """Resource requirement for project"""
    role: str
    allocation_percentage: int
    critical_phases: List[str]

@dataclass
class Risk:
    """Project risk with mitigation"""
    name: str
    probability: str  # low, medium, high
    impact: str       # low, medium, high
    mitigation: str

@dataclass
class ProjectRoadmap:
    """Complete project roadmap"""
    project_name: str
    template_used: str
    phases: List[Phase]
    critical_path: List[str]
    total_duration_weeks: int
    resource_requirements: List[ResourceRequirement]
    risks: List[Risk]
    success_criteria: List[str]
    generated_at: str
    start_date: str
    target_date: str

class ProjectPlanner:
    """
    Intelligent project planner that generates roadmaps using templates,
    analyzes dependencies, and identifies resource conflicts.
    """

    def __init__(self, config_dir: str = ".claude"):
        self.config_dir = Path(config_dir)
        self.templates_dir = Path("templates/planning")
        self.projects_config = self._load_projects_config()

        # Initialize status analyzer if available
        if STATUS_ANALYZER_AVAILABLE:
            self.status_analyzer = ProjectStatusAnalyzer(config_dir)
        else:
            self.status_analyzer = None

        # Ensure templates directory exists
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def _load_projects_config(self) -> Dict[str, Any]:
        """Load project configuration"""
        config_path = self.config_dir / "projects.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _load_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Load a planning template"""
        template_path = self.templates_dir / f"{template_name}.yaml"
        if not template_path.exists():
            return None

        try:
            with open(template_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading template {template_name}: {e}")
            return None

    def list_available_templates(self) -> List[str]:
        """List all available planning templates"""
        templates = []
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob("*.yaml"):
                templates.append(template_file.stem)
        return sorted(templates)

    def _calculate_dates(self, start_date: datetime, activities: List[Activity]) -> List[Activity]:
        """Calculate start and end dates for activities based on dependencies"""
        # Create a mapping of activity names to activities for dependency resolution
        activity_map = {activity.name: activity for activity in activities}
        calculated_activities = []

        # Track completion dates for dependency calculation
        completion_dates = {}

        for activity in activities:
            # Calculate start date based on dependencies
            if activity.dependencies:
                # Find the latest completion date among dependencies
                latest_dependency_end = start_date
                for dep in activity.dependencies:
                    if dep in completion_dates:
                        dep_end = datetime.fromisoformat(completion_dates[dep])
                        if dep_end > latest_dependency_end:
                            latest_dependency_end = dep_end
                activity_start = latest_dependency_end
            else:
                # No dependencies, can start at project start
                activity_start = start_date

            activity_end = activity_start + timedelta(days=activity.duration_days)

            # Update activity with calculated dates
            activity.start_date = activity_start.isoformat()[:10]
            activity.end_date = activity_end.isoformat()[:10]
            completion_dates[activity.name] = activity.end_date

            calculated_activities.append(activity)

        return calculated_activities

    def _identify_critical_path(self, activities: List[Activity]) -> List[str]:
        """Identify the critical path through project activities"""
        # Build dependency graph
        activity_map = {activity.name: activity for activity in activities}

        # Calculate earliest start and finish times
        earliest_times = {}

        def calculate_earliest(activity_name: str) -> Tuple[datetime, datetime]:
            if activity_name in earliest_times:
                return earliest_times[activity_name]

            activity = activity_map[activity_name]

            # Base case: no dependencies
            if not activity.dependencies:
                start = datetime.fromisoformat(activity.start_date)
                end = datetime.fromisoformat(activity.end_date)
                earliest_times[activity_name] = (start, end)
                return start, end

            # Find latest dependency completion
            latest_end = datetime.min
            for dep in activity.dependencies:
                if dep in activity_map:
                    _, dep_end = calculate_earliest(dep)
                    if dep_end > latest_end:
                        latest_end = dep_end

            start = latest_end
            end = start + timedelta(days=activity.duration_days)
            earliest_times[activity_name] = (start, end)
            return start, end

        # Calculate for all activities
        for activity in activities:
            calculate_earliest(activity.name)

        # Find activities with no successors (end of chains)
        successors = set()
        for activity in activities:
            successors.update(activity.dependencies)

        end_activities = [a.name for a in activities if a.name not in successors]

        if not end_activities:
            return []

        # Find the longest path (critical path)
        def find_longest_path(activity_name: str, visited: set) -> List[str]:
            if activity_name in visited:
                return []

            visited.add(activity_name)
            activity = activity_map.get(activity_name)
            if not activity or not activity.dependencies:
                return [activity_name]

            longest_sub_path = []
            for dep in activity.dependencies:
                if dep in activity_map:
                    sub_path = find_longest_path(dep, visited.copy())
                    if len(sub_path) > len(longest_sub_path):
                        longest_sub_path = sub_path

            return longest_sub_path + [activity_name]

        # Find the longest path among all end activities
        critical_path = []
        for end_activity in end_activities:
            path = find_longest_path(end_activity, set())
            if len(path) > len(critical_path):
                critical_path = path

        return critical_path

    def _detect_resource_conflicts(self, roadmap: ProjectRoadmap) -> List[Dict[str, Any]]:
        """Detect resource conflicts across projects and within the roadmap"""
        conflicts = []

        try:
            # Get all active projects for conflict detection
            all_projects = self.projects_config.get('projects', {})

            # Check for owner conflicts
            project_config = all_projects.get(roadmap.project_name.replace(' ', '-').lower())
            if project_config:
                owner = project_config.get('owner')

                # Check if owner is assigned to other active projects
                for proj_id, proj_config in all_projects.items():
                    if proj_id != roadmap.project_name.replace(' ', '-').lower():
                        if proj_config.get('owner') == owner and proj_config.get('status') in ['active', 'in_progress']:
                            # Calculate overlap periods
                            other_start = proj_config.get('start_date', '2024-01-01')
                            other_end = proj_config.get('target_date', '2024-12-31')

                            conflicts.append({
                                'type': 'owner_conflict',
                                'description': f'Owner {owner} is assigned to active project {proj_config.get("name")}',
                                'severity': 'medium',
                                'conflicting_project': proj_config.get('name'),
                                'overlap_period': f"{other_start} to {other_end}",
                                'recommendation': 'Consider reassigning ownership or adjusting timelines'
                            })

            # Check for resource allocation conflicts within the roadmap
            resource_allocation = {}
            for phase in roadmap.phases:
                for activity in phase.activities:
                    if activity.assigned_to:
                        if activity.assigned_to not in resource_allocation:
                            resource_allocation[activity.assigned_to] = []
                        resource_allocation[activity.assigned_to].append({
                            'activity': activity.name,
                            'start': activity.start_date,
                            'end': activity.end_date,
                            'phase': phase.name
                        })

            # Detect overlapping assignments
            for person, assignments in resource_allocation.items():
                assignments.sort(key=lambda x: x['start'])
                for i in range(len(assignments) - 1):
                    current = assignments[i]
                    next_assign = assignments[i + 1]

                    current_end = datetime.fromisoformat(current['end'])
                    next_start = datetime.fromisoformat(next_assign['start'])

                    if current_end > next_start:
                        conflicts.append({
                            'type': 'resource_overlap',
                            'description': f'{person} has overlapping assignments: {current["activity"]} and {next_assign["activity"]}',
                            'severity': 'high',
                            'activities': [current['activity'], next_assign['activity']],
                            'recommendation': 'Adjust activity timelines or reassign resources'
                        })

        except Exception as e:
            print(f"Warning: Error detecting resource conflicts: {e}")

        return conflicts

    def generate_roadmap(self, project_name: str, template_name: str = "software-development",
                        start_date: Optional[str] = None, customizations: Optional[Dict[str, Any]] = None) -> Optional[ProjectRoadmap]:
        """Generate a project roadmap using the specified template"""

        # Load template
        template = self._load_template(template_name)
        if not template:
            print(f"Template '{template_name}' not found")
            return None

        # Set default start date if not provided
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')

        start_dt = datetime.fromisoformat(start_date)

        # Apply customizations
        if customizations:
            # Adjust duration based on complexity
            complexity = customizations.get('project_complexity', 'medium')
            duration_multiplier = {
                'simple': 0.8,
                'medium': 1.0,
                'complex': 1.3
            }.get(complexity, 1.0)

            # Adjust team size impact (more people = potentially faster, but communication overhead)
            team_size = customizations.get('team_size', 5)
            if team_size > 7:
                duration_multiplier *= 1.1  # Communication overhead
            elif team_size < 3:
                duration_multiplier *= 1.2  # Limited parallelization
        else:
            duration_multiplier = 1.0

        # Process phases and activities
        phases = []
        all_activities = []
        current_date = start_dt

        for phase_data in template.get('phases', []):
            # Create activities for this phase
            phase_activities = []
            for activity_data in phase_data.get('activities', []):
                adjusted_duration = max(1, int(activity_data['duration_days'] * duration_multiplier))

                activity = Activity(
                    name=activity_data['name'],
                    duration_days=adjusted_duration,
                    description=activity_data['description'],
                    deliverables=activity_data['deliverables'],
                    dependencies=activity_data['dependencies']
                )
                phase_activities.append(activity)
                all_activities.append(activity)

            # Calculate phase dates (will be refined after dependency analysis)
            adjusted_phase_duration = max(1, int(phase_data['duration_weeks'] * duration_multiplier))
            phase = Phase(
                name=phase_data['name'],
                duration_weeks=adjusted_phase_duration,
                description=phase_data['description'],
                activities=phase_activities
            )
            phases.append(phase)

        # Calculate activity dates based on dependencies
        all_activities = self._calculate_dates(start_dt, all_activities)

        # Update phase dates based on activity dates
        for phase in phases:
            if phase.activities:
                phase_start = min([datetime.fromisoformat(a.start_date) for a in phase.activities])
                phase_end = max([datetime.fromisoformat(a.end_date) for a in phase.activities])
                phase.start_date = phase_start.isoformat()[:10]
                phase.end_date = phase_end.isoformat()[:10]

        # Calculate total duration
        if all_activities:
            project_end = max([datetime.fromisoformat(a.end_date) for a in all_activities])
            total_duration_weeks = (project_end - start_dt).days / 7
            target_date = project_end.isoformat()[:10]
        else:
            total_duration_weeks = template.get('duration_estimate_weeks', 14) * duration_multiplier
            target_date = (start_dt + timedelta(weeks=total_duration_weeks)).isoformat()[:10]

        # Identify critical path
        critical_path = self._identify_critical_path(all_activities)

        # Process resource requirements
        resource_requirements = []
        for resource_data in template.get('resources', {}).get('roles', []):
            resource_requirements.append(ResourceRequirement(
                role=resource_data['name'],
                allocation_percentage=resource_data['allocation_percentage'],
                critical_phases=resource_data['critical_phases']
            ))

        # Process risks
        risks = []
        for risk_data in template.get('risks', []):
            risks.append(Risk(
                name=risk_data['name'],
                probability=risk_data['probability'],
                impact=risk_data['impact'],
                mitigation=risk_data['mitigation']
            ))

        # Create roadmap
        roadmap = ProjectRoadmap(
            project_name=project_name,
            template_used=template_name,
            phases=phases,
            critical_path=critical_path,
            total_duration_weeks=int(total_duration_weeks),
            resource_requirements=resource_requirements,
            risks=risks,
            success_criteria=template.get('success_criteria', []),
            generated_at=datetime.now().isoformat(),
            start_date=start_date,
            target_date=target_date
        )

        return roadmap

    def analyze_dependencies(self, project_name: str) -> Dict[str, Any]:
        """Analyze project dependencies and blocking relationships"""
        analysis = {
            'project_dependencies': [],
            'blocking_projects': [],
            'dependency_health': 'unknown',
            'critical_path_risks': [],
            'recommendations': []
        }

        try:
            project_config = self.projects_config.get('projects', {}).get(project_name)
            if not project_config:
                return analysis

            # Analyze project-level dependencies
            dependencies = project_config.get('dependencies', [])
            all_projects = self.projects_config.get('projects', {})

            for dep in dependencies:
                if dep in all_projects:
                    dep_config = all_projects[dep]
                    analysis['project_dependencies'].append({
                        'name': dep_config.get('name', dep),
                        'status': dep_config.get('status', 'unknown'),
                        'target_date': dep_config.get('target_date'),
                        'health': 'healthy' if dep_config.get('status') in ['completed', 'active'] else 'at_risk'
                    })

            # Find projects that depend on this one
            for proj_id, proj_config in all_projects.items():
                if proj_id != project_name:
                    proj_deps = proj_config.get('dependencies', [])
                    if project_name in proj_deps:
                        analysis['blocking_projects'].append({
                            'name': proj_config.get('name', proj_id),
                            'status': proj_config.get('status'),
                            'target_date': proj_config.get('target_date')
                        })

            # Use status analyzer if available for deeper analysis
            if self.status_analyzer:
                try:
                    insight = self.status_analyzer.analyze_project(project_name)
                    if insight:
                        # Extract dependency-related information
                        dependency_blockers = [b for b in insight.blockers if b.get('type') == 'dependency']
                        if dependency_blockers:
                            analysis['critical_path_risks'].extend([
                                {
                                    'type': 'dependency_blocker',
                                    'description': blocker['description'],
                                    'severity': blocker['severity']
                                } for blocker in dependency_blockers
                            ])

                        analysis['dependency_health'] = 'healthy' if len(dependency_blockers) == 0 else 'at_risk'

                        # Generate recommendations
                        for rec in insight.recommendations:
                            if 'dependency' in rec.get('action', '').lower():
                                analysis['recommendations'].append(rec['action'])

                except Exception as e:
                    print(f"Warning: Could not analyze dependencies with status analyzer: {e}")

        except Exception as e:
            print(f"Warning: Error analyzing dependencies: {e}")

        return analysis

    def update_project_with_roadmap(self, project_name: str, roadmap: ProjectRoadmap) -> bool:
        """Update the project configuration with roadmap information"""
        try:
            project_id = project_name.replace(' ', '-').lower()
            projects_config = self.projects_config.copy()

            if 'projects' not in projects_config:
                projects_config['projects'] = {}

            # Create or update project entry
            if project_id not in projects_config['projects']:
                projects_config['projects'][project_id] = {
                    'name': project_name,
                    'status': 'planning',
                    'priority': 'medium',
                    'owner': 'unassigned@company.com'
                }

            # Update with roadmap information
            project_entry = projects_config['projects'][project_id]
            project_entry.update({
                'start_date': roadmap.start_date,
                'target_date': roadmap.target_date,
                'template_used': roadmap.template_used,
                'milestones': []
            })

            # Convert phases to milestones
            for phase in roadmap.phases:
                project_entry['milestones'].append({
                    'name': phase.name,
                    'date': phase.end_date,
                    'status': 'planned'
                })

            # Save updated configuration
            projects_path = self.config_dir / "projects.yaml"
            with open(projects_path, 'w') as f:
                yaml.dump(projects_config, f, default_flow_style=False, sort_keys=False, indent=2)

            # Update our internal config
            self.projects_config = projects_config

            return True

        except Exception as e:
            print(f"Error updating project configuration: {e}")
            return False

def main():
    """CLI interface for project planning"""
    import argparse

    parser = argparse.ArgumentParser(description='Project Planning & Roadmap Generation')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List templates command
    list_parser = subparsers.add_parser('list-templates', help='List available planning templates')

    # Generate roadmap command
    plan_parser = subparsers.add_parser('plan', help='Generate project roadmap')
    plan_parser.add_argument('project_name', help='Name of the project to plan')
    plan_parser.add_argument('--template', default='software-development', help='Planning template to use')
    plan_parser.add_argument('--start-date', help='Project start date (YYYY-MM-DD)')
    plan_parser.add_argument('--complexity', choices=['simple', 'medium', 'complex'], default='medium')
    plan_parser.add_argument('--team-size', type=int, default=5, help='Team size')
    plan_parser.add_argument('--output', help='Output file path (JSON format)')
    plan_parser.add_argument('--update-config', action='store_true', help='Update projects.yaml with roadmap')

    # Analyze dependencies command
    deps_parser = subparsers.add_parser('dependencies', help='Analyze project dependencies')
    deps_parser.add_argument('project_name', help='Name of the project to analyze')

    args = parser.parse_args()

    planner = ProjectPlanner()

    try:
        if args.command == 'list-templates':
            templates = planner.list_available_templates()
            print("Available planning templates:")
            for template in templates:
                print(f"  - {template}")

        elif args.command == 'plan':
            customizations = {
                'project_complexity': args.complexity,
                'team_size': args.team_size
            }

            roadmap = planner.generate_roadmap(
                args.project_name,
                args.template,
                args.start_date,
                customizations
            )

            if roadmap:
                result = asdict(roadmap)

                # Detect resource conflicts
                conflicts = planner._detect_resource_conflicts(roadmap)
                result['resource_conflicts'] = conflicts

                if args.output:
                    with open(args.output, 'w') as f:
                        json.dump(result, f, indent=2, default=str)
                    print(f"Roadmap saved to: {args.output}")
                else:
                    print(json.dumps(result, indent=2, default=str))

                if args.update_config:
                    if planner.update_project_with_roadmap(args.project_name, roadmap):
                        print(f"Updated projects.yaml with roadmap for {args.project_name}")
                    else:
                        print("Failed to update projects.yaml")
            else:
                print("Failed to generate roadmap")
                return 1

        elif args.command == 'dependencies':
            analysis = planner.analyze_dependencies(args.project_name)
            print(json.dumps(analysis, indent=2, default=str))

        else:
            parser.print_help()
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
#!/usr/bin/env python3
"""
Multi-Project Synchronization System
Priority: Medium | Epic: Data Integration | Labels: claude-code, sync

Build system to automatically sync project data across tools and identify cross-project impacts.
Integrates with ProjectDataCollector, ProjectStatusAnalyzer, and ProjectPlanner.
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
import argparse

# Import existing project management components
try:
    from project_data_collector import ProjectDataCollector
    DATA_COLLECTOR_AVAILABLE = True
except ImportError:
    DATA_COLLECTOR_AVAILABLE = False
    print("Warning: ProjectDataCollector not available")

try:
    from project_status_analyzer import ProjectStatusAnalyzer, ProjectInsight
    STATUS_ANALYZER_AVAILABLE = True
except ImportError:
    STATUS_ANALYZER_AVAILABLE = False
    print("Warning: ProjectStatusAnalyzer not available")

try:
    from project_planner import ProjectPlanner
    PLANNER_AVAILABLE = True
except ImportError:
    PLANNER_AVAILABLE = False
    print("Warning: ProjectPlanner not available")

@dataclass
class ResourceConflict:
    """Resource allocation conflict"""
    resource: str  # person email or resource name
    conflict_type: str  # time_overlap, over_allocation, dependency_chain
    projects: List[str]  # conflicting projects
    time_period: str  # when the conflict occurs
    severity: str  # low, medium, high, critical
    description: str
    resolution_suggestions: List[str]

@dataclass
class DependencyIssue:
    """Cross-project dependency issue"""
    dependent_project: str
    blocking_project: str
    dependency_name: str
    issue_type: str  # delayed, at_risk, blocked, circular
    impact: str  # low, medium, high, critical
    description: str
    resolution_suggestions: List[str]

@dataclass
class SyncResult:
    """Result of synchronization operation"""
    timestamp: str
    projects_synced: List[str]
    data_sources_updated: List[str]
    conflicts_detected: List[ResourceConflict]
    dependency_issues: List[DependencyIssue]
    status_updates: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    summary: Dict[str, Any]

class ProjectSynchronizer:
    """Multi-project synchronization and conflict detection system"""

    def __init__(self, config_dir: str = ".claude"):
        self.config_dir = Path(config_dir)
        self.projects_file = self.config_dir / "projects.yaml"
        self.cache_dir = self.config_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize component systems
        self.data_collector = ProjectDataCollector() if DATA_COLLECTOR_AVAILABLE else None
        self.status_analyzer = ProjectStatusAnalyzer() if STATUS_ANALYZER_AVAILABLE else None
        self.planner = ProjectPlanner() if PLANNER_AVAILABLE else None

        # Load project configuration
        self.projects_config = self._load_projects_config()

    def _load_projects_config(self) -> Dict[str, Any]:
        """Load projects configuration"""
        if not self.projects_file.exists():
            return {"projects": {}}

        try:
            with open(self.projects_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {"projects": {}}
        except Exception as e:
            print(f"Error loading projects config: {e}")
            return {"projects": {}}

    def _save_projects_config(self, config: Dict[str, Any]) -> None:
        """Save updated projects configuration"""
        try:
            with open(self.projects_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            print(f"Error saving projects config: {e}")

    def sync_all_projects(self, analyze_conflicts: bool = True) -> SyncResult:
        """Sync all projects and perform cross-project analysis"""
        timestamp = datetime.now().isoformat()
        synced_projects = []
        data_sources_updated = []
        conflicts = []
        dependency_issues = []
        status_updates = []
        recommendations = []

        # Sync individual projects
        project_data = {}
        for project_id, project_config in self.projects_config.get('projects', {}).items():
            try:
                # Collect fresh data for project
                if self.data_collector:
                    fresh_data = self.data_collector.collect_project_data(project_id)
                    project_data[project_id] = fresh_data
                    if fresh_data:
                        data_sources_updated.extend(['github', 'calendar', 'notes'])

                # Update project status based on fresh data
                updated = self._update_project_status(project_id, project_config, project_data.get(project_id))
                if updated:
                    status_updates.append({
                        'project': project_id,
                        'updates': updated,
                        'timestamp': timestamp
                    })

                synced_projects.append(project_id)

            except Exception as e:
                print(f"Error syncing project {project_id}: {e}")

        # Perform cross-project analysis if requested
        if analyze_conflicts:
            conflicts = self._detect_resource_conflicts(project_data)
            dependency_issues = self._analyze_cross_project_dependencies(project_data)
            recommendations = self._generate_sync_recommendations(conflicts, dependency_issues, status_updates)

        # Update configuration with synchronized data
        self._save_projects_config(self.projects_config)

        # Create summary
        summary = {
            'projects_count': len(synced_projects),
            'conflicts_count': len(conflicts),
            'dependency_issues_count': len(dependency_issues),
            'status_updates_count': len(status_updates),
            'data_freshness': timestamp
        }

        return SyncResult(
            timestamp=timestamp,
            projects_synced=synced_projects,
            data_sources_updated=list(set(data_sources_updated)),
            conflicts_detected=conflicts,
            dependency_issues=dependency_issues,
            status_updates=status_updates,
            recommendations=recommendations,
            summary=summary
        )

    def sync_project(self, project_id: str, analyze_conflicts: bool = True) -> SyncResult:
        """Sync specific project and check for cross-project impacts"""
        timestamp = datetime.now().isoformat()

        if project_id not in self.projects_config.get('projects', {}):
            raise ValueError(f"Project '{project_id}' not found in configuration")

        project_config = self.projects_config['projects'][project_id]

        # Collect fresh data for specific project
        project_data = {}
        data_sources_updated = []

        if self.data_collector:
            fresh_data = self.data_collector.collect_project_data(project_id)
            project_data[project_id] = fresh_data
            if fresh_data:
                data_sources_updated.extend(['github', 'calendar', 'notes'])

        # Update project status
        status_updates = []
        updated = self._update_project_status(project_id, project_config, project_data.get(project_id))
        if updated:
            status_updates.append({
                'project': project_id,
                'updates': updated,
                'timestamp': timestamp
            })

        # Analyze impacts on other projects if requested
        conflicts = []
        dependency_issues = []
        if analyze_conflicts:
            # Load data for all projects to detect cross-project impacts
            all_project_data = {}
            for other_project_id in self.projects_config.get('projects', {}):
                if other_project_id != project_id:
                    # Use cached data for other projects, fresh for target
                    cached_data = self._load_cached_project_data(other_project_id)
                    if cached_data:
                        all_project_data[other_project_id] = cached_data
            all_project_data[project_id] = project_data.get(project_id)

            conflicts = self._detect_resource_conflicts(all_project_data)
            dependency_issues = self._analyze_cross_project_dependencies(all_project_data)

        # Generate recommendations
        recommendations = self._generate_sync_recommendations(conflicts, dependency_issues, status_updates)

        # Update configuration
        self._save_projects_config(self.projects_config)

        # Create summary
        summary = {
            'target_project': project_id,
            'conflicts_count': len(conflicts),
            'dependency_issues_count': len(dependency_issues),
            'status_updates_count': len(status_updates),
            'cross_project_impacts': len([c for c in conflicts if project_id in c.projects])
        }

        return SyncResult(
            timestamp=timestamp,
            projects_synced=[project_id],
            data_sources_updated=list(set(data_sources_updated)),
            conflicts_detected=conflicts,
            dependency_issues=dependency_issues,
            status_updates=status_updates,
            recommendations=recommendations,
            summary=summary
        )

    def _update_project_status(self, project_id: str, project_config: Dict[str, Any],
                              fresh_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Update project status based on fresh data"""
        if not fresh_data:
            return None

        updates = {}

        # Update milestone status based on GitHub data
        if 'github_data' in fresh_data:
            github_data = fresh_data['github_data']
            milestones = project_config.get('milestones', [])

            for milestone in milestones:
                # Check if milestone completion can be determined from GitHub milestones
                if 'milestones' in github_data:
                    for gh_milestone in github_data['milestones']:
                        if (gh_milestone.get('title', '').lower() in milestone['name'].lower() or
                            milestone['name'].lower() in gh_milestone.get('title', '').lower()):
                            if gh_milestone.get('state') == 'closed' and milestone.get('status') != 'completed':
                                milestone['status'] = 'completed'
                                updates[f"milestone_{milestone['name']}"] = 'marked as completed from GitHub'

        # Update project status based on activity level
        if self.status_analyzer and 'github_data' in fresh_data:
            try:
                insight = self.status_analyzer.analyze_project(project_id, fresh_data)
                if insight and insight.health_metrics:
                    health_category = insight.health_metrics.category
                    current_status = project_config.get('status')

                    # Suggest status changes based on health
                    if health_category == 'critical' and current_status not in ['blocked', 'on_hold']:
                        updates['status_suggestion'] = 'blocked'
                        updates['reason'] = 'Health metrics indicate critical issues'
                    elif health_category == 'excellent' and current_status == 'blocked':
                        updates['status_suggestion'] = 'active'
                        updates['reason'] = 'Health metrics show recovery'
            except Exception as e:
                print(f"Error analyzing project {project_id}: {e}")

        return updates if updates else None

    def _detect_resource_conflicts(self, project_data: Dict[str, Any]) -> List[ResourceConflict]:
        """Detect resource allocation conflicts across projects"""
        conflicts = []

        # Track resource allocations by person and time period
        resource_allocations = {}  # {person: {time_period: [projects]}}

        # Use all projects from configuration, not just those with external data
        for project_id in self.projects_config.get('projects', {}):
            project_config = self.projects_config.get('projects', {}).get(project_id, {})
            owner = project_config.get('owner')
            start_date = project_config.get('start_date')
            target_date = project_config.get('target_date')

            if owner and start_date and target_date:
                # Create time period key (month-based)
                try:
                    start = datetime.fromisoformat(start_date)
                    end = datetime.fromisoformat(target_date)

                    # Check each month in project duration
                    current = start
                    while current <= end:
                        month_key = current.strftime('%Y-%m')

                        if owner not in resource_allocations:
                            resource_allocations[owner] = {}
                        if month_key not in resource_allocations[owner]:
                            resource_allocations[owner][month_key] = []

                        if project_id not in resource_allocations[owner][month_key]:
                            resource_allocations[owner][month_key].append(project_id)
                        current += timedelta(days=30)

                except Exception as e:
                    print(f"Error parsing dates for {project_id}: {e}")

        # Detect conflicts (same person on multiple projects in same time period)
        for person, allocations in resource_allocations.items():
            for time_period, projects in allocations.items():
                if len(projects) > 1:
                    severity = 'high' if len(projects) > 2 else 'medium'
                    conflicts.append(ResourceConflict(
                        resource=person,
                        conflict_type='time_overlap',
                        projects=projects,
                        time_period=time_period,
                        severity=severity,
                        description=f"{person} is allocated to {len(projects)} projects in {time_period}",
                        resolution_suggestions=[
                            f"Stagger project timelines to reduce {person}'s workload",
                            f"Consider reassigning ownership of one project",
                            f"Bring in additional resources to support {person}"
                        ]
                    ))

        return conflicts

    def _analyze_cross_project_dependencies(self, project_data: Dict[str, Any]) -> List[DependencyIssue]:
        """Analyze dependencies between projects"""
        dependency_issues = []

        # Build dependency graph
        dependencies = {}  # {project: [dependencies]}
        project_status = {}

        # Use all projects from configuration, not just those with external data
        for project_id in self.projects_config.get('projects', {}):
            project_config = self.projects_config.get('projects', {}).get(project_id, {})
            dependencies[project_id] = project_config.get('dependencies', [])
            project_status[project_id] = project_config.get('status', 'unknown')

        # Check for dependency issues
        for project_id, deps in dependencies.items():
            for dep in deps:
                # Find dependent project
                dependent_project = None
                for other_project_id in self.projects_config.get('projects', {}):
                    other_config = self.projects_config['projects'][other_project_id]
                    if (other_project_id == dep or
                        other_config.get('name', '').lower() == dep.lower() or
                        dep in other_config.get('tags', [])):
                        dependent_project = other_project_id
                        break

                if dependent_project:
                    dep_status = project_status.get(dependent_project, 'unknown')
                    current_status = project_status.get(project_id, 'unknown')

                    # Check for problematic dependency states
                    if dep_status in ['blocked', 'on_hold'] and current_status in ['active', 'in_progress', 'planning']:
                        dependency_issues.append(DependencyIssue(
                            dependent_project=project_id,
                            blocking_project=dependent_project,
                            dependency_name=dep,
                            issue_type='blocked',
                            impact='high',
                            description=f"{project_id} depends on {dependent_project} which is {dep_status}",
                            resolution_suggestions=[
                                f"Unblock {dependent_project} to enable {project_id} progress",
                                f"Find alternative solution for {project_id} that doesn't depend on {dependent_project}",
                                f"Put {project_id} on hold until {dependent_project} is resolved"
                            ]
                        ))

        return dependency_issues

    def _generate_sync_recommendations(self, conflicts: List[ResourceConflict],
                                     dependency_issues: List[DependencyIssue],
                                     status_updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on sync results"""
        recommendations = []

        # High priority recommendations for conflicts
        high_priority_conflicts = [c for c in conflicts if c.severity in ['critical', 'high']]
        if high_priority_conflicts:
            recommendations.append({
                'type': 'resource_conflict',
                'priority': 'high',
                'title': f'{len(high_priority_conflicts)} high-priority resource conflicts detected',
                'description': 'Multiple projects are competing for the same resources',
                'action_items': [
                    'Review project timelines and consider staggering overlapping projects',
                    'Identify opportunities to bring in additional resources',
                    'Reassign project ownership where feasible'
                ],
                'affected_projects': list(set([p for c in high_priority_conflicts for p in c.projects]))
            })

        # Dependency issue recommendations
        critical_dependencies = [d for d in dependency_issues if d.impact in ['critical', 'high']]
        if critical_dependencies:
            recommendations.append({
                'type': 'dependency_issue',
                'priority': 'high',
                'title': f'{len(critical_dependencies)} critical dependency issues found',
                'description': 'Project dependencies are blocking progress',
                'action_items': [
                    'Focus on unblocking dependent projects first',
                    'Consider alternative approaches for blocked projects',
                    'Update project timelines based on dependency health'
                ],
                'affected_projects': list(set([d.dependent_project for d in critical_dependencies]))
            })

        # Status update recommendations
        if status_updates:
            recommendations.append({
                'type': 'status_sync',
                'priority': 'medium',
                'title': f'{len(status_updates)} projects have status updates',
                'description': 'Projects status has changed based on recent activity',
                'action_items': [
                    'Review updated project statuses',
                    'Update stakeholder communications',
                    'Adjust resource allocation based on status changes'
                ],
                'affected_projects': [update['project'] for update in status_updates]
            })

        # Overall portfolio health recommendation
        if not conflicts and not dependency_issues:
            recommendations.append({
                'type': 'portfolio_health',
                'priority': 'low',
                'title': 'Project portfolio is healthy',
                'description': 'No major conflicts or dependency issues detected',
                'action_items': [
                    'Continue regular sync to maintain project health',
                    'Monitor for emerging issues in upcoming weeks'
                ],
                'affected_projects': []
            })

        return recommendations

    def _load_cached_project_data(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Load cached project data"""
        cache_file = self.cache_dir / f"{project_id}_data.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cached data for {project_id}: {e}")
        return None

    def generate_sync_report(self, sync_result: SyncResult) -> str:
        """Generate human-readable sync report"""
        report = []

        report.append("# 🔄 Project Synchronization Report")
        report.append(f"**Generated:** {sync_result.timestamp}")
        report.append(f"**Projects Synced:** {len(sync_result.projects_synced)}")
        report.append("")

        # Executive Summary
        report.append("## 📊 Executive Summary")
        summary = sync_result.summary
        report.append(f"- **Projects Updated:** {summary.get('projects_count', 0)}")
        report.append(f"- **Resource Conflicts:** {summary.get('conflicts_count', 0)}")
        report.append(f"- **Dependency Issues:** {summary.get('dependency_issues_count', 0)}")
        report.append(f"- **Status Changes:** {summary.get('status_updates_count', 0)}")
        report.append("")

        # Data Updates
        if sync_result.data_sources_updated:
            report.append("## 📥 Data Updates")
            for source in sync_result.data_sources_updated:
                report.append(f"- ✅ {source.title()} data refreshed")
            report.append("")

        # Status Updates
        if sync_result.status_updates:
            report.append("## 🔄 Status Updates")
            for update in sync_result.status_updates:
                project = update['project']
                report.append(f"**{project.title()}:**")
                for key, value in update['updates'].items():
                    report.append(f"  - {key}: {value}")
                report.append("")

        # Resource Conflicts
        if sync_result.conflicts_detected:
            report.append("## ⚠️ Resource Conflicts")
            for conflict in sync_result.conflicts_detected:
                severity_emoji = "🔴" if conflict.severity == "critical" else "🟡" if conflict.severity == "high" else "🟢"
                report.append(f"{severity_emoji} **{conflict.resource}** - {conflict.conflict_type}")
                report.append(f"  - **Projects:** {', '.join(conflict.projects)}")
                report.append(f"  - **Period:** {conflict.time_period}")
                report.append(f"  - **Issue:** {conflict.description}")
                report.append(f"  - **Suggestions:**")
                for suggestion in conflict.resolution_suggestions[:2]:  # Limit to first 2
                    report.append(f"    - {suggestion}")
                report.append("")

        # Dependency Issues
        if sync_result.dependency_issues:
            report.append("## 🔗 Dependency Issues")
            for issue in sync_result.dependency_issues:
                impact_emoji = "🚨" if issue.impact == "critical" else "⚠️" if issue.impact == "high" else "ℹ️"
                report.append(f"{impact_emoji} **{issue.dependent_project}** ← **{issue.blocking_project}**")
                report.append(f"  - **Issue:** {issue.description}")
                report.append(f"  - **Type:** {issue.issue_type}")
                report.append(f"  - **Suggestions:**")
                for suggestion in issue.resolution_suggestions[:2]:  # Limit to first 2
                    report.append(f"    - {suggestion}")
                report.append("")

        # Recommendations
        if sync_result.recommendations:
            report.append("## 💡 Recommendations")
            for rec in sync_result.recommendations:
                priority_emoji = "🔴" if rec['priority'] == "high" else "🟡" if rec['priority'] == "medium" else "🟢"
                report.append(f"{priority_emoji} **{rec['title']}**")
                report.append(f"  {rec['description']}")
                if rec['action_items']:
                    report.append("  **Action Items:**")
                    for item in rec['action_items']:
                        report.append(f"  - {item}")
                if rec.get('affected_projects'):
                    report.append(f"  **Affected Projects:** {', '.join(rec['affected_projects'])}")
                report.append("")

        return "\n".join(report)

def main():
    """CLI interface for project synchronization"""
    parser = argparse.ArgumentParser(description="Multi-Project Synchronization System")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Sync all projects
    sync_all_parser = subparsers.add_parser('sync', help='Sync all projects')
    sync_all_parser.add_argument('--analyze-conflicts', action='store_true',
                                help='Analyze cross-project conflicts')
    sync_all_parser.add_argument('--json', action='store_true', help='Output JSON format')

    # Sync specific project
    sync_project_parser = subparsers.add_parser('sync-project', help='Sync specific project')
    sync_project_parser.add_argument('project_name', help='Name of project to sync')
    sync_project_parser.add_argument('--analyze-conflicts', action='store_true',
                                    help='Analyze cross-project impacts')
    sync_project_parser.add_argument('--json', action='store_true', help='Output JSON format')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    synchronizer = ProjectSynchronizer()

    if args.command == 'sync':
        result = synchronizer.sync_all_projects(analyze_conflicts=args.analyze_conflicts)

        if args.json:
            print(json.dumps(asdict(result), indent=2, default=str))
        else:
            print(synchronizer.generate_sync_report(result))

    elif args.command == 'sync-project':
        try:
            result = synchronizer.sync_project(args.project_name, analyze_conflicts=args.analyze_conflicts)

            if args.json:
                print(json.dumps(asdict(result), indent=2, default=str))
            else:
                print(synchronizer.generate_sync_report(result))
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
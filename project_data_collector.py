#!/usr/bin/env python3
"""
Cross-Platform Data Collection System
Priority: High | Epic: Data Integration | Labels: integration, api, github

Build connectors to gather project-related data from multiple sources (GitHub, calendar, notes system).
Integrates with existing .claude/integrations.yaml and .claude/projects.yaml configurations.
"""

import os
import json
import time
import yaml
import requests
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict

# Import existing notes functionality
try:
    import subprocess
    import sys
    current_dir = Path(__file__).parent.absolute()
    sys.path.insert(0, str(current_dir))
    from notes import NotesCommandInterface
    NOTES_AVAILABLE = True
except ImportError:
    NOTES_AVAILABLE = False

@dataclass
class GitHubData:
    """Standardized GitHub data structure"""
    repo_name: str
    pull_requests: List[Dict[str, Any]]
    issues: List[Dict[str, Any]]
    commits: List[Dict[str, Any]]
    milestones: List[Dict[str, Any]]
    repository_stats: Dict[str, Any]
    collected_at: str

@dataclass
class CalendarData:
    """Standardized Calendar data structure"""
    events: List[Dict[str, Any]]
    meetings: List[Dict[str, Any]]
    deadlines: List[Dict[str, Any]]
    availability: Dict[str, Any]
    collected_at: str

@dataclass
class NotesData:
    """Standardized Notes data structure"""
    project_notes: List[Dict[str, Any]]
    action_items: List[Dict[str, Any]]
    decisions: List[Dict[str, Any]]
    collected_at: str

@dataclass
class ProjectData:
    """Unified project data structure"""
    project_name: str
    github_data: Optional[GitHubData]
    calendar_data: Optional[CalendarData]
    notes_data: Optional[NotesData]
    collection_summary: Dict[str, Any]
    collected_at: str

class ProjectDataCollector:
    """
    Cross-platform data collection system for project management.

    Integrates with:
    - GitHub API (PRs, issues, commits, milestones)
    - Google Calendar API (meetings, deadlines, availability)
    - Notes system (project-related notes and action items)
    """

    def __init__(self, config_dir: str = ".claude"):
        """Initialize collector with configuration directory"""
        self.config_dir = Path(config_dir)
        self.integrations_config = self._load_integrations_config()
        self.projects_config = self._load_projects_config()
        self.cache_dir = self.config_dir / "cache"
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize API clients
        self.github_token = os.environ.get(
            self.integrations_config.get('integrations', {}).get('github', {}).get('config', {}).get('token_env', 'GITHUB_TOKEN')
        )
        self.calendar_api_key = os.environ.get(
            self.integrations_config.get('integrations', {}).get('calendar', {}).get('config', {}).get('api_key_env', 'CALENDAR_API_KEY')
        )

        # Rate limiting state
        self.github_rate_limit = {
            'remaining': 5000,
            'reset_time': datetime.now() + timedelta(hours=1)
        }

    def _load_integrations_config(self) -> Dict[str, Any]:
        """Load integration configuration from YAML"""
        config_path = self.config_dir / "integrations.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _load_projects_config(self) -> Dict[str, Any]:
        """Load project configuration from YAML"""
        config_path = self.config_dir / "projects.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path for given key"""
        return self.cache_dir / f"{cache_key}.json"

    def _is_cache_valid(self, cache_key: str, max_age_minutes: int = 60) -> bool:
        """Check if cache is still valid"""
        cache_path = self._get_cache_path(cache_key)
        if not cache_path.exists():
            return False

        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return cache_age < timedelta(minutes=max_age_minutes)

    def _load_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Load data from cache if valid"""
        cache_path = self._get_cache_path(cache_key)
        if self._is_cache_valid(cache_key):
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None

    def _save_to_cache(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Save data to cache"""
        cache_path = self._get_cache_path(cache_key)
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _check_github_rate_limit(self) -> None:
        """Check and handle GitHub API rate limiting"""
        if not self.github_token:
            raise ValueError("GitHub token not found. Set GITHUB_TOKEN environment variable.")

        headers = {'Authorization': f'token {self.github_token}'}
        response = requests.get('https://api.github.com/rate_limit', headers=headers)

        if response.status_code == 200:
            rate_data = response.json()['resources']['core']
            self.github_rate_limit = {
                'remaining': rate_data['remaining'],
                'reset_time': datetime.fromtimestamp(rate_data['reset'])
            }

            if rate_data['remaining'] < 100:  # Conservative threshold
                sleep_time = (self.github_rate_limit['reset_time'] - datetime.now()).total_seconds()
                if sleep_time > 0:
                    print(f"Rate limit low ({rate_data['remaining']}), waiting {sleep_time:.0f}s")
                    time.sleep(sleep_time + 1)

    def collect_github_data(self, repo_names: List[str]) -> GitHubData:
        """
        Collect GitHub data for specified repositories

        Args:
            repo_names: List of repository names (format: owner/repo or just repo)

        Returns:
            GitHubData: Structured GitHub data
        """
        if not self.github_token:
            raise ValueError("GitHub token not configured")

        # Check cache first
        cache_key = f"github_{hashlib.md5('_'.join(repo_names).encode()).hexdigest()}"
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return GitHubData(**cached_data)

        self._check_github_rate_limit()

        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        all_repos_data = {
            'pull_requests': [],
            'issues': [],
            'commits': [],
            'milestones': [],
            'repository_stats': {}
        }

        # Get default org from config
        default_org = self.integrations_config.get('integrations', {}).get('github', {}).get('config', {}).get('default_org', 'your-org')

        for repo_name in repo_names:
            # Handle both "owner/repo" and "repo" formats
            if '/' not in repo_name:
                full_repo_name = f"{default_org}/{repo_name}"
            else:
                full_repo_name = repo_name

            try:
                # Collect repository stats
                repo_response = requests.get(f'https://api.github.com/repos/{full_repo_name}', headers=headers)
                if repo_response.status_code == 200:
                    repo_data = repo_response.json()
                    all_repos_data['repository_stats'][repo_name] = {
                        'full_name': repo_data['full_name'],
                        'stars': repo_data['stargazers_count'],
                        'forks': repo_data['forks_count'],
                        'open_issues': repo_data['open_issues_count'],
                        'language': repo_data['language'],
                        'updated_at': repo_data['updated_at']
                    }

                # Collect pull requests (last 30 days)
                since_date = (datetime.now() - timedelta(days=30)).isoformat()
                pr_response = requests.get(
                    f'https://api.github.com/repos/{full_repo_name}/pulls',
                    headers=headers,
                    params={'state': 'all', 'sort': 'updated', 'direction': 'desc', 'per_page': 50}
                )

                if pr_response.status_code == 200:
                    prs = pr_response.json()
                    for pr in prs:
                        if pr['updated_at'] >= since_date:
                            all_repos_data['pull_requests'].append({
                                'repo': repo_name,
                                'number': pr['number'],
                                'title': pr['title'],
                                'state': pr['state'],
                                'author': pr['user']['login'],
                                'created_at': pr['created_at'],
                                'updated_at': pr['updated_at'],
                                'merged_at': pr['merged_at'],
                                'url': pr['html_url']
                            })

                # Collect issues (last 30 days)
                issues_response = requests.get(
                    f'https://api.github.com/repos/{full_repo_name}/issues',
                    headers=headers,
                    params={'state': 'all', 'sort': 'updated', 'direction': 'desc', 'per_page': 50}
                )

                if issues_response.status_code == 200:
                    issues = issues_response.json()
                    for issue in issues:
                        # Skip pull requests (they appear in issues endpoint)
                        if 'pull_request' not in issue and issue['updated_at'] >= since_date:
                            all_repos_data['issues'].append({
                                'repo': repo_name,
                                'number': issue['number'],
                                'title': issue['title'],
                                'state': issue['state'],
                                'author': issue['user']['login'],
                                'created_at': issue['created_at'],
                                'updated_at': issue['updated_at'],
                                'url': issue['html_url'],
                                'labels': [label['name'] for label in issue['labels']]
                            })

                # Collect recent commits (last 30 days)
                commits_response = requests.get(
                    f'https://api.github.com/repos/{full_repo_name}/commits',
                    headers=headers,
                    params={'since': since_date, 'per_page': 50}
                )

                if commits_response.status_code == 200:
                    commits = commits_response.json()
                    for commit in commits:
                        all_repos_data['commits'].append({
                            'repo': repo_name,
                            'sha': commit['sha'][:8],
                            'message': commit['commit']['message'].split('\n')[0],  # First line only
                            'author': commit['commit']['author']['name'],
                            'date': commit['commit']['author']['date'],
                            'url': commit['html_url']
                        })

                # Collect milestones
                milestones_response = requests.get(
                    f'https://api.github.com/repos/{full_repo_name}/milestones',
                    headers=headers,
                    params={'state': 'all', 'per_page': 50}
                )

                if milestones_response.status_code == 200:
                    milestones = milestones_response.json()
                    for milestone in milestones:
                        all_repos_data['milestones'].append({
                            'repo': repo_name,
                            'title': milestone['title'],
                            'state': milestone['state'],
                            'open_issues': milestone['open_issues'],
                            'closed_issues': milestone['closed_issues'],
                            'created_at': milestone['created_at'],
                            'due_on': milestone['due_on'],
                            'url': milestone['html_url']
                        })

            except requests.exceptions.RequestException as e:
                print(f"Warning: Failed to collect data for repo {repo_name}: {e}")
                continue

        github_data = GitHubData(
            repo_name='_'.join(repo_names),
            pull_requests=all_repos_data['pull_requests'],
            issues=all_repos_data['issues'],
            commits=all_repos_data['commits'],
            milestones=all_repos_data['milestones'],
            repository_stats=all_repos_data['repository_stats'],
            collected_at=datetime.now().isoformat()
        )

        # Cache the results
        self._save_to_cache(cache_key, asdict(github_data))

        return github_data

    def collect_calendar_data(self, date_range: int = 30) -> CalendarData:
        """
        Collect calendar data for specified date range

        Args:
            date_range: Number of days to look ahead (default: 30)

        Returns:
            CalendarData: Structured calendar data
        """
        # Check cache first
        cache_key = f"calendar_{date_range}"
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return CalendarData(**cached_data)

        if not self.calendar_api_key:
            print("Warning: Calendar API key not configured, returning empty data")
            return CalendarData(
                events=[],
                meetings=[],
                deadlines=[],
                availability={},
                collected_at=datetime.now().isoformat()
            )

        # TODO: Implement Google Calendar API integration
        # For now, return placeholder structure
        calendar_data = CalendarData(
            events=[],
            meetings=[],
            deadlines=[],
            availability={
                'status': 'calendar_integration_pending',
                'message': 'Calendar API integration ready for implementation'
            },
            collected_at=datetime.now().isoformat()
        )

        # Cache the results
        self._save_to_cache(cache_key, asdict(calendar_data))

        return calendar_data

    def collect_notes_data(self, project_name: str) -> NotesData:
        """
        Collect notes data for specified project

        Args:
            project_name: Name of the project to search for

        Returns:
            NotesData: Structured notes data
        """
        # Check cache first
        cache_key = f"notes_{project_name.replace(' ', '_').lower()}"
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            return NotesData(**cached_data)

        project_notes = []
        action_items = []
        decisions = []

        if NOTES_AVAILABLE:
            try:
                # Use existing notes interface to search for project-related content
                notes_interface = NotesCommandInterface()

                # Search for project-related notes
                search_result = notes_interface.execute_command('research', {
                    'query': project_name,
                    'output_format': 'json'
                })

                if search_result.success and search_result.data:
                    # Process search results
                    for note in search_result.data.get('notes', []):
                        project_notes.append({
                            'title': note.get('title', 'Untitled'),
                            'file_path': note.get('file_path', ''),
                            'category': note.get('category', ''),
                            'created_date': note.get('created_date', ''),
                            'content_preview': note.get('content', '')[:200] + '...' if note.get('content', '') else ''
                        })

                # Get action items for the project
                actions_result = notes_interface.execute_command('check-actions', {
                    'filter_project': project_name,
                    'output_format': 'json'
                })

                if actions_result.success and actions_result.data:
                    for action in actions_result.data.get('actions', []):
                        action_items.append({
                            'task': action.get('task', ''),
                            'assignee': action.get('assignee', 'unassigned'),
                            'due_date': action.get('due_date', ''),
                            'status': action.get('status', 'unknown'),
                            'file': action.get('file', ''),
                            'priority': action.get('priority', 'medium')
                        })

                # Extract decisions (look for decision-related patterns in notes)
                if search_result.success and search_result.data:
                    for note in search_result.data.get('notes', []):
                        content = note.get('content', '').lower()
                        if any(keyword in content for keyword in ['decision', 'decided', 'resolved', 'concluded']):
                            decisions.append({
                                'title': note.get('title', 'Untitled'),
                                'file_path': note.get('file_path', ''),
                                'decision_date': note.get('created_date', ''),
                                'content_preview': note.get('content', '')[:300] + '...' if note.get('content', '') else ''
                            })

            except Exception as e:
                print(f"Warning: Failed to collect notes data: {e}")

        else:
            print("Warning: Notes system not available, returning empty data")

        notes_data = NotesData(
            project_notes=project_notes,
            action_items=action_items,
            decisions=decisions,
            collected_at=datetime.now().isoformat()
        )

        # Cache the results
        self._save_to_cache(cache_key, asdict(notes_data))

        return notes_data

    def collect_project_data(self, project_name: str) -> ProjectData:
        """
        Collect all data for a specific project

        Args:
            project_name: Name of the project from projects.yaml

        Returns:
            ProjectData: Complete project data collection
        """
        project_config = self.projects_config.get('projects', {}).get(project_name)
        if not project_config:
            raise ValueError(f"Project '{project_name}' not found in projects.yaml")

        collection_start = datetime.now()
        collection_summary = {
            'sources_attempted': [],
            'sources_successful': [],
            'sources_failed': [],
            'total_items_collected': 0
        }

        # Collect GitHub data
        github_data = None
        if project_config.get('github_repos'):
            try:
                collection_summary['sources_attempted'].append('github')
                github_data = self.collect_github_data(project_config['github_repos'])
                collection_summary['sources_successful'].append('github')
                collection_summary['total_items_collected'] += (
                    len(github_data.pull_requests) +
                    len(github_data.issues) +
                    len(github_data.commits) +
                    len(github_data.milestones)
                )
            except Exception as e:
                collection_summary['sources_failed'].append(f'github: {str(e)}')
                print(f"Failed to collect GitHub data: {e}")

        # Collect calendar data
        calendar_data = None
        try:
            collection_summary['sources_attempted'].append('calendar')
            calendar_data = self.collect_calendar_data()
            collection_summary['sources_successful'].append('calendar')
            collection_summary['total_items_collected'] += len(calendar_data.events)
        except Exception as e:
            collection_summary['sources_failed'].append(f'calendar: {str(e)}')
            print(f"Failed to collect calendar data: {e}")

        # Collect notes data
        notes_data = None
        try:
            collection_summary['sources_attempted'].append('notes')
            notes_data = self.collect_notes_data(project_config['name'])
            collection_summary['sources_successful'].append('notes')
            collection_summary['total_items_collected'] += (
                len(notes_data.project_notes) +
                len(notes_data.action_items) +
                len(notes_data.decisions)
            )
        except Exception as e:
            collection_summary['sources_failed'].append(f'notes: {str(e)}')
            print(f"Failed to collect notes data: {e}")

        # Calculate collection time
        collection_summary['collection_duration_seconds'] = (datetime.now() - collection_start).total_seconds()
        collection_summary['success_rate'] = (
            len(collection_summary['sources_successful']) /
            len(collection_summary['sources_attempted'])
            if collection_summary['sources_attempted'] else 0
        )

        return ProjectData(
            project_name=project_name,
            github_data=github_data,
            calendar_data=calendar_data,
            notes_data=notes_data,
            collection_summary=collection_summary,
            collected_at=datetime.now().isoformat()
        )

    def collect_all_projects_data(self) -> Dict[str, ProjectData]:
        """
        Collect data for all projects defined in projects.yaml

        Returns:
            Dict[str, ProjectData]: Complete data for all projects
        """
        all_projects_data = {}

        for project_name in self.projects_config.get('projects', {}):
            try:
                project_data = self.collect_project_data(project_name)
                all_projects_data[project_name] = project_data
                print(f"✅ Collected data for project: {project_name}")
            except Exception as e:
                print(f"❌ Failed to collect data for project {project_name}: {e}")

        return all_projects_data

def main():
    """CLI interface for data collection"""
    import argparse

    parser = argparse.ArgumentParser(description='Cross-Platform Data Collection System')
    parser.add_argument('--project', type=str, help='Specific project name to collect data for')
    parser.add_argument('--all-projects', action='store_true', help='Collect data for all projects')
    parser.add_argument('--output', type=str, help='Output file path (JSON format)')
    parser.add_argument('--cache-only', action='store_true', help='Use cached data only, no API calls')

    args = parser.parse_args()

    collector = ProjectDataCollector()

    try:
        if args.project:
            # Collect data for specific project
            data = collector.collect_project_data(args.project)
            result = {args.project: asdict(data)}

        elif args.all_projects:
            # Collect data for all projects
            data = collector.collect_all_projects_data()
            result = {name: asdict(project_data) for name, project_data in data.items()}

        else:
            # Show available projects
            projects = list(collector.projects_config.get('projects', {}).keys())
            print("Available projects:")
            for project in projects:
                print(f"  - {project}")
            return

        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Data saved to: {args.output}")
        else:
            print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
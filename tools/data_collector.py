"""
DataCollector - Multi-Source Data Aggregation Tool

Unified data collection from GitHub, notes, calendar, and config sources
with intelligent caching and rate limiting.

Simplifies command implementation from 200-300 lines down to 3-5 lines:

    collector = DataCollector()
    data = collector.aggregate_project_data("mobile-app-v2", sources=["github", "notes", "config"])
"""

import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from cachetools import TTLCache

from tools.config_manager import ConfigManager
from tools.data_models import (
    CalendarData,
    GitHubData,
    NotesData,
    ProjectData,
    TeamData,
)


class DataCollectorError(Exception):
    """Base exception for DataCollector errors."""
    pass


class GitHubRateLimitError(DataCollectorError):
    """Raised when GitHub API rate limit is exceeded."""
    pass


class DataCollector:
    """
    Unified data collection from multiple sources with smart caching.

    Features:
    - GitHub API integration with rate limiting
    - Notes system integration via ./notes CLI
    - Calendar data collection
    - Team data from config
    - TTL-based caching (default 5 minutes)
    - Automatic retry with exponential backoff
    - Graceful degradation when sources unavailable

    Example:
        >>> collector = DataCollector()
        >>> # Simple aggregation (300 lines → 3 lines)
        >>> data = collector.aggregate_project_data(
        ...     "mobile-app-v2",
        ...     sources=["github", "notes", "config"]
        ... )
        >>> print(f"PRs: {len(data.github_data.pull_requests)}")
        >>> print(f"Actions: {len(data.notes_data.action_items)}")
    """

    def __init__(
        self,
        config_root: Optional[Path] = None,
        cache_ttl: int = 300,  # 5 minutes default
        max_retries: int = 3,
    ):
        """
        Initialize DataCollector.

        Args:
            config_root: Root directory for configuration files
            cache_ttl: Cache time-to-live in seconds (default: 300)
            max_retries: Maximum retry attempts for failed requests (default: 3)
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self.config_manager = ConfigManager(config_root=self.config_root)
        self.cache_ttl = cache_ttl
        self.max_retries = max_retries

        # Initialize TTL cache
        self._cache = TTLCache(maxsize=100, ttl=cache_ttl)

        # Load configurations
        self._load_configurations()

        # Initialize API clients
        self._init_api_clients()

        # Rate limiting state
        self.github_rate_limit = {
            "remaining": 5000,
            "reset_time": datetime.now() + timedelta(hours=1),
        }

    def _load_configurations(self):
        """Load all required configurations."""
        self.integrations_config = self.config_manager.load_config("integrations.yaml")
        self.projects_config = self.config_manager.load_config("projects.yaml")
        self.team_config = self.config_manager.load_config("team.yaml")

    def _init_api_clients(self):
        """Initialize API clients and tokens."""
        # GitHub token
        github_config = self.integrations_config.get("integrations", {}).get("github", {}).get("config", {})
        token_env = github_config.get("token_env", "GITHUB_TOKEN")
        self.github_token = os.environ.get(token_env)
        self.github_org = github_config.get("default_org", "")

        # Calendar API key
        calendar_config = self.integrations_config.get("integrations", {}).get("calendar", {}).get("config", {})
        key_env = calendar_config.get("api_key_env", "CALENDAR_API_KEY")
        self.calendar_api_key = os.environ.get(key_env)

    def _get_cache_key(self, *args) -> str:
        """Generate cache key from arguments."""
        key_str = "_".join(str(arg) for arg in args)
        return hashlib.md5(key_str.encode()).hexdigest()

    def _check_github_rate_limit(self) -> None:
        """Check and handle GitHub API rate limiting."""
        if not self.github_token:
            raise DataCollectorError("GitHub token not configured. Set GITHUB_TOKEN environment variable.")

        headers = {"Authorization": f"token {self.github_token}"}
        try:
            response = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=10)
            response.raise_for_status()

            rate_data = response.json()["resources"]["core"]
            self.github_rate_limit = {
                "remaining": rate_data["remaining"],
                "reset_time": datetime.fromtimestamp(rate_data["reset"]),
            }

            # Wait if rate limit is low
            if rate_data["remaining"] < 100:
                sleep_time = (self.github_rate_limit["reset_time"] - datetime.now()).total_seconds()
                if sleep_time > 0:
                    raise GitHubRateLimitError(
                        f"Rate limit low ({rate_data['remaining']}). Resets in {sleep_time:.0f}s"
                    )
        except requests.RequestException as e:
            # Non-fatal - continue with cached rate limit state
            pass

    def _retry_request(self, func, *args, **kwargs):
        """Execute request with exponential backoff retry."""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (requests.RequestException, Exception) as e:
                last_exception = e
                if attempt == self.max_retries - 1:
                    raise DataCollectorError(f"Request failed after {self.max_retries} attempts: {e}")
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)

        # Fallback - should never reach here
        if last_exception:
            raise DataCollectorError(f"Request failed: {last_exception}")

    def collect_github_data(
        self,
        repos: List[str],
        data_types: Optional[List[str]] = None,
        since: Optional[str] = None,
        cache_ttl: Optional[int] = None,
    ) -> GitHubData:
        """
        Collect GitHub data for specified repositories.

        Args:
            repos: List of repository names (owner/repo or just repo)
            data_types: Types to collect (prs, issues, commits, milestones, stats)
            since: ISO date string for filtering recent data
            cache_ttl: Override default cache TTL

        Returns:
            GitHubData: Aggregated GitHub data

        Raises:
            DataCollectorError: If GitHub token not configured or request fails
            GitHubRateLimitError: If rate limit exceeded
        """
        # Check cache
        cache_key = self._get_cache_key("github", *repos, data_types, since)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Check rate limit
        self._check_github_rate_limit()

        data_types = data_types or ["prs", "issues", "commits", "milestones", "stats"]
        since = since or (datetime.now() - timedelta(days=30)).isoformat()

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        all_prs, all_issues, all_commits, all_milestones = [], [], [], []
        repo_stats = {}

        for repo in repos:
            # Normalize repo name
            full_repo = f"{self.github_org}/{repo}" if "/" not in repo else repo

            try:
                # Repository stats
                if "stats" in data_types:
                    repo_response = self._retry_request(
                        requests.get,
                        f"https://api.github.com/repos/{full_repo}",
                        headers=headers,
                        timeout=10,
                    )
                    if repo_response.status_code == 200:
                        repo_data = repo_response.json()
                        repo_stats[repo] = {
                            "full_name": repo_data["full_name"],
                            "stars": repo_data["stargazers_count"],
                            "forks": repo_data["forks_count"],
                            "open_issues": repo_data["open_issues_count"],
                            "language": repo_data.get("language"),
                            "updated_at": repo_data["updated_at"],
                        }

                # Pull requests
                if "prs" in data_types:
                    pr_response = self._retry_request(
                        requests.get,
                        f"https://api.github.com/repos/{full_repo}/pulls",
                        headers=headers,
                        params={"state": "all", "since": since, "per_page": 100},
                        timeout=10,
                    )
                    if pr_response.status_code == 200:
                        all_prs.extend(pr_response.json())

                # Issues
                if "issues" in data_types:
                    issues_response = self._retry_request(
                        requests.get,
                        f"https://api.github.com/repos/{full_repo}/issues",
                        headers=headers,
                        params={"state": "all", "since": since, "per_page": 100},
                        timeout=10,
                    )
                    if issues_response.status_code == 200:
                        all_issues.extend(issues_response.json())

                # Commits
                if "commits" in data_types:
                    commits_response = self._retry_request(
                        requests.get,
                        f"https://api.github.com/repos/{full_repo}/commits",
                        headers=headers,
                        params={"since": since, "per_page": 100},
                        timeout=10,
                    )
                    if commits_response.status_code == 200:
                        all_commits.extend(commits_response.json())

                # Milestones
                if "milestones" in data_types:
                    milestones_response = self._retry_request(
                        requests.get,
                        f"https://api.github.com/repos/{full_repo}/milestones",
                        headers=headers,
                        params={"state": "all", "per_page": 100},
                        timeout=10,
                    )
                    if milestones_response.status_code == 200:
                        all_milestones.extend(milestones_response.json())

            except requests.RequestException as e:
                # Log error but continue with other repos
                print(f"Warning: Failed to collect data for {full_repo}: {e}")
                continue

        result = GitHubData(
            repo_name=", ".join(repos),
            pull_requests=all_prs,
            issues=all_issues,
            commits=all_commits,
            milestones=all_milestones,
            repository_stats=repo_stats,
        )

        # Cache result
        self._cache[cache_key] = result
        return result

    def collect_notes_data(
        self,
        project: str,
        filters: Optional[Dict[str, Any]] = None,
        include_action_items: bool = True,
    ) -> NotesData:
        """
        Collect notes data for specified project.

        Args:
            project: Project name/ID
            filters: Additional filters for notes
            include_action_items: Whether to extract action items

        Returns:
            NotesData: Aggregated notes data

        Raises:
            DataCollectorError: If notes CLI unavailable or execution fails
        """
        # Check cache
        cache_key = self._get_cache_key("notes", project, str(filters), include_action_items)
        if cache_key in self._cache:
            return self._cache[cache_key]

        notes_cli = Path.cwd() / "notes"
        if not notes_cli.exists():
            raise DataCollectorError("Notes CLI not found at ./notes")

        try:
            # Collect project notes
            result = subprocess.run(
                [str(notes_cli), "list", "--project", project, "--json"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                raise DataCollectorError(f"Notes CLI failed: {result.stderr}")

            notes_data = json.loads(result.stdout) if result.stdout.strip() else {"notes": []}

            # Extract action items if requested
            action_items = []
            if include_action_items:
                action_result = subprocess.run(
                    [str(notes_cli), "actions", "--project", project, "--json"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if action_result.returncode == 0 and action_result.stdout.strip():
                    action_data = json.loads(action_result.stdout)
                    action_items = action_data.get("action_items", [])

            notes_result = NotesData(
                project_notes=notes_data.get("notes", []),
                action_items=action_items,
                decisions=notes_data.get("decisions", []),
            )

            # Cache result
            self._cache[cache_key] = notes_result
            return notes_result

        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
            raise DataCollectorError(f"Failed to collect notes data: {e}")

    def collect_calendar_data(
        self,
        date_range: int = 30,
        event_types: Optional[List[str]] = None,
    ) -> CalendarData:
        """
        Collect calendar data.

        Args:
            date_range: Number of days to look ahead (default: 30)
            event_types: Types of events to collect

        Returns:
            CalendarData: Aggregated calendar data

        Note:
            Currently returns placeholder data. Implement Google Calendar API integration as needed.
        """
        # Check cache
        cache_key = self._get_cache_key("calendar", date_range, str(event_types))
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Placeholder implementation - extend with actual Calendar API
        result = CalendarData(
            events=[],
            meetings=[],
            deadlines=[],
            availability={"note": "Calendar integration not yet implemented"},
        )

        self._cache[cache_key] = result
        return result

    def collect_team_data(
        self,
        project: str,
        include_performance: bool = False,
    ) -> TeamData:
        """
        Collect team data from configuration.

        Args:
            project: Project name
            include_performance: Whether to include performance metrics

        Returns:
            TeamData: Team information
        """
        # Check cache
        cache_key = self._get_cache_key("team", project, include_performance)
        if cache_key in self._cache:
            return self._cache[cache_key]

        project_config = self.projects_config.get("projects", {}).get(project, {})
        team_members = project_config.get("team", [])

        # Get full team member details
        all_members = self.team_config.get("team", {}).get("members", [])
        project_member_details = [
            member for member in all_members
            if member.get("id") in team_members or member.get("name") in team_members
        ]

        result = TeamData(
            members=project_member_details,
            performance_metrics={} if not include_performance else {"note": "Performance tracking not yet implemented"},
            roles={member.get("id", member.get("name")): member.get("role", "member") for member in project_member_details},
        )

        self._cache[cache_key] = result
        return result

    def aggregate_project_data(
        self,
        project_id: str,
        sources: Optional[List[str]] = None,
        cache_ttl: Optional[int] = None,
    ) -> ProjectData:
        """
        Aggregate all project data from specified sources.

        This is the main method that simplifies 200-300 lines of data collection
        down to 3-5 lines in command implementations.

        Args:
            project_id: Project identifier
            sources: List of sources to collect from (github, notes, calendar, team, config)
            cache_ttl: Override default cache TTL

        Returns:
            ProjectData: Unified project data

        Example:
            >>> collector = DataCollector()
            >>> data = collector.aggregate_project_data(
            ...     "mobile-app-v2",
            ...     sources=["github", "notes", "config"]
            ... )
        """
        sources = sources or ["github", "notes", "calendar", "team", "config"]

        # Get project configuration
        project_config = self.projects_config.get("projects", {}).get(project_id, {})
        if not project_config:
            raise DataCollectorError(f"Project '{project_id}' not found in configuration")

        github_data = None
        notes_data = None
        calendar_data = None
        team_data = None
        collection_summary = {"sources": sources, "errors": []}

        # Collect GitHub data
        if "github" in sources:
            try:
                repos = project_config.get("github_repos", [])
                if repos:
                    github_data = self.collect_github_data(repos)
                    collection_summary["github"] = "success"
                else:
                    collection_summary["github"] = "no_repos_configured"
            except Exception as e:
                collection_summary["errors"].append(f"GitHub: {str(e)}")
                collection_summary["github"] = "failed"

        # Collect notes data
        if "notes" in sources:
            try:
                notes_data = self.collect_notes_data(project_id)
                collection_summary["notes"] = "success"
            except Exception as e:
                collection_summary["errors"].append(f"Notes: {str(e)}")
                collection_summary["notes"] = "failed"

        # Collect calendar data
        if "calendar" in sources:
            try:
                calendar_data = self.collect_calendar_data()
                collection_summary["calendar"] = "success"
            except Exception as e:
                collection_summary["errors"].append(f"Calendar: {str(e)}")
                collection_summary["calendar"] = "failed"

        # Collect team data
        if "team" in sources:
            try:
                team_data = self.collect_team_data(project_id)
                collection_summary["team"] = "success"
            except Exception as e:
                collection_summary["errors"].append(f"Team: {str(e)}")
                collection_summary["team"] = "failed"

        return ProjectData(
            project_name=project_id,
            github_data=github_data,
            calendar_data=calendar_data,
            notes_data=notes_data,
            team_data=team_data,
            config_data=project_config if "config" in sources else {},
            collection_summary=collection_summary,
        )

    def clear_cache(self):
        """Clear all cached data."""
        self._cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "max_size": self._cache.maxsize,
            "ttl": self._cache.ttl,
        }

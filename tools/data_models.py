"""
Data models for DataCollector - Multi-Source Data Aggregation

Provides standardized data structures for GitHub, Notes, Calendar, and aggregated project data.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class GitHubData:
    """Standardized GitHub data structure."""

    repo_name: str
    pull_requests: List[Dict[str, Any]] = field(default_factory=list)
    issues: List[Dict[str, Any]] = field(default_factory=list)
    commits: List[Dict[str, Any]] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    repository_stats: Dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CalendarData:
    """Standardized Calendar data structure."""

    events: List[Dict[str, Any]] = field(default_factory=list)
    meetings: List[Dict[str, Any]] = field(default_factory=list)
    deadlines: List[Dict[str, Any]] = field(default_factory=list)
    availability: Dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class NotesData:
    """Standardized Notes data structure."""

    project_notes: List[Dict[str, Any]] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TeamData:
    """Standardized Team data structure."""

    members: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    roles: Dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ProjectData:
    """Unified project data structure aggregating all sources."""

    project_name: str
    github_data: Optional[GitHubData] = None
    calendar_data: Optional[CalendarData] = None
    notes_data: Optional[NotesData] = None
    team_data: Optional[TeamData] = None
    config_data: Dict[str, Any] = field(default_factory=dict)
    collection_summary: Dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        from dataclasses import asdict
        return asdict(self)

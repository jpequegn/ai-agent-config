"""
Data models for NLP processing.

Provides structured types for command intent, date ranges, and entity extraction.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Command action types."""

    FIND = "find"
    SHOW = "show"
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ANALYZE = "analyze"
    GENERATE = "generate"
    EXPORT = "export"
    IMPORT = "import"


class SubjectType(str, Enum):
    """Command subject types."""

    NOTES = "notes"
    PROJECTS = "projects"
    TASKS = "tasks"
    MEETINGS = "meetings"
    DECISIONS = "decisions"
    STAKEHOLDERS = "stakeholders"
    TEAM = "team"
    REPORTS = "reports"


class Priority(str, Enum):
    """Priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DateRange(BaseModel):
    """Date range model."""

    start: datetime
    end: datetime
    description: Optional[str] = None

    def contains(self, date: datetime) -> bool:
        """Check if date falls within range."""
        return self.start <= date <= self.end

    def duration_days(self) -> int:
        """Calculate duration in days."""
        return (self.end - self.start).days


class CommandIntent(BaseModel):
    """Parsed command intent model."""

    action: Optional[ActionType] = None
    subject: Optional[SubjectType] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    raw_text: str
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)

    def has_filter(self, key: str) -> bool:
        """Check if filter exists."""
        return key in self.filters

    def get_filter(self, key: str, default: Any = None) -> Any:
        """Get filter value with default."""
        return self.filters.get(key, default)


class EntityMatch(BaseModel):
    """Extracted entity with metadata."""

    value: str
    entity_type: str
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    start_position: Optional[int] = None
    end_position: Optional[int] = None


class FuzzyMatch(BaseModel):
    """Fuzzy match result."""

    candidate: str
    score: float = Field(ge=0.0, le=1.0)
    original_query: str

    def is_confident(self, threshold: float = 0.8) -> bool:
        """Check if match meets confidence threshold."""
        return self.score >= threshold


class DateExpression(BaseModel):
    """Parsed date expression."""

    resolved_date: datetime
    original_expression: str
    expression_type: str  # "relative", "absolute", "range"
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)

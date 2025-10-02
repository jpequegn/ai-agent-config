"""
OutputFormatter Data Models

Data classes for output formatting system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class OutputFormat(Enum):
    """Supported output formats."""

    MARKDOWN = "markdown"
    JSON = "json"
    TABLE = "table"
    HTML = "html"


class AudienceType(Enum):
    """Audience types for targeted formatting."""

    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    STAKEHOLDER = "stakeholder"
    GENERAL = "general"


class DateStyle(Enum):
    """Date formatting styles."""

    RELATIVE = "relative"  # "2 hours ago", "3 days ago"
    ABSOLUTE = "absolute"  # "2025-10-02 19:45:00"
    SHORT = "short"  # "Oct 2, 2025"
    LONG = "long"  # "October 2, 2025 at 7:45 PM"
    ISO = "iso"  # "2025-10-02T19:45:00Z"


@dataclass
class FormattingContext:
    """Context for formatting operations."""

    audience: AudienceType = AudienceType.GENERAL
    format: OutputFormat = OutputFormat.MARKDOWN
    date_style: DateStyle = DateStyle.RELATIVE
    include_emoji: bool = True
    max_length: Optional[int] = None
    focus_area: Optional[str] = None
    custom_variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemplateMetadata:
    """Metadata for templates."""

    name: str
    description: str
    format: OutputFormat
    audience: AudienceType
    version: str = "1.0.0"
    author: str = "PARA System"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    variables: List[str] = field(default_factory=list)


@dataclass
class FormattedOutput:
    """Result of formatting operation."""

    content: str
    format: OutputFormat
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time_ms: float = 0.0
    template_used: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


@dataclass
class TableColumn:
    """Column definition for table formatting."""

    name: str
    key: str
    width: Optional[int] = None
    align: str = "left"  # left, center, right
    format_fn: Optional[Any] = None  # Callable for custom formatting


@dataclass
class EmojiIndicators:
    """Emoji indicators for health/status visualization."""

    excellent: str = "🟢"
    good: str = "🟡"
    fair: str = "🟠"
    poor: str = "🔴"
    critical: str = "🚨"
    unknown: str = "⚪"
    warning: str = "⚠️"
    info: str = "ℹ️"
    success: str = "✅"
    failure: str = "❌"
    in_progress: str = "🔄"
    pending: str = "⏳"
    blocked: str = "🚧"


@dataclass
class HealthScoreFormat:
    """Formatting rules for health scores."""

    excellent_threshold: float = 0.8
    good_threshold: float = 0.6
    fair_threshold: float = 0.4
    poor_threshold: float = 0.2
    show_percentage: bool = True
    show_emoji: bool = True
    precision: int = 2  # Decimal places


@dataclass
class OutputSchema:
    """JSON schema definition for structured output."""

    version: str = "1.0"
    type: str = "object"
    properties: Dict[str, Any] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    additional_properties: bool = False

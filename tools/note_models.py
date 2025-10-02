"""
Note Models - Data structures for note processing operations

Provides Pydantic models and dataclasses for note processing results,
aligned with existing para-processor.py infrastructure.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel


class ParaCategory(str, Enum):
    """PARA Method categories"""

    PROJECTS = "1-projects"
    AREAS = "2-areas"
    RESOURCES = "3-resources"
    ARCHIVE = "4-archive"
    INBOX = "inbox"


@dataclass
class ActionItem:
    """Represents an action item extracted from a note"""

    text: str
    completed: bool
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    line_number: Optional[int] = None
    priority: Optional[str] = None


@dataclass
class CategorizationResult:
    """Represents a PARA categorization result with confidence and reasoning"""

    category: ParaCategory
    confidence: float  # 0.0 to 1.0
    reasoning: List[str]  # List of reasons for this categorization
    alternative_categories: List[
        Tuple[ParaCategory, float]
    ]  # Other possibilities with scores
    manual_override: bool = False  # Whether this was manually set


@dataclass
class ParsedNote:
    """Represents a fully parsed note with all extracted information"""

    file_path: str
    frontmatter: Dict[str, Any]
    content: str
    raw_content: str
    action_items: List[ActionItem]
    attendees: List[str]
    dates: List[str]
    tags: List[str]
    categorization_result: Optional[CategorizationResult] = None
    suggested_category: Optional[ParaCategory] = None  # Backward compatibility
    word_count: int = 0
    estimated_read_time: int = 0  # in minutes


class FrontmatterUpdate(BaseModel):
    """Schema for frontmatter updates"""

    updates: Dict[str, Any]
    create_backup: bool = True


class NoteSearchFilters(BaseModel):
    """Filters for note search operations"""

    query: Optional[str] = None
    para_category: Optional[ParaCategory] = None
    has_action_items: Optional[bool] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    date_range: Optional[Tuple[str, str]] = None
    project: Optional[str] = None


class ActionItemFilters(BaseModel):
    """Filters for action item extraction"""

    status: Optional[str] = None  # 'pending', 'completed', 'overdue'
    assignee: Optional[str] = None
    priority: Optional[str] = None
    has_due_date: Optional[bool] = None
    date_range: Optional[Tuple[str, str]] = None


class BatchProcessResult(BaseModel):
    """Result of batch note processing"""

    total_processed: int
    successful: int
    failed: int
    notes: List[Dict[str, Any]]
    errors: List[Dict[str, str]]


class NoteLink(BaseModel):
    """Represents a note-project link"""

    note_path: str
    project_id: str
    link_type: str = "manual"  # 'manual', 'auto-detected', 'synced'
    created_at: Optional[str] = None

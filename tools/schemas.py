"""
Pydantic schemas for YAML configuration validation.

Provides type-safe models for all configuration files used in the system.
"""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# Enums
class ProjectStatus(str, Enum):
    """Project status options."""

    PLANNING = "planning"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class Priority(str, Enum):
    """Priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MilestoneStatus(str, Enum):
    """Milestone status options."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Project Models
class Milestone(BaseModel):
    """Project milestone model."""

    name: str
    date: date
    status: MilestoneStatus
    description: Optional[str] = None


class Project(BaseModel):
    """Project configuration model."""

    name: str
    status: ProjectStatus
    priority: Priority
    owner: str
    start_date: date
    target_date: date
    github_repos: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)
    template_used: Optional[str] = None
    description: Optional[str] = None


class ProjectsConfig(BaseModel):
    """Root projects configuration model."""

    projects: Dict[str, Project]


# Team Models
class TeamMember(BaseModel):
    """Team member model."""

    name: str
    role: str
    start_date: date
    current_projects: List[str] = Field(default_factory=list)
    goals_2024: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    development_areas: List[str] = Field(default_factory=list)
    last_review: Optional[date] = None
    next_review: Optional[date] = None
    status: str = "active"
    timezone: Optional[str] = None
    location: Optional[str] = None
    manager: Optional[str] = None


class TeamRosterConfig(BaseModel):
    """Team roster configuration model."""

    team_members: Dict[str, TeamMember]


# Stakeholder Models
class DecisionPreferences(BaseModel):
    """Decision-making preferences."""

    communication_style: str
    detail_level: str
    preferred_formats: List[str] = Field(default_factory=list)
    decision_speed: str
    risk_tolerance: str


class InfluenceFactors(BaseModel):
    """Decision influence factors with weights.

    Supports flexible influence factor keys (technical_feasibility, business_impact, etc.)
    All values must be floats between 0 and 1.
    """

    model_config = {"extra": "allow"}  # Allow additional fields

    # Common influence factors (all optional to support flexible keys)
    technical_feasibility: Optional[float] = Field(default=None, ge=0, le=1)
    team_impact: Optional[float] = Field(default=None, ge=0, le=1)
    learning_opportunities: Optional[float] = Field(default=None, ge=0, le=1)
    timeline_constraints: Optional[float] = Field(default=None, ge=0, le=1)
    business_impact: Optional[float] = Field(default=None, ge=0, le=1)
    resource_efficiency: Optional[float] = Field(default=None, ge=0, le=1)
    strategic_alignment: Optional[float] = Field(default=None, ge=0, le=1)
    risk_management: Optional[float] = Field(default=None, ge=0, le=1)
    operational_impact: Optional[float] = Field(default=None, ge=0, le=1)
    security_implications: Optional[float] = Field(default=None, ge=0, le=1)
    maintenance_complexity: Optional[float] = Field(default=None, ge=0, le=1)
    automation_potential: Optional[float] = Field(default=None, ge=0, le=1)

    @field_validator("*")
    @classmethod
    def validate_weights(cls, v: Optional[float]) -> Optional[float]:
        """Validate weight is between 0 and 1."""
        if v is not None and not 0 <= v <= 1:
            raise ValueError("Weight must be between 0 and 1")
        return v


class NotificationPreferences(BaseModel):
    """Communication notification preferences."""

    decision_updates: str
    urgent_decisions: str
    meeting_preferences: str


class DecisionHistory(BaseModel):
    """Historical decision patterns."""

    frameworks_used: List[str] = Field(default_factory=list)
    recent_decisions: List[str] = Field(default_factory=list)


class StakeholderProfile(BaseModel):
    """Stakeholder decision-making profile."""

    name: str
    role: str
    department: str
    decision_authority_level: str
    decision_preferences: DecisionPreferences
    expertise_areas: List[str] = Field(default_factory=list)
    influence_factors: InfluenceFactors
    typical_concerns: List[str] = Field(default_factory=list)
    notification_preferences: NotificationPreferences
    decision_history: DecisionHistory


class StakeholderContextsConfig(BaseModel):
    """Stakeholder contexts configuration model."""

    stakeholder_profiles: Dict[str, StakeholderProfile]


# Integration Models
class RateLimits(BaseModel):
    """API rate limits."""

    requests_per_hour: int
    requests_per_day: int


class Credentials(BaseModel):
    """API credentials (values should be encrypted)."""

    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class FinancialTool(BaseModel):
    """Financial integration tool model."""

    enabled: bool
    provider: str
    connection_type: str
    api_version: Optional[str] = None
    credentials: Credentials
    sync_frequency: str
    sync_time: Optional[str] = None
    data_types: List[str] = Field(default_factory=list)
    rate_limits: Optional[RateLimits] = None
    status: str
    last_sync: Optional[datetime] = None
    sync_errors: int = 0
    notes: Optional[str] = None


class IntegrationsConfig(BaseModel):
    """Integrations configuration model."""

    financial_tools: Dict[str, FinancialTool]


# Decision Framework Models
class DecisionCriteria(BaseModel):
    """Decision criteria with weight."""

    name: str
    weight: float = Field(ge=0, le=1)
    description: Optional[str] = None


class DecisionFramework(BaseModel):
    """Decision framework model."""

    name: str
    description: str
    criteria: List[DecisionCriteria]
    scoring_method: str
    approval_threshold: Optional[float] = None


class DecisionFrameworksConfig(BaseModel):
    """Decision frameworks configuration model."""

    frameworks: Dict[str, DecisionFramework]

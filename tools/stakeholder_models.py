"""
Stakeholder models for decision support and stakeholder management.

Provides data structures for stakeholder analysis, influence mapping, and communication planning.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class InfluenceLevel(str, Enum):
    """Stakeholder influence levels."""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class InterestLevel(str, Enum):
    """Stakeholder interest levels."""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class PowerInterestQuadrant(str, Enum):
    """Power-Interest grid quadrants."""
    MANAGE_CLOSELY = "manage_closely"      # High power, high interest
    KEEP_SATISFIED = "keep_satisfied"      # High power, low interest
    KEEP_INFORMED = "keep_informed"        # Low power, high interest
    MONITOR = "monitor"                    # Low power, low interest


class AlignmentStatus(str, Enum):
    """Stakeholder alignment status."""
    STRONG_SUPPORT = "strong_support"
    SUPPORT = "support"
    NEUTRAL = "neutral"
    CONCERNS = "concerns"
    OPPOSITION = "opposition"


class CommunicationPriority(str, Enum):
    """Communication priority levels."""
    IMMEDIATE = "immediate"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Stakeholder:
    """
    Stakeholder profile for decision analysis.

    Example:
        >>> stakeholder = Stakeholder(
        ...     id="ceo-jane-smith",
        ...     name="Jane Smith",
        ...     role="CEO",
        ...     email="jane@company.com"
        ... )
    """
    id: str
    name: str
    role: str
    email: str
    department: Optional[str] = None
    influence_level: Optional[InfluenceLevel] = None
    interest_areas: List[str] = field(default_factory=list)
    communication_style: Optional[str] = None
    decision_factors: List[str] = field(default_factory=list)
    authority_scope: List[str] = field(default_factory=list)
    relationship_strength: Optional[str] = None
    last_interaction: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        from dataclasses import asdict
        return asdict(self)


@dataclass
class PowerInterestPosition:
    """Stakeholder position on power-interest grid."""
    stakeholder_id: str
    power_score: float  # 0.0 - 1.0
    interest_score: float  # 0.0 - 1.0
    quadrant: PowerInterestQuadrant
    influence_level: InfluenceLevel
    interest_level: InterestLevel
    reasoning: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "stakeholder_id": self.stakeholder_id,
            "power_score": self.power_score,
            "interest_score": self.interest_score,
            "quadrant": self.quadrant.value,
            "influence_level": self.influence_level.value,
            "interest_level": self.interest_level.value,
            "reasoning": self.reasoning,
        }


@dataclass
class PowerInterestGrid:
    """
    Power-Interest grid analysis results.

    Example:
        >>> grid = PowerInterestGrid(
        ...     positions=[
        ...         PowerInterestPosition("ceo", 0.9, 0.9, PowerInterestQuadrant.MANAGE_CLOSELY, ...),
        ...     ],
        ...     decision_context="Mobile app technology stack"
        ... )
    """
    positions: List[PowerInterestPosition]
    decision_context: str
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    summary: Dict[str, Any] = field(default_factory=dict)

    def get_by_quadrant(self, quadrant: PowerInterestQuadrant) -> List[PowerInterestPosition]:
        """Get all stakeholders in a specific quadrant."""
        return [p for p in self.positions if p.quadrant == quadrant]

    def get_high_influence(self, threshold: float = 0.7) -> List[PowerInterestPosition]:
        """Get stakeholders with high influence (power score above threshold)."""
        return [p for p in self.positions if p.power_score >= threshold]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "positions": [p.to_dict() for p in self.positions],
            "decision_context": self.decision_context,
            "analyzed_at": self.analyzed_at,
            "summary": self.summary,
            "quadrant_counts": {
                quadrant.value: len(self.get_by_quadrant(quadrant))
                for quadrant in PowerInterestQuadrant
            },
        }


@dataclass
class StakeholderAlignment:
    """Individual stakeholder alignment assessment."""
    stakeholder_id: str
    alignment_status: AlignmentStatus
    confidence: float  # 0.0 - 1.0
    key_concerns: List[str] = field(default_factory=list)
    supporting_factors: List[str] = field(default_factory=list)
    resistance_factors: List[str] = field(default_factory=list)
    predicted_position: str = ""
    influence_on_others: float = 0.0  # 0.0 - 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "stakeholder_id": self.stakeholder_id,
            "alignment_status": self.alignment_status.value,
            "confidence": self.confidence,
            "key_concerns": self.key_concerns,
            "supporting_factors": self.supporting_factors,
            "resistance_factors": self.resistance_factors,
            "predicted_position": self.predicted_position,
            "influence_on_others": self.influence_on_others,
        }


@dataclass
class AlignmentAnalysis:
    """
    Comprehensive alignment analysis results.

    Example:
        >>> analysis = AlignmentAnalysis(
        ...     alignments=[...],
        ...     decision_context="API redesign",
        ...     overall_support_score=0.72
        ... )
    """
    alignments: List[StakeholderAlignment]
    decision_context: str
    decision_options: List[str] = field(default_factory=list)
    overall_support_score: float = 0.0  # 0.0 - 1.0
    consensus_likelihood: float = 0.0  # 0.0 - 1.0
    key_supporters: List[str] = field(default_factory=list)
    key_resistors: List[str] = field(default_factory=list)
    coalition_opportunities: List[str] = field(default_factory=list)
    conflict_areas: List[str] = field(default_factory=list)
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def get_by_status(self, status: AlignmentStatus) -> List[StakeholderAlignment]:
        """Get all stakeholders with a specific alignment status."""
        return [a for a in self.alignments if a.alignment_status == status]

    def get_high_influence_supporters(self) -> List[StakeholderAlignment]:
        """Get supporters with high influence on others."""
        supporters = self.get_by_status(AlignmentStatus.STRONG_SUPPORT) + \
                    self.get_by_status(AlignmentStatus.SUPPORT)
        return [s for s in supporters if s.influence_on_others >= 0.7]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "alignments": [a.to_dict() for a in self.alignments],
            "decision_context": self.decision_context,
            "decision_options": self.decision_options,
            "overall_support_score": self.overall_support_score,
            "consensus_likelihood": self.consensus_likelihood,
            "key_supporters": self.key_supporters,
            "key_resistors": self.key_resistors,
            "coalition_opportunities": self.coalition_opportunities,
            "conflict_areas": self.conflict_areas,
            "analyzed_at": self.analyzed_at,
            "alignment_distribution": {
                status.value: len(self.get_by_status(status))
                for status in AlignmentStatus
            },
        }


@dataclass
class CommunicationMessage:
    """Individual communication message."""
    stakeholder_id: str
    message_type: str  # email, meeting, presentation, etc.
    priority: CommunicationPriority
    subject: str
    key_points: List[str] = field(default_factory=list)
    tone: str = "professional"
    timing: str = "immediate"
    follow_up_needed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "stakeholder_id": self.stakeholder_id,
            "message_type": self.message_type,
            "priority": self.priority.value,
            "subject": self.subject,
            "key_points": self.key_points,
            "tone": self.tone,
            "timing": self.timing,
            "follow_up_needed": self.follow_up_needed,
        }


@dataclass
class CommunicationPlan:
    """
    Comprehensive communication strategy.

    Example:
        >>> plan = CommunicationPlan(
        ...     messages=[...],
        ...     decision_context="Mobile tech stack",
        ...     overall_strategy="Build coalition with technical leaders first"
        ... )
    """
    messages: List[CommunicationMessage]
    decision_context: str
    overall_strategy: str
    communication_sequence: List[str] = field(default_factory=list)
    timing_strategy: str = ""
    key_messages: Dict[str, List[str]] = field(default_factory=dict)
    resistance_mitigation: List[str] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def get_immediate_communications(self) -> List[CommunicationMessage]:
        """Get all immediate priority communications."""
        return [m for m in self.messages if m.priority == CommunicationPriority.IMMEDIATE]

    def get_by_stakeholder(self, stakeholder_id: str) -> List[CommunicationMessage]:
        """Get all messages for a specific stakeholder."""
        return [m for m in self.messages if m.stakeholder_id == stakeholder_id]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "messages": [m.to_dict() for m in self.messages],
            "decision_context": self.decision_context,
            "overall_strategy": self.overall_strategy,
            "communication_sequence": self.communication_sequence,
            "timing_strategy": self.timing_strategy,
            "key_messages": self.key_messages,
            "resistance_mitigation": self.resistance_mitigation,
            "success_metrics": self.success_metrics,
            "created_at": self.created_at,
            "priority_breakdown": {
                priority.value: len([m for m in self.messages if m.priority == priority])
                for priority in CommunicationPriority
            },
        }


@dataclass
class InfluenceScore:
    """Calculated influence score for a stakeholder."""
    stakeholder_id: str
    overall_score: float  # 0.0 - 1.0
    power_component: float  # 0.0 - 1.0
    interest_component: float  # 0.0 - 1.0
    network_component: float  # 0.0 - 1.0 (influence on others)
    decision_authority: float  # 0.0 - 1.0
    factors: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "stakeholder_id": self.stakeholder_id,
            "overall_score": self.overall_score,
            "power_component": self.power_component,
            "interest_component": self.interest_component,
            "network_component": self.network_component,
            "decision_authority": self.decision_authority,
            "factors": self.factors,
        }

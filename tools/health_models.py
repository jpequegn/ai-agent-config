"""
Health models for project health scoring and risk assessment.

Provides data structures for health scores, trend analysis, and risk assessment.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class HealthCategory(str, Enum):
    """Health score categories."""
    EXCELLENT = "excellent"  # 0.85 - 1.0
    GOOD = "good"            # 0.70 - 0.84
    FAIR = "fair"            # 0.50 - 0.69
    POOR = "poor"            # 0.30 - 0.49
    CRITICAL = "critical"    # 0.0 - 0.29


class RiskSeverity(str, Enum):
    """Risk severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLikelihood(str, Enum):
    """Risk likelihood levels."""
    UNLIKELY = "unlikely"
    POSSIBLE = "possible"
    LIKELY = "likely"
    CERTAIN = "certain"


class TrendDirection(str, Enum):
    """Trend direction indicators."""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


@dataclass
class ComponentScore:
    """Individual component of health score."""
    name: str
    score: float  # 0.0 - 1.0
    weight: float
    weighted_score: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthScore:
    """
    Project health score with breakdown.

    Example:
        >>> health = HealthScore(
        ...     score=0.72,
        ...     category=HealthCategory.GOOD,
        ...     components={
        ...         "timeline": ComponentScore("timeline", 0.8, 0.3, 0.24),
        ...         "activity": ComponentScore("activity", 0.7, 0.25, 0.175),
        ...     }
        ... )
        >>> print(f"{health.category.value}: {health.score:.2f}")
        good: 0.72
    """
    score: float  # Overall score 0.0 - 1.0
    category: HealthCategory
    components: Dict[str, ComponentScore] = field(default_factory=dict)
    calculated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_score(cls, score: float, components: Optional[Dict[str, ComponentScore]] = None) -> "HealthScore":
        """Create HealthScore from numeric score with automatic categorization."""
        category = cls._categorize_score(score)
        return cls(
            score=score,
            category=category,
            components=components or {},
        )

    @staticmethod
    def _categorize_score(score: float) -> HealthCategory:
        """Categorize score into health category."""
        if score >= 0.85:
            return HealthCategory.EXCELLENT
        elif score >= 0.70:
            return HealthCategory.GOOD
        elif score >= 0.50:
            return HealthCategory.FAIR
        elif score >= 0.30:
            return HealthCategory.POOR
        else:
            return HealthCategory.CRITICAL

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "score": self.score,
            "category": self.category.value,
            "components": {
                name: {
                    "name": comp.name,
                    "score": comp.score,
                    "weight": comp.weight,
                    "weighted_score": comp.weighted_score,
                    "details": comp.details,
                }
                for name, comp in self.components.items()
            },
            "calculated_at": self.calculated_at,
            "details": self.details,
        }


@dataclass
class TrendDataPoint:
    """Single data point in trend analysis."""
    timestamp: str
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrendAnalysis:
    """
    Trend analysis results.

    Example:
        >>> trend = TrendAnalysis(
        ...     direction=TrendDirection.IMPROVING,
        ...     slope=0.05,
        ...     confidence=0.85,
        ...     data_points=[
        ...         TrendDataPoint("2025-09-01", 0.65),
        ...         TrendDataPoint("2025-10-01", 0.72),
        ...     ]
        ... )
        >>> print(f"Trend: {trend.direction.value} ({trend.slope:+.2f}/month)")
        Trend: improving (+0.05/month)
    """
    direction: TrendDirection
    slope: float  # Rate of change per time unit
    confidence: float  # 0.0 - 1.0
    data_points: List[TrendDataPoint] = field(default_factory=list)
    time_window_days: int = 30
    prediction: Optional[float] = None
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "direction": self.direction.value,
            "slope": self.slope,
            "confidence": self.confidence,
            "data_points": [
                {
                    "timestamp": dp.timestamp,
                    "value": dp.value,
                    "metadata": dp.metadata,
                }
                for dp in self.data_points
            ],
            "time_window_days": self.time_window_days,
            "prediction": self.prediction,
            "analyzed_at": self.analyzed_at,
            "details": self.details,
        }


@dataclass
class Risk:
    """
    Risk assessment result.

    Example:
        >>> risk = Risk(
        ...     risk_id="timeline-delay",
        ...     title="Timeline delay risk",
        ...     description="Project 2 weeks behind schedule",
        ...     severity=RiskSeverity.HIGH,
        ...     likelihood=RiskLikelihood.LIKELY,
        ...     impact_score=0.8,
        ...     mitigation_suggestions=["Add resources", "Reduce scope"]
        ... )
    """
    risk_id: str
    title: str
    description: str
    severity: RiskSeverity
    likelihood: RiskLikelihood
    impact_score: float  # 0.0 - 1.0
    category: str = "general"
    affected_areas: List[str] = field(default_factory=list)
    mitigation_suggestions: List[str] = field(default_factory=list)
    identified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def priority_score(self) -> float:
        """Calculate priority score (0.0 - 1.0) based on severity and likelihood."""
        severity_weights = {
            RiskSeverity.LOW: 0.25,
            RiskSeverity.MEDIUM: 0.50,
            RiskSeverity.HIGH: 0.75,
            RiskSeverity.CRITICAL: 1.0,
        }

        likelihood_weights = {
            RiskLikelihood.UNLIKELY: 0.25,
            RiskLikelihood.POSSIBLE: 0.50,
            RiskLikelihood.LIKELY: 0.75,
            RiskLikelihood.CERTAIN: 1.0,
        }

        severity_weight = severity_weights.get(self.severity, 0.5)
        likelihood_weight = likelihood_weights.get(self.likelihood, 0.5)

        # Priority = (severity * 0.6) + (likelihood * 0.4)
        return (severity_weight * 0.6) + (likelihood_weight * 0.4)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "risk_id": self.risk_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "likelihood": self.likelihood.value,
            "impact_score": self.impact_score,
            "priority_score": self.priority_score,
            "category": self.category,
            "affected_areas": self.affected_areas,
            "mitigation_suggestions": self.mitigation_suggestions,
            "identified_at": self.identified_at,
            "details": self.details,
        }


@dataclass
class TeamPerformanceMetrics:
    """Team performance metrics."""
    velocity: float  # Story points or tasks per sprint
    quality_score: float  # 0.0 - 1.0 (based on bug rate, code review, etc.)
    collaboration_score: float  # 0.0 - 1.0 (based on PR reviews, pair programming, etc.)
    throughput: float  # Tasks completed per time unit
    cycle_time: float  # Average time from start to done (hours/days)
    calculated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        from dataclasses import asdict
        return asdict(self)

"""
Health calculation configuration with default weights, thresholds, and categories.

Provides customizable configuration for health scoring algorithms.
"""

from typing import Any, Dict, List, Optional


class HealthConfig:
    """
    Configuration for health calculations.

    Default weights follow the specification:
    - Timeline: 30%
    - Activity: 25%
    - Blockers: 25%
    - Dependencies: 20%
    """

    # Default component weights (must sum to 1.0)
    DEFAULT_WEIGHTS = {
        "timeline": 0.30,    # Progress toward deadlines
        "activity": 0.25,    # Development activity level
        "blockers": 0.25,    # Impact of blockers
        "dependencies": 0.20,  # Health of dependencies
    }

    # Health score thresholds
    HEALTH_THRESHOLDS = {
        "excellent": 0.85,  # >= 0.85
        "good": 0.70,       # >= 0.70
        "fair": 0.50,       # >= 0.50
        "poor": 0.30,       # >= 0.30
        "critical": 0.0,    # < 0.30
    }

    # Timeline scoring thresholds
    TIMELINE_THRESHOLDS = {
        "ahead_of_schedule": 1.10,  # >10% ahead
        "on_track": 0.95,           # Within 5% of target
        "slightly_behind": 0.85,    # 5-15% behind
        "behind": 0.70,             # 15-30% behind
        "significantly_behind": 0.50,  # 30-50% behind
        "critical": 0.0,            # >50% behind
    }

    # Activity scoring thresholds (compared to baseline)
    ACTIVITY_THRESHOLDS = {
        "high": 1.5,        # 50% above baseline
        "normal": 0.8,      # Within 20% of baseline
        "low": 0.5,         # 20-50% below baseline
        "very_low": 0.0,    # >50% below baseline
    }

    # Blocker impact thresholds
    BLOCKER_THRESHOLDS = {
        "none": 0,
        "minor": 1,         # 1-2 blockers
        "moderate": 3,      # 3-5 blockers
        "significant": 6,   # 6-10 blockers
        "critical": 10,     # >10 blockers
    }

    # Risk severity weights
    RISK_SEVERITY_WEIGHTS = {
        "low": 0.25,
        "medium": 0.50,
        "high": 0.75,
        "critical": 1.0,
    }

    # Risk likelihood weights
    RISK_LIKELIHOOD_WEIGHTS = {
        "unlikely": 0.25,
        "possible": 0.50,
        "likely": 0.75,
        "certain": 1.0,
    }

    # Trend analysis settings
    TREND_SETTINGS = {
        "default_window_days": 30,
        "min_data_points": 3,
        "confidence_threshold": 0.7,
        "stable_threshold": 0.05,  # +/- 5% = stable
    }

    # Performance settings
    PERFORMANCE_SETTINGS = {
        "max_calculation_time_ms": 50,
        "cache_ttl_seconds": 300,  # 5 minutes
    }

    def __init__(self, custom_config: Optional[Dict[str, Any]] = None):
        """
        Initialize health configuration.

        Args:
            custom_config: Custom configuration to override defaults
        """
        self.config = {
            "weights": self.DEFAULT_WEIGHTS.copy(),
            "health_thresholds": self.HEALTH_THRESHOLDS.copy(),
            "timeline_thresholds": self.TIMELINE_THRESHOLDS.copy(),
            "activity_thresholds": self.ACTIVITY_THRESHOLDS.copy(),
            "blocker_thresholds": self.BLOCKER_THRESHOLDS.copy(),
            "risk_severity_weights": self.RISK_SEVERITY_WEIGHTS.copy(),
            "risk_likelihood_weights": self.RISK_LIKELIHOOD_WEIGHTS.copy(),
            "trend_settings": self.TREND_SETTINGS.copy(),
            "performance_settings": self.PERFORMANCE_SETTINGS.copy(),
        }

        if custom_config:
            self._merge_config(custom_config)

        # Validate weights sum to 1.0
        self._validate_weights()

    def _merge_config(self, custom_config: Dict[str, Any]) -> None:
        """Merge custom configuration with defaults."""
        for key, value in custom_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value

    def _validate_weights(self) -> None:
        """Validate that component weights sum to approximately 1.0."""
        weights = self.config["weights"]
        total = sum(weights.values())

        if abs(total - 1.0) > 0.01:  # Allow 1% tolerance
            raise ValueError(
                f"Component weights must sum to 1.0, got {total:.2f}. "
                f"Weights: {weights}"
            )

    def get_weight(self, component: str) -> float:
        """Get weight for a component."""
        return self.config["weights"].get(component, 0.0)

    def get_health_category(self, score: float) -> str:
        """Get health category for a score."""
        thresholds = self.config["health_thresholds"]

        if score >= thresholds["excellent"]:
            return "excellent"
        elif score >= thresholds["good"]:
            return "good"
        elif score >= thresholds["fair"]:
            return "fair"
        elif score >= thresholds["poor"]:
            return "poor"
        else:
            return "critical"

    def get_timeline_score(self, progress_ratio: float) -> float:
        """
        Calculate timeline score based on progress ratio.

        Args:
            progress_ratio: Actual progress / expected progress

        Returns:
            Score between 0.0 and 1.0
        """
        thresholds = self.config["timeline_thresholds"]

        if progress_ratio >= thresholds["ahead_of_schedule"]:
            return 1.0
        elif progress_ratio >= thresholds["on_track"]:
            return 0.9
        elif progress_ratio >= thresholds["slightly_behind"]:
            return 0.75
        elif progress_ratio >= thresholds["behind"]:
            return 0.6
        elif progress_ratio >= thresholds["significantly_behind"]:
            return 0.4
        else:
            return 0.2

    def get_activity_score(self, activity_ratio: float) -> float:
        """
        Calculate activity score based on activity ratio.

        Args:
            activity_ratio: Current activity / baseline activity

        Returns:
            Score between 0.0 and 1.0
        """
        thresholds = self.config["activity_thresholds"]

        if activity_ratio >= thresholds["high"]:
            return 1.0
        elif activity_ratio >= thresholds["normal"]:
            return 0.8
        elif activity_ratio >= thresholds["low"]:
            return 0.5
        else:
            return 0.2

    def get_blocker_score(self, blocker_count: int) -> float:
        """
        Calculate blocker score based on number of blockers.

        Args:
            blocker_count: Number of active blockers

        Returns:
            Score between 0.0 and 1.0 (inverse - fewer blockers = higher score)
        """
        thresholds = self.config["blocker_thresholds"]

        if blocker_count <= thresholds["none"]:
            return 1.0
        elif blocker_count <= thresholds["minor"]:
            return 0.85
        elif blocker_count <= thresholds["moderate"]:
            return 0.65
        elif blocker_count <= thresholds["significant"]:
            return 0.4
        else:
            return 0.15

    def get_dependency_score(self, dependency_scores: List[float]) -> float:
        """
        Calculate dependency score based on dependent project health.

        Args:
            dependency_scores: List of health scores from dependent projects

        Returns:
            Average score or 1.0 if no dependencies
        """
        if not dependency_scores:
            return 1.0

        return sum(dependency_scores) / len(dependency_scores)

    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary."""
        return self.config.copy()

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "HealthConfig":
        """Create configuration from dictionary."""
        return cls(custom_config=config_dict)

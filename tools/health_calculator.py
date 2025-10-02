"""
HealthCalculator - Algorithmic Scoring and Metrics Tool

Provides deterministic health scoring, metrics tracking, and trend analysis.

Simplifies command implementation from 80+ lines of math descriptions to 1-3 lines:

    calculator = HealthCalculator()
    health = calculator.calculate_project_health(project_data)
    # Returns: HealthScore(score=0.72, category="good", breakdown={...})
"""

import time
from datetime import datetime, timedelta
from statistics import mean, stdev
from typing import Any, Dict, List, Optional, Tuple

from tools.health_config import HealthConfig
from tools.health_models import (
    ComponentScore,
    HealthCategory,
    HealthScore,
    Risk,
    RiskLikelihood,
    RiskSeverity,
    TeamPerformanceMetrics,
    TrendAnalysis,
    TrendDataPoint,
    TrendDirection,
)


class HealthCalculatorError(Exception):
    """Base exception for HealthCalculator errors."""
    pass


class HealthCalculator:
    """
    Algorithmic health scoring and metrics calculator.

    Features:
    - Project health scoring (0.0-1.0 scale)
    - Component-based scoring with configurable weights
    - Team performance metrics
    - Trend analysis and prediction
    - Risk assessment and classification
    - Performance: <50ms for all calculations

    Example:
        >>> calc = HealthCalculator()
        >>> health = calc.calculate_project_health({
        ...     "milestones": [...],
        ...     "github_data": {...},
        ...     "blockers": [...],
        ...     "dependencies": [...]
        ... })
        >>> print(f"{health.category.value}: {health.score:.2f}")
        good: 0.72
    """

    def __init__(self, config: Optional[HealthConfig] = None):
        """
        Initialize HealthCalculator.

        Args:
            config: Custom health configuration (uses defaults if not provided)
        """
        self.config = config or HealthConfig()
        self._calculation_times = []  # Track performance

    def calculate_project_health(
        self,
        project_data: Dict[str, Any],
        weights: Optional[Dict[str, float]] = None,
    ) -> HealthScore:
        """
        Calculate overall project health score.

        Replaces 80+ lines of manual calculations with a single call.

        Args:
            project_data: Project data including milestones, github_data, blockers, etc.
            weights: Custom component weights (uses config defaults if not provided)

        Returns:
            HealthScore with overall score, category, and component breakdown

        Example:
            >>> health = calc.calculate_project_health(project_data)
            >>> print(f"Health: {health.score:.2f} ({health.category.value})")
            Health: 0.72 (good)
            >>> print(f"Timeline: {health.components['timeline'].score:.2f}")
            Timeline: 0.80
        """
        start_time = time.time()

        # Use custom weights or fall back to config
        component_weights = weights or self.config.config["weights"]

        # Calculate component scores
        components = {}

        # Timeline component (30%)
        timeline_score = self._calculate_timeline_score(project_data)
        components["timeline"] = ComponentScore(
            name="timeline",
            score=timeline_score,
            weight=component_weights["timeline"],
            weighted_score=timeline_score * component_weights["timeline"],
            details={"milestones": project_data.get("milestones", [])},
        )

        # Activity component (25%)
        activity_score = self._calculate_activity_score(project_data)
        components["activity"] = ComponentScore(
            name="activity",
            score=activity_score,
            weight=component_weights["activity"],
            weighted_score=activity_score * component_weights["activity"],
            details={"github_data": project_data.get("github_data", {})},
        )

        # Blockers component (25%)
        blocker_score = self._calculate_blocker_score(project_data)
        components["blockers"] = ComponentScore(
            name="blockers",
            score=blocker_score,
            weight=component_weights["blockers"],
            weighted_score=blocker_score * component_weights["blockers"],
            details={"blockers": project_data.get("blockers", [])},
        )

        # Dependencies component (20%)
        dependency_score = self._calculate_dependency_score(project_data)
        components["dependencies"] = ComponentScore(
            name="dependencies",
            score=dependency_score,
            weight=component_weights["dependencies"],
            weighted_score=dependency_score * component_weights["dependencies"],
            details={"dependencies": project_data.get("dependencies", [])},
        )

        # Calculate overall score
        overall_score = sum(comp.weighted_score for comp in components.values())

        # Track performance
        calculation_time = (time.time() - start_time) * 1000  # Convert to ms
        self._calculation_times.append(calculation_time)

        # Create health score
        health = HealthScore.from_score(overall_score, components)
        health.details["calculation_time_ms"] = calculation_time

        return health

    def calculate_timeline_progress(
        self,
        milestones: List[Dict[str, Any]],
        start_date: Optional[str] = None,
        target_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Calculate timeline progress metrics.

        Args:
            milestones: List of milestone dictionaries
            start_date: Project start date (ISO format)
            target_date: Project target completion date (ISO format)

        Returns:
            Dictionary with progress metrics
        """
        if not milestones:
            return {
                "progress_ratio": 0.0,
                "completed_count": 0,
                "total_count": 0,
                "percent_complete": 0.0,
                "on_track": False,
            }

        # Count completed vs total milestones
        completed = sum(1 for m in milestones if m.get("status") == "completed")
        total = len(milestones)
        percent_complete = (completed / total * 100) if total > 0 else 0

        # Calculate expected progress if dates provided
        progress_ratio = 1.0
        on_track = True

        if start_date and target_date:
            try:
                start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                target = datetime.fromisoformat(target_date.replace("Z", "+00:00"))
                now = datetime.now(start.tzinfo)

                total_duration = (target - start).days
                elapsed_duration = (now - start).days

                if total_duration > 0:
                    expected_progress = elapsed_duration / total_duration
                    actual_progress = completed / total if total > 0 else 0
                    progress_ratio = actual_progress / expected_progress if expected_progress > 0 else 1.0
                    on_track = progress_ratio >= 0.95  # Within 5% of target

            except (ValueError, AttributeError):
                pass  # Use default values if date parsing fails

        return {
            "progress_ratio": progress_ratio,
            "completed_count": completed,
            "total_count": total,
            "percent_complete": percent_complete,
            "on_track": on_track,
            "expected_completion": target_date,
        }

    def calculate_activity_score(
        self,
        github_data: Dict[str, Any],
        baseline: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Calculate activity score based on GitHub data.

        Args:
            github_data: GitHub activity data (commits, PRs, issues)
            baseline: Baseline activity metrics for comparison

        Returns:
            Activity score (0.0 - 1.0)
        """
        if not github_data:
            return 0.5  # Neutral score if no data

        # Extract activity metrics
        commits = len(github_data.get("commits", []))
        pull_requests = len(github_data.get("pull_requests", []))
        issues_closed = sum(
            1 for issue in github_data.get("issues", [])
            if issue.get("state") == "closed"
        )

        # Calculate activity score
        total_activity = commits + (pull_requests * 2) + issues_closed

        # Use baseline or default
        if baseline:
            baseline_activity = baseline.get("total_activity", 10)
            activity_ratio = total_activity / baseline_activity if baseline_activity > 0 else 1.0
        else:
            # Default baseline: >20 activities = high, 10 = normal, <5 = low
            activity_ratio = total_activity / 10 if total_activity < 20 else 2.0

        return self.config.get_activity_score(activity_ratio)

    def calculate_blocker_impact(self, blockers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate blocker impact metrics.

        Args:
            blockers: List of blocker items

        Returns:
            Dictionary with blocker impact metrics
        """
        if not blockers:
            return {
                "count": 0,
                "impact_score": 1.0,
                "severity_breakdown": {},
                "blocked_items": [],
            }

        # Count by severity
        severity_breakdown = {}
        for blocker in blockers:
            severity = blocker.get("severity", "medium")
            severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1

        # Calculate impact score
        blocker_count = len(blockers)
        impact_score = self.config.get_blocker_score(blocker_count)

        return {
            "count": blocker_count,
            "impact_score": impact_score,
            "severity_breakdown": severity_breakdown,
            "blocked_items": blockers,
        }

    def calculate_team_performance(
        self,
        team_data: Dict[str, Any],
        metrics: Optional[List[str]] = None,
    ) -> TeamPerformanceMetrics:
        """
        Calculate team performance metrics.

        Args:
            team_data: Team performance data
            metrics: Specific metrics to calculate (default: all)

        Returns:
            TeamPerformanceMetrics object
        """
        # Default metrics if not specified
        if metrics is None:
            metrics = ["velocity", "quality", "collaboration"]

        # Extract metrics
        velocity = team_data.get("velocity", 0.0)
        quality_score = team_data.get("quality_score", 0.8)
        collaboration_score = team_data.get("collaboration_score", 0.7)
        throughput = team_data.get("throughput", 0.0)
        cycle_time = team_data.get("cycle_time", 0.0)

        return TeamPerformanceMetrics(
            velocity=velocity,
            quality_score=quality_score,
            collaboration_score=collaboration_score,
            throughput=throughput,
            cycle_time=cycle_time,
            details=team_data,
        )

    def analyze_trends(
        self,
        historical_data: List[Dict[str, Any]],
        time_window: int = 30,
    ) -> TrendAnalysis:
        """
        Analyze trends in historical data.

        Args:
            historical_data: List of historical data points with timestamps and values
            time_window: Time window in days for analysis

        Returns:
            TrendAnalysis object with direction, slope, and predictions
        """
        if not historical_data or len(historical_data) < 2:
            return TrendAnalysis(
                direction=TrendDirection.STABLE,
                slope=0.0,
                confidence=0.0,
                data_points=[],
                time_window_days=time_window,
            )

        # Convert to data points
        data_points = []
        for item in historical_data:
            timestamp = item.get("timestamp") or item.get("date") or datetime.now().isoformat()
            value = item.get("value") or item.get("score", 0.0)
            data_points.append(
                TrendDataPoint(
                    timestamp=timestamp,
                    value=value,
                    metadata=item,
                )
            )

        # Sort by timestamp
        data_points.sort(key=lambda x: x.timestamp)

        # Calculate slope using linear regression
        values = [dp.value for dp in data_points]
        n = len(values)

        if n < 2:
            slope = 0.0
            confidence = 0.0
        else:
            # Simple linear regression
            x = list(range(n))
            mean_x = mean(x)
            mean_y = mean(values)

            numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
            denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

            slope = numerator / denominator if denominator != 0 else 0.0

            # Calculate confidence based on variance
            if n > 2:
                predictions = [mean_y + slope * (xi - mean_x) for xi in x]
                residuals = [values[i] - predictions[i] for i in range(n)]
                variance = sum(r ** 2 for r in residuals) / (n - 2)
                confidence = max(0.0, min(1.0, 1.0 - (variance / (stdev(values) ** 2 if stdev(values) > 0 else 1))))
            else:
                confidence = 0.5

        # Determine direction
        stable_threshold = self.config.config["trend_settings"]["stable_threshold"]
        if abs(slope) < stable_threshold:
            direction = TrendDirection.STABLE
        elif slope > 0:
            direction = TrendDirection.IMPROVING
        else:
            direction = TrendDirection.DECLINING

        # Predict next value
        prediction = values[-1] + slope if slope != 0 else values[-1]

        return TrendAnalysis(
            direction=direction,
            slope=slope,
            confidence=confidence,
            data_points=data_points,
            time_window_days=time_window,
            prediction=prediction,
        )

    def predict_completion(
        self,
        current_progress: float,
        velocity: float,
        remaining_work: float,
    ) -> Dict[str, Any]:
        """
        Predict project completion based on current progress and velocity.

        Args:
            current_progress: Current progress percentage (0.0 - 1.0)
            velocity: Current velocity (work units per time period)
            remaining_work: Remaining work units

        Returns:
            Dictionary with completion predictions
        """
        if velocity <= 0:
            return {
                "estimated_completion": None,
                "confidence": 0.0,
                "risk_level": "high",
                "message": "Insufficient velocity data",
            }

        # Calculate estimated time to completion
        estimated_days = remaining_work / velocity if velocity > 0 else 0
        estimated_completion = (datetime.now() + timedelta(days=estimated_days)).isoformat()

        # Calculate confidence based on progress consistency
        confidence = min(1.0, current_progress + 0.5) if current_progress > 0.2 else 0.3

        # Assess risk
        if estimated_days < 7:
            risk_level = "low"
        elif estimated_days < 30:
            risk_level = "medium"
        else:
            risk_level = "high"

        return {
            "estimated_completion": estimated_completion,
            "estimated_days": estimated_days,
            "confidence": confidence,
            "risk_level": risk_level,
            "current_velocity": velocity,
            "remaining_work": remaining_work,
        }

    def assess_risks(
        self,
        project_data: Dict[str, Any],
        thresholds: Optional[Dict[str, Any]] = None,
    ) -> List[Risk]:
        """
        Assess project risks based on data and thresholds.

        Args:
            project_data: Project data for risk assessment
            thresholds: Custom risk thresholds

        Returns:
            List of identified risks sorted by priority
        """
        risks = []

        # Timeline risks
        timeline_progress = self.calculate_timeline_progress(
            project_data.get("milestones", []),
            project_data.get("start_date"),
            project_data.get("target_date"),
        )

        if not timeline_progress["on_track"]:
            severity = RiskSeverity.HIGH if timeline_progress["progress_ratio"] < 0.7 else RiskSeverity.MEDIUM
            risks.append(
                Risk(
                    risk_id="timeline-delay",
                    title="Timeline delay risk",
                    description=f"Project is {(1 - timeline_progress['progress_ratio']) * 100:.0f}% behind schedule",
                    severity=severity,
                    likelihood=RiskLikelihood.LIKELY,
                    impact_score=0.8,
                    category="timeline",
                    affected_areas=["delivery", "milestones"],
                    mitigation_suggestions=[
                        "Review and adjust timeline",
                        "Allocate additional resources",
                        "Reduce scope or defer features",
                    ],
                )
            )

        # Blocker risks
        blockers = project_data.get("blockers", [])
        if len(blockers) > 3:
            risks.append(
                Risk(
                    risk_id="high-blocker-count",
                    title="High number of blockers",
                    description=f"{len(blockers)} active blockers impacting progress",
                    severity=RiskSeverity.HIGH if len(blockers) > 6 else RiskSeverity.MEDIUM,
                    likelihood=RiskLikelihood.CERTAIN,
                    impact_score=0.7,
                    category="blockers",
                    affected_areas=["velocity", "team_morale"],
                    mitigation_suggestions=[
                        "Prioritize blocker resolution",
                        "Escalate critical blockers",
                        "Assign dedicated resources to unblock",
                    ],
                )
            )

        # Activity risks
        github_data = project_data.get("github_data", {})
        if github_data:
            activity_score = self.calculate_activity_score(github_data)
            if activity_score < 0.5:
                risks.append(
                    Risk(
                        risk_id="low-activity",
                        title="Low development activity",
                        description="Development activity below expected baseline",
                        severity=RiskSeverity.MEDIUM,
                        likelihood=RiskLikelihood.LIKELY,
                        impact_score=0.6,
                        category="activity",
                        affected_areas=["velocity", "delivery"],
                        mitigation_suggestions=[
                            "Review team capacity and workload",
                            "Identify and remove impediments",
                            "Check for team availability issues",
                        ],
                    )
                )

        # Sort risks by priority score
        risks.sort(key=lambda r: r.priority_score, reverse=True)

        return risks

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for health calculations."""
        if not self._calculation_times:
            return {
                "average_time_ms": 0.0,
                "max_time_ms": 0.0,
                "min_time_ms": 0.0,
                "total_calculations": 0,
            }

        return {
            "average_time_ms": mean(self._calculation_times),
            "max_time_ms": max(self._calculation_times),
            "min_time_ms": min(self._calculation_times),
            "total_calculations": len(self._calculation_times),
        }

    # Private helper methods

    def _calculate_timeline_score(self, project_data: Dict[str, Any]) -> float:
        """Calculate timeline component score."""
        timeline_progress = self.calculate_timeline_progress(
            project_data.get("milestones", []),
            project_data.get("start_date"),
            project_data.get("target_date"),
        )
        return self.config.get_timeline_score(timeline_progress["progress_ratio"])

    def _calculate_activity_score(self, project_data: Dict[str, Any]) -> float:
        """Calculate activity component score."""
        github_data = project_data.get("github_data", {})
        baseline = project_data.get("baseline", None)
        return self.calculate_activity_score(github_data, baseline)

    def _calculate_blocker_score(self, project_data: Dict[str, Any]) -> float:
        """Calculate blocker component score."""
        blockers = project_data.get("blockers", [])
        impact = self.calculate_blocker_impact(blockers)
        return impact["impact_score"]

    def _calculate_dependency_score(self, project_data: Dict[str, Any]) -> float:
        """Calculate dependency component score."""
        dependencies = project_data.get("dependencies", [])
        dependency_scores = [
            dep.get("health_score", 0.8) for dep in dependencies if isinstance(dep, dict)
        ]
        return self.config.get_dependency_score(dependency_scores)

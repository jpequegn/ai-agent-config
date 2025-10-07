"""
ProjectReviewGenerator - Comprehensive Project Review Tool

Coordinates multi-source data collection, health calculation, trend analysis,
and formatted output generation for weekly and monthly project reviews.

Simplifies command implementation from 600+ lines to 15-20 lines:

    generator = ProjectReviewGenerator()
    review = generator.generate_review(period="weekly")
    print(review.formatted_output)
"""

import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal

from tools.config_manager import ConfigManager
from tools.data_collector import DataCollector
from tools.health_calculator import HealthCalculator
from tools.note_processor import NoteProcessor
from tools.output_formatter import OutputFormatter
from tools.data_models import ProjectData
from tools.health_models import HealthScore, Risk, TrendAnalysis
from tools.output_models import FormattedOutput


class ProjectReviewGeneratorError(Exception):
    """Base exception for ProjectReviewGenerator errors."""
    pass


class ProjectReview:
    """
    Container for project review data and metadata.

    Attributes:
        period: Review period ("weekly" or "monthly")
        start_date: Review period start date
        end_date: Review period end date
        projects: List of project IDs included in review
        portfolio_health: Overall portfolio health score
        project_statuses: Dictionary of project health statuses
        trends: Portfolio-wide trend analysis
        critical_decisions: List of decisions requiring attention
        recommendations: Strategic recommendations
        formatted_output: Formatted review content
        processing_time_ms: Total processing time
    """

    def __init__(
        self,
        period: str,
        start_date: datetime,
        end_date: datetime,
        projects: List[str],
        portfolio_health: float,
        project_statuses: Dict[str, Dict[str, Any]],
        trends: Optional[TrendAnalysis] = None,
        critical_decisions: Optional[List[Dict[str, Any]]] = None,
        recommendations: Optional[List[str]] = None,
        formatted_output: str = "",
        processing_time_ms: float = 0.0,
    ):
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.projects = projects
        self.portfolio_health = portfolio_health
        self.project_statuses = project_statuses
        self.trends = trends
        self.critical_decisions = critical_decisions or []
        self.recommendations = recommendations or []
        self.formatted_output = formatted_output
        self.processing_time_ms = processing_time_ms


class ProjectReviewGenerator:
    """
    Comprehensive project review analysis and reporting tool.

    Features:
    - Weekly and monthly portfolio reviews
    - Multi-project health tracking and trend analysis
    - Critical decision identification
    - Strategic recommendations
    - Stakeholder-ready communications
    - Velocity and performance analytics
    - Predictive insights using HealthCalculator

    Example:
        >>> generator = ProjectReviewGenerator()
        >>> # Weekly review for all active projects
        >>> review = generator.generate_review(period="weekly")
        >>> print(review.formatted_output)
        >>>
        >>> # Monthly strategic review
        >>> review = generator.generate_review(
        ...     period="monthly",
        ...     format="executive"
        ... )
        >>>
        >>> # Project-specific review
        >>> review = generator.generate_review(
        ...     period="weekly",
        ...     project_id="mobile-app-v2",
        ...     format="detailed"
        ... )
    """

    def __init__(self, config_root: Optional[Path] = None):
        """
        Initialize ProjectReviewGenerator.

        Args:
            config_root: Root directory for configuration files
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self.config_manager = ConfigManager(config_root=self.config_root)
        self.data_collector = DataCollector(config_root=self.config_root)
        self.health_calculator = HealthCalculator()
        self.note_processor = NoteProcessor(config_root=self.config_root)
        self.output_formatter = OutputFormatter()
        self._performance_stats = []

    def generate_review(
        self,
        period: Literal["weekly", "monthly"] = "weekly",
        project_id: Optional[str] = None,
        format: Literal["executive", "detailed", "email"] = "executive",
        output_format: str = "markdown",
    ) -> ProjectReview:
        """
        Generate comprehensive project review.

        Args:
            period: Review period ("weekly" or "monthly")
            project_id: Specific project ID (None for all active projects)
            format: Review format ("executive", "detailed", "email")
            output_format: Output format ("markdown" or "json")

        Returns:
            ProjectReview object with all analysis and formatted output

        Raises:
            ProjectReviewGeneratorError: If data collection or analysis fails

        Example:
            >>> review = generator.generate_review(
            ...     period="weekly",
            ...     format="executive"
            ... )
            >>> print(review.formatted_output)
        """
        start_time = time.time()

        try:
            # Step 1: Determine review period dates
            start_date, end_date = self._calculate_period_dates(period)

            # Step 2: Get projects for review
            projects = self._get_review_projects(project_id)

            # Step 3: Collect and analyze project data
            project_statuses = self._analyze_projects(projects, start_date, end_date)

            # Step 4: Calculate portfolio-wide metrics
            portfolio_health = self._calculate_portfolio_health(project_statuses)

            # Step 5: Analyze portfolio trends
            trends = self._analyze_portfolio_trends(project_statuses, period)

            # Step 6: Identify critical decisions
            critical_decisions = self._identify_critical_decisions(project_statuses)

            # Step 7: Generate recommendations
            recommendations = self._generate_recommendations(
                project_statuses, trends, critical_decisions
            )

            # Step 8: Format output
            formatted_output = self._format_review_output(
                period=period,
                start_date=start_date,
                end_date=end_date,
                projects=projects,
                project_statuses=project_statuses,
                portfolio_health=portfolio_health,
                trends=trends,
                critical_decisions=critical_decisions,
                recommendations=recommendations,
                format=format,
                output_format=output_format,
            )

            processing_time = (time.time() - start_time) * 1000

            # Track performance
            self._performance_stats.append({
                "operation": "generate_review",
                "period": period,
                "project_count": len(projects),
                "processing_time_ms": processing_time,
                "timestamp": datetime.now().isoformat(),
            })

            return ProjectReview(
                period=period,
                start_date=start_date,
                end_date=end_date,
                projects=projects,
                portfolio_health=portfolio_health,
                project_statuses=project_statuses,
                trends=trends,
                critical_decisions=critical_decisions,
                recommendations=recommendations,
                formatted_output=formatted_output,
                processing_time_ms=processing_time,
            )

        except Exception as e:
            raise ProjectReviewGeneratorError(
                f"Failed to generate {period} review: {str(e)}"
            ) from e

    def analyze_velocity_trends(
        self,
        project_data: Dict[str, Any],
        period: str
    ) -> Dict[str, Any]:
        """
        Analyze velocity patterns and trends for projects.

        Args:
            project_data: Project data dictionary
            period: Time period for analysis

        Returns:
            Dictionary with velocity analysis results
        """
        time_window = 30 if period == "weekly" else 90

        velocity_data = []
        for project_id, status in project_data.items():
            if "health_score" in status and hasattr(status["health_score"], "components"):
                activity_score = status["health_score"].components.get("activity", 0.0)
                velocity_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "value": activity_score,
                    "project": project_id,
                })

        if velocity_data:
            trends = self.health_calculator.analyze_trends(
                velocity_data,
                time_window=time_window
            )
            return {
                "trend_direction": trends.direction.value,
                "slope": trends.slope,
                "confidence": trends.confidence,
                "prediction": trends.predicted_value,
            }

        return {
            "trend_direction": "stable",
            "slope": 0.0,
            "confidence": 0.0,
            "prediction": 0.0,
        }

    def generate_predictive_insights(
        self,
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate predictive insights based on historical patterns.

        Args:
            project_data: Project data dictionary

        Returns:
            Dictionary with predictive insights
        """
        insights = {
            "completion_predictions": [],
            "risk_forecasts": [],
            "resource_demands": [],
        }

        for project_id, status in project_data.items():
            if "health_score" not in status:
                continue

            health = status["health_score"]

            # Predict completion
            if status.get("progress") and status.get("velocity"):
                remaining_work = status.get("remaining_milestones", 0)
                prediction = self.health_calculator.predict_completion(
                    current_progress=status["progress"],
                    velocity=status["velocity"],
                    remaining_work=remaining_work,
                )
                insights["completion_predictions"].append({
                    "project": project_id,
                    "eta": prediction.eta.isoformat() if prediction.eta else None,
                    "confidence": prediction.confidence,
                    "risk_level": prediction.risk_level.value,
                })

            # Assess risks
            if "project_data" in status:
                risks = self.health_calculator.assess_risks(status["project_data"])
                high_risks = [r for r in risks if r.severity.value in ["high", "critical"]]
                if high_risks:
                    insights["risk_forecasts"].append({
                        "project": project_id,
                        "high_risk_count": len(high_risks),
                        "risks": [{"title": r.title, "severity": r.severity.value} for r in high_risks],
                    })

        return insights

    def _calculate_period_dates(self, period: str) -> tuple[datetime, datetime]:
        """Calculate start and end dates for review period."""
        now = datetime.now()

        if period == "weekly":
            # Current week (Monday to Sunday)
            start_date = now - timedelta(days=now.weekday())
            end_date = start_date + timedelta(days=6)
        else:  # monthly
            # Current month
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                end_date = start_date.replace(year=now.year + 1, month=1) - timedelta(days=1)
            else:
                end_date = start_date.replace(month=now.month + 1) - timedelta(days=1)

        return start_date, end_date

    def _get_review_projects(self, project_id: Optional[str]) -> List[str]:
        """Get list of projects to include in review."""
        if project_id:
            return [project_id]

        # Get all active projects
        return self.config_manager.get_all_projects(
            filters={"status": ["active", "in_progress", "planning"]}
        )

    def _analyze_projects(
        self,
        projects: List[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze all projects for the review period."""
        statuses = {}

        for project_id in projects:
            try:
                # Collect project data
                project_data = self.data_collector.aggregate_project_data(
                    project_id=project_id,
                    sources=["github", "notes", "calendar", "team", "config"]
                )

                # Calculate health score
                health_score = self.health_calculator.calculate_project_health(project_data)

                # Analyze trends
                trends = self.health_calculator.analyze_trends(
                    historical_data=project_data.history if hasattr(project_data, 'history') else [],
                    time_window=30
                )

                # Calculate team performance
                team_metrics = None
                if hasattr(project_data, 'team_data') and project_data.team_data:
                    team_metrics = self.health_calculator.calculate_team_performance(
                        project_data.team_data
                    )

                # Predict completion
                prediction = None
                if hasattr(project_data, 'milestones'):
                    timeline_progress = self.health_calculator.calculate_timeline_progress(
                        project_data.milestones,
                        getattr(project_data, 'start_date', None),
                        getattr(project_data, 'target_date', None)
                    )
                    if timeline_progress["total_count"] > 0:
                        prediction = self.health_calculator.predict_completion(
                            current_progress=timeline_progress["percent_complete"] / 100,
                            velocity=getattr(project_data, 'velocity', 1.0),
                            remaining_work=timeline_progress["total_count"] - timeline_progress["completed_count"]
                        )

                # Assess risks
                risks = self.health_calculator.assess_risks(project_data)

                statuses[project_id] = {
                    "project_data": project_data,
                    "health_score": health_score,
                    "trends": trends,
                    "team_metrics": team_metrics,
                    "prediction": prediction,
                    "risks": risks,
                    "progress": timeline_progress["percent_complete"] / 100 if 'timeline_progress' in locals() else 0.0,
                    "velocity": getattr(project_data, 'velocity', 1.0),
                    "remaining_milestones": timeline_progress["total_count"] - timeline_progress["completed_count"] if 'timeline_progress' in locals() else 0,
                }

            except Exception as e:
                print(f"Warning: Failed to analyze project {project_id}: {e}")
                # Include minimal status for failed projects
                statuses[project_id] = {
                    "error": str(e),
                    "health_score": None,
                }

        return statuses

    def _calculate_portfolio_health(
        self,
        project_statuses: Dict[str, Dict[str, Any]]
    ) -> float:
        """Calculate overall portfolio health score."""
        valid_scores = [
            status["health_score"].score
            for status in project_statuses.values()
            if status.get("health_score")
        ]

        if not valid_scores:
            return 0.0

        return sum(valid_scores) / len(valid_scores)

    def _analyze_portfolio_trends(
        self,
        project_statuses: Dict[str, Dict[str, Any]],
        period: str
    ) -> Optional[TrendAnalysis]:
        """Analyze portfolio-wide trends."""
        time_window = 30 if period == "weekly" else 90

        # Aggregate health scores across all projects
        portfolio_data = []
        for project_id, status in project_statuses.items():
            if status.get("health_score"):
                portfolio_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "value": status["health_score"].score,
                    "project": project_id,
                })

        if portfolio_data:
            return self.health_calculator.analyze_trends(
                portfolio_data,
                time_window=time_window
            )

        return None

    def _identify_critical_decisions(
        self,
        project_statuses: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify projects requiring critical decisions."""
        decisions = []

        for project_id, status in project_statuses.items():
            if not status.get("health_score"):
                continue

            health = status["health_score"]
            risks = status.get("risks", [])

            # Check for critical risks
            critical_risks = [r for r in risks if r.severity.value == "critical"]
            high_risks = [r for r in risks if r.severity.value == "high"]

            # Declining health
            if status.get("trends") and status["trends"].direction.value == "declining":
                decisions.append({
                    "project": project_id,
                    "priority": "high",
                    "issue": "Declining health trend",
                    "health_score": health.score,
                    "recommendation": f"Investigate causes of {abs(status['trends'].slope):.2%} weekly decline",
                })

            # Critical or multiple high risks
            if critical_risks or len(high_risks) > 2:
                decisions.append({
                    "project": project_id,
                    "priority": "critical" if critical_risks else "high",
                    "issue": f"{len(critical_risks)} critical, {len(high_risks)} high risks identified",
                    "risks": [r.title for r in (critical_risks + high_risks)[:3]],
                    "recommendation": "Immediate risk mitigation required",
                })

            # Poor prediction
            if status.get("prediction") and status["prediction"].risk_level.value in ["high", "critical"]:
                decisions.append({
                    "project": project_id,
                    "priority": "medium",
                    "issue": f"Completion at risk: {status['prediction'].confidence:.0%} confidence",
                    "eta": status["prediction"].eta.isoformat() if status["prediction"].eta else "Unknown",
                    "recommendation": "Consider timeline adjustment or resource allocation",
                })

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        decisions.sort(key=lambda d: priority_order.get(d.get("priority", "low"), 3))

        return decisions

    def _generate_recommendations(
        self,
        project_statuses: Dict[str, Dict[str, Any]],
        trends: Optional[TrendAnalysis],
        critical_decisions: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate strategic recommendations based on analysis."""
        recommendations = []

        # Immediate actions based on critical decisions
        if critical_decisions:
            critical_count = sum(1 for d in critical_decisions if d.get("priority") == "critical")
            if critical_count > 0:
                recommendations.append(
                    f"🔴 IMMEDIATE: Address {critical_count} critical decision(s) this week"
                )

        # Portfolio trend recommendations
        if trends:
            if trends.direction.value == "improving":
                recommendations.append(
                    f"🟢 Portfolio health improving ({trends.slope:.2%}/week) - maintain current practices"
                )
            elif trends.direction.value == "declining":
                recommendations.append(
                    f"🟡 Portfolio health declining ({abs(trends.slope):.2%}/week) - review resource allocation"
                )

        # Team performance recommendations
        high_performers = []
        struggling_teams = []
        for project_id, status in project_statuses.items():
            if status.get("team_metrics"):
                metrics = status["team_metrics"]
                if metrics.velocity_score > 1.2:
                    high_performers.append(project_id)
                elif metrics.velocity_score < 0.7:
                    struggling_teams.append(project_id)

        if high_performers:
            recommendations.append(
                f"🟢 Replicate success patterns from {', '.join(high_performers[:2])}"
            )

        if struggling_teams:
            recommendations.append(
                f"🟡 Provide support to {', '.join(struggling_teams[:2])}"
            )

        return recommendations

    def _format_review_output(
        self,
        period: str,
        start_date: datetime,
        end_date: datetime,
        projects: List[str],
        project_statuses: Dict[str, Dict[str, Any]],
        portfolio_health: float,
        trends: Optional[TrendAnalysis],
        critical_decisions: List[Dict[str, Any]],
        recommendations: List[str],
        format: str,
        output_format: str,
    ) -> str:
        """Format review output using OutputFormatter."""
        # Prepare data for template
        template_data = {
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "projects": projects,
            "project_statuses": project_statuses,
            "portfolio_health": portfolio_health,
            "trends": trends,
            "critical_decisions": critical_decisions,
            "recommendations": recommendations,
            "active_count": len(projects),
            "milestone_count": sum(
                status.get("project_data", {}).get("milestone_count", 0)
                for status in project_statuses.values()
            ),
        }

        if output_format == "json":
            result = self.output_formatter.format_json(template_data, pretty=True)
            return result.content

        # Determine template based on format and period
        template_name = f"project_review_{period}_{format}"

        try:
            result = self.output_formatter.format_markdown(
                data=template_data,
                template=template_name,
                context={"format": format, "period": period}
            )
            return result.content
        except Exception:
            # Fallback to basic formatting if template not found
            return self._format_basic_output(template_data)

    def _format_basic_output(self, data: Dict[str, Any]) -> str:
        """Basic fallback formatting when templates are unavailable."""
        period = data["period"].title()
        start = data["start_date"].strftime("%Y-%m-%d")
        end = data["end_date"].strftime("%Y-%m-%d")

        output = [
            f"# 📊 {period} Project Review",
            f"**Review Period:** {start} to {end}",
            f"**Active Projects:** {data['active_count']}",
            f"**Portfolio Health:** {data['portfolio_health']:.2f}/1.0",
            "",
            "## 🎯 Critical Decisions",
        ]

        if data["critical_decisions"]:
            for decision in data["critical_decisions"]:
                output.append(f"- **{decision['project']}** ({decision['priority']}): {decision['issue']}")
        else:
            output.append("No critical decisions identified.")

        output.append("")
        output.append("## 💡 Recommendations")

        if data["recommendations"]:
            for rec in data["recommendations"]:
                output.append(f"- {rec}")
        else:
            output.append("No specific recommendations at this time.")

        return "\n".join(output)

    def get_performance_stats(self) -> List[Dict[str, Any]]:
        """
        Get performance statistics for recent operations.

        Returns:
            List of performance stat dictionaries
        """
        return self._performance_stats.copy()

    def clear_cache(self) -> None:
        """Clear all cached data in underlying tools."""
        self.data_collector.clear_cache()
        self.output_formatter.clear_cache()

"""
Test suite for ProjectReviewGenerator tool.
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from tools.project_review_generator import (
    ProjectReviewGenerator,
    ProjectReviewGeneratorError,
    ProjectReview,
)
from tools.health_models import (
    HealthScore,
    HealthCategory,
    ComponentScore,
    TrendAnalysis,
    TrendDirection,
    RiskSeverity,
    RiskLikelihood,
    Risk,
    TeamPerformanceMetrics,
)
from tools.data_models import ProjectData


class TestProjectReviewGenerator:
    """Test suite for ProjectReviewGenerator."""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create ProjectReviewGenerator instance with mocked dependencies."""
        with patch("tools.project_review_generator.ConfigManager"), \
             patch("tools.project_review_generator.DataCollector"), \
             patch("tools.project_review_generator.HealthCalculator"), \
             patch("tools.project_review_generator.NoteProcessor"), \
             patch("tools.project_review_generator.OutputFormatter"):
            return ProjectReviewGenerator(config_root=tmp_path / ".claude")

    @pytest.fixture
    def mock_project_data(self):
        """Create mock project data."""
        return {
            "project-1": {
                "health_score": HealthScore(
                    score=0.85,
                    category=HealthCategory.EXCELLENT,
                    components={
                        "timeline": 0.90,
                        "activity": 0.85,
                        "blockers": 1.0,
                        "dependencies": 0.75,
                    },
                ),
                "trends": TrendAnalysis(
                    direction=TrendDirection.IMPROVING,
                    slope=0.05,
                    confidence=0.92,
                    data_points=[],
                ),
                "project_data": Mock(spec=ProjectData),
                "risks": [],
                "progress": 0.75,
                "velocity": 1.15,
                "remaining_milestones": 5,
            },
            "project-2": {
                "health_score": HealthScore(
                    score=0.45,
                    category=HealthCategory.POOR,
                    components={
                        "timeline": 0.50,
                        "activity": 0.40,
                        "blockers": 0.30,
                        "dependencies": 0.60,
                    },
                ),
                "trends": TrendAnalysis(
                    direction=TrendDirection.DECLINING,
                    slope=-0.08,
                    confidence=0.78,
                    data_points=[],
                ),
                "project_data": Mock(spec=ProjectData),
                "risks": [
                    Risk(
                        risk_id="blocker-1",
                        title="Critical blocker",
                        description="Blocking deployment",
                        severity=RiskSeverity.CRITICAL,
                        likelihood=RiskLikelihood.LIKELY,
                        impact_score=0.9,
                        mitigation_suggestions=["Immediate intervention"],
                    )
                ],
                "progress": 0.25,
                "velocity": 0.65,
                "remaining_milestones": 15,
            },
        }

    def test_initialization(self, generator):
        """Test ProjectReviewGenerator initialization."""
        assert generator.config_manager is not None
        assert generator.data_collector is not None
        assert generator.health_calculator is not None
        assert generator.note_processor is not None
        assert generator.output_formatter is not None
        assert generator._performance_stats == []

    def test_calculate_period_dates_weekly(self, generator):
        """Test weekly period date calculation."""
        start_date, end_date = generator._calculate_period_dates("weekly")

        # Should be current week (Monday to Sunday)
        assert start_date.weekday() == 0  # Monday
        assert (end_date - start_date).days == 6
        assert end_date.weekday() == 6  # Sunday

    def test_calculate_period_dates_monthly(self, generator):
        """Test monthly period date calculation."""
        start_date, end_date = generator._calculate_period_dates("monthly")

        # Should be current month (1st to last day)
        assert start_date.day == 1
        assert end_date.month == start_date.month or end_date.month == start_date.month + 1

    def test_calculate_portfolio_health(self, generator, mock_project_data):
        """Test portfolio health calculation."""
        portfolio_health = generator._calculate_portfolio_health(mock_project_data)

        # Should be average of project health scores
        expected = (0.85 + 0.45) / 2
        assert portfolio_health == expected

    def test_calculate_portfolio_health_empty(self, generator):
        """Test portfolio health with no valid scores."""
        portfolio_health = generator._calculate_portfolio_health({})
        assert portfolio_health == 0.0

    def test_identify_critical_decisions(self, generator, mock_project_data):
        """Test critical decision identification."""
        decisions = generator._identify_critical_decisions(mock_project_data)

        # Should identify declining health and critical risks
        assert len(decisions) > 0

        # Check for declining health decision
        declining_decisions = [d for d in decisions if "Declining health" in d.get("issue", "")]
        assert len(declining_decisions) > 0

        # Check for critical risk decision
        risk_decisions = [d for d in decisions if "critical" in d.get("issue", "").lower()]
        assert len(risk_decisions) > 0

        # Check priority sorting
        priorities = [d.get("priority") for d in decisions]
        assert priorities[0] in ["critical", "high"]  # Highest priority first

    def test_generate_recommendations(self, generator, mock_project_data):
        """Test recommendation generation."""
        trends = TrendAnalysis(
            direction=TrendDirection.DECLINING,
            slope=-0.05,
            confidence=0.85,
            data_points=[],
        )
        critical_decisions = [
            {"priority": "critical", "project": "project-2", "issue": "Critical issue"}
        ]

        recommendations = generator._generate_recommendations(
            mock_project_data, trends, critical_decisions
        )

        # Should generate recommendations
        assert len(recommendations) > 0

        # Should include immediate action for critical decisions
        immediate_recs = [r for r in recommendations if "IMMEDIATE" in r or "critical" in r.lower()]
        assert len(immediate_recs) > 0

        # Should include portfolio trend recommendation
        trend_recs = [r for r in recommendations if "declining" in r.lower()]
        assert len(trend_recs) > 0

    def test_analyze_velocity_trends(self, generator, mock_project_data):
        """Test velocity trend analysis."""
        velocity_analysis = generator.analyze_velocity_trends(
            mock_project_data,
            period="weekly"
        )

        assert "trend_direction" in velocity_analysis
        assert "slope" in velocity_analysis
        assert "confidence" in velocity_analysis
        assert "prediction" in velocity_analysis

    def test_analyze_velocity_trends_empty(self, generator):
        """Test velocity analysis with no data."""
        velocity_analysis = generator.analyze_velocity_trends({}, period="weekly")

        assert velocity_analysis["trend_direction"] == "stable"
        assert velocity_analysis["slope"] == 0.0
        assert velocity_analysis["confidence"] == 0.0

    @patch("tools.project_review_generator.ProjectReviewGenerator._analyze_projects")
    @patch("tools.project_review_generator.ProjectReviewGenerator._get_review_projects")
    def test_generate_review_weekly(
        self, mock_get_projects, mock_analyze_projects, generator, mock_project_data
    ):
        """Test weekly review generation."""
        # Setup mocks
        mock_get_projects.return_value = ["project-1", "project-2"]
        mock_analyze_projects.return_value = mock_project_data

        # Generate review
        review = generator.generate_review(period="weekly", format="executive")

        # Verify review structure
        assert isinstance(review, ProjectReview)
        assert review.period == "weekly"
        assert len(review.projects) == 2
        assert review.portfolio_health > 0
        assert review.formatted_output != ""

        # Verify calls
        mock_get_projects.assert_called_once()
        mock_analyze_projects.assert_called_once()

    @patch("tools.project_review_generator.ProjectReviewGenerator._analyze_projects")
    @patch("tools.project_review_generator.ProjectReviewGenerator._get_review_projects")
    def test_generate_review_monthly(
        self, mock_get_projects, mock_analyze_projects, generator, mock_project_data
    ):
        """Test monthly review generation."""
        # Setup mocks
        mock_get_projects.return_value = ["project-1", "project-2"]
        mock_analyze_projects.return_value = mock_project_data

        # Generate review
        review = generator.generate_review(period="monthly", format="executive")

        # Verify review structure
        assert isinstance(review, ProjectReview)
        assert review.period == "monthly"
        assert review.formatted_output != ""

    @patch("tools.project_review_generator.ProjectReviewGenerator._analyze_projects")
    @patch("tools.project_review_generator.ProjectReviewGenerator._get_review_projects")
    def test_generate_review_project_specific(
        self, mock_get_projects, mock_analyze_projects, generator, mock_project_data
    ):
        """Test project-specific review generation."""
        # Setup mocks
        mock_get_projects.return_value = ["project-1"]
        mock_analyze_projects.return_value = {"project-1": mock_project_data["project-1"]}

        # Generate review
        review = generator.generate_review(
            period="weekly", project_id="project-1", format="detailed"
        )

        # Verify review
        assert len(review.projects) == 1
        assert "project-1" in review.projects

        # Verify mock was called with project_id
        mock_get_projects.assert_called_once_with("project-1")

    def test_format_basic_output(self, generator):
        """Test basic fallback output formatting."""
        data = {
            "period": "weekly",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=7),
            "active_count": 2,
            "portfolio_health": 0.75,
            "critical_decisions": [
                {"project": "test-project", "priority": "high", "issue": "Test issue"}
            ],
            "recommendations": ["Test recommendation"],
        }

        output = generator._format_basic_output(data)

        # Verify output structure
        assert "Weekly Project Review" in output
        assert "Portfolio Health:" in output
        assert "0.75" in output
        assert "Critical Decisions" in output
        assert "test-project" in output
        assert "Recommendations" in output
        assert "Test recommendation" in output

    def test_performance_stats_tracking(self, generator):
        """Test performance statistics tracking."""
        # Add mock stats
        generator._performance_stats.append({
            "operation": "generate_review",
            "period": "weekly",
            "processing_time_ms": 150.5,
            "timestamp": datetime.now().isoformat(),
        })

        stats = generator.get_performance_stats()

        assert len(stats) == 1
        assert stats[0]["operation"] == "generate_review"
        assert stats[0]["processing_time_ms"] == 150.5

    @patch("tools.project_review_generator.DataCollector")
    @patch("tools.project_review_generator.OutputFormatter")
    def test_clear_cache(self, mock_formatter, mock_collector, generator):
        """Test cache clearing."""
        # Setup mocks
        generator.data_collector = mock_collector.return_value
        generator.output_formatter = mock_formatter.return_value

        # Clear cache
        generator.clear_cache()

        # Verify calls
        generator.data_collector.clear_cache.assert_called_once()
        generator.output_formatter.clear_cache.assert_called_once()

    def test_generate_predictive_insights(self, generator, mock_project_data):
        """Test predictive insights generation."""
        insights = generator.generate_predictive_insights(mock_project_data)

        assert "completion_predictions" in insights
        assert "risk_forecasts" in insights
        assert "resource_demands" in insights

        # Should have predictions for projects with progress/velocity
        assert len(insights["completion_predictions"]) > 0

        # Should identify high risks
        assert len(insights["risk_forecasts"]) > 0

    @patch("tools.project_review_generator.ProjectReviewGenerator._analyze_projects")
    def test_error_handling(self, mock_analyze_projects, generator):
        """Test error handling in review generation."""
        # Force an error
        mock_analyze_projects.side_effect = Exception("Test error")

        # Should raise ProjectReviewGeneratorError
        with pytest.raises(ProjectReviewGeneratorError) as exc_info:
            generator.generate_review(period="weekly")

        assert "Failed to generate weekly review" in str(exc_info.value)
        assert "Test error" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

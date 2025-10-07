"""
Tests for TeamManager tool.

Tests 1:1 preparation, performance analysis, feedback generation, and output formatting.
"""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from tools.team_manager import (
    TeamManager,
    TeamManagerError,
    TeamMember,
    OneOnOneMeeting,
    PerformanceAnalysis,
    FeedbackReport,
)


@pytest.fixture
def manager():
    """Create TeamManager instance with mocked dependencies."""
    with patch('tools.team_manager.ConfigManager'), \
         patch('tools.team_manager.DataCollector'), \
         patch('tools.team_manager.HealthCalculator'), \
         patch('tools.team_manager.OutputFormatter'):
        manager = TeamManager()

        # Mock team data - note: uses .members not .team_members
        manager.data_collector.collect_team_data.return_value = MagicMock(
            members=[
                {
                    "name": "Alice Johnson",
                    "email": "alice@example.com",
                    "role": "Senior Engineer",
                    "join_date": "2023-01-15",
                    "skills": ["Python", "React", "AWS"],
                    "projects": ["mobile-app-v2", "api-gateway"],
                    "performance_rating": 4.5
                },
                {
                    "name": "Bob Smith",
                    "email": "bob@example.com",
                    "role": "Product Manager",
                    "join_date": "2022-06-01",
                    "skills": ["Product Strategy", "Agile", "Analytics"],
                    "projects": ["mobile-app-v2"],
                    "performance_rating": 4.2
                }
            ],
            performance_metrics={
                "alice@example.com": {
                    "task_completion_rate": 0.92,
                    "code_quality_score": 0.88,
                    "collaboration_score": 0.95
                }
            }
        )

        # Mock output formatter
        manager.output_formatter.format_markdown.return_value = MagicMock(
            content="# Formatted Output\nTest content"
        )

        return manager


@pytest.fixture
def sample_team_member():
    """Sample team member for testing."""
    return TeamMember(
        name="Alice Johnson",
        email="alice@example.com",
        role="Senior Engineer",
        join_date=datetime(2023, 1, 15),
        skills=["Python", "React", "AWS"],
        projects=["mobile-app-v2", "api-gateway"],
        performance_rating=4.5
    )


class TestTeamMember:
    """Test TeamMember dataclass."""

    def test_team_member_creation(self):
        """Test creating team member."""
        member = TeamMember(
            name="Alice Johnson",
            email="alice@example.com",
            role="Senior Engineer"
        )

        assert member.name == "Alice Johnson"
        assert member.email == "alice@example.com"
        assert member.role == "Senior Engineer"

    def test_team_member_defaults(self):
        """Test team member default values."""
        member = TeamMember(
            name="Test User",
            email="test@example.com"
        )

        assert member.role == ""
        assert member.join_date is None
        assert member.skills == []
        assert member.projects == []
        assert member.performance_rating == 0.0

    def test_team_member_with_all_fields(self):
        """Test team member with all fields populated."""
        join_date = datetime(2023, 1, 15)
        member = TeamMember(
            name="Alice Johnson",
            email="alice@example.com",
            role="Senior Engineer",
            join_date=join_date,
            skills=["Python", "React"],
            projects=["mobile-app-v2"],
            performance_rating=4.5
        )

        assert member.join_date == join_date
        assert len(member.skills) == 2
        assert len(member.projects) == 1
        assert member.performance_rating == 4.5


class TestOneOnOneMeeting:
    """Test OneOnOneMeeting dataclass."""

    def test_meeting_creation(self, sample_team_member):
        """Test creating 1:1 meeting."""
        meeting = OneOnOneMeeting(
            team_member=sample_team_member,
            date=datetime.now()
        )

        assert meeting.team_member == sample_team_member
        assert isinstance(meeting.date, datetime)

    def test_meeting_defaults(self, sample_team_member):
        """Test meeting default values."""
        meeting = OneOnOneMeeting(
            team_member=sample_team_member,
            date=datetime.now()
        )

        assert meeting.agenda == []
        assert meeting.accomplishments == []
        assert meeting.goals == []
        assert meeting.challenges == []
        assert meeting.career_development == {}
        assert meeting.action_items == []
        assert meeting.formatted_output == ""

    def test_meeting_with_full_data(self, sample_team_member):
        """Test meeting with comprehensive data."""
        meeting = OneOnOneMeeting(
            team_member=sample_team_member,
            date=datetime.now(),
            agenda=["Project status", "Career development"],
            accomplishments=["Completed API migration"],
            goals=[{"title": "Learn Kubernetes", "progress": 0.5}],
            challenges=[{"title": "Database performance", "severity": "medium"}],
            career_development={"skills": ["Kubernetes", "GraphQL"]},
            action_items=[{"action": "Schedule training", "owner": "Alice"}]
        )

        assert len(meeting.agenda) == 2
        assert len(meeting.accomplishments) == 1
        assert len(meeting.goals) == 1
        assert len(meeting.challenges) == 1
        assert "skills" in meeting.career_development
        assert len(meeting.action_items) == 1


class TestPerformanceAnalysis:
    """Test PerformanceAnalysis dataclass."""

    def test_analysis_creation(self, sample_team_member):
        """Test creating performance analysis."""
        analysis = PerformanceAnalysis(
            team_member=sample_team_member,
            period="Q4 2024",
            overall_score=4.5
        )

        assert analysis.team_member == sample_team_member
        assert analysis.period == "Q4 2024"
        assert analysis.overall_score == 4.5

    def test_analysis_defaults(self):
        """Test analysis default values."""
        analysis = PerformanceAnalysis(
            team_member=None,
            period="Q4 2024",
            overall_score=0.0
        )

        assert analysis.strengths == []
        assert analysis.areas_for_improvement == []
        assert analysis.metrics == {}
        assert analysis.trends == {}
        assert analysis.recommendations == []
        assert analysis.formatted_output == ""

    def test_team_wide_analysis(self):
        """Test team-wide analysis (no specific member)."""
        analysis = PerformanceAnalysis(
            team_member=None,
            period="Q4 2024",
            overall_score=4.2,
            strengths=["Strong collaboration", "High quality"],
            areas_for_improvement=["Documentation", "Testing"],
            metrics={"velocity": 42.5, "quality_score": 0.88}
        )

        assert analysis.team_member is None
        assert len(analysis.strengths) == 2
        assert len(analysis.areas_for_improvement) == 2
        assert analysis.metrics["velocity"] == 42.5


class TestFeedbackReport:
    """Test FeedbackReport dataclass."""

    def test_feedback_creation(self, sample_team_member):
        """Test creating feedback report."""
        report = FeedbackReport(
            team_member=sample_team_member,
            period="Q4 2024",
            rating=4.5
        )

        assert report.team_member == sample_team_member
        assert report.period == "Q4 2024"
        assert report.rating == 4.5

    def test_feedback_defaults(self, sample_team_member):
        """Test feedback default values."""
        report = FeedbackReport(
            team_member=sample_team_member,
            period="Q4 2024",
            rating=4.0
        )

        assert report.strengths == []
        assert report.achievements == []
        assert report.growth_areas == []
        assert report.growth_plan == []
        assert report.feedback_summary == ""
        assert report.formatted_output == ""

    def test_feedback_with_full_data(self, sample_team_member):
        """Test feedback with comprehensive data."""
        report = FeedbackReport(
            team_member=sample_team_member,
            period="Q4 2024",
            rating=4.5,
            strengths=[
                {"area": "Technical Leadership", "evidence": "Mentored 3 juniors"}
            ],
            achievements=["Led API migration", "Improved test coverage to 90%"],
            growth_areas=[
                {"area": "Public Speaking", "plan": "Attend Toastmasters"}
            ],
            growth_plan=[
                {"goal": "Kubernetes certification", "timeline": "6 months"}
            ],
            feedback_summary="Exceptional performance with strong technical leadership"
        )

        assert len(report.strengths) == 1
        assert len(report.achievements) == 2
        assert len(report.growth_areas) == 1
        assert len(report.growth_plan) == 1
        assert "Exceptional" in report.feedback_summary


class TestTeamManagerInit:
    """Test TeamManager initialization."""

    def test_initialization(self, manager):
        """Test TeamManager initializes with all dependencies."""
        assert manager.config_manager is not None
        assert manager.data_collector is not None
        assert manager.health_calculator is not None
        assert manager.output_formatter is not None

    def test_initialization_error_handling(self):
        """Test graceful handling of initialization errors."""
        with patch('tools.team_manager.ConfigManager', side_effect=Exception("Config error")):
            with pytest.raises(TeamManagerError) as exc:
                TeamManager()
            assert "initialization" in str(exc.value).lower()


class TestPrepare1on1:
    """Test prepare_1on1 method."""

    def test_basic_1on1_preparation(self, manager):
        """Test basic 1:1 meeting preparation."""
        meeting = manager.prepare_1on1(
            team_member_email="alice@example.com"
        )

        assert isinstance(meeting, OneOnOneMeeting)
        assert meeting.team_member.email == "alice@example.com"
        assert isinstance(meeting.date, datetime)
        assert meeting.formatted_output != ""

    def test_1on1_with_project_context(self, manager):
        """Test 1:1 preparation with project context."""
        meeting = manager.prepare_1on1(
            team_member_email="alice@example.com",
            include_project_context=True
        )

        assert isinstance(meeting, OneOnOneMeeting)
        assert len(meeting.agenda) > 0
        # Verify project context included
        manager.data_collector.collect_project_data.assert_called()

    def test_1on1_without_project_context(self, manager):
        """Test 1:1 preparation without project context."""
        meeting = manager.prepare_1on1(
            team_member_email="alice@example.com",
            include_project_context=False
        )

        assert isinstance(meeting, OneOnOneMeeting)
        # Verify project data not collected
        manager.data_collector.collect_project_data.assert_not_called()

    def test_1on1_invalid_email(self, manager):
        """Test 1:1 preparation with invalid email."""
        manager.data_collector.collect_team_data.return_value = MagicMock(
            members=[]
        )

        with pytest.raises(TeamManagerError) as exc:
            manager.prepare_1on1(team_member_email="invalid@example.com")
        assert "not found" in str(exc.value).lower()

    def test_1on1_output_formats(self, manager):
        """Test 1:1 preparation with different output formats."""
        # Markdown format
        meeting_md = manager.prepare_1on1(
            team_member_email="alice@example.com",
            output_format="markdown"
        )
        assert meeting_md.formatted_output != ""

        # JSON format
        meeting_json = manager.prepare_1on1(
            team_member_email="alice@example.com",
            output_format="json"
        )
        assert meeting_json.formatted_output != ""


class TestAnalyzePerformance:
    """Test analyze_performance method."""

    def test_individual_performance_analysis(self, manager):
        """Test individual performance analysis."""
        analysis = manager.analyze_performance(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(analysis, PerformanceAnalysis)
        assert analysis.team_member is not None
        assert analysis.team_member.email == "alice@example.com"
        assert analysis.period == "Q4 2024"
        assert analysis.overall_score > 0

    def test_team_wide_performance_analysis(self, manager):
        """Test team-wide performance analysis."""
        analysis = manager.analyze_performance(
            team_member_email=None,
            period="Q4 2024"
        )

        assert isinstance(analysis, PerformanceAnalysis)
        assert analysis.team_member is None
        assert analysis.period == "Q4 2024"
        # Verify metrics and trends are calculated
        assert isinstance(analysis.metrics, dict)
        assert isinstance(analysis.trends, dict)

    def test_performance_with_metrics(self, manager):
        """Test performance analysis includes metrics."""
        analysis = manager.analyze_performance(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(analysis.metrics, dict)
        assert len(analysis.metrics) > 0

    def test_performance_with_trends(self, manager):
        """Test performance analysis includes trends."""
        analysis = manager.analyze_performance(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(analysis.trends, dict)

    def test_performance_invalid_email(self, manager):
        """Test performance analysis with invalid email."""
        manager.data_collector.collect_team_data.return_value = MagicMock(
            members=[]
        )

        with pytest.raises(TeamManagerError) as exc:
            manager.analyze_performance(
                team_member_email="invalid@example.com"
            )
        assert "not found" in str(exc.value).lower()


class TestGenerateFeedback:
    """Test generate_feedback method."""

    def test_basic_feedback_generation(self, manager):
        """Test basic feedback report generation."""
        report = manager.generate_feedback(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(report, FeedbackReport)
        assert report.team_member.email == "alice@example.com"
        assert report.period == "Q4 2024"
        assert report.rating > 0

    def test_feedback_with_strengths(self, manager):
        """Test feedback includes strengths."""
        report = manager.generate_feedback(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(report.strengths, list)

    def test_feedback_with_growth_plan(self, manager):
        """Test feedback includes growth plan."""
        report = manager.generate_feedback(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(report.growth_plan, list)

    def test_feedback_with_achievements(self, manager):
        """Test feedback includes achievements."""
        report = manager.generate_feedback(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )

        assert isinstance(report.achievements, list)

    def test_feedback_invalid_email(self, manager):
        """Test feedback generation with invalid email."""
        manager.data_collector.collect_team_data.return_value = MagicMock(
            members=[]
        )

        with pytest.raises(TeamManagerError) as exc:
            manager.generate_feedback(
                team_member_email="invalid@example.com",
                period="Q4 2024"
            )
        assert "not found" in str(exc.value).lower()


class TestIdentifyGrowthOpportunities:
    """Test identify_growth_opportunities method."""

    def test_basic_growth_identification(self, manager):
        """Test basic growth opportunity identification."""
        opportunities = manager.identify_growth_opportunities(
            team_member_email="alice@example.com"
        )

        assert isinstance(opportunities, list)

    def test_growth_opportunities_structure(self, manager):
        """Test growth opportunities have proper structure."""
        opportunities = manager.identify_growth_opportunities(
            team_member_email="alice@example.com"
        )

        if len(opportunities) > 0:
            opp = opportunities[0]
            assert isinstance(opp, dict)
            # Verify expected keys
            assert any(key in opp for key in ["area", "skill", "opportunity"])

    def test_growth_invalid_email(self, manager):
        """Test growth identification with invalid email."""
        manager.data_collector.collect_team_data.return_value = MagicMock(
            members=[]
        )

        with pytest.raises(TeamManagerError) as exc:
            manager.identify_growth_opportunities(
                team_member_email="invalid@example.com"
            )
        assert "not found" in str(exc.value).lower()


class TestPrivateHelperMethods:
    """Test private helper methods."""

    def test_get_team_member(self, manager):
        """Test _get_team_member helper."""
        member = manager._get_team_member("alice@example.com")

        assert isinstance(member, TeamMember)
        assert member.email == "alice@example.com"

    def test_get_team_member_not_found(self, manager):
        """Test _get_team_member with non-existent email."""
        manager.data_collector.collect_team_data.return_value = MagicMock(
            members=[]
        )

        with pytest.raises(TeamManagerError) as exc:
            manager._get_team_member("nonexistent@example.com")
        assert "not found" in str(exc.value).lower()

    def test_calculate_performance_metrics(self, manager, sample_team_member):
        """Test _calculate_performance_metrics helper."""
        members = [sample_team_member]

        metrics = manager._calculate_performance_metrics(members, "Q4 2024")

        assert isinstance(metrics, dict)
        assert "overall_score" in metrics
        assert isinstance(metrics["overall_score"], float)
        assert 0.0 <= metrics["overall_score"] <= 5.0


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_data_collector_failure(self, manager):
        """Test graceful handling of data collector failure."""
        manager.data_collector.collect_team_data.side_effect = Exception(
            "Data collection failed"
        )

        with pytest.raises(TeamManagerError) as exc:
            manager.prepare_1on1(team_member_email="alice@example.com")
        assert "data collection" in str(exc.value).lower()

    def test_output_formatter_failure(self, manager):
        """Test graceful handling of output formatter failure."""
        manager.output_formatter.format_markdown.side_effect = Exception(
            "Formatting failed"
        )

        # Should still return meeting object even if formatting fails
        meeting = manager.prepare_1on1(team_member_email="alice@example.com")
        assert isinstance(meeting, OneOnOneMeeting)

    def test_health_calculator_failure(self, manager):
        """Test graceful handling of health calculator failure."""
        manager.health_calculator.calculate_health_score.side_effect = Exception(
            "Calculation failed"
        )

        # Should still complete analysis with degraded metrics
        analysis = manager.analyze_performance(
            team_member_email="alice@example.com"
        )
        assert isinstance(analysis, PerformanceAnalysis)


class TestOutputFormatting:
    """Test output formatting integration."""

    def test_markdown_formatting(self, manager):
        """Test markdown output formatting."""
        meeting = manager.prepare_1on1(
            team_member_email="alice@example.com",
            output_format="markdown"
        )

        assert meeting.formatted_output != ""
        assert "# " in meeting.formatted_output or "## " in meeting.formatted_output

    def test_json_formatting(self, manager):
        """Test JSON output formatting."""
        manager.output_formatter.format_json.return_value = MagicMock(
            content='{"team_member": "Alice Johnson"}'
        )

        meeting = manager.prepare_1on1(
            team_member_email="alice@example.com",
            output_format="json"
        )

        assert meeting.formatted_output != ""

    def test_template_selection(self, manager):
        """Test correct template selection for different operations."""
        # 1:1 meeting should use team_1on1 template
        manager.prepare_1on1(team_member_email="alice@example.com")
        manager.output_formatter.format_markdown.assert_called()
        call_args = manager.output_formatter.format_markdown.call_args
        assert call_args[1].get("template") == "team_1on1"

        # Performance analysis should use team_performance template
        manager.analyze_performance(team_member_email="alice@example.com")
        call_args = manager.output_formatter.format_markdown.call_args
        assert call_args[1].get("template") == "team_performance"

        # Feedback should use team_feedback template
        manager.generate_feedback(
            team_member_email="alice@example.com",
            period="Q4 2024"
        )
        call_args = manager.output_formatter.format_markdown.call_args
        assert call_args[1].get("template") == "team_feedback"

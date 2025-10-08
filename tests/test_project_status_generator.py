#!/usr/bin/env python3
"""
Comprehensive tests for ProjectStatusGenerator tool.

Tests project status generation, overview generation, and integration
with DataCollector, HealthCalculator, NoteProcessor, and OutputFormatter.
Target: >80% code coverage
"""

import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from tools.project_status_generator import (
    ProjectStatusGenerator,
    ProjectStatusGeneratorError,
    ProjectStatus,
)
from tools.data_models import ProjectData, GitHubData, NotesData
from tools.health_models import (
    HealthScore,
    HealthCategory,
    ComponentScore,
    Risk,
    RiskSeverity,
    RiskLikelihood,
    TrendAnalysis,
    TrendDirection,
)


class TestProjectStatusGenerator(unittest.TestCase):
    """Test suite for ProjectStatusGenerator."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = ProjectStatusGenerator()

        # Sample project data
        self.sample_project_data = ProjectData(
            project_name="mobile-app",
            github_data=GitHubData(
                repo_name="mobile-app",
                commits=[{"sha": f"abc{i}", "message": f"Commit {i}"} for i in range(45)],
                pull_requests=[{"number": i, "state": "closed"} for i in range(12)],
                issues=[{"number": i, "state": "closed"} for i in range(8)],
                repository_stats={"contributors": ["alice", "bob"]},
            ),
            notes_data=NotesData(
                project_notes=[{"title": f"Note {i}"} for i in range(15)],
                action_items=[{"description": f"Action {i}"} for i in range(10)],
                decisions=[],
            ),
            calendar_data=None,
            team_data=None,
            config_data={"name": "Mobile App", "status": "active"},
        )

        # Sample health score
        self.sample_health_score = HealthScore(
            score=0.75,
            category=HealthCategory.GOOD,
            components={
                "timeline": ComponentScore(name="timeline", score=0.80, weight=0.30, weighted_score=0.24),
                "activity": ComponentScore(name="activity", score=0.75, weight=0.25, weighted_score=0.1875),
                "blockers": ComponentScore(name="blockers", score=0.65, weight=0.25, weighted_score=0.1625),
                "dependencies": ComponentScore(name="dependencies", score=0.70, weight=0.20, weighted_score=0.14),
            },
        )

        # Sample trend analysis
        self.sample_trends = TrendAnalysis(
            direction=TrendDirection.IMPROVING,
            slope=0.05,
            confidence=0.85,
        )

        # Sample risks
        self.sample_risks = [
            Risk(
                risk_id="timeline-delay",
                title="Timeline delay risk",
                description="Timeline may slip if budget approval delayed",
                severity=RiskSeverity.MEDIUM,
                likelihood=RiskLikelihood.LIKELY,
                impact_score=0.6,
                mitigation_suggestions=["Fast-track budget approval process"],
            ),
        ]

    @patch("tools.project_status_generator.DataCollector")
    @patch("tools.project_status_generator.HealthCalculator")
    @patch("tools.project_status_generator.NoteProcessor")
    @patch("tools.project_status_generator.OutputFormatter")
    def test_generate_status_success(self, mock_formatter, mock_note_processor, mock_health_calc, mock_data_collector):
        """Test successful project status generation."""
        # Mock data collector
        mock_collector_instance = mock_data_collector.return_value
        mock_collector_instance.aggregate_project_data.return_value = self.sample_project_data

        # Mock health calculator
        mock_calc_instance = mock_health_calc.return_value
        mock_calc_instance.calculate_project_health.return_value = self.sample_health_score
        mock_calc_instance.analyze_trends.return_value = self.sample_trends
        mock_calc_instance.assess_risks.return_value = self.sample_risks

        # Mock note processor
        mock_processor_instance = mock_note_processor.return_value
        mock_processor_instance.get_project_notes.return_value = []
        mock_processor_instance.get_action_items_by_status.return_value = []

        # Mock output formatter
        mock_formatter_instance = mock_formatter.return_value
        mock_formatter_instance.format_markdown.return_value = MagicMock(
            content="# Project Status\n\nHealth: Good",
        )

        # Manually set mocked instances on generator
        self.generator.data_collector = mock_collector_instance
        self.generator.health_calculator = mock_calc_instance
        self.generator.note_processor = mock_processor_instance
        self.generator.output_formatter = mock_formatter_instance

        # Generate status
        status = self.generator.generate_status(project_id="mobile-app")

        # Assertions
        self.assertIsInstance(status, ProjectStatus)
        self.assertEqual(status.project_name, "mobile-app")
        self.assertEqual(status.health_score.category, HealthCategory.GOOD)
        self.assertEqual(status.trends.direction, TrendDirection.IMPROVING)
        self.assertEqual(len(status.risks), 1)
        self.assertGreater(status.processing_time_ms, 0)
        self.assertIn("Project Status", status.formatted_output)

    @patch("tools.project_status_generator.DataCollector")
    @patch("tools.project_status_generator.HealthCalculator")
    @patch("tools.project_status_generator.NoteProcessor")
    @patch("tools.project_status_generator.OutputFormatter")
    def test_generate_status_with_focus(self, mock_formatter, mock_note_processor, mock_health_calc, mock_data_collector):
        """Test project status generation with focus mode."""
        # Mock setup
        mock_collector_instance = mock_data_collector.return_value
        mock_collector_instance.aggregate_project_data.return_value = self.sample_project_data

        mock_calc_instance = mock_health_calc.return_value
        mock_calc_instance.calculate_project_health.return_value = self.sample_health_score
        mock_calc_instance.analyze_trends.return_value = self.sample_trends
        mock_calc_instance.assess_risks.return_value = self.sample_risks

        mock_processor_instance = mock_note_processor.return_value
        mock_processor_instance.get_project_notes.return_value = []
        mock_processor_instance.get_action_items_by_status.return_value = []

        mock_formatter_instance = mock_formatter.return_value
        mock_formatter_instance.format_markdown.return_value = MagicMock(
            content="# Risk Analysis\n\nRisks: 1",
        )

        # Manually set mocked instances on generator
        self.generator.data_collector = mock_collector_instance
        self.generator.health_calculator = mock_calc_instance
        self.generator.note_processor = mock_processor_instance
        self.generator.output_formatter = mock_formatter_instance

        # Generate with focus
        status = self.generator.generate_status(
            project_id="mobile-app",
            focus="risks"
        )

        # Verify focus was passed to formatter
        mock_formatter_instance.format_markdown.assert_called_once()
        call_kwargs = mock_formatter_instance.format_markdown.call_args[1]
        self.assertEqual(call_kwargs["context"]["focus"], "risks")

    @patch("tools.project_status_generator.DataCollector")
    @patch("tools.project_status_generator.HealthCalculator")
    @patch("tools.project_status_generator.NoteProcessor")
    @patch("tools.project_status_generator.OutputFormatter")
    def test_generate_status_json_output(self, mock_formatter, mock_note_processor, mock_health_calc, mock_data_collector):
        """Test JSON output format."""
        # Mock setup
        mock_collector_instance = mock_data_collector.return_value
        mock_collector_instance.aggregate_project_data.return_value = self.sample_project_data

        mock_calc_instance = mock_health_calc.return_value
        mock_calc_instance.calculate_project_health.return_value = self.sample_health_score
        mock_calc_instance.analyze_trends.return_value = self.sample_trends
        mock_calc_instance.assess_risks.return_value = self.sample_risks

        mock_processor_instance = mock_note_processor.return_value
        mock_processor_instance.get_project_notes.return_value = []
        mock_processor_instance.get_action_items_by_status.return_value = []

        mock_formatter_instance = mock_formatter.return_value
        mock_formatter_instance.format_json.return_value = MagicMock(
            content='{"health": {"score": 0.75}}',
        )

        # Manually set mocked instances on generator
        self.generator.data_collector = mock_collector_instance
        self.generator.health_calculator = mock_calc_instance
        self.generator.note_processor = mock_processor_instance
        self.generator.output_formatter = mock_formatter_instance

        # Generate JSON output
        status = self.generator.generate_status(
            project_id="mobile-app",
            output_format="json"
        )

        # Verify JSON formatter was called
        mock_formatter_instance.format_json.assert_called_once()

    def test_generate_status_missing_project_id(self):
        """Test error handling when project_id is missing."""
        with self.assertRaises(ProjectStatusGeneratorError) as context:
            self.generator.generate_status(project_id=None)

        self.assertIn("project_id is required", str(context.exception))

    @patch("tools.project_status_generator.DataCollector")
    @patch("tools.project_status_generator.ConfigManager")
    @patch("tools.project_status_generator.HealthCalculator")
    @patch("tools.project_status_generator.NoteProcessor")
    @patch("tools.project_status_generator.OutputFormatter")
    def test_generate_overview(self, mock_formatter, mock_note_processor, mock_health_calc, mock_config_mgr, mock_data_collector):
        """Test overview generation for multiple projects."""
        # Mock config manager
        mock_config_instance = mock_config_mgr.return_value
        mock_config_instance.get_all_projects.return_value = {"mobile-app": {}, "web-app": {}}

        # Mock data collector
        mock_collector_instance = mock_data_collector.return_value
        mock_collector_instance.aggregate_project_data.return_value = self.sample_project_data

        # Mock health calculator
        mock_calc_instance = mock_health_calc.return_value
        mock_calc_instance.calculate_project_health.return_value = self.sample_health_score
        mock_calc_instance.analyze_trends.return_value = self.sample_trends
        mock_calc_instance.assess_risks.return_value = self.sample_risks

        # Mock note processor
        mock_processor_instance = mock_note_processor.return_value
        mock_processor_instance.get_project_notes.return_value = []
        mock_processor_instance.get_action_items_by_status.return_value = []

        # Mock output formatter
        mock_formatter_instance = mock_formatter.return_value
        mock_formatter_instance.format_markdown.return_value = MagicMock(
            content="# Project Status",
        )

        # Manually set all mocked instances on generator
        self.generator.config_manager = mock_config_instance
        self.generator.data_collector = mock_collector_instance
        self.generator.health_calculator = mock_calc_instance
        self.generator.note_processor = mock_processor_instance
        self.generator.output_formatter = mock_formatter_instance

        # Generate overview
        overview = self.generator.generate_overview()

        # Assertions
        self.assertIsInstance(overview, dict)
        self.assertEqual(len(overview), 2)
        self.assertIn("mobile-app", overview)
        self.assertIn("web-app", overview)
        self.assertIsInstance(overview["mobile-app"], ProjectStatus)

    @patch("tools.project_status_generator.NoteProcessor")
    def test_analyze_notes_success(self, mock_note_processor):
        """Test successful note analysis."""
        # Mock note processor
        mock_processor_instance = mock_note_processor.return_value
        mock_processor_instance.get_project_notes.return_value = [MagicMock(), MagicMock()]
        mock_processor_instance.get_action_items_by_status.side_effect = [
            [MagicMock()],  # pending
            [MagicMock(), MagicMock()],  # overdue
            [MagicMock(), MagicMock(), MagicMock()],  # completed
        ]

        # Manually set mocked processor
        self.generator.note_processor = mock_processor_instance

        # Analyze notes
        result = self.generator._analyze_notes("mobile-app")

        # Assertions
        self.assertEqual(result["total_notes"], 2)
        self.assertEqual(result["pending_actions"], 1)
        self.assertEqual(result["overdue_actions"], 2)
        self.assertEqual(result["completed_actions"], 3)
        self.assertAlmostEqual(result["action_completion_rate"], 0.75)

    @patch("tools.project_status_generator.NoteProcessor")
    def test_analyze_notes_graceful_degradation(self, mock_note_processor):
        """Test graceful degradation when note analysis fails."""
        # Mock note processor to raise exception
        mock_processor_instance = mock_note_processor.return_value
        mock_processor_instance.get_project_notes.side_effect = Exception("Note processor error")

        # Manually set mocked processor
        self.generator.note_processor = mock_processor_instance

        # Analyze notes should not raise exception
        result = self.generator._analyze_notes("mobile-app")

        # Should return empty data
        self.assertEqual(result["total_notes"], 0)
        self.assertEqual(result["pending_actions"], 0)
        self.assertEqual(result["action_completion_rate"], 0.0)

    def test_get_performance_stats(self):
        """Test performance stats retrieval."""
        # Add some mock stats
        self.generator._performance_stats = [
            {"operation": "generate_status", "processing_time_ms": 123.45},
            {"operation": "generate_overview", "processing_time_ms": 456.78},
        ]

        stats = self.generator.get_performance_stats()

        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0]["operation"], "generate_status")

    @patch("tools.project_status_generator.DataCollector")
    @patch("tools.project_status_generator.OutputFormatter")
    def test_clear_cache(self, mock_formatter, mock_data_collector):
        """Test cache clearing."""
        mock_collector_instance = mock_data_collector.return_value
        mock_formatter_instance = mock_formatter.return_value

        # Manually set mocked instances
        self.generator.data_collector = mock_collector_instance
        self.generator.output_formatter = mock_formatter_instance

        # Clear cache
        self.generator.clear_cache()

        # Verify cache clear methods were called
        mock_collector_instance.clear_cache.assert_called_once()
        mock_formatter_instance.clear_cache.assert_called_once()


if __name__ == "__main__":
    unittest.main()

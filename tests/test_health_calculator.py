#!/usr/bin/env python3
"""
Comprehensive tests for HealthCalculator tool.

Tests all scoring algorithms, trend analysis, risk assessment, and edge cases.
Target: >80% code coverage
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from tools.health_calculator import HealthCalculator, HealthCalculatorError
from tools.health_config import HealthConfig
from tools.health_models import (
    HealthCategory,
    HealthScore,
    Risk,
    RiskLikelihood,
    RiskSeverity,
    TeamPerformanceMetrics,
    TrendAnalysis,
    TrendDirection,
)


class TestHealthCalculator(unittest.TestCase):
    """Test suite for HealthCalculator."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = HealthCalculator()
        self.sample_project_data = {
            "milestones": [
                {"id": "m1", "status": "completed"},
                {"id": "m2", "status": "completed"},
                {"id": "m3", "status": "in_progress"},
                {"id": "m4", "status": "pending"},
            ],
            "github_data": {
                "commits": [{"sha": f"commit{i}"} for i in range(15)],
                "pull_requests": [{"number": i} for i in range(5)],
                "issues": [
                    {"number": 1, "state": "closed"},
                    {"number": 2, "state": "open"},
                ],
            },
            "blockers": [
                {"id": "b1", "severity": "high"},
                {"id": "b2", "severity": "medium"},
            ],
            "dependencies": [
                {"name": "dep1", "health_score": 0.8},
                {"name": "dep2", "health_score": 0.9},
            ],
            "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
        }

    def test_calculate_project_health_success(self):
        """Test successful project health calculation."""
        health = self.calculator.calculate_project_health(self.sample_project_data)

        # Verify basic structure
        self.assertIsInstance(health, HealthScore)
        self.assertGreaterEqual(health.score, 0.0)
        self.assertLessEqual(health.score, 1.0)
        self.assertIsInstance(health.category, HealthCategory)

        # Verify components
        self.assertIn("timeline", health.components)
        self.assertIn("activity", health.components)
        self.assertIn("blockers", health.components)
        self.assertIn("dependencies", health.components)

        # Verify each component has correct structure
        for component in health.components.values():
            self.assertGreaterEqual(component.score, 0.0)
            self.assertLessEqual(component.score, 1.0)
            self.assertGreater(component.weight, 0.0)
            self.assertGreaterEqual(component.weighted_score, 0.0)

    def test_calculate_project_health_with_custom_weights(self):
        """Test health calculation with custom weights."""
        custom_weights = {
            "timeline": 0.4,
            "activity": 0.3,
            "blockers": 0.2,
            "dependencies": 0.1,
        }

        health = self.calculator.calculate_project_health(
            self.sample_project_data,
            weights=custom_weights,
        )

        # Verify custom weights are applied
        self.assertEqual(health.components["timeline"].weight, 0.4)
        self.assertEqual(health.components["activity"].weight, 0.3)
        self.assertEqual(health.components["blockers"].weight, 0.2)
        self.assertEqual(health.components["dependencies"].weight, 0.1)

    def test_calculate_project_health_empty_data(self):
        """Test health calculation with minimal/empty data."""
        empty_data = {}
        health = self.calculator.calculate_project_health(empty_data)

        # Should not crash, should return valid health score
        self.assertIsInstance(health, HealthScore)
        self.assertGreaterEqual(health.score, 0.0)
        self.assertLessEqual(health.score, 1.0)

    def test_calculate_project_health_performance(self):
        """Test that calculation completes within performance target (<50ms)."""
        import time

        start = time.time()
        health = self.calculator.calculate_project_health(self.sample_project_data)
        duration_ms = (time.time() - start) * 1000

        # Verify performance target
        self.assertLess(duration_ms, 50, "Health calculation exceeded 50ms target")
        self.assertIn("calculation_time_ms", health.details)

    def test_calculate_timeline_progress_completed_milestones(self):
        """Test timeline progress calculation with various completion states."""
        milestones = [
            {"id": "m1", "status": "completed"},
            {"id": "m2", "status": "completed"},
            {"id": "m3", "status": "in_progress"},
            {"id": "m4", "status": "pending"},
        ]

        progress = self.calculator.calculate_timeline_progress(milestones)

        self.assertEqual(progress["completed_count"], 2)
        self.assertEqual(progress["total_count"], 4)
        self.assertEqual(progress["percent_complete"], 50.0)

    def test_calculate_timeline_progress_with_dates(self):
        """Test timeline progress with start and target dates."""
        milestones = [
            {"id": "m1", "status": "completed"},
            {"id": "m2", "status": "completed"},
            {"id": "m3", "status": "pending"},
            {"id": "m4", "status": "pending"},
        ]
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
        target_date = (datetime.now() + timedelta(days=30)).isoformat()

        progress = self.calculator.calculate_timeline_progress(
            milestones,
            start_date=start_date,
            target_date=target_date,
        )

        self.assertIn("progress_ratio", progress)
        self.assertIn("on_track", progress)
        self.assertIsInstance(progress["on_track"], bool)

    def test_calculate_timeline_progress_empty_milestones(self):
        """Test timeline progress with no milestones."""
        progress = self.calculator.calculate_timeline_progress([])

        self.assertEqual(progress["completed_count"], 0)
        self.assertEqual(progress["total_count"], 0)
        self.assertEqual(progress["percent_complete"], 0.0)
        self.assertFalse(progress["on_track"])

    def test_calculate_activity_score_high_activity(self):
        """Test activity score with high activity."""
        github_data = {
            "commits": [{"sha": f"commit{i}"} for i in range(30)],
            "pull_requests": [{"number": i} for i in range(10)],
            "issues": [{"number": i, "state": "closed"} for i in range(5)],
        }

        score = self.calculator.calculate_activity_score(github_data)

        self.assertGreater(score, 0.8, "High activity should score above 0.8")

    def test_calculate_activity_score_low_activity(self):
        """Test activity score with low activity."""
        github_data = {
            "commits": [{"sha": "commit1"}],
            "pull_requests": [],
            "issues": [],
        }

        score = self.calculator.calculate_activity_score(github_data)

        self.assertLess(score, 0.6, "Low activity should score below 0.6")

    def test_calculate_activity_score_with_baseline(self):
        """Test activity score with custom baseline."""
        github_data = {
            "commits": [{"sha": f"commit{i}"} for i in range(20)],
            "pull_requests": [{"number": i} for i in range(5)],
            "issues": [],
        }
        baseline = {"total_activity": 50}

        score = self.calculator.calculate_activity_score(github_data, baseline)

        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_calculate_activity_score_empty_data(self):
        """Test activity score with no GitHub data."""
        score = self.calculator.calculate_activity_score({})

        # Should return neutral score
        self.assertEqual(score, 0.5)

    def test_calculate_blocker_impact_no_blockers(self):
        """Test blocker impact with no blockers."""
        impact = self.calculator.calculate_blocker_impact([])

        self.assertEqual(impact["count"], 0)
        self.assertEqual(impact["impact_score"], 1.0)
        self.assertEqual(impact["severity_breakdown"], {})

    def test_calculate_blocker_impact_multiple_blockers(self):
        """Test blocker impact with multiple blockers."""
        blockers = [
            {"id": "b1", "severity": "high"},
            {"id": "b2", "severity": "medium"},
            {"id": "b3", "severity": "high"},
            {"id": "b4", "severity": "low"},
        ]

        impact = self.calculator.calculate_blocker_impact(blockers)

        self.assertEqual(impact["count"], 4)
        self.assertLess(impact["impact_score"], 1.0)
        self.assertEqual(impact["severity_breakdown"]["high"], 2)
        self.assertEqual(impact["severity_breakdown"]["medium"], 1)
        self.assertEqual(impact["severity_breakdown"]["low"], 1)

    def test_calculate_team_performance(self):
        """Test team performance metrics calculation."""
        team_data = {
            "velocity": 25.0,
            "quality_score": 0.85,
            "collaboration_score": 0.75,
            "throughput": 15.0,
            "cycle_time": 3.5,
        }

        metrics = self.calculator.calculate_team_performance(team_data)

        self.assertIsInstance(metrics, TeamPerformanceMetrics)
        self.assertEqual(metrics.velocity, 25.0)
        self.assertEqual(metrics.quality_score, 0.85)
        self.assertEqual(metrics.collaboration_score, 0.75)
        self.assertEqual(metrics.throughput, 15.0)
        self.assertEqual(metrics.cycle_time, 3.5)

    def test_calculate_team_performance_defaults(self):
        """Test team performance with default values."""
        team_data = {}

        metrics = self.calculator.calculate_team_performance(team_data)

        self.assertIsInstance(metrics, TeamPerformanceMetrics)
        # Should have default values
        self.assertEqual(metrics.velocity, 0.0)

    def test_analyze_trends_improving(self):
        """Test trend analysis with improving trend."""
        historical_data = [
            {"timestamp": "2025-09-01", "value": 0.60},
            {"timestamp": "2025-09-08", "value": 0.65},
            {"timestamp": "2025-09-15", "value": 0.70},
            {"timestamp": "2025-09-22", "value": 0.75},
            {"timestamp": "2025-09-29", "value": 0.80},
        ]

        trend = self.calculator.analyze_trends(historical_data, time_window=30)

        self.assertIsInstance(trend, TrendAnalysis)
        self.assertEqual(trend.direction, TrendDirection.IMPROVING)
        self.assertGreater(trend.slope, 0)
        self.assertGreater(trend.confidence, 0)

    def test_analyze_trends_declining(self):
        """Test trend analysis with declining trend."""
        historical_data = [
            {"timestamp": "2025-09-01", "value": 0.80},
            {"timestamp": "2025-09-08", "value": 0.75},
            {"timestamp": "2025-09-15", "value": 0.70},
            {"timestamp": "2025-09-22", "value": 0.65},
            {"timestamp": "2025-09-29", "value": 0.60},
        ]

        trend = self.calculator.analyze_trends(historical_data, time_window=30)

        self.assertEqual(trend.direction, TrendDirection.DECLINING)
        self.assertLess(trend.slope, 0)

    def test_analyze_trends_stable(self):
        """Test trend analysis with stable trend."""
        historical_data = [
            {"timestamp": "2025-09-01", "value": 0.70},
            {"timestamp": "2025-09-08", "value": 0.71},
            {"timestamp": "2025-09-15", "value": 0.69},
            {"timestamp": "2025-09-22", "value": 0.70},
            {"timestamp": "2025-09-29", "value": 0.70},
        ]

        trend = self.calculator.analyze_trends(historical_data, time_window=30)

        self.assertEqual(trend.direction, TrendDirection.STABLE)

    def test_analyze_trends_insufficient_data(self):
        """Test trend analysis with insufficient data."""
        historical_data = [{"timestamp": "2025-09-01", "value": 0.70}]

        trend = self.calculator.analyze_trends(historical_data)

        self.assertEqual(trend.direction, TrendDirection.STABLE)
        self.assertEqual(trend.slope, 0.0)
        self.assertEqual(trend.confidence, 0.0)

    def test_analyze_trends_empty_data(self):
        """Test trend analysis with empty data."""
        trend = self.calculator.analyze_trends([])

        self.assertEqual(trend.direction, TrendDirection.STABLE)
        self.assertEqual(trend.slope, 0.0)
        self.assertEqual(trend.confidence, 0.0)

    def test_predict_completion_valid(self):
        """Test completion prediction with valid inputs."""
        prediction = self.calculator.predict_completion(
            current_progress=0.5,
            velocity=10.0,
            remaining_work=50.0,
        )

        self.assertIsNotNone(prediction["estimated_completion"])
        self.assertEqual(prediction["estimated_days"], 5.0)
        self.assertGreater(prediction["confidence"], 0)
        self.assertEqual(prediction["risk_level"], "low")

    def test_predict_completion_zero_velocity(self):
        """Test completion prediction with zero velocity."""
        prediction = self.calculator.predict_completion(
            current_progress=0.3,
            velocity=0.0,
            remaining_work=50.0,
        )

        self.assertIsNone(prediction["estimated_completion"])
        self.assertEqual(prediction["confidence"], 0.0)
        self.assertEqual(prediction["risk_level"], "high")

    def test_assess_risks_timeline_delay(self):
        """Test risk assessment identifies timeline delays."""
        project_data = {
            "milestones": [
                {"id": "m1", "status": "completed"},
                {"id": "m2", "status": "pending"},
                {"id": "m3", "status": "pending"},
                {"id": "m4", "status": "pending"},
            ],
            "start_date": (datetime.now() - timedelta(days=60)).isoformat(),
            "target_date": (datetime.now() + timedelta(days=10)).isoformat(),
            "blockers": [],
            "github_data": {"commits": [{"sha": f"c{i}"} for i in range(20)]},
        }

        risks = self.calculator.assess_risks(project_data)

        # Should identify timeline risk
        timeline_risks = [r for r in risks if r.category == "timeline"]
        self.assertGreater(len(timeline_risks), 0)

    def test_assess_risks_high_blockers(self):
        """Test risk assessment identifies high blocker count."""
        project_data = {
            "milestones": [{"id": "m1", "status": "completed"}],
            "blockers": [{"id": f"b{i}"} for i in range(5)],
            "github_data": {},
        }

        risks = self.calculator.assess_risks(project_data)

        # Should identify blocker risk
        blocker_risks = [r for r in risks if r.category == "blockers"]
        self.assertGreater(len(blocker_risks), 0)

    def test_assess_risks_low_activity(self):
        """Test risk assessment identifies low activity."""
        project_data = {
            "milestones": [{"id": "m1", "status": "in_progress"}],
            "blockers": [],
            "github_data": {
                "commits": [{"sha": "c1"}],
                "pull_requests": [],
                "issues": [],
            },
        }

        risks = self.calculator.assess_risks(project_data)

        # Should identify activity risk
        activity_risks = [r for r in risks if r.category == "activity"]
        self.assertGreater(len(activity_risks), 0)

    def test_assess_risks_sorting_by_priority(self):
        """Test that risks are sorted by priority score."""
        project_data = {
            "milestones": [{"id": "m1", "status": "pending"}],
            "start_date": (datetime.now() - timedelta(days=60)).isoformat(),
            "target_date": (datetime.now() - timedelta(days=10)).isoformat(),
            "blockers": [{"id": f"b{i}"} for i in range(8)],
            "github_data": {"commits": []},
        }

        risks = self.calculator.assess_risks(project_data)

        # Verify sorting (higher priority first)
        for i in range(len(risks) - 1):
            self.assertGreaterEqual(
                risks[i].priority_score,
                risks[i + 1].priority_score,
                "Risks should be sorted by priority score descending",
            )

    def test_get_performance_stats(self):
        """Test performance statistics tracking."""
        # Run some calculations
        self.calculator.calculate_project_health(self.sample_project_data)
        self.calculator.calculate_project_health(self.sample_project_data)

        stats = self.calculator.get_performance_stats()

        self.assertEqual(stats["total_calculations"], 2)
        self.assertGreater(stats["average_time_ms"], 0)
        self.assertGreater(stats["max_time_ms"], 0)
        self.assertGreater(stats["min_time_ms"], 0)

    def test_get_performance_stats_no_calculations(self):
        """Test performance stats with no calculations."""
        calc = HealthCalculator()
        stats = calc.get_performance_stats()

        self.assertEqual(stats["total_calculations"], 0)
        self.assertEqual(stats["average_time_ms"], 0.0)


class TestHealthConfig(unittest.TestCase):
    """Test suite for HealthConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = HealthConfig()

        # Verify weights sum to 1.0
        total_weight = sum(config.config["weights"].values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)

    def test_custom_config(self):
        """Test custom configuration."""
        custom = {
            "weights": {
                "timeline": 0.4,
                "activity": 0.3,
                "blockers": 0.2,
                "dependencies": 0.1,
            }
        }

        config = HealthConfig(custom_config=custom)

        self.assertEqual(config.get_weight("timeline"), 0.4)
        self.assertEqual(config.get_weight("activity"), 0.3)

    def test_invalid_weights_raise_error(self):
        """Test that invalid weights raise an error."""
        custom = {
            "weights": {
                "timeline": 0.5,
                "activity": 0.3,
                "blockers": 0.1,
                "dependencies": 0.05,  # Sum = 0.95, not 1.0
            }
        }

        with self.assertRaises(ValueError):
            HealthConfig(custom_config=custom)

    def test_get_health_category(self):
        """Test health category determination."""
        config = HealthConfig()

        self.assertEqual(config.get_health_category(0.90), "excellent")
        self.assertEqual(config.get_health_category(0.75), "good")
        self.assertEqual(config.get_health_category(0.60), "fair")
        self.assertEqual(config.get_health_category(0.40), "poor")
        self.assertEqual(config.get_health_category(0.20), "critical")


class TestHealthModels(unittest.TestCase):
    """Test suite for health models."""

    def test_health_score_from_score(self):
        """Test HealthScore creation from numeric score."""
        health = HealthScore.from_score(0.72)

        self.assertEqual(health.score, 0.72)
        self.assertEqual(health.category, HealthCategory.GOOD)

    def test_health_score_categorization(self):
        """Test health score categorization."""
        self.assertEqual(
            HealthScore.from_score(0.90).category, HealthCategory.EXCELLENT
        )
        self.assertEqual(HealthScore.from_score(0.75).category, HealthCategory.GOOD)
        self.assertEqual(HealthScore.from_score(0.60).category, HealthCategory.FAIR)
        self.assertEqual(HealthScore.from_score(0.40).category, HealthCategory.POOR)
        self.assertEqual(
            HealthScore.from_score(0.20).category, HealthCategory.CRITICAL
        )

    def test_health_score_to_dict(self):
        """Test HealthScore dictionary conversion."""
        health = HealthScore.from_score(0.72)
        health_dict = health.to_dict()

        self.assertIn("score", health_dict)
        self.assertIn("category", health_dict)
        self.assertIn("components", health_dict)
        self.assertIn("calculated_at", health_dict)

    def test_risk_priority_score(self):
        """Test risk priority score calculation."""
        risk = Risk(
            risk_id="test",
            title="Test Risk",
            description="Test",
            severity=RiskSeverity.HIGH,
            likelihood=RiskLikelihood.LIKELY,
            impact_score=0.8,
        )

        # Priority = (severity * 0.6) + (likelihood * 0.4)
        # HIGH = 0.75, LIKELY = 0.75
        # (0.75 * 0.6) + (0.75 * 0.4) = 0.45 + 0.30 = 0.75
        self.assertAlmostEqual(risk.priority_score, 0.75, places=2)

    def test_risk_to_dict(self):
        """Test risk dictionary conversion."""
        risk = Risk(
            risk_id="test",
            title="Test Risk",
            description="Test",
            severity=RiskSeverity.MEDIUM,
            likelihood=RiskLikelihood.POSSIBLE,
            impact_score=0.6,
        )

        risk_dict = risk.to_dict()

        self.assertIn("risk_id", risk_dict)
        self.assertIn("severity", risk_dict)
        self.assertIn("likelihood", risk_dict)
        self.assertIn("priority_score", risk_dict)


if __name__ == "__main__":
    unittest.main()

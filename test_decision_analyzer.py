"""
Tests for DecisionAnalyzer tool.

Tests decision analysis, framework application, stakeholder impact, and output formatting.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from tools.decision_analyzer import (
    DecisionAnalyzer,
    DecisionAnalyzerError,
    DecisionAnalysis,
    DecisionContext,
    DecisionOption,
    DecisionRecommendation,
    DecisionRisk,
    UrgencyLevel,
    SentimentType,
)


@pytest.fixture
def analyzer():
    """Create DecisionAnalyzer instance with mocked dependencies."""
    with patch('tools.decision_analyzer.ConfigManager'), \
         patch('tools.decision_analyzer.StakeholderAnalyzer'), \
         patch('tools.decision_analyzer.OutputFormatter'):
        analyzer = DecisionAnalyzer()
        return analyzer


@pytest.fixture
def sample_options():
    """Sample decision options for testing."""
    return [
        {
            "name": "React with TypeScript",
            "description": "Modern web framework with strong ecosystem",
            "pros": ["Strong community", "Team experience", "Great tooling"],
            "cons": ["Learning curve for TypeScript", "Additional build complexity"],
            "strategic_impact_score": 0.85,
            "cost_efficiency_score": 0.70,
            "implementation_risk_score": 0.60,
            "timeline_score": 0.75,
            "estimated_cost": "$50,000",
            "estimated_time": "3 months"
        },
        {
            "name": "Vue.js",
            "description": "Progressive framework with gentle learning curve",
            "pros": ["Easy to learn", "Good documentation", "Flexible"],
            "cons": ["Smaller ecosystem", "Less team experience"],
            "strategic_impact_score": 0.70,
            "cost_efficiency_score": 0.80,
            "implementation_risk_score": 0.70,
            "timeline_score": 0.80,
            "estimated_cost": "$40,000",
            "estimated_time": "2.5 months"
        },
        {
            "name": "Status Quo",
            "description": "Continue with current jQuery implementation",
            "pros": ["No change cost", "No learning curve"],
            "cons": ["Technical debt", "Limited capabilities"],
            "strategic_impact_score": 0.30,
            "cost_efficiency_score": 0.95,
            "implementation_risk_score": 0.90,
            "timeline_score": 0.95,
            "estimated_cost": "$0",
            "estimated_time": "0 months"
        }
    ]


class TestDecisionContext:
    """Test DecisionContext dataclass."""

    def test_decision_context_creation(self):
        """Test creating decision context."""
        context = DecisionContext(
            title="Technology Stack Selection",
            description="Choose framework for new product",
            urgency=UrgencyLevel.HIGH,
            deadline="2024-12-15",
            decision_type="technical"
        )

        assert context.title == "Technology Stack Selection"
        assert context.urgency == UrgencyLevel.HIGH
        assert context.decision_type == "technical"

    def test_decision_context_defaults(self):
        """Test decision context default values."""
        context = DecisionContext(title="Test Decision")

        assert context.description == ""
        assert context.urgency == UrgencyLevel.MEDIUM
        assert context.deadline is None
        assert context.success_criteria == []
        assert context.constraints == {}
        assert context.decision_type == "general"


class TestDecisionOption:
    """Test DecisionOption dataclass."""

    def test_decision_option_creation(self):
        """Test creating decision option."""
        option = DecisionOption(
            name="Option A",
            description="Test option",
            pros=["Pro 1", "Pro 2"],
            cons=["Con 1"],
            criteria_scores={"quality": 0.8, "cost": 0.6},
            overall_score=0.7
        )

        assert option.name == "Option A"
        assert len(option.pros) == 2
        assert len(option.cons) == 1
        assert option.criteria_scores["quality"] == 0.8
        assert option.overall_score == 0.7

    def test_decision_option_defaults(self):
        """Test decision option default values."""
        option = DecisionOption(name="Test Option")

        assert option.description == ""
        assert option.pros == []
        assert option.cons == []
        assert option.criteria_scores == {}
        assert option.estimated_cost is None
        assert option.estimated_time is None
        assert option.overall_score == 0.0


class TestDecisionAnalyzer:
    """Test DecisionAnalyzer core functionality."""

    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer is not None
        assert hasattr(analyzer, 'config_manager')
        assert hasattr(analyzer, 'stakeholder_analyzer')
        assert hasattr(analyzer, 'output_formatter')

    def test_apply_framework(self, analyzer, sample_options):
        """Test applying decision framework to options."""
        analysis = analyzer.apply_framework(
            decision_title="Technology Stack Selection",
            options=sample_options,
            framework_type="technical",
            description="Choose framework for new product",
            urgency="high"
        )

        assert isinstance(analysis, DecisionAnalysis)
        assert analysis.decision.title == "Technology Stack Selection"
        assert analysis.decision.urgency == UrgencyLevel.HIGH
        assert len(analysis.options) == 3
        assert analysis.framework_applied == "Technical"
        assert analysis.recommendation.option is not None

    def test_apply_framework_scores_options(self, analyzer, sample_options):
        """Test that framework application scores options correctly."""
        analysis = analyzer.apply_framework(
            decision_title="Test Decision",
            options=sample_options,
            framework_type="business"
        )

        # Check that options are scored
        for option in analysis.options:
            assert option.overall_score >= 0.0
            assert option.overall_score <= 1.0
            assert len(option.criteria_scores) > 0

        # Check that options are sorted by score
        scores = [opt.overall_score for opt in analysis.options]
        assert scores == sorted(scores, reverse=True)

    def test_apply_framework_with_deadline(self, analyzer, sample_options):
        """Test framework application with deadline."""
        analysis = analyzer.apply_framework(
            decision_title="Urgent Decision",
            options=sample_options,
            framework_type="strategic",
            deadline="2024-12-31",
            urgency="critical"
        )

        assert analysis.decision.deadline == "2024-12-31"
        assert analysis.decision.urgency == UrgencyLevel.CRITICAL

    def test_apply_framework_generates_recommendation(self, analyzer, sample_options):
        """Test that framework application generates recommendation."""
        analysis = analyzer.apply_framework(
            decision_title="Test Decision",
            options=sample_options,
            framework_type="general"
        )

        assert isinstance(analysis.recommendation, DecisionRecommendation)
        assert analysis.recommendation.option in [opt.name for opt in analysis.options]
        assert 0.0 <= analysis.recommendation.confidence <= 1.0
        assert len(analysis.recommendation.reasoning) > 0

    def test_apply_framework_identifies_risks(self, analyzer, sample_options):
        """Test that framework application identifies risks."""
        analysis = analyzer.apply_framework(
            decision_title="Test Decision",
            options=sample_options,
            framework_type="general"
        )

        assert isinstance(analysis.risks, list)
        # Should have some risks based on cons
        assert len(analysis.risks) > 0

        for risk in analysis.risks:
            assert isinstance(risk, DecisionRisk)
            assert len(risk.title) > 0
            assert len(risk.description) > 0

    def test_apply_framework_generates_next_steps(self, analyzer, sample_options):
        """Test that framework application generates next steps."""
        analysis = analyzer.apply_framework(
            decision_title="Test Decision",
            options=sample_options,
            framework_type="general"
        )

        assert isinstance(analysis.next_steps, list)
        assert len(analysis.next_steps) > 0

        for step in analysis.next_steps:
            assert "action" in step
            assert "owner" in step
            assert "deadline" in step

    def test_apply_framework_error_handling(self, analyzer):
        """Test error handling in framework application."""
        # Empty title should still work (graceful handling)
        analysis = analyzer.apply_framework(
            decision_title="Test",
            options=[],  # Empty options
            framework_type="general"
        )

        # Should handle empty options gracefully
        assert isinstance(analysis, DecisionAnalysis)
        assert len(analysis.options) == 0
        assert analysis.recommendation.option == "None"

    def test_analyze_stakeholder_impact(self, analyzer, sample_options):
        """Test stakeholder impact analysis."""
        impact = analyzer.analyze_stakeholder_impact(
            decision_title="Technology Stack Selection",
            options=sample_options,
            stakeholders=["engineering", "product", "executive"],
            decision_type="technical"
        )

        assert isinstance(impact, dict)
        assert "engineering" in impact
        assert "product" in impact
        assert "executive" in impact

        for stakeholder, data in impact.items():
            assert "description" in data
            assert "sentiment" in data
            assert data["sentiment"] in ["positive", "neutral", "negative"]
            assert "concerns" in data
            assert "communication_priority" in data

    def test_analyze_stakeholder_impact_auto_identification(self, analyzer, sample_options):
        """Test automatic stakeholder identification."""
        # Mock stakeholder_analyzer.identify_stakeholders
        analyzer.stakeholder_analyzer.identify_stakeholders = Mock(return_value=[
            {"id": "engineering", "name": "Engineering Team"},
            {"id": "product", "name": "Product Management"}
        ])

        impact = analyzer.analyze_stakeholder_impact(
            decision_title="API Redesign",
            options=sample_options,
            stakeholders=None,  # Auto-identify
            decision_type="technical"
        )

        assert "engineering" in impact
        assert "product" in impact

    def test_compare_options(self, analyzer, sample_options):
        """Test multi-criteria option comparison."""
        criteria = [
            {"name": "strategic_impact", "weight": 0.3},
            {"name": "cost_efficiency", "weight": 0.4},
            {"name": "implementation_risk", "weight": 0.3}
        ]

        comparison = analyzer.compare_options(
            options=sample_options,
            criteria=criteria
        )

        assert "criteria" in comparison
        assert "comparison_matrix" in comparison
        assert "recommended" in comparison

        # Check that criteria weights sum to 1.0
        total_weight = sum(c["weight"] for c in comparison["criteria"])
        assert abs(total_weight - 1.0) < 0.01

        # Check that comparison matrix has entries for all options
        assert len(comparison["comparison_matrix"]) == len(sample_options)

        # Check that options are sorted by weighted score
        scores = [entry["weighted_score"] for entry in comparison["comparison_matrix"]]
        assert scores == sorted(scores, reverse=True)

    def test_compare_options_normalizes_weights(self, analyzer, sample_options):
        """Test that option comparison normalizes criterion weights."""
        criteria = [
            {"name": "cost", "weight": 2.0},
            {"name": "time", "weight": 3.0}
        ]

        comparison = analyzer.compare_options(
            options=sample_options,
            criteria=criteria
        )

        # Weights should be normalized to sum to 1.0
        total_weight = sum(c["weight"] for c in comparison["criteria"])
        assert abs(total_weight - 1.0) < 0.01

    def test_generate_decision_report(self, analyzer, sample_options):
        """Test decision report generation."""
        # First create analysis
        analysis = analyzer.apply_framework(
            decision_title="Test Decision",
            options=sample_options,
            framework_type="general"
        )

        # Mock output_formatter
        mock_result = Mock()
        mock_result.content = "# Test Decision Report\n\nFormatted output..."
        analyzer.output_formatter.format_markdown = Mock(return_value=mock_result)

        # Generate report
        report = analyzer.generate_decision_report(
            analysis=analysis,
            template="decision_analysis",
            include_stakeholders=True
        )

        assert isinstance(report, str)
        assert len(report) > 0
        analyzer.output_formatter.format_markdown.assert_called_once()

    def test_generate_decision_report_templates(self, analyzer, sample_options):
        """Test decision report generation with different templates."""
        analysis = analyzer.apply_framework(
            decision_title="Test Decision",
            options=sample_options,
            framework_type="general"
        )

        mock_result = Mock()
        mock_result.content = "Formatted report"
        analyzer.output_formatter.format_markdown = Mock(return_value=mock_result)

        # Test different templates
        templates = ["decision_analysis", "framework_analysis", "stakeholder_impact", "option_comparison"]

        for template in templates:
            report = analyzer.generate_decision_report(
                analysis=analysis,
                template=template,
                include_stakeholders=True
            )

            assert isinstance(report, str)
            assert len(report) > 0


class TestDecisionAnalyzerPrivateMethods:
    """Test DecisionAnalyzer private helper methods."""

    def test_load_framework(self, analyzer):
        """Test framework loading."""
        framework = analyzer._load_framework("technical")

        assert isinstance(framework, dict)
        assert "name" in framework
        assert "criteria" in framework
        assert len(framework["criteria"]) > 0

        # Check criteria structure
        for criterion in framework["criteria"]:
            assert "name" in criterion
            assert "weight" in criterion
            assert criterion["weight"] >= 0.0
            assert criterion["weight"] <= 1.0

    def test_load_framework_fallback(self, analyzer):
        """Test framework loading fallback to default."""
        # Even with invalid framework type, should return default
        framework = analyzer._load_framework("nonexistent_framework")

        assert isinstance(framework, dict)
        assert "criteria" in framework
        assert len(framework["criteria"]) > 0

    def test_score_options(self, analyzer, sample_options):
        """Test option scoring logic."""
        framework = analyzer._load_framework("general")
        scored = analyzer._score_options(sample_options, framework)

        assert len(scored) == len(sample_options)

        for option in scored:
            assert isinstance(option, DecisionOption)
            assert option.overall_score >= 0.0
            assert option.overall_score <= 1.0
            assert len(option.criteria_scores) > 0

        # Check sorting
        scores = [opt.overall_score for opt in scored]
        assert scores == sorted(scores, reverse=True)

    def test_generate_recommendation_best_option(self, analyzer):
        """Test recommendation generation selects best option."""
        options = [
            DecisionOption(name="Option A", overall_score=0.8),
            DecisionOption(name="Option B", overall_score=0.6),
            DecisionOption(name="Option C", overall_score=0.7)
        ]

        framework = {"name": "Test Framework"}
        recommendation = analyzer._generate_recommendation(options, framework)

        assert recommendation.option == "Option A"  # Highest score
        assert recommendation.confidence > 0.0

    def test_generate_recommendation_confidence_calculation(self, analyzer):
        """Test recommendation confidence calculation."""
        # Close scores = lower confidence
        close_options = [
            DecisionOption(name="Option A", overall_score=0.75),
            DecisionOption(name="Option B", overall_score=0.74)
        ]

        # Wide gap = higher confidence
        wide_options = [
            DecisionOption(name="Option A", overall_score=0.90),
            DecisionOption(name="Option B", overall_score=0.50)
        ]

        framework = {"name": "Test Framework"}

        close_rec = analyzer._generate_recommendation(close_options, framework)
        wide_rec = analyzer._generate_recommendation(wide_options, framework)

        # Wider gap should have higher confidence
        assert wide_rec.confidence > close_rec.confidence

    def test_identify_risks_from_low_scores(self, analyzer):
        """Test risk identification from low-scoring options."""
        options = [
            DecisionOption(name="Good Option", overall_score=0.8),
            DecisionOption(name="Poor Option", overall_score=0.3)
        ]

        framework = {"name": "Test Framework"}
        risks = analyzer._identify_risks(options, framework)

        assert len(risks) > 0
        # Should identify risk for low-scoring option
        assert any("Poor Option" in risk.title for risk in risks)

    def test_identify_risks_from_cons(self, analyzer):
        """Test risk identification from option cons."""
        options = [
            DecisionOption(
                name="Best Option",
                overall_score=0.9,
                cons=["High initial cost", "Long implementation time"]
            )
        ]

        framework = {"name": "Test Framework"}
        risks = analyzer._identify_risks(options, framework)

        # Should create risks from cons in recommended option
        assert len(risks) > 0

    def test_generate_next_steps(self, analyzer):
        """Test next steps generation."""
        recommendation = DecisionRecommendation(
            option="React with TypeScript",
            reasoning="Best fit for requirements",
            confidence=0.85
        )

        framework = {"name": "Technical Framework"}
        next_steps = analyzer._generate_next_steps(recommendation, framework)

        assert len(next_steps) > 0

        for step in next_steps:
            assert "action" in step
            assert "owner" in step
            assert "deadline" in step
            assert len(step["action"]) > 0


class TestDecisionAnalysisIntegration:
    """Integration tests for complete decision analysis workflow."""

    def test_complete_analysis_workflow(self, analyzer, sample_options):
        """Test complete end-to-end decision analysis workflow."""
        # Apply framework
        analysis = analyzer.apply_framework(
            decision_title="Technology Stack Selection",
            options=sample_options,
            framework_type="technical",
            description="Choose modern web framework for new product line",
            urgency="high",
            deadline="2024-12-15"
        )

        # Verify complete analysis structure
        assert isinstance(analysis, DecisionAnalysis)
        assert isinstance(analysis.decision, DecisionContext)
        assert len(analysis.options) == 3
        assert isinstance(analysis.recommendation, DecisionRecommendation)
        assert len(analysis.risks) > 0
        assert len(analysis.next_steps) > 0
        assert analysis.framework_applied == "Technical"

        # Verify options are properly scored and sorted
        assert analysis.options[0].overall_score >= analysis.options[1].overall_score
        assert analysis.options[1].overall_score >= analysis.options[2].overall_score

        # Verify recommendation is from analyzed options
        option_names = [opt.name for opt in analysis.options]
        assert analysis.recommendation.option in option_names

    def test_analysis_with_stakeholder_integration(self, analyzer, sample_options):
        """Test analysis with stakeholder impact integration."""
        # Apply framework
        analysis = analyzer.apply_framework(
            decision_title="API Redesign",
            options=sample_options,
            framework_type="strategic"
        )

        # Add stakeholder impact
        stakeholder_impact = analyzer.analyze_stakeholder_impact(
            decision_title="API Redesign",
            options=sample_options,
            stakeholders=["engineering", "product"],
            decision_type="strategic"
        )

        analysis.stakeholder_impact = stakeholder_impact

        # Verify integration
        assert len(analysis.stakeholder_impact) > 0
        assert "engineering" in analysis.stakeholder_impact
        assert "product" in analysis.stakeholder_impact

        # Generate report with stakeholders
        mock_result = Mock()
        mock_result.content = "Report with stakeholders"
        analyzer.output_formatter.format_markdown = Mock(return_value=mock_result)

        report = analyzer.generate_decision_report(
            analysis=analysis,
            template="stakeholder_impact",
            include_stakeholders=True
        )

        assert isinstance(report, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Tests for OutputFormatter tool.

Target: >80% code coverage for all formatting functions.
"""

import json
import pytest
from datetime import datetime, timedelta
from pathlib import Path

from tools.output_formatter import OutputFormatter, OutputFormatterError, TemplateLoadError
from tools.output_models import (
    AudienceType,
    DateStyle,
    EmojiIndicators,
    FormattedOutput,
    FormattingContext,
    HealthScoreFormat,
    OutputFormat,
    TableColumn,
)


@pytest.fixture
def formatter():
    """Create OutputFormatter instance for testing."""
    return OutputFormatter()


@pytest.fixture
def sample_health_data():
    """Sample health data for testing."""
    return {
        "title": "Project Alpha Status",
        "subtitle": "Q4 2025 Update",
        "timestamp": datetime.now().isoformat(),
        "health": {
            "overall_score": 0.75,
            "components": {
                "timeline": {"score": 0.8, "status": "good"},
                "activity": {"score": 0.7, "status": "good"},
                "blockers": {"score": 0.8, "status": "good"},
                "dependencies": {"score": 0.7, "status": "fair"},
            },
        },
        "timeline": {
            "status": "on_track",
            "on_track": True,
            "progress_ratio": 0.95,
            "milestones": [
                {
                    "name": "Design Phase",
                    "status": "completed",
                    "due_date": (datetime.now() - timedelta(days=30)).isoformat(),
                    "progress": 1.0,
                },
                {
                    "name": "Implementation",
                    "status": "in_progress",
                    "due_date": datetime.now().isoformat(),
                    "progress": 0.6,
                },
            ],
        },
        "activity": {
            "commits": 45,
            "pull_requests": 12,
            "issues_closed": 8,
            "score": 0.7,
        },
        "blockers": [
            {
                "title": "API Rate Limiting",
                "severity": "medium",
                "description": "Third-party API is rate limiting requests",
            }
        ],
        "dependencies": [
            {"name": "Database Service", "health_score": 0.9},
            {"name": "Auth Service", "health_score": 0.8},
        ],
        "risks": [
            {
                "title": "Timeline Slippage Risk",
                "severity": "medium",
                "likelihood": "possible",
                "description": "Current velocity may impact delivery date",
                "mitigation_suggestions": [
                    "Add developer resources",
                    "Reduce scope for v1",
                ],
            }
        ],
        "next_steps": [
            "Complete implementation phase",
            "Begin integration testing",
            "Plan deployment strategy",
        ],
    }


class TestOutputFormatter:
    """Test suite for OutputFormatter."""

    def test_initialization(self, formatter):
        """Test OutputFormatter initialization."""
        assert formatter is not None
        assert formatter.templates_dir.exists()
        assert isinstance(formatter.emoji, EmojiIndicators)
        assert len(formatter._render_times) == 0

    def test_format_markdown_project_status(self, formatter, sample_health_data):
        """Test markdown formatting with project_status template."""
        # Warm up template cache
        formatter.format_markdown(sample_health_data, "project_status", context={})

        # Actual test with warmed cache
        output = formatter.format_markdown(
            sample_health_data,
            "project_status",
            context={"focus": "risks"},
        )

        assert isinstance(output, FormattedOutput)
        assert output.format == OutputFormat.MARKDOWN
        assert output.processing_time_ms > 0
        assert output.processing_time_ms < 100  # Relaxed for first run
        assert output.template_used == "project_status.md.j2"
        assert "Project Alpha Status" in output.content
        assert "Overall Health" in output.content
        assert "Timeline" in output.content

    def test_format_markdown_missing_template(self, formatter):
        """Test error handling for missing template."""
        with pytest.raises(TemplateLoadError):
            formatter.format_markdown(
                {"title": "Test"},
                "nonexistent_template",
            )

    def test_format_json(self, formatter, sample_health_data):
        """Test JSON formatting."""
        output = formatter.format_json(sample_health_data, pretty=True)

        assert isinstance(output, FormattedOutput)
        assert output.format == OutputFormat.JSON
        assert output.processing_time_ms > 0

        # Verify valid JSON
        parsed = json.loads(output.content)
        assert parsed["title"] == "Project Alpha Status"
        assert parsed["health"]["overall_score"] == 0.75

    def test_format_json_compact(self, formatter, sample_health_data):
        """Test compact JSON formatting."""
        output = formatter.format_json(sample_health_data, pretty=False)

        assert "\n" not in output.content or output.content.count("\n") < 5
        # Verify valid JSON
        json.loads(output.content)

    def test_format_table(self, formatter):
        """Test table formatting."""
        data = [
            {"name": "Alice", "role": "Engineer", "tasks": 5},
            {"name": "Bob", "role": "Designer", "tasks": 3},
            {"name": "Carol", "role": "Manager", "tasks": 8},
        ]

        columns = [
            TableColumn(name="Name", key="name"),
            TableColumn(name="Role", key="role"),
            TableColumn(name="Tasks", key="tasks", align="right"),
        ]

        output = formatter.format_table(data, columns)

        assert isinstance(output, FormattedOutput)
        assert output.format == OutputFormat.TABLE
        assert "Alice" in output.content
        assert "Bob" in output.content
        assert "Carol" in output.content
        assert "|" in output.content  # Markdown table format
        assert "---:" in output.content  # Right alignment for tasks column

    def test_format_table_empty(self, formatter):
        """Test table formatting with no data."""
        columns = [TableColumn(name="Name", key="name")]
        output = formatter.format_table([], columns)

        assert "No data available" in output.content

    def test_format_table_with_custom_formatter(self, formatter):
        """Test table with custom column formatter."""
        data = [{"name": "Test", "score": 0.85}]

        columns = [
            TableColumn(name="Name", key="name"),
            TableColumn(
                name="Score",
                key="score",
                format_fn=lambda x: f"{x * 100:.0f}%",
            ),
        ]

        output = formatter.format_table(data, columns)
        assert "85%" in output.content

    def test_executive_summary(self, formatter):
        """Test executive summary generation."""
        data = {
            "title": "Q4 Summary",
            "summary": "Project is on track with minor challenges",
            "metrics": {"completion": "75%", "budget": "On target"},
            "health": {"overall_score": 0.8},
            "status": "good",
            "critical_items": [],
            "recommendation": "Continue current plan",
        }

        output = formatter.executive_summary(data, max_length=500)

        assert isinstance(output, FormattedOutput)
        assert "Q4 Summary" in output.content or "Executive Summary" in output.content

    def test_technical_report(self, formatter):
        """Test technical report generation."""
        data = {
            "title": "Technical Analysis",
            "overview": "System analysis complete",
            "technical_details": {
                "architecture": "Microservices-based",
                "database": "PostgreSQL with replication",
            },
            "metrics": {
                "latency": {"value": "45ms", "score": 0.9},
                "throughput": {"value": "1000 req/s", "score": 0.85},
            },
        }

        output = formatter.technical_report(data, include_code=True)

        assert isinstance(output, FormattedOutput)
        assert "Technical" in output.content

    def test_stakeholder_update(self, formatter):
        """Test stakeholder update generation."""
        data = {
            "title": "Stakeholder Update",
            "period": "October 2025",
            "executive_summary": "Strong progress this month",
            "highlights": ["Feature A launched", "Performance improved 20%"],
            "progress": {
                "overall": 0.75,
                "on_track": True,
                "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
            },
        }

        output = formatter.stakeholder_update(data, stakeholder="Executive Team")

        assert isinstance(output, FormattedOutput)
        assert "Stakeholder Update" in output.content or "Executive" in output.content

    def test_apply_emoji_indicators(self, formatter):
        """Test emoji indicator application."""
        text = "Timeline health: timeline\nActivity health: activity"
        health_scores = {"timeline": 0.85, "activity": 0.65}

        result = formatter.apply_emoji_indicators(text, health_scores)

        # Check that emojis were added
        assert result != text
        assert len(result) > len(text)

    def test_format_date_relative(self, formatter):
        """Test relative date formatting."""
        # Test various time deltas
        now = datetime.now()

        # Just now
        result = formatter.format_date(now, DateStyle.RELATIVE)
        assert result == "just now"

        # Minutes ago
        past = now - timedelta(minutes=5)
        result = formatter.format_date(past, DateStyle.RELATIVE)
        assert "minute" in result.lower()

        # Hours ago
        past = now - timedelta(hours=3)
        result = formatter.format_date(past, DateStyle.RELATIVE)
        assert "hour" in result.lower()

        # Days ago
        past = now - timedelta(days=2)
        result = formatter.format_date(past, DateStyle.RELATIVE)
        assert "day" in result.lower()

    def test_format_date_absolute(self, formatter):
        """Test absolute date formatting."""
        dt = datetime(2025, 10, 2, 14, 30, 0)
        result = formatter.format_date(dt, DateStyle.ABSOLUTE)
        assert "2025-10-02" in result
        assert "14:30" in result

    def test_format_date_short(self, formatter):
        """Test short date formatting."""
        dt = datetime(2025, 10, 2)
        result = formatter.format_date(dt, DateStyle.SHORT)
        assert "Oct" in result
        assert "2025" in result

    def test_format_date_long(self, formatter):
        """Test long date formatting."""
        dt = datetime(2025, 10, 2, 14, 30)
        result = formatter.format_date(dt, DateStyle.LONG)
        assert "October" in result
        assert "2025" in result

    def test_format_date_iso(self, formatter):
        """Test ISO date formatting."""
        dt = datetime(2025, 10, 2, 14, 30)
        result = formatter.format_date(dt, DateStyle.ISO)
        assert result.startswith("2025-10-02")

    def test_format_date_string_input(self, formatter):
        """Test date formatting with string input."""
        date_str = "2025-10-02T14:30:00Z"
        result = formatter.format_date(date_str, DateStyle.SHORT)
        assert "Oct" in result
        assert "2025" in result

    def test_score_to_emoji(self, formatter):
        """Test score to emoji conversion."""
        assert formatter._score_to_emoji(0.9) == formatter.emoji.excellent
        assert formatter._score_to_emoji(0.7) == formatter.emoji.good
        assert formatter._score_to_emoji(0.5) == formatter.emoji.fair
        assert formatter._score_to_emoji(0.3) == formatter.emoji.poor
        assert formatter._score_to_emoji(0.1) == formatter.emoji.critical

    def test_format_health_score_default(self, formatter):
        """Test health score formatting with default rules."""
        result = formatter._format_health_score(0.75)
        assert "75" in result
        assert "%" in result

    def test_format_health_score_custom_rules(self, formatter):
        """Test health score formatting with custom rules."""
        rules = HealthScoreFormat(
            show_emoji=False,
            show_percentage=True,
            precision=1,
        )
        result = formatter._format_health_score(0.756, rules)
        assert "75.6%" in result

    def test_performance_stats(self, formatter, sample_health_data):
        """Test performance statistics tracking."""
        # Perform markdown operations (only these track render times)
        formatter.format_markdown(sample_health_data, "project_status")
        formatter.format_markdown(sample_health_data, "project_status")

        stats = formatter.get_performance_stats()

        assert stats["total_renders"] == 2
        assert stats["average_time_ms"] > 0
        assert stats["max_time_ms"] >= stats["min_time_ms"]
        assert stats["average_time_ms"] < 100  # Relaxed for first template loads

    def test_performance_requirement(self, formatter, sample_health_data):
        """Test that rendering meets <50ms performance requirement after warmup."""
        # Warm up template cache
        formatter.format_markdown(sample_health_data, "project_status")

        # Test with warmed cache - should be fast
        output = formatter.format_markdown(sample_health_data, "project_status")
        assert output.processing_time_ms < 50  # <50ms after cache warmup

    def test_jinja2_filters(self, formatter):
        """Test custom Jinja2 filters are registered."""
        assert "format_date" in formatter.env.filters
        assert "score_to_emoji" in formatter.env.filters
        assert "format_health_score" in formatter.env.filters
        assert "format_percentage" in formatter.env.filters

    def test_context_building(self, formatter):
        """Test template context building."""
        data = {"test": "value"}
        extra = {"custom": "variable"}

        ctx = formatter._build_context(data, extra)

        assert "data" in ctx
        assert ctx["data"] == data
        assert "custom" in ctx
        assert ctx["custom"] == "variable"
        assert "emoji" in ctx
        assert "now" in ctx
        assert callable(ctx["format_date"])


class TestOutputModels:
    """Test suite for output models."""

    def test_formatted_output(self):
        """Test FormattedOutput dataclass."""
        output = FormattedOutput(
            content="Test content",
            format=OutputFormat.MARKDOWN,
            metadata={"key": "value"},
            processing_time_ms=10.5,
            template_used="test.md.j2",
        )

        assert output.content == "Test content"
        assert output.format == OutputFormat.MARKDOWN
        assert output.metadata["key"] == "value"
        assert output.processing_time_ms == 10.5
        assert output.template_used == "test.md.j2"

    def test_table_column(self):
        """Test TableColumn dataclass."""
        col = TableColumn(
            name="Test Column",
            key="test_key",
            width=100,
            align="center",
        )

        assert col.name == "Test Column"
        assert col.key == "test_key"
        assert col.width == 100
        assert col.align == "center"

    def test_emoji_indicators(self):
        """Test EmojiIndicators dataclass."""
        emoji = EmojiIndicators()

        assert emoji.excellent == "🟢"
        assert emoji.good == "🟡"
        assert emoji.fair == "🟠"
        assert emoji.poor == "🔴"
        assert emoji.critical == "🚨"
        assert emoji.success == "✅"
        assert emoji.failure == "❌"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=tools.output_formatter", "--cov-report=term-missing"])

"""
OutputFormatter - Template-Based Output Generation

Consistent output generation across formats using Jinja2 templates.

Replaces 200-300 lines of template specifications per command with 5-10 lines:

    formatter = OutputFormatter()
    output = formatter.format_markdown(data, "project_status", context={"focus": "risks"})
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from tools.output_models import (
    AudienceType,
    DateStyle,
    EmojiIndicators,
    FormattedOutput,
    FormattingContext,
    HealthScoreFormat,
    OutputFormat,
    OutputSchema,
    TableColumn,
    TemplateMetadata,
)


class OutputFormatterError(Exception):
    """Base exception for OutputFormatter errors."""

    pass


class TemplateLoadError(OutputFormatterError):
    """Raised when template cannot be loaded."""

    pass


class OutputFormatter:
    """
    Template-based output generation system.

    Features:
    - Markdown, JSON, table, HTML formatting
    - Audience-specific content (executive, technical, stakeholder)
    - Jinja2 template system with caching
    - Emoji indicators and visual hierarchy
    - Date formatting with multiple styles
    - Performance: <50ms for template rendering

    Example:
        >>> formatter = OutputFormatter()
        >>> output = formatter.format_markdown(
        ...     health_data,
        ...     template="project_status",
        ...     context={"focus": "risks"}
        ... )
        >>> print(output.content)
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize OutputFormatter.

        Args:
            templates_dir: Custom templates directory (uses default if not provided)
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates" / "output"

        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False,  # We control the output
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters
        self._register_filters()

        # Initialize emoji indicators
        self.emoji = EmojiIndicators()

        # Performance tracking
        self._render_times = []

    def format_markdown(
        self,
        data: Dict[str, Any],
        template: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> FormattedOutput:
        """
        Format data as markdown using specified template.

        Replaces 200-300 lines of template specs with 5-10 lines.

        Args:
            data: Data to format
            template: Template name (without .md.j2 extension)
            context: Additional context for formatting

        Returns:
            FormattedOutput with rendered markdown

        Example:
            >>> output = formatter.format_markdown(
            ...     project_data,
            ...     "project_status",
            ...     context={"focus": "timeline"}
            ... )
        """
        start_time = time.time()

        # Build formatting context
        ctx = self._build_context(data, context or {})

        # Load and render template
        template_name = f"{template}.md.j2"
        try:
            tmpl = self.env.get_template(template_name)
            content = tmpl.render(**ctx)
        except TemplateNotFound:
            raise TemplateLoadError(f"Template not found: {template_name}")

        # Track performance
        render_time = (time.time() - start_time) * 1000
        self._render_times.append(render_time)

        return FormattedOutput(
            content=content,
            format=OutputFormat.MARKDOWN,
            metadata={"context": context},
            processing_time_ms=render_time,
            template_used=template_name,
        )

    def format_json(
        self,
        data: Dict[str, Any],
        schema: Optional[OutputSchema] = None,
        pretty: bool = True,
    ) -> FormattedOutput:
        """
        Format data as JSON with optional schema validation.

        Args:
            data: Data to format
            schema: Optional JSON schema for validation
            pretty: Pretty-print JSON (default: True)

        Returns:
            FormattedOutput with JSON content
        """
        start_time = time.time()

        # TODO: Add schema validation when schema provided
        warnings = []
        if schema:
            warnings.append("Schema validation not yet implemented")

        # Serialize to JSON
        if pretty:
            content = json.dumps(data, indent=2, default=str)
        else:
            content = json.dumps(data, default=str)

        render_time = (time.time() - start_time) * 1000

        return FormattedOutput(
            content=content,
            format=OutputFormat.JSON,
            metadata={"pretty": pretty, "schema": schema},
            processing_time_ms=render_time,
            warnings=warnings,
        )

    def format_table(
        self,
        data: List[Dict[str, Any]],
        columns: List[TableColumn],
    ) -> FormattedOutput:
        """
        Format data as markdown table.

        Args:
            data: List of row dictionaries
            columns: Column definitions

        Returns:
            FormattedOutput with markdown table
        """
        start_time = time.time()

        if not data:
            content = "_No data available_"
        else:
            # Build table header
            headers = [col.name for col in columns]
            header_row = "| " + " | ".join(headers) + " |"

            # Build alignment row
            alignment = []
            for col in columns:
                if col.align == "center":
                    alignment.append(":---:")
                elif col.align == "right":
                    alignment.append("---:")
                else:
                    alignment.append(":---")
            alignment_row = "| " + " | ".join(alignment) + " |"

            # Build data rows
            rows = []
            for row_data in data:
                row_values = []
                for col in columns:
                    value = row_data.get(col.key, "")
                    # Apply custom formatting function if provided
                    if col.format_fn:
                        value = col.format_fn(value)
                    row_values.append(str(value))
                rows.append("| " + " | ".join(row_values) + " |")

            # Combine all parts
            content = "\n".join([header_row, alignment_row] + rows)

        render_time = (time.time() - start_time) * 1000

        return FormattedOutput(
            content=content,
            format=OutputFormat.TABLE,
            metadata={"rows": len(data), "columns": len(columns)},
            processing_time_ms=render_time,
        )

    def executive_summary(
        self,
        data: Dict[str, Any],
        max_length: int = 500,
    ) -> FormattedOutput:
        """
        Generate executive summary (high-level, concise).

        Args:
            data: Data to summarize
            max_length: Maximum character length

        Returns:
            FormattedOutput with executive summary
        """
        context = {
            "audience": AudienceType.EXECUTIVE,
            "max_length": max_length,
        }
        return self.format_markdown(data, "executive_summary", context)

    def technical_report(
        self,
        data: Dict[str, Any],
        include_code: bool = True,
    ) -> FormattedOutput:
        """
        Generate technical report (detailed, code examples).

        Args:
            data: Data for report
            include_code: Include code examples

        Returns:
            FormattedOutput with technical report
        """
        context = {
            "audience": AudienceType.TECHNICAL,
            "include_code": include_code,
        }
        return self.format_markdown(data, "technical_report", context)

    def stakeholder_update(
        self,
        data: Dict[str, Any],
        stakeholder: Optional[str] = None,
    ) -> FormattedOutput:
        """
        Generate stakeholder-specific update.

        Args:
            data: Data for update
            stakeholder: Specific stakeholder name/role

        Returns:
            FormattedOutput with stakeholder update
        """
        context = {
            "audience": AudienceType.STAKEHOLDER,
            "stakeholder": stakeholder,
        }
        return self.format_markdown(data, "stakeholder_update", context)

    def apply_emoji_indicators(
        self,
        text: str,
        health_scores: Dict[str, float],
    ) -> str:
        """
        Apply emoji indicators based on health scores.

        Args:
            text: Text to augment with emojis
            health_scores: Dictionary of metric names to scores (0.0-1.0)

        Returns:
            Text with emoji indicators added
        """
        # Apply emoji based on score thresholds
        for metric, score in health_scores.items():
            emoji = self._score_to_emoji(score)
            # Replace metric name with emoji + metric name
            text = text.replace(metric, f"{emoji} {metric}")

        return text

    def format_date(
        self,
        date: Union[str, datetime],
        style: DateStyle = DateStyle.RELATIVE,
    ) -> str:
        """
        Format date according to style.

        Args:
            date: Date to format (ISO string or datetime object)
            style: Formatting style

        Returns:
            Formatted date string
        """
        # Convert to datetime if string
        if isinstance(date, str):
            try:
                dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
            except ValueError:
                return date  # Return as-is if parsing fails
        else:
            dt = date

        if style == DateStyle.RELATIVE:
            return self._format_relative_date(dt)
        elif style == DateStyle.ABSOLUTE:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        elif style == DateStyle.SHORT:
            return dt.strftime("%b %d, %Y")
        elif style == DateStyle.LONG:
            return dt.strftime("%B %d, %Y at %I:%M %p")
        elif style == DateStyle.ISO:
            return dt.isoformat()
        else:
            return str(dt)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for rendering operations."""
        if not self._render_times:
            return {
                "average_time_ms": 0.0,
                "max_time_ms": 0.0,
                "min_time_ms": 0.0,
                "total_renders": 0,
            }

        return {
            "average_time_ms": sum(self._render_times) / len(self._render_times),
            "max_time_ms": max(self._render_times),
            "min_time_ms": min(self._render_times),
            "total_renders": len(self._render_times),
        }

    # Private helper methods

    def _build_context(
        self,
        data: Dict[str, Any],
        extra_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build complete template context."""
        ctx = {
            "data": data,
            "emoji": self.emoji,
            "now": datetime.now(),
            "format_date": self.format_date,
            "score_to_emoji": self._score_to_emoji,
            "format_health_score": self._format_health_score,
        }
        ctx.update(extra_context)
        return ctx

    def _register_filters(self):
        """Register custom Jinja2 filters."""
        self.env.filters["format_date"] = self.format_date
        self.env.filters["score_to_emoji"] = self._score_to_emoji
        self.env.filters["format_health_score"] = self._format_health_score
        self.env.filters["format_percentage"] = lambda x: f"{x * 100:.1f}%"

    def _score_to_emoji(self, score: float) -> str:
        """Convert health score to emoji indicator."""
        if score >= 0.8:
            return self.emoji.excellent
        elif score >= 0.6:
            return self.emoji.good
        elif score >= 0.4:
            return self.emoji.fair
        elif score >= 0.2:
            return self.emoji.poor
        else:
            return self.emoji.critical

    def _format_health_score(
        self,
        score: float,
        format_rules: Optional[HealthScoreFormat] = None,
    ) -> str:
        """Format health score with emoji and percentage."""
        rules = format_rules or HealthScoreFormat()

        parts = []
        if rules.show_emoji:
            parts.append(self._score_to_emoji(score))

        if rules.show_percentage:
            parts.append(f"{score * 100:.{rules.precision}f}%")
        else:
            parts.append(f"{score:.{rules.precision}f}")

        return " ".join(parts)

    def _format_relative_date(self, dt: datetime) -> str:
        """Format date as relative time (e.g., '2 hours ago')."""
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        delta = now - dt

        if delta < timedelta(seconds=60):
            return "just now"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif delta < timedelta(days=30):
            weeks = delta.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif delta < timedelta(days=365):
            months = delta.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = delta.days // 365
            return f"{years} year{'s' if years != 1 else ''} ago"

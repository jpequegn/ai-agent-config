"""
ProjectStatusGenerator - Comprehensive Project Status Analysis Tool

Coordinates multi-source data collection, health calculation, and formatted output
generation for project status reporting.

Simplifies command implementation from 400+ lines to 15-20 lines:

    generator = ProjectStatusGenerator()
    status = generator.generate_status(project_id="mobile-app")
    print(status.formatted_output)
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.config_manager import ConfigManager
from tools.data_collector import DataCollector
from tools.health_calculator import HealthCalculator
from tools.note_processor import NoteProcessor
from tools.output_formatter import OutputFormatter
from tools.data_models import ProjectData
from tools.health_models import HealthScore, Risk, TrendAnalysis
from tools.output_models import FormattedOutput, OutputFormat


class ProjectStatusGeneratorError(Exception):
    """Base exception for ProjectStatusGenerator errors."""
    pass


class ProjectStatus:
    """
    Container for project status data and metadata.

    Attributes:
        project_name: Project identifier
        project_data: Aggregated project data from multiple sources
        health_score: Calculated health score
        trends: Trend analysis results
        risks: Identified risks and mitigations
        notes_analysis: Detailed note analysis
        formatted_output: Formatted output content
        processing_time_ms: Total processing time
    """

    def __init__(
        self,
        project_name: str,
        project_data: ProjectData,
        health_score: HealthScore,
        trends: Optional[TrendAnalysis] = None,
        risks: Optional[List[Risk]] = None,
        notes_analysis: Optional[Dict[str, Any]] = None,
        formatted_output: Optional[str] = None,
        processing_time_ms: float = 0.0,
    ):
        self.project_name = project_name
        self.project_data = project_data
        self.health_score = health_score
        self.trends = trends
        self.risks = risks or []
        self.notes_analysis = notes_analysis or {}
        self.formatted_output = formatted_output or ""
        self.processing_time_ms = processing_time_ms


class ProjectStatusGenerator:
    """
    Comprehensive project status analysis and reporting tool.

    Features:
    - Multi-source data aggregation (GitHub, notes, calendar, team)
    - Health scoring and trend analysis
    - Risk identification and assessment
    - Template-based output formatting
    - Performance tracking and caching

    Example:
        >>> generator = ProjectStatusGenerator()
        >>> # Single project detailed status
        >>> status = generator.generate_status(project_id="mobile-app")
        >>> print(status.formatted_output)
        >>>
        >>> # All projects overview
        >>> overview = generator.generate_overview()
        >>> print(overview.formatted_output)
        >>>
        >>> # Focus mode analysis
        >>> risks = generator.generate_status(
        ...     project_id="mobile-app",
        ...     focus="risks"
        ... )
    """

    def __init__(self, config_root: Optional[Path] = None):
        """
        Initialize ProjectStatusGenerator.

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

    def generate_status(
        self,
        project_id: Optional[str] = None,
        focus: Optional[str] = None,
        output_format: str = "markdown",
        include_json: bool = False,
    ) -> ProjectStatus:
        """
        Generate comprehensive project status for a single project.

        Args:
            project_id: Project identifier (required)
            focus: Focus area ("risks", "health", "trends", or None)
            output_format: Output format ("markdown" or "json")
            include_json: Whether to include JSON in markdown output

        Returns:
            ProjectStatus object with all analysis and formatted output

        Raises:
            ProjectStatusGeneratorError: If project not found or data collection fails

        Example:
            >>> status = generator.generate_status(
            ...     project_id="mobile-app",
            ...     focus="risks"
            ... )
            >>> print(f"Health: {status.health_score.category}")
            >>> print(status.formatted_output)
        """
        if not project_id:
            raise ProjectStatusGeneratorError("project_id is required for single project status")

        start_time = time.time()

        try:
            # Step 1: Collect data from all sources
            project_data = self.data_collector.aggregate_project_data(
                project_id=project_id,
                sources=["github", "notes", "calendar", "team", "config"]
            )

            # Step 2: Enhanced note analysis
            notes_analysis = self._analyze_notes(project_id)

            # Step 3: Calculate health score
            health_score = self.health_calculator.calculate_project_health(project_data)

            # Step 4: Analyze trends
            trends = self.health_calculator.analyze_trends(
                historical_data=project_data.history if hasattr(project_data, 'history') else [],
                time_window=30
            )

            # Step 5: Assess risks
            risks = self.health_calculator.assess_risks(project_data)

            # Step 6: Format output
            formatted_output = self._format_output(
                project_data=project_data,
                health_score=health_score,
                trends=trends,
                risks=risks,
                notes_analysis=notes_analysis,
                focus=focus,
                output_format=output_format,
                include_json=include_json,
            )

            processing_time = (time.time() - start_time) * 1000

            # Track performance
            self._performance_stats.append({
                "operation": "generate_status",
                "project_id": project_id,
                "processing_time_ms": processing_time,
                "timestamp": datetime.now().isoformat(),
            })

            return ProjectStatus(
                project_name=project_id,
                project_data=project_data,
                health_score=health_score,
                trends=trends,
                risks=risks,
                notes_analysis=notes_analysis,
                formatted_output=formatted_output,
                processing_time_ms=processing_time,
            )

        except Exception as e:
            raise ProjectStatusGeneratorError(
                f"Failed to generate status for project '{project_id}': {str(e)}"
            ) from e

    def generate_overview(
        self,
        filters: Optional[Dict[str, Any]] = None,
        output_format: str = "markdown",
    ) -> Dict[str, ProjectStatus]:
        """
        Generate overview of all active projects.

        Args:
            filters: Project filters (e.g., {"status": ["active", "in_progress"]})
            output_format: Output format ("markdown" or "json")

        Returns:
            Dictionary mapping project_id to ProjectStatus

        Example:
            >>> overview = generator.generate_overview(
            ...     filters={"status": ["active"]}
            ... )
            >>> for pid, status in overview.items():
            ...     print(f"{pid}: {status.health_score.category}")
        """
        start_time = time.time()

        # Get all projects matching filters
        default_filters = {"status": ["active", "in_progress"]}
        filters = filters or default_filters

        try:
            all_projects = self.config_manager.get_all_projects(filters=filters)

            overview = {}
            for project_id in all_projects:
                try:
                    status = self.generate_status(
                        project_id=project_id,
                        output_format=output_format,
                    )
                    overview[project_id] = status
                except Exception as e:
                    # Log error but continue with other projects
                    print(f"Warning: Failed to generate status for {project_id}: {e}")

            processing_time = (time.time() - start_time) * 1000

            # Track performance
            self._performance_stats.append({
                "operation": "generate_overview",
                "project_count": len(overview),
                "processing_time_ms": processing_time,
                "timestamp": datetime.now().isoformat(),
            })

            return overview

        except Exception as e:
            raise ProjectStatusGeneratorError(
                f"Failed to generate project overview: {str(e)}"
            ) from e

    def _analyze_notes(self, project_id: str) -> Dict[str, Any]:
        """
        Perform detailed note analysis for a project.

        Args:
            project_id: Project identifier

        Returns:
            Dictionary with note analysis metrics
        """
        try:
            project_notes = self.note_processor.get_project_notes(project_id)
            pending_actions = self.note_processor.get_action_items_by_status("pending", project=project_id)
            overdue_actions = self.note_processor.get_action_items_by_status("overdue", project=project_id)
            completed_actions = self.note_processor.get_action_items_by_status("completed", project=project_id)

            total_actions = len(pending_actions) + len(completed_actions)
            completion_rate = len(completed_actions) / total_actions if total_actions > 0 else 0.0

            return {
                "total_notes": len(project_notes),
                "pending_actions": len(pending_actions),
                "overdue_actions": len(overdue_actions),
                "completed_actions": len(completed_actions),
                "action_completion_rate": completion_rate,
                "notes": project_notes,
                "pending_items": pending_actions,
                "overdue_items": overdue_actions,
            }
        except Exception:
            # Graceful degradation if note analysis fails
            return {
                "total_notes": 0,
                "pending_actions": 0,
                "overdue_actions": 0,
                "completed_actions": 0,
                "action_completion_rate": 0.0,
                "notes": [],
                "pending_items": [],
                "overdue_items": [],
            }

    def _format_output(
        self,
        project_data: ProjectData,
        health_score: HealthScore,
        trends: Optional[TrendAnalysis],
        risks: List[Risk],
        notes_analysis: Dict[str, Any],
        focus: Optional[str],
        output_format: str,
        include_json: bool,
    ) -> str:
        """
        Format project status output using OutputFormatter.

        Args:
            project_data: Aggregated project data
            health_score: Calculated health score
            trends: Trend analysis
            risks: Risk list
            notes_analysis: Note analysis results
            focus: Focus area
            output_format: Output format
            include_json: Include JSON in markdown

        Returns:
            Formatted output string
        """
        # Prepare data for template
        template_data = {
            "project": project_data,
            "health": health_score,
            "trends": trends,
            "risks": risks,
            "notes": notes_analysis,
            "focus": focus,
        }

        if output_format == "json":
            result = self.output_formatter.format_json(template_data, pretty=True)
            return result.content
        else:
            # Use markdown template
            result = self.output_formatter.format_markdown(
                data=template_data,
                template="project_status",
                context={"focus": focus}
            )

            if include_json:
                json_result = self.output_formatter.format_json(template_data, pretty=True)
                return f"{result.content}\n\n## JSON Data\n\n```json\n{json_result.content}\n```"

            return result.content

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

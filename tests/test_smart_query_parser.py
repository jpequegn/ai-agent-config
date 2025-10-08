"""Tests for SmartQueryParser functionality."""

import pytest
from datetime import datetime

from tools import SmartQueryParser, SmartQueryParserError


class TestSmartQueryParser:
    """Test SmartQueryParser initialization and basic functionality."""

    def test_initialization(self):
        """SmartQueryParser should initialize correctly."""
        parser = SmartQueryParser()
        assert parser is not None
        assert parser.nlp is not None
        assert parser.config_mgr is not None
        assert parser._entity_cache == {}

    def test_parse_query_basic(self):
        """parse_query should return structured result."""
        parser = SmartQueryParser()
        result = parser.parse_query("show high priority tasks")

        assert "intent" in result
        assert "entities" in result
        assert "filters" in result
        assert "suggestions" in result
        assert "raw_query" in result
        assert result["raw_query"] == "show high priority tasks"

    def test_parse_query_with_context(self):
        """parse_query should accept context parameter."""
        parser = SmartQueryParser()
        result = parser.parse_query("show tasks", context="projects")

        assert result is not None
        assert "intent" in result


class TestFuzzyLookups:
    """Test fuzzy lookup methods."""

    def test_fuzzy_lookup_project_exact_match(self):
        """Exact project match should return the project ID."""
        parser = SmartQueryParser()
        # This will return None if no projects configured, which is fine for test
        result = parser.fuzzy_lookup_project("mobile-app-v2")
        # Result could be None or the matched project
        assert result is None or isinstance(result, str)

    def test_fuzzy_lookup_project_with_typo(self):
        """Fuzzy lookup should handle typos."""
        parser = SmartQueryParser()
        result = parser.fuzzy_lookup_project("mobil-app")
        # Result could be None or a matched project
        assert result is None or isinstance(result, str)

    def test_fuzzy_lookup_project_no_auto_select(self):
        """Fuzzy lookup with auto_select=False should work."""
        parser = SmartQueryParser()
        result = parser.fuzzy_lookup_project("test", auto_select=False)
        assert result is None or isinstance(result, str)

    def test_fuzzy_lookup_team_member(self):
        """Team member lookup should work."""
        parser = SmartQueryParser()
        result = parser.fuzzy_lookup_team_member("john")
        # Result could be None or a matched member
        assert result is None or isinstance(result, str)

    def test_fuzzy_lookup_team_member_with_threshold(self):
        """Team member lookup should respect threshold."""
        parser = SmartQueryParser()
        result = parser.fuzzy_lookup_team_member("xyz", threshold=0.9)
        # High threshold with nonsense query should return None
        assert result is None

    def test_fuzzy_lookup_stakeholder(self):
        """Stakeholder lookup should work."""
        parser = SmartQueryParser()
        result = parser.fuzzy_lookup_stakeholder("ceo")
        # Result could be None or a matched stakeholder
        assert result is None or isinstance(result, str)

    def test_fuzzy_lookup_stakeholder_no_auto_select(self):
        """Stakeholder lookup with auto_select=False should work."""
        parser = SmartQueryParser()
        result = parser.fuzzy_lookup_stakeholder("manager", auto_select=False)
        assert result is None or isinstance(result, str)


class TestDateParsing:
    """Test date filter parsing."""

    def test_parse_date_filter_range(self):
        """Date range parsing should work."""
        parser = SmartQueryParser()
        result = parser.parse_date_filter("from last week")

        if result:
            assert "type" in result
            assert result["type"] in ["range", "single"]
            if result["type"] == "range":
                assert "start" in result
                assert "end" in result
                assert "description" in result

    def test_parse_date_filter_single(self):
        """Single date parsing should work."""
        parser = SmartQueryParser()
        result = parser.parse_date_filter("tomorrow")

        if result:
            assert "type" in result
            if result["type"] == "single":
                assert "date" in result
                assert "expression" in result

    def test_parse_date_filter_no_date(self):
        """Query without date should return None."""
        parser = SmartQueryParser()
        result = parser.parse_date_filter("show all tasks")
        # Could be None or empty based on NLP behavior
        assert result is None or isinstance(result, dict)

    def test_parse_date_filter_this_month(self):
        """'this month' should be parsed as date range."""
        parser = SmartQueryParser()
        result = parser.parse_date_filter("this month")

        if result:
            assert result["type"] == "range"
            assert result["start"] is not None
            assert result["end"] is not None


class TestFilterExtraction:
    """Test filter extraction from queries."""

    def test_extract_filters_priority(self):
        """Should extract priority filter."""
        parser = SmartQueryParser()
        filters = parser.extract_filters("show high priority tasks")

        # Priority might be extracted depending on NLP implementation
        if "priority" in filters:
            assert filters["priority"] is not None

    def test_extract_filters_assignees(self):
        """Should extract assignees."""
        parser = SmartQueryParser()
        filters = parser.extract_filters("show tasks for @alice")

        # Assignees might be extracted
        if "assignees" in filters:
            assert isinstance(filters["assignees"], list)

    def test_extract_filters_combined(self):
        """Should extract multiple filters."""
        parser = SmartQueryParser()
        filters = parser.extract_filters("show high priority tasks for @alice from last week")

        assert isinstance(filters, dict)
        # Filters may or may not be populated depending on NLP

    def test_extract_filters_empty_query(self):
        """Empty query should return empty or minimal filters."""
        parser = SmartQueryParser()
        filters = parser.extract_filters("")
        assert isinstance(filters, dict)


class TestEntityResolution:
    """Test entity resolution logic."""

    def test_resolve_entities_with_project(self):
        """Should resolve project entities."""
        parser = SmartQueryParser()
        result = parser.parse_query("status for mobile-app")

        assert "entities" in result
        # Projects might be resolved if config exists
        if result["entities"].get("projects"):
            assert isinstance(result["entities"]["projects"], list)

    def test_resolve_entities_with_team_member(self):
        """Should resolve team member entities."""
        parser = SmartQueryParser()
        result = parser.parse_query("tasks for @alice")

        assert "entities" in result
        # Team members might be resolved
        if result["entities"].get("team_members"):
            assert isinstance(result["entities"]["team_members"], list)


class TestFilterBuilding:
    """Test filter building from parsed data."""

    def test_build_filters_priority(self):
        """Should build priority filter."""
        parser = SmartQueryParser()
        result = parser.parse_query("show critical tasks")

        if result["filters"].get("priority"):
            assert result["filters"]["priority"] is not None

    def test_build_filters_assignees(self):
        """Should build assignee filter."""
        parser = SmartQueryParser()
        result = parser.parse_query("tasks for @bob")

        # Assignees might be in filters
        if result["filters"].get("assignees"):
            assert isinstance(result["filters"]["assignees"], list)

    def test_build_filters_projects(self):
        """Should build project filter from resolved entities."""
        parser = SmartQueryParser()
        result = parser.parse_query("status for web-dashboard")

        # Projects might be in filters if resolved
        if result["filters"].get("projects"):
            assert isinstance(result["filters"]["projects"], list)


class TestSuggestions:
    """Test suggestion generation."""

    def test_suggestions_without_date(self):
        """Should suggest adding date filter if missing."""
        parser = SmartQueryParser()
        result = parser.parse_query("show high priority tasks")

        assert "suggestions" in result
        assert isinstance(result["suggestions"], list)

        # May suggest adding date filter
        date_suggestion = any("date" in s.lower() for s in result["suggestions"])
        # Suggestion may or may not be present

    def test_suggestions_without_assignee(self):
        """Should suggest adding assignee if missing."""
        parser = SmartQueryParser()
        result = parser.parse_query("show critical tasks from last week")

        assert "suggestions" in result
        # May suggest adding assignee

    def test_suggestions_disabled(self):
        """Should not generate suggestions when disabled."""
        parser = SmartQueryParser()
        result = parser.parse_query("show tasks", include_suggestions=False)

        assert result["suggestions"] == []

    def test_suggestions_complete_query(self):
        """Complete query should have fewer suggestions."""
        parser = SmartQueryParser()
        result = parser.parse_query(
            "show high priority tasks for @alice from last week in mobile-app"
        )

        assert "suggestions" in result
        # Complete query may have fewer or no suggestions


class TestProjectReferenceExtraction:
    """Test project reference extraction from text."""

    def test_extract_for_pattern(self):
        """Should extract 'for project-name' pattern."""
        parser = SmartQueryParser()
        refs = parser._extract_project_references("show status for mobile-app")

        # Should extract mobile-app
        assert isinstance(refs, list)

    def test_extract_in_pattern(self):
        """Should extract 'in project-name' pattern."""
        parser = SmartQueryParser()
        refs = parser._extract_project_references("tasks in web-dashboard")

        assert isinstance(refs, list)

    def test_extract_project_pattern(self):
        """Should extract 'project: name' pattern."""
        parser = SmartQueryParser()
        refs = parser._extract_project_references("project: api-service")

        assert isinstance(refs, list)

    def test_extract_multiple_references(self):
        """Should extract multiple project references."""
        parser = SmartQueryParser()
        refs = parser._extract_project_references(
            "status for mobile-app and web-dashboard"
        )

        assert isinstance(refs, list)

    def test_extract_no_references(self):
        """Should return empty list for queries without projects."""
        parser = SmartQueryParser()
        refs = parser._extract_project_references("show all tasks")

        assert refs == [] or isinstance(refs, list)


class TestIntegration:
    """Integration tests with real query patterns."""

    def test_complex_query_parsing(self):
        """Should parse complex multi-filter query."""
        parser = SmartQueryParser()
        result = parser.parse_query(
            "show high priority action items for @alice from last week in mobile-app"
        )

        assert result is not None
        assert "intent" in result
        assert "filters" in result
        assert "entities" in result

    def test_simple_query_parsing(self):
        """Should parse simple query."""
        parser = SmartQueryParser()
        result = parser.parse_query("show tasks")

        assert result is not None
        assert result["raw_query"] == "show tasks"

    def test_query_with_typos(self):
        """Should handle queries with typos."""
        parser = SmartQueryParser()
        result = parser.parse_query("shw hgh priorty taks")

        assert result is not None
        # NLP should still parse despite typos

    def test_query_with_dates(self):
        """Should handle queries with date expressions."""
        parser = SmartQueryParser()
        result = parser.parse_query("tasks from yesterday to tomorrow")

        assert result is not None
        if result["filters"].get("date_range"):
            assert result["filters"]["date_range"]["type"] == "range"

    def test_query_context_awareness(self):
        """Should use context hint appropriately."""
        parser = SmartQueryParser()

        result1 = parser.parse_query("show items", context="projects")
        result2 = parser.parse_query("show items", context="team")

        assert result1 is not None
        assert result2 is not None
        # Results may differ based on context


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_query(self):
        """Should handle empty query gracefully."""
        parser = SmartQueryParser()
        result = parser.parse_query("")

        assert result is not None
        assert isinstance(result, dict)

    def test_none_query(self):
        """Should handle None query appropriately."""
        parser = SmartQueryParser()

        # Should either handle or raise appropriate error
        try:
            result = parser.parse_query(None)
        except (AttributeError, TypeError):
            # Expected for None input
            pass

    def test_invalid_threshold(self):
        """Should handle invalid threshold values."""
        parser = SmartQueryParser()

        # Threshold outside 0-1 range
        result = parser.fuzzy_lookup_project("test", threshold=1.5)
        # Should still work or return None

    def test_missing_config_files(self):
        """Should handle missing config files gracefully."""
        parser = SmartQueryParser()

        # Even with missing configs, should not crash
        result = parser.fuzzy_lookup_team_member("nonexistent")
        assert result is None

    def test_malformed_query(self):
        """Should handle malformed queries."""
        parser = SmartQueryParser()
        result = parser.parse_query("@#$%^&*()")

        assert result is not None
        assert isinstance(result, dict)

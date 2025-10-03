"""Tests for NLPProcessor natural language processing utilities."""

import pytest
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from tools.nlp_processor import NLPProcessor, DateParsingError
from tools.nlp_models import (
    ActionType,
    CommandIntent,
    DateExpression,
    DateRange,
    Priority,
    SubjectType,
)


@pytest.fixture
def nlp():
    """Create NLPProcessor with fixed reference date."""
    reference_date = datetime(2024, 10, 1, 12, 0, 0)
    return NLPProcessor(reference_date=reference_date)


@pytest.fixture
def reference_date():
    """Fixed reference date for tests."""
    return datetime(2024, 10, 1, 12, 0, 0)


class TestDateParsing:
    """Test date expression parsing."""

    def test_parse_tomorrow(self, nlp, reference_date):
        """Test parsing 'tomorrow'."""
        result = nlp.parse_date_expression("tomorrow")
        expected = reference_date + timedelta(days=1)
        assert result.resolved_date.date() == expected.date()
        assert result.expression_type == "relative"

    def test_parse_yesterday(self, nlp, reference_date):
        """Test parsing 'yesterday'."""
        result = nlp.parse_date_expression("yesterday")
        expected = reference_date - timedelta(days=1)
        assert result.resolved_date.date() == expected.date()

    def test_parse_today(self, nlp, reference_date):
        """Test parsing 'today'."""
        result = nlp.parse_date_expression("today")
        assert result.resolved_date.date() == reference_date.date()

    def test_parse_next_week(self, nlp, reference_date):
        """Test parsing 'next week'."""
        result = nlp.parse_date_expression("next week")
        expected = reference_date + timedelta(weeks=1)
        assert result.resolved_date.date() == expected.date()

    def test_parse_last_month(self, nlp, reference_date):
        """Test parsing 'last month'."""
        result = nlp.parse_date_expression("last month")
        expected = reference_date - relativedelta(months=1)
        assert result.resolved_date.date() == expected.date()

    def test_parse_in_n_days(self, nlp, reference_date):
        """Test parsing 'in 3 days'."""
        result = nlp.parse_date_expression("in 3 days")
        expected = reference_date + timedelta(days=3)
        assert result.resolved_date.date() == expected.date()

    def test_parse_days_ago(self, nlp, reference_date):
        """Test parsing '5 days ago'."""
        result = nlp.parse_date_expression("5 days ago")
        expected = reference_date - timedelta(days=5)
        assert result.resolved_date.date() == expected.date()

    def test_parse_absolute_date_iso(self, nlp):
        """Test parsing ISO format date."""
        result = nlp.parse_date_expression("2024-12-25")
        assert result.resolved_date.date() == datetime(2024, 12, 25).date()
        assert result.expression_type == "absolute"

    def test_parse_absolute_date_us(self, nlp):
        """Test parsing US format date."""
        result = nlp.parse_date_expression("12/25/2024")
        assert result.resolved_date.date() == datetime(2024, 12, 25).date()

    def test_parse_invalid_date(self, nlp):
        """Test parsing invalid date raises error."""
        with pytest.raises(DateParsingError):
            nlp.parse_date_expression("invalid date string")

    def test_parse_date_with_custom_reference(self):
        """Test parsing with custom reference date."""
        custom_ref = datetime(2024, 6, 15)
        nlp = NLPProcessor(reference_date=custom_ref)
        result = nlp.parse_date_expression("tomorrow")
        assert result.resolved_date.date() == datetime(2024, 6, 16).date()


class TestDateRangeParsing:
    """Test date range expression parsing."""

    def test_parse_this_week(self, nlp, reference_date):
        """Test parsing 'this week'."""
        result = nlp.parse_date_range("this week")
        # Tuesday Oct 1, 2024 -> week starts Monday Sep 30
        assert result.start.date() == datetime(2024, 9, 30).date()
        assert result.end.date() == datetime(2024, 10, 6).date()

    def test_parse_this_month(self, nlp, reference_date):
        """Test parsing 'this month'."""
        result = nlp.parse_date_range("this month")
        assert result.start.date() == datetime(2024, 10, 1).date()
        assert result.end.date() == datetime(2024, 10, 31).date()

    def test_parse_this_year(self, nlp, reference_date):
        """Test parsing 'this year'."""
        result = nlp.parse_date_range("this year")
        assert result.start.date() == datetime(2024, 1, 1).date()
        assert result.end.date() == datetime(2024, 12, 31).date()

    def test_date_range_contains(self, nlp):
        """Test DateRange.contains method."""
        date_range = nlp.parse_date_range("this month")
        assert date_range.contains(datetime(2024, 10, 15))
        assert not date_range.contains(datetime(2024, 11, 1))

    def test_date_range_duration(self, nlp):
        """Test DateRange.duration_days method."""
        date_range = nlp.parse_date_range("this month")
        assert date_range.duration_days() == 30  # October has 31 days


class TestAssigneeExtraction:
    """Test assignee extraction."""

    def test_extract_at_mentions(self, nlp):
        """Test extracting @mentions."""
        assignees = nlp.extract_assignees("@john @sarah please review")
        assert assignees == ["john", "sarah"]

    def test_extract_comma_separated(self, nlp):
        """Test extracting comma-separated names."""
        assignees = nlp.extract_assignees("assignees: john,sarah,mike")
        assert "john" in assignees
        assert "sarah" in assignees
        assert "mike" in assignees

    def test_extract_and_separated(self, nlp):
        """Test extracting 'and' separated names."""
        assignees = nlp.extract_assignees("assign to john and sarah")
        assert "john" in assignees
        assert "sarah" in assignees

    def test_extract_mixed_formats(self, nlp):
        """Test extracting mixed formats."""
        # Note: sarah needs context keyword to be extracted
        assignees = nlp.extract_assignees("assign to @john, sarah and @mike")
        assert "john" in assignees
        assert "sarah" in assignees
        assert "mike" in assignees

    def test_extract_no_duplicates(self, nlp):
        """Test that duplicates are removed."""
        assignees = nlp.extract_assignees("assign to @john @john john")
        assert assignees.count("john") == 1

    def test_extract_empty(self, nlp):
        """Test extraction with no assignees."""
        # Without context keywords, names won't be extracted
        assignees = nlp.extract_assignees("regular text without context")
        assert len(assignees) == 0


class TestPriorityExtraction:
    """Test priority extraction."""

    def test_extract_bracket_format(self, nlp):
        """Test extracting [high] format."""
        assert nlp.extract_priorities("[high] priority task") == Priority.HIGH
        assert nlp.extract_priorities("[medium] task") == Priority.MEDIUM
        assert nlp.extract_priorities("[low] priority") == Priority.LOW

    def test_extract_keyword(self, nlp):
        """Test extracting priority keywords."""
        assert nlp.extract_priorities("urgent task") == Priority.CRITICAL
        assert nlp.extract_priorities("critical bug") == Priority.CRITICAL
        assert nlp.extract_priorities("high priority") == Priority.HIGH
        assert nlp.extract_priorities("normal task") == Priority.MEDIUM
        assert nlp.extract_priorities("low priority") == Priority.LOW

    def test_extract_colon_format(self, nlp):
        """Test extracting priority:value format."""
        assert nlp.extract_priorities("priority: high") == Priority.HIGH
        assert nlp.extract_priorities("priority:medium") == Priority.MEDIUM

    def test_extract_no_priority(self, nlp):
        """Test extraction with no priority."""
        assert nlp.extract_priorities("regular task") is None

    def test_extract_first_priority(self, nlp):
        """Test that first priority is returned."""
        # "urgent" maps to CRITICAL and should be found first
        result = nlp.extract_priorities("urgent high low")
        assert result == Priority.CRITICAL


class TestCommandIntentParsing:
    """Test command intent parsing."""

    def test_parse_find_notes(self, nlp):
        """Test parsing 'find notes' command."""
        intent = nlp.parse_command_intent("find notes about budget")
        assert intent.action == ActionType.FIND
        assert intent.subject == SubjectType.NOTES
        assert intent.get_filter("query") == "budget"

    def test_parse_show_projects(self, nlp):
        """Test parsing 'show projects' command."""
        intent = nlp.parse_command_intent("show projects")
        assert intent.action == ActionType.SHOW
        assert intent.subject == SubjectType.PROJECTS

    def test_parse_create_task(self, nlp):
        """Test parsing 'create task' command."""
        intent = nlp.parse_command_intent("create task for implementation")
        assert intent.action == ActionType.CREATE
        assert intent.subject == SubjectType.TASKS

    def test_parse_with_date_range(self, nlp):
        """Test parsing command with date range."""
        intent = nlp.parse_command_intent("find notes from last month")
        assert intent.action == ActionType.FIND
        assert intent.subject == SubjectType.NOTES
        assert "date_range" in intent.filters

    def test_parse_with_assignees(self, nlp):
        """Test parsing command with assignees."""
        intent = nlp.parse_command_intent("show tasks for @john and @sarah")
        assert intent.subject == SubjectType.TASKS
        assert "assignees" in intent.filters
        assert "john" in intent.filters["assignees"]
        assert "sarah" in intent.filters["assignees"]

    def test_parse_with_priority(self, nlp):
        """Test parsing command with priority."""
        intent = nlp.parse_command_intent("list high priority tasks")
        assert intent.subject == SubjectType.TASKS
        assert intent.get_filter("priority") == "high"

    def test_parse_complex_command(self, nlp):
        """Test parsing complex command."""
        intent = nlp.parse_command_intent(
            "find notes about budget from last month assigned to @john [high]"
        )
        assert intent.action == ActionType.FIND
        assert intent.subject == SubjectType.NOTES
        assert intent.get_filter("query") == "budget"
        assert "date_range" in intent.filters
        assert "john" in intent.get_filter("assignees", [])
        assert intent.get_filter("priority") == "high"

    def test_parse_confidence_scoring(self, nlp):
        """Test confidence scoring."""
        # Full intent with action and subject
        intent1 = nlp.parse_command_intent("find notes")
        assert intent1.confidence == 1.0

        # Only action
        intent2 = nlp.parse_command_intent("find something")
        assert intent2.confidence == 0.75

        # Neither action nor subject
        intent3 = nlp.parse_command_intent("random text")
        assert intent3.confidence == 0.5


class TestFuzzyMatching:
    """Test fuzzy matching."""

    def test_fuzzy_match_exact(self, nlp):
        """Test exact match."""
        candidates = ["mobile-app-v2", "web-portal", "api-service"]
        matches = nlp.fuzzy_match("mobile-app-v2", candidates)
        assert len(matches) > 0
        assert matches[0].candidate == "mobile-app-v2"
        assert matches[0].score == 1.0

    def test_fuzzy_match_typo(self, nlp):
        """Test match with typo."""
        candidates = ["mobile-app-v2", "web-portal", "api-service"]
        matches = nlp.fuzzy_match("mobil", candidates, threshold=0.5)
        assert len(matches) > 0
        # "mobil" should match "mobile-app-v2" even with lower threshold
        assert any("mobile" in match.candidate for match in matches)

    def test_fuzzy_match_threshold(self, nlp):
        """Test threshold filtering."""
        candidates = ["mobile-app-v2", "web-portal", "api-service"]
        matches = nlp.fuzzy_match("xyz", candidates, threshold=0.9)
        assert len(matches) == 0

    def test_fuzzy_match_sorted(self, nlp):
        """Test results are sorted by score."""
        candidates = ["mobile-app", "mobile-app-v2", "mobile"]
        matches = nlp.fuzzy_match("mobile", candidates, threshold=0.5)
        assert len(matches) >= 2
        # Scores should be descending
        for i in range(len(matches) - 1):
            assert matches[i].score >= matches[i + 1].score

    def test_fuzzy_match_empty_candidates(self, nlp):
        """Test with empty candidates."""
        matches = nlp.fuzzy_match("query", [])
        assert len(matches) == 0

    def test_fuzzy_match_confidence(self, nlp):
        """Test FuzzyMatch.is_confident method."""
        candidates = ["mobile-app-v2"]
        matches = nlp.fuzzy_match("mobile-app-v2", candidates)
        assert matches[0].is_confident(threshold=0.8)
        assert not matches[0].is_confident(threshold=1.1)


class TestEntityExtraction:
    """Test entity extraction."""

    def test_extract_all_entities(self, nlp):
        """Test extracting all entity types."""
        entities = nlp.extract_entities("@john urgent task tomorrow")
        assert len(entities) >= 2  # assignee, priority, date

        entity_types = {e.entity_type for e in entities}
        assert "assignee" in entity_types
        assert "priority" in entity_types
        assert "date" in entity_types

    def test_extract_specific_entities(self, nlp):
        """Test extracting specific entity types."""
        entities = nlp.extract_entities(
            "assign to @john", entity_types=["assignee"]
        )
        assert len(entities) == 1
        assert entities[0].entity_type == "assignee"
        assert entities[0].value == "john"

    def test_extract_with_positions(self, nlp):
        """Test entity positions are captured."""
        entities = nlp.extract_entities("assign to @john", entity_types=["assignee"])
        assert entities[0].start_position is not None
        assert entities[0].end_position is not None

    def test_extract_no_entities(self, nlp):
        """Test extraction with no matching entities."""
        # Without context keywords, no entities extracted
        entities = nlp.extract_entities("regular text without context", entity_types=["assignee"])
        assert len(entities) == 0


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_text_parsing(self, nlp):
        """Test parsing empty text."""
        intent = nlp.parse_command_intent("")
        assert intent.action is None
        assert intent.subject is None

    def test_special_characters(self, nlp):
        """Test handling special characters."""
        assignees = nlp.extract_assignees("assign to @user_name-123")
        assert "user_name-123" in assignees

    def test_case_insensitivity(self, nlp):
        """Test case insensitive parsing."""
        intent1 = nlp.parse_command_intent("FIND NOTES")
        intent2 = nlp.parse_command_intent("find notes")
        assert intent1.action == intent2.action
        assert intent1.subject == intent2.subject

    def test_unicode_text(self, nlp):
        """Test handling unicode text."""
        intent = nlp.parse_command_intent("find notes about café")
        assert "café" in intent.get_filter("query", "")

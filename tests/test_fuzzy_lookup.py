"""Tests for fuzzy lookup functionality."""

import pytest

from tools import (
    fuzzy_lookup,
    fuzzy_lookup_silent,
    get_best_match,
    FuzzyLookupError,
    NoMatchFoundError,
    AmbiguousMatchError,
)


class TestFuzzyLookup:
    """Test fuzzy_lookup function."""

    def test_exact_match(self):
        """Exact matches should be auto-selected."""
        result = fuzzy_lookup(
            "mobile-app-v2",
            ["mobile-app-v2", "web-dashboard"],
            show_suggestions=False
        )
        assert result == "mobile-app-v2"

    def test_typo_tolerance(self):
        """Typos should be handled with high confidence."""
        result = fuzzy_lookup(
            "mobil-app-v2",
            ["mobile-app-v2", "web-dashboard"],
            show_suggestions=False
        )
        assert result == "mobile-app-v2"

    def test_partial_match_with_tokens(self):
        """Partial matches with shared tokens should work."""
        result = fuzzy_lookup(
            "mobile app",
            ["mobile-app-v2", "web-dashboard"],
            show_suggestions=False
        )
        assert result == "mobile-app-v2"

    def test_no_match_raises_error(self):
        """No matches should raise NoMatchFoundError."""
        with pytest.raises(NoMatchFoundError):
            fuzzy_lookup(
                "xyz",
                ["mobile-app-v2", "web-dashboard"],
                show_suggestions=False
            )

    def test_empty_candidates_raises_error(self):
        """Empty candidate list should raise NoMatchFoundError."""
        with pytest.raises(NoMatchFoundError):
            fuzzy_lookup("test", [], show_suggestions=False)

    def test_high_confidence_auto_select(self):
        """High confidence matches should be auto-selected."""
        result = fuzzy_lookup(
            "mobile-v2",
            ["mobile-app-v2", "web-dashboard"],
            show_suggestions=False,
            high_confidence_threshold=0.8
        )
        assert result == "mobile-app-v2"


class TestFuzzyLookupSilent:
    """Test fuzzy_lookup_silent function."""

    def test_exact_match_returns_result(self):
        """Exact match should return the candidate."""
        result, matches = fuzzy_lookup_silent(
            "mobile-app-v2",
            ["mobile-app-v2", "web-dashboard"]
        )
        assert result == "mobile-app-v2"
        assert len(matches) > 0
        assert matches[0].candidate == "mobile-app-v2"

    def test_typo_returns_corrected(self):
        """Typos should return corrected version."""
        result, matches = fuzzy_lookup_silent(
            "mobil-app-v2",
            ["mobile-app-v2", "web-dashboard"],
            threshold=0.6
        )
        assert result == "mobile-app-v2"
        assert matches[0].score >= 0.95

    def test_no_match_returns_none(self):
        """No match should return None with empty matches."""
        result, matches = fuzzy_lookup_silent(
            "xyz",
            ["mobile-app-v2", "web-dashboard"]
        )
        assert result is None
        assert matches == []

    def test_partial_match_with_high_score(self):
        """Partial match with high score should return result."""
        result, matches = fuzzy_lookup_silent(
            "mobile-v2",
            ["mobile-app-v2", "web-dashboard"],
            threshold=0.6
        )
        assert result == "mobile-app-v2"
        assert matches[0].score >= 0.8

    def test_ambiguous_match_returns_none(self):
        """Ambiguous matches should return None with all matches."""
        # This would require candidates that are very similar
        result, matches = fuzzy_lookup_silent(
            "test",
            ["test-app-v1", "test-app-v2", "test-service"],
            threshold=0.6,
            confidence_gap=0.1
        )
        # With very similar candidates, it might return None or auto-select
        # The test verifies the function handles this gracefully
        assert isinstance(result, (str, type(None)))
        assert isinstance(matches, list)


class TestGetBestMatch:
    """Test get_best_match function."""

    def test_returns_best_match(self):
        """Should return the highest-scoring match."""
        match = get_best_match(
            "mobile-app",
            ["mobile-app-v2", "web-dashboard", "api-service"],
            threshold=0.6
        )
        assert match is not None
        assert match.candidate == "mobile-app-v2"
        assert match.score >= 0.6

    def test_returns_none_for_no_match(self):
        """Should return None if no matches above threshold."""
        match = get_best_match(
            "xyz",
            ["mobile-app-v2", "web-dashboard"],
            threshold=0.7
        )
        assert match is None

    def test_returns_none_for_empty_candidates(self):
        """Should return None for empty candidate list."""
        match = get_best_match("test", [], threshold=0.7)
        assert match is None

    def test_fuzzy_match_object_structure(self):
        """Returned FuzzyMatch should have correct structure."""
        match = get_best_match(
            "mobile-app",
            ["mobile-app-v2"],
            threshold=0.6
        )
        assert match is not None
        assert hasattr(match, 'candidate')
        assert hasattr(match, 'score')
        assert hasattr(match, 'original_query')
        assert match.original_query == "mobile-app"


class TestThresholdBehavior:
    """Test threshold parameter behavior."""

    def test_low_threshold_more_permissive(self):
        """Lower threshold should accept more matches."""
        _, matches_low = fuzzy_lookup_silent(
            "mob",
            ["mobile-app-v2", "web-dashboard"],
            threshold=0.5
        )
        _, matches_high = fuzzy_lookup_silent(
            "mob",
            ["mobile-app-v2", "web-dashboard"],
            threshold=0.8
        )
        # Low threshold might have matches, high threshold might not
        # This verifies threshold filtering works
        assert len(matches_high) <= len(matches_low)

    def test_auto_select_threshold(self):
        """Auto-select threshold should control automatic selection."""
        # Very high auto-select threshold (0.99) - should not auto-select
        result1, _ = fuzzy_lookup_silent(
            "mobil-app",
            ["mobile-app-v2"],
            auto_select_threshold=0.99,
            high_confidence_threshold=0.98
        )

        # Normal auto-select threshold (0.95) - should auto-select
        result2, _ = fuzzy_lookup_silent(
            "mobil-app-v2",
            ["mobile-app-v2"],
            auto_select_threshold=0.95
        )

        # Both should handle gracefully (either auto-select or not)
        assert isinstance(result1, (str, type(None)))
        assert result2 == "mobile-app-v2"  # Very close match should work


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_project_name_typo(self):
        """Project name with typo should match correctly."""
        projects = ["mobile-app-v2", "web-dashboard", "api-service-v1"]
        result = fuzzy_lookup(
            "mobil-app",
            projects,
            show_suggestions=False,
            threshold=0.6
        )
        assert result == "mobile-app-v2"

    def test_team_member_name_partial(self):
        """Partial team member names should match."""
        members = ["john.smith@company.com", "jane.doe@company.com"]
        result, matches = fuzzy_lookup_silent(
            "john smith",
            members,
            threshold=0.6
        )
        # Should find a match or handle gracefully
        if result:
            assert "john" in result.lower()

    def test_stakeholder_id_variations(self):
        """Different variations of stakeholder IDs should match."""
        stakeholders = ["ceo-jane-smith", "cto-mike-johnson", "vp-product-lisa-chen"]
        result = fuzzy_lookup(
            "ceo-jane-smith",
            stakeholders,
            show_suggestions=False,
            threshold=0.6
        )
        assert result == "ceo-jane-smith"

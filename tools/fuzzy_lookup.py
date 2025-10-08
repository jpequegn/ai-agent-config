"""
Fuzzy lookup utilities for command parameter matching.

Provides intelligent fuzzy matching for project names, team members, stakeholders,
and other entities with automatic selection and "did you mean" suggestions.
"""

from typing import List, Optional, Tuple

from tools.nlp_processor import NLPProcessor
from tools.nlp_models import FuzzyMatch


class FuzzyLookupError(Exception):
    """Base exception for fuzzy lookup errors."""
    pass


class NoMatchFoundError(FuzzyLookupError):
    """No fuzzy match found for the given query."""
    pass


class AmbiguousMatchError(FuzzyLookupError):
    """Multiple potential matches with similar confidence scores."""
    def __init__(self, query: str, matches: List[FuzzyMatch]):
        self.query = query
        self.matches = matches
        super().__init__(f"Multiple matches found for '{query}'")


def fuzzy_lookup(
    query: str,
    candidates: List[str],
    threshold: float = 0.7,
    auto_select_threshold: float = 0.95,
    high_confidence_threshold: float = 0.8,
    confidence_gap: float = 0.2,
    show_suggestions: bool = True,
    max_suggestions: int = 3,
) -> Optional[str]:
    """
    Fuzzy lookup with automatic selection or suggestions.

    Handles typos, partial matches, and provides "did you mean" suggestions.
    Uses NLPProcessor's fuzzy_match for consistent matching logic.

    Args:
        query: Search query (can contain typos or be partial)
        candidates: List of valid candidate strings to match against
        threshold: Minimum confidence threshold (0.0-1.0, default 0.7)
        auto_select_threshold: Auto-select if match score >= this (default 0.95)
        high_confidence_threshold: High confidence threshold (default 0.8)
        confidence_gap: Minimum gap between top 2 matches for auto-select (default 0.2)
        show_suggestions: Print "did you mean" suggestions (default True)
        max_suggestions: Maximum number of suggestions to show (default 3)

    Returns:
        - Matched candidate string if auto-selected (high confidence)
        - None if no matches or ambiguous (suggestions printed if enabled)

    Raises:
        NoMatchFoundError: If no matches found above threshold
        AmbiguousMatchError: If multiple matches with similar scores

    Examples:
        >>> # Exact match (auto-selected)
        >>> fuzzy_lookup("mobile-app-v2", ["mobile-app-v2", "web-dashboard"])
        'mobile-app-v2'

        >>> # Typo tolerance (auto-selected)
        >>> fuzzy_lookup("mobil-app", ["mobile-app-v2", "web-dashboard"])
        Using 'mobile-app-v2' (matched 'mobil-app')
        'mobile-app-v2'

        >>> # Partial match (auto-selected)
        >>> fuzzy_lookup("mobile", ["mobile-app-v2", "web-dashboard"])
        Using 'mobile-app-v2' (matched 'mobile')
        'mobile-app-v2'

        >>> # Ambiguous (suggestions shown)
        >>> fuzzy_lookup("jo", ["john-smith", "joanna-lee", "joe-wilson"])
        No exact match for 'jo'. Did you mean:
          1. john-smith (85% match)
          2. joanna-lee (82% match)
          3. joe-wilson (78% match)
        None

        >>> # No match (empty list)
        >>> fuzzy_lookup("xyz", ["mobile-app-v2", "web-dashboard"])
        No match found for 'xyz'
        Available options: mobile-app-v2, web-dashboard
        None
    """
    if not candidates:
        if show_suggestions:
            print(f"No candidates provided for lookup")
        raise NoMatchFoundError(f"No candidates provided for lookup")

    # Use NLPProcessor for fuzzy matching
    nlp = NLPProcessor()
    matches = nlp.fuzzy_match(query, candidates, threshold=threshold)

    if not matches:
        if show_suggestions:
            print(f"No match found for '{query}'")
            if len(candidates) <= 10:
                print(f"Available options: {', '.join(candidates)}")
            else:
                print(f"Available options: {', '.join(candidates[:10])}... ({len(candidates)} total)")
        raise NoMatchFoundError(f"No match found for '{query}'")

    best = matches[0]

    # Auto-select if very high confidence (exact or near-exact match)
    if best.score >= auto_select_threshold:
        return best.candidate

    # Auto-select if high confidence and clear winner
    if best.score >= high_confidence_threshold:
        if len(matches) == 1 or (best.score - matches[1].score) >= confidence_gap:
            if show_suggestions and best.score < auto_select_threshold:
                print(f"Using '{best.candidate}' (matched '{query}')")
            return best.candidate

    # Ambiguous - show suggestions
    if show_suggestions:
        print(f"No exact match for '{query}'. Did you mean:")
        for i, match in enumerate(matches[:max_suggestions], 1):
            percentage = int(match.score * 100)
            print(f"  {i}. {match.candidate} ({percentage}% match)")

    raise AmbiguousMatchError(query, matches[:max_suggestions])


def fuzzy_lookup_silent(
    query: str,
    candidates: List[str],
    threshold: float = 0.7,
    auto_select_threshold: float = 0.95,
    high_confidence_threshold: float = 0.8,
    confidence_gap: float = 0.2,
) -> Tuple[Optional[str], List[FuzzyMatch]]:
    """
    Silent fuzzy lookup that returns match and suggestions without printing.

    Same logic as fuzzy_lookup but returns data instead of printing suggestions.
    Useful for programmatic usage or custom suggestion display.

    Args:
        query: Search query
        candidates: List of valid candidates
        threshold: Minimum confidence threshold (default 0.7)
        auto_select_threshold: Auto-select threshold (default 0.95)
        high_confidence_threshold: High confidence threshold (default 0.8)
        confidence_gap: Minimum gap for auto-select (default 0.2)

    Returns:
        Tuple of (matched_candidate, all_matches)
        - matched_candidate is None if ambiguous or no match
        - all_matches is list of FuzzyMatch objects

    Examples:
        >>> result, matches = fuzzy_lookup_silent("mobile", ["mobile-app-v2"])
        >>> result
        'mobile-app-v2'
        >>> matches
        [FuzzyMatch(candidate='mobile-app-v2', score=0.92, original_query='mobile')]

        >>> result, matches = fuzzy_lookup_silent("jo", ["john", "joanna", "joe"])
        >>> result
        None
        >>> len(matches)
        3
    """
    if not candidates:
        return None, []

    # Use NLPProcessor for fuzzy matching
    nlp = NLPProcessor()
    matches = nlp.fuzzy_match(query, candidates, threshold=threshold)

    if not matches:
        return None, []

    best = matches[0]

    # Auto-select if very high confidence
    if best.score >= auto_select_threshold:
        return best.candidate, matches

    # Auto-select if high confidence and clear winner
    if best.score >= high_confidence_threshold:
        if len(matches) == 1 or (best.score - matches[1].score) >= confidence_gap:
            return best.candidate, matches

    # Ambiguous or low confidence
    return None, matches


def get_best_match(query: str, candidates: List[str], threshold: float = 0.7) -> Optional[FuzzyMatch]:
    """
    Get the best fuzzy match without auto-selection logic.

    Returns the highest-scoring match above threshold, or None.
    Useful when you want the raw best match without selection rules.

    Args:
        query: Search query
        candidates: List of valid candidates
        threshold: Minimum confidence threshold (default 0.7)

    Returns:
        FuzzyMatch object with highest score, or None if no matches

    Example:
        >>> match = get_best_match("mobile", ["mobile-app-v2", "web-app"])
        >>> match.candidate
        'mobile-app-v2'
        >>> match.score
        0.92
    """
    if not candidates:
        return None

    nlp = NLPProcessor()
    matches = nlp.fuzzy_match(query, candidates, threshold=threshold)

    return matches[0] if matches else None

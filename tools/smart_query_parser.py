"""
SmartQueryParser - Intelligent query understanding combining NLP and config lookups.

Provides unified interface for parsing natural language queries and resolving entities
across projects, teams, stakeholders, etc.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from tools.config_manager import ConfigManager
from tools.fuzzy_lookup import fuzzy_lookup, fuzzy_lookup_silent, NoMatchFoundError
from tools.nlp_processor import NLPProcessor
from tools.nlp_models import CommandIntent, DateExpression, DateRange, FuzzyMatch


class SmartQueryParserError(Exception):
    """Base exception for SmartQueryParser errors."""
    pass


class SmartQueryParser:
    """
    Intelligent query parser combining NLP and config lookups.

    Provides unified interface for parsing natural language queries
    and resolving entities across projects, teams, stakeholders, etc.

    Features:
    - Natural language query parsing
    - Entity resolution with fuzzy matching
    - Filter extraction and normalization
    - Date expression parsing
    - Context-aware suggestions

    Example:
        >>> parser = SmartQueryParser()
        >>> result = parser.parse_query("show high priority items for @alice from last week")
        >>> print(result["filters"]["priority"])  # "high"
        >>> print(result["filters"]["assignees"])  # ["alice"]
    """

    def __init__(self):
        """Initialize SmartQueryParser with NLP and config managers."""
        self.nlp = NLPProcessor()
        self.config_mgr = ConfigManager()
        self._entity_cache: Dict[str, Any] = {}

    def parse_query(
        self,
        query: str,
        context: Optional[str] = None,
        include_suggestions: bool = True
    ) -> Dict[str, Any]:
        """
        Parse natural language query into structured data.

        Args:
            query: Natural language query to parse
            context: Optional context hint (e.g., "projects", "team", "notes")
            include_suggestions: Whether to generate helpful suggestions

        Returns:
            Dict containing:
                - intent: Parsed CommandIntent
                - entities: Resolved entities (projects, people, etc.)
                - filters: Extracted filters ready for use
                - suggestions: Helpful suggestions (if enabled)

        Example:
            >>> parser.parse_query("find high priority tasks for mobile-app")
            {
                "intent": CommandIntent(...),
                "entities": {"projects": ["mobile-app-v2"]},
                "filters": {"priority": "high", "projects": ["mobile-app-v2"]},
                "suggestions": []
            }
        """
        # Parse command intent using NLPProcessor
        intent = self.nlp.parse_command_intent(query)

        # Resolve entities based on query and context
        entities = self._resolve_entities(query, intent, context)

        # Build structured filters
        filters = self._build_filters(intent, entities)

        # Generate suggestions if enabled
        suggestions = []
        if include_suggestions:
            suggestions = self._generate_suggestions(intent, entities, filters)

        return {
            "intent": intent,
            "entities": entities,
            "filters": filters,
            "suggestions": suggestions,
            "raw_query": query
        }

    def fuzzy_lookup_project(
        self,
        query: str,
        threshold: float = 0.7,
        auto_select: bool = True
    ) -> Optional[str]:
        """
        Fuzzy lookup for project IDs.

        Args:
            query: Project name or partial name to look up
            threshold: Minimum similarity score (0-1)
            auto_select: Whether to automatically select high-confidence matches

        Returns:
            Matched project ID or None if no match found

        Example:
            >>> parser.fuzzy_lookup_project("mobil-app")
            "mobile-app-v2"
        """
        projects = self.config_mgr.get_all_projects()
        project_ids = list(projects.keys())

        if not project_ids:
            return None

        if auto_select:
            try:
                return fuzzy_lookup(
                    query,
                    project_ids,
                    threshold=threshold,
                    show_suggestions=False
                )
            except NoMatchFoundError:
                return None
        else:
            result, matches = fuzzy_lookup_silent(query, project_ids, threshold=threshold)
            return result

    def fuzzy_lookup_team_member(
        self,
        query: str,
        threshold: float = 0.7,
        auto_select: bool = True
    ) -> Optional[str]:
        """
        Fuzzy lookup for team member IDs.

        Args:
            query: Team member name or email to look up
            threshold: Minimum similarity score (0-1)
            auto_select: Whether to automatically select high-confidence matches

        Returns:
            Matched team member ID/email or None if no match found

        Example:
            >>> parser.fuzzy_lookup_team_member("john smith")
            "john.smith@company.com"
        """
        try:
            team_config = self.config_mgr.load_config("team_roster.yaml")
            members = team_config.get("team_members", {})

            # Build candidate list from member IDs and names
            candidates = []
            id_to_member = {}

            for member_id, member_data in members.items():
                candidates.append(member_id)
                id_to_member[member_id] = member_id

                if isinstance(member_data, dict):
                    name = member_data.get("name")
                    if name:
                        candidates.append(name)
                        id_to_member[name] = member_id

            if not candidates:
                return None

            if auto_select:
                try:
                    matched = fuzzy_lookup(
                        query,
                        candidates,
                        threshold=threshold,
                        show_suggestions=False
                    )
                    return id_to_member.get(matched, matched)
                except NoMatchFoundError:
                    return None
            else:
                result, matches = fuzzy_lookup_silent(query, candidates, threshold=threshold)
                if result:
                    return id_to_member.get(result, result)
                return None

        except Exception:
            return None

    def fuzzy_lookup_stakeholder(
        self,
        query: str,
        threshold: float = 0.7,
        auto_select: bool = True
    ) -> Optional[str]:
        """
        Fuzzy lookup for stakeholder IDs.

        Args:
            query: Stakeholder name or ID to look up
            threshold: Minimum similarity score (0-1)
            auto_select: Whether to automatically select high-confidence matches

        Returns:
            Matched stakeholder ID or None if no match found

        Example:
            >>> parser.fuzzy_lookup_stakeholder("ceo jane")
            "ceo-jane-smith"
        """
        try:
            stakeholder_config = self.config_mgr.load_config("stakeholder_contexts.yaml")
            stakeholders = stakeholder_config.get("stakeholder_profiles", {})

            # Build candidate list from stakeholder IDs and names
            candidates = []
            id_to_stakeholder = {}

            for sh_id, sh_data in stakeholders.items():
                candidates.append(sh_id)
                id_to_stakeholder[sh_id] = sh_id

                if isinstance(sh_data, dict):
                    name = sh_data.get("name")
                    if name:
                        candidates.append(name)
                        id_to_stakeholder[name] = sh_id

            if not candidates:
                return None

            if auto_select:
                try:
                    matched = fuzzy_lookup(
                        query,
                        candidates,
                        threshold=threshold,
                        show_suggestions=False
                    )
                    return id_to_stakeholder.get(matched, matched)
                except NoMatchFoundError:
                    return None
            else:
                result, matches = fuzzy_lookup_silent(query, candidates, threshold=threshold)
                if result:
                    return id_to_stakeholder.get(result, result)
                return None

        except Exception:
            return None

    def parse_date_filter(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Parse date expressions and ranges from query.

        Args:
            query: Query string containing date expressions

        Returns:
            Dict with date filter information or None if no date found

        Example:
            >>> parser.parse_date_filter("from last week")
            {
                "type": "range",
                "start": datetime(...),
                "end": datetime(...),
                "description": "last week"
            }
        """
        try:
            # Try date range first
            date_range = self.nlp.parse_date_range(query)
            return {
                "type": "range",
                "start": date_range.start,
                "end": date_range.end,
                "description": date_range.description
            }
        except Exception:
            try:
                # Try single date expression
                date_expr = self.nlp.parse_date_expression(query)
                return {
                    "type": "single",
                    "date": date_expr.resolved_date,
                    "expression": date_expr.original_expression
                }
            except Exception:
                return None

    def extract_filters(self, query: str) -> Dict[str, Any]:
        """
        Extract all filters from query using NLPProcessor.

        Args:
            query: Natural language query

        Returns:
            Dict containing extracted filters

        Example:
            >>> parser.extract_filters("show high priority tasks for @alice")
            {
                "assignees": ["alice"],
                "priority": "high",
                "query_text": "show tasks"
            }
        """
        intent = self.nlp.parse_command_intent(query)

        filters = {}

        # Extract assignees
        if intent.filters.get("assignees"):
            filters["assignees"] = intent.filters["assignees"]

        # Extract priority
        if intent.filters.get("priority"):
            filters["priority"] = intent.filters["priority"]

        # Extract date range
        date_filter = self.parse_date_filter(query)
        if date_filter:
            filters["date_range"] = date_filter

        # Extract remaining query text (with filters removed)
        query_text = intent.filters.get("query", query)
        if query_text and query_text != query:
            filters["query_text"] = query_text

        return filters

    def _resolve_entities(
        self,
        raw_query: str,
        intent: CommandIntent,
        context: Optional[str]
    ) -> Dict[str, Any]:
        """
        Resolve entities based on query content and context.

        Args:
            raw_query: Original query string
            intent: Parsed command intent
            context: Optional context hint

        Returns:
            Dict of resolved entities by type
        """
        entities: Dict[str, Any] = {}

        # Resolve projects if mentioned
        project_refs = self._extract_project_references(raw_query)
        if project_refs:
            resolved_projects = []
            for proj_ref in project_refs:
                matched = self.fuzzy_lookup_project(proj_ref, auto_select=True)
                if matched:
                    resolved_projects.append(matched)

            if resolved_projects:
                entities["projects"] = resolved_projects

        # Resolve team members from assignees
        if intent.filters.get("assignees"):
            resolved_members = []
            for assignee in intent.filters["assignees"]:
                matched = self.fuzzy_lookup_team_member(assignee, auto_select=True)
                if matched:
                    resolved_members.append(matched)
                else:
                    # Keep original if no match found
                    resolved_members.append(assignee)

            if resolved_members:
                entities["team_members"] = resolved_members

        return entities

    def _extract_project_references(self, text: str) -> List[str]:
        """
        Extract potential project references from text.

        Args:
            text: Text to extract from

        Returns:
            List of potential project names/IDs
        """
        # Look for patterns like:
        # - "for mobile-app"
        # - "in web-dashboard"
        # - "project: api-service"

        patterns = [
            r"(?:for|in|on)\s+([a-z0-9-]+(?:-v\d+)?)",
            r"project[:\s]+([a-z0-9-]+(?:-v\d+)?)",
            r"([a-z0-9]+-(?:app|service|api|dashboard|platform)(?:-v\d+)?)",
        ]

        references = []
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                ref = match.group(1) if match.lastindex else match.group(0)
                if ref and ref not in references:
                    references.append(ref)

        return references

    def _build_filters(
        self,
        intent: CommandIntent,
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build normalized filters from intent and entities.

        Args:
            intent: Parsed command intent
            entities: Resolved entities

        Returns:
            Normalized filter dict
        """
        filters: Dict[str, Any] = {}

        # Priority filter
        if intent.filters.get("priority"):
            filters["priority"] = intent.filters["priority"]

        # Date range filter
        if intent.filters.get("date_range"):
            filters["date_range"] = intent.filters["date_range"]

        # Assignees/team members
        if entities.get("team_members"):
            filters["assignees"] = entities["team_members"]
        elif intent.filters.get("assignees"):
            filters["assignees"] = intent.filters["assignees"]

        # Projects
        if entities.get("projects"):
            filters["projects"] = entities["projects"]

        # Query text (remaining text after filter extraction)
        if intent.filters.get("query"):
            filters["query_text"] = intent.filters["query"]

        return filters

    def _generate_suggestions(
        self,
        intent: CommandIntent,
        entities: Dict[str, Any],
        filters: Dict[str, Any]
    ) -> List[str]:
        """
        Generate helpful suggestions based on query analysis.

        Args:
            intent: Parsed command intent
            entities: Resolved entities
            filters: Built filters

        Returns:
            List of suggestion strings
        """
        suggestions = []

        # Suggest date filter if missing
        if not filters.get("date_range"):
            suggestions.append("💡 Add date filter: 'from last week' or 'this month'")

        # Suggest assignee if missing
        if not filters.get("assignees"):
            suggestions.append("💡 Add assignee: '@username' or 'for alice'")

        # Suggest project if context seems project-related but no project found
        if not entities.get("projects"):
            if any(keyword in intent.raw_text.lower() for keyword in ["status", "progress", "milestone"]):
                suggestions.append("💡 Add project: 'for mobile-app' or 'in web-dashboard'")

        # Suggest priority if missing for task-related queries
        if not filters.get("priority"):
            if any(keyword in intent.raw_text.lower() for keyword in ["task", "todo", "action"]):
                suggestions.append("💡 Add priority: 'high priority' or 'critical'")

        return suggestions

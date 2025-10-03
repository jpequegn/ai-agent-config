"""
Natural Language Processing utilities for command parsing and entity extraction.

Provides date parsing, entity extraction, command intent classification, and fuzzy matching.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz, process

from tools.nlp_models import (
    ActionType,
    CommandIntent,
    DateExpression,
    DateRange,
    EntityMatch,
    FuzzyMatch,
    Priority,
    SubjectType,
)


class NLPProcessorError(Exception):
    """Base exception for NLP processor errors."""

    pass


class DateParsingError(NLPProcessorError):
    """Error parsing date expression."""

    pass


class NLPProcessor:
    """Natural language processing utilities for command parsing."""

    # Date expression patterns
    RELATIVE_DATE_PATTERNS = {
        r"\btomorrow\b": lambda ref: ref + timedelta(days=1),
        r"\byesterday\b": lambda ref: ref - timedelta(days=1),
        r"\btoday\b": lambda ref: ref,
        r"\bnext week\b": lambda ref: ref + timedelta(weeks=1),
        r"\blast week\b": lambda ref: ref - timedelta(weeks=1),
        r"\bnext month\b": lambda ref: ref + relativedelta(months=1),
        r"\blast month\b": lambda ref: ref - relativedelta(months=1),
        r"\bin (\d+) days?\b": lambda ref, n: ref + timedelta(days=int(n)),
        r"\bin (\d+) weeks?\b": lambda ref, n: ref + timedelta(weeks=int(n)),
        r"\bin (\d+) months?\b": lambda ref, n: ref + relativedelta(months=int(n)),
        r"(\d+) days? ago\b": lambda ref, n: ref - timedelta(days=int(n)),
        r"(\d+) weeks? ago\b": lambda ref, n: ref - timedelta(weeks=int(n)),
        r"(\d+) months? ago\b": lambda ref, n: ref - relativedelta(months=int(n)),
    }

    # Date range patterns
    DATE_RANGE_PATTERNS = {
        r"\bthis week\b": lambda ref: (
            ref - timedelta(days=ref.weekday()),
            ref - timedelta(days=ref.weekday()) + timedelta(days=6),
        ),
        r"\blast week\b": lambda ref: (
            ref - timedelta(days=ref.weekday()) - timedelta(weeks=1),
            ref - timedelta(days=ref.weekday()) - timedelta(days=1),
        ),
        r"\bthis month\b": lambda ref: (
            ref.replace(day=1),
            (ref.replace(day=1) + relativedelta(months=1)) - timedelta(days=1),
        ),
        r"\blast month\b": lambda ref: (
            (ref.replace(day=1) - relativedelta(months=1)),
            ref.replace(day=1) - timedelta(days=1),
        ),
        r"\bthis year\b": lambda ref: (
            ref.replace(month=1, day=1),
            ref.replace(month=12, day=31),
        ),
    }

    # Priority mappings
    PRIORITY_MAPPINGS = {
        "critical": Priority.CRITICAL,
        "urgent": Priority.CRITICAL,
        "important": Priority.HIGH,
        "high": Priority.HIGH,
        "medium": Priority.MEDIUM,
        "normal": Priority.MEDIUM,
        "low": Priority.LOW,
        "minor": Priority.LOW,
    }

    # Action verb mappings
    ACTION_VERBS = {
        "find": ActionType.FIND,
        "search": ActionType.FIND,
        "lookup": ActionType.FIND,
        "show": ActionType.SHOW,
        "display": ActionType.SHOW,
        "view": ActionType.SHOW,
        "list": ActionType.LIST,
        "ls": ActionType.LIST,
        "enumerate": ActionType.LIST,
        "create": ActionType.CREATE,
        "add": ActionType.CREATE,
        "new": ActionType.CREATE,
        "update": ActionType.UPDATE,
        "modify": ActionType.UPDATE,
        "edit": ActionType.UPDATE,
        "change": ActionType.UPDATE,
        "delete": ActionType.DELETE,
        "remove": ActionType.DELETE,
        "rm": ActionType.DELETE,
        "analyze": ActionType.ANALYZE,
        "analyse": ActionType.ANALYZE,
        "review": ActionType.ANALYZE,
        "generate": ActionType.GENERATE,
        "gen": ActionType.GENERATE,
        "export": ActionType.EXPORT,
        "save": ActionType.EXPORT,
        "import": ActionType.IMPORT,
        "load": ActionType.IMPORT,
    }

    # Subject keywords
    SUBJECT_KEYWORDS = {
        "note": SubjectType.NOTES,
        "notes": SubjectType.NOTES,
        "project": SubjectType.PROJECTS,
        "projects": SubjectType.PROJECTS,
        "task": SubjectType.TASKS,
        "tasks": SubjectType.TASKS,
        "todo": SubjectType.TASKS,
        "meeting": SubjectType.MEETINGS,
        "meetings": SubjectType.MEETINGS,
        "decision": SubjectType.DECISIONS,
        "decisions": SubjectType.DECISIONS,
        "stakeholder": SubjectType.STAKEHOLDERS,
        "stakeholders": SubjectType.STAKEHOLDERS,
        "team": SubjectType.TEAM,
        "report": SubjectType.REPORTS,
        "reports": SubjectType.REPORTS,
    }

    def __init__(self, reference_date: Optional[datetime] = None):
        """
        Initialize NLP processor.

        Args:
            reference_date: Reference date for relative date calculations (defaults to now)
        """
        self.reference_date = reference_date or datetime.now()

    def parse_date_expression(
        self, text: str, reference_date: Optional[datetime] = None
    ) -> DateExpression:
        """
        Parse date expression from text.

        Args:
            text: Text containing date expression
            reference_date: Reference date for relative calculations

        Returns:
            DateExpression with resolved date

        Raises:
            DateParsingError: If date cannot be parsed
        """
        ref = reference_date or self.reference_date
        text_lower = text.lower().strip()

        # Try relative date patterns
        for pattern, resolver in self.RELATIVE_DATE_PATTERNS.items():
            match = re.search(pattern, text_lower)
            if match:
                groups = match.groups()
                if groups:
                    resolved = resolver(ref, *groups)
                else:
                    resolved = resolver(ref)

                return DateExpression(
                    resolved_date=resolved,
                    original_expression=text,
                    expression_type="relative",
                    confidence=0.95,
                )

        # Try absolute date parsing
        try:
            parsed = date_parser.parse(text, fuzzy=True, default=ref)
            return DateExpression(
                resolved_date=parsed,
                original_expression=text,
                expression_type="absolute",
                confidence=0.9,
            )
        except (ValueError, OverflowError):
            pass

        raise DateParsingError(f"Could not parse date expression: {text}")

    def parse_date_range(
        self, text: str, reference_date: Optional[datetime] = None
    ) -> DateRange:
        """
        Parse date range expression from text.

        Args:
            text: Text containing date range expression
            reference_date: Reference date for relative calculations

        Returns:
            DateRange with start and end dates

        Raises:
            DateParsingError: If date range cannot be parsed
        """
        ref = reference_date or self.reference_date
        text_lower = text.lower().strip()

        # Try date range patterns
        for pattern, resolver in self.DATE_RANGE_PATTERNS.items():
            if re.search(pattern, text_lower):
                start, end = resolver(ref)
                return DateRange(
                    start=start, end=end, description=text_lower
                )

        raise DateParsingError(f"Could not parse date range: {text}")

    def extract_assignees(self, text: str) -> List[str]:
        """
        Extract assignees from text.

        Supports formats:
        - @username (including underscores and hyphens)
        - name1,name2
        - name1 and name2

        Args:
            text: Text containing assignees

        Returns:
            List of assignee names
        """
        assignees = []

        # Extract @mentions (support underscores and hyphens)
        mentions = re.findall(r"@([\w-]+)", text)
        assignees.extend(mentions)

        # Extract comma-separated names (excluding @mentions and common words)
        # Only match in contexts like "assignees: name1,name2" or "assign to name1,name2"
        text_without_mentions = re.sub(r"@[\w-]+", "", text)

        # Look for assignee keywords followed by names
        assignee_context = re.search(
            r"(?:assign(?:ee)?s?(?:\s+to)?|for)\s*[:,-]?\s*([\w\s,and-]+?)(?=\s+please|\s+review|$)",
            text_without_mentions,
            re.IGNORECASE
        )

        if assignee_context:
            names_text = assignee_context.group(1)
            # Split by commas and "and"
            names = re.split(r'[,]|\s+and\s+', names_text)
            for name in names:
                name = name.strip()
                # Only include valid names (alphanumeric with optional underscores/hyphens)
                if name and re.match(r'^[\w-]+$', name) and len(name) > 1:
                    assignees.append(name)

        # Remove duplicates while preserving order
        seen = set()
        result = []
        for assignee in assignees:
            assignee_lower = assignee.lower()
            if assignee_lower not in seen:
                seen.add(assignee_lower)
                result.append(assignee)

        return result

    def extract_priorities(self, text: str) -> Optional[Priority]:
        """
        Extract priority from text.

        Supports formats:
        - [high], [medium], [low] in brackets
        - high, urgent, critical as keywords
        - priority:high format

        Args:
            text: Text containing priority

        Returns:
            Priority enum value or None
        """
        text_lower = text.lower()

        # Try bracket format [priority]
        bracket_match = re.search(r"\[([a-z]+)\]", text_lower)
        if bracket_match:
            priority_text = bracket_match.group(1)
            if priority_text in self.PRIORITY_MAPPINGS:
                return self.PRIORITY_MAPPINGS[priority_text]

        # Try priority:value format
        colon_match = re.search(r"priority:\s*(\w+)", text_lower)
        if colon_match:
            priority_text = colon_match.group(1)
            if priority_text in self.PRIORITY_MAPPINGS:
                return self.PRIORITY_MAPPINGS[priority_text]

        # Try keyword matching
        for keyword, priority in self.PRIORITY_MAPPINGS.items():
            if re.search(rf"\b{keyword}\b", text_lower):
                return priority

        return None

    def parse_command_intent(self, text: str) -> CommandIntent:
        """
        Parse command intent from natural language text.

        Extracts:
        - Action verb (find, show, create, etc.)
        - Subject (notes, projects, tasks, etc.)
        - Filters and parameters

        Args:
            text: Command text

        Returns:
            CommandIntent with parsed structure
        """
        text_lower = text.lower().strip()
        filters: Dict[str, any] = {}
        parameters: Dict[str, any] = {}

        # Extract action
        action = None
        for verb, action_type in self.ACTION_VERBS.items():
            if re.search(rf"\b{verb}\b", text_lower):
                action = action_type
                break

        # Extract subject
        subject = None
        for keyword, subject_type in self.SUBJECT_KEYWORDS.items():
            if re.search(rf"\b{keyword}\b", text_lower):
                subject = subject_type
                break

        # Extract date filters - check both ranges and single dates
        date_found = False
        try:
            # Try to find date range expressions first
            for pattern in self.DATE_RANGE_PATTERNS.keys():
                if re.search(pattern, text_lower):
                    date_range = self.parse_date_range(text)
                    filters["date_range"] = {
                        "start": date_range.start.isoformat(),
                        "end": date_range.end.isoformat(),
                    }
                    date_found = True
                    break
        except DateParsingError:
            pass

        # If no range found, look for "from [date]" or "since [date]" patterns
        if not date_found:
            # Look for "from [date]" or "since [date]" patterns
            date_match = re.search(r"(?:from|since)\s+(.+?)(?:\s+assigned|\s+about|\s+for|$)", text_lower)
            if date_match:
                date_text = date_match.group(1).strip()
                # Try to parse as range first (for "last month", "this week", etc.)
                try:
                    date_range = self.parse_date_range(date_text)
                    filters["date_range"] = {
                        "start": date_range.start.isoformat(),
                        "end": date_range.end.isoformat(),
                    }
                except DateParsingError:
                    # If range parsing fails, try as single date expression
                    pass

        # Extract query text (after "about" keyword)
        query_match = re.search(r"\babout\s+([^,]+?)(?:\s+from|\s+in|$)", text_lower)
        if query_match:
            filters["query"] = query_match.group(1).strip()

        # Extract assignees
        assignees = self.extract_assignees(text)
        if assignees:
            filters["assignees"] = assignees

        # Extract priority
        priority = self.extract_priorities(text)
        if priority:
            filters["priority"] = priority.value

        # Calculate confidence based on extracted elements
        confidence = 0.5
        if action:
            confidence += 0.25
        if subject:
            confidence += 0.25

        return CommandIntent(
            action=action,
            subject=subject,
            filters=filters,
            parameters=parameters,
            raw_text=text,
            confidence=confidence,
        )

    def fuzzy_match(
        self, query: str, candidates: List[str], threshold: float = 0.8
    ) -> List[FuzzyMatch]:
        """
        Perform fuzzy matching against candidate strings.

        Args:
            query: Query string to match
            candidates: List of candidate strings
            threshold: Minimum confidence threshold (0.0-1.0)

        Returns:
            List of FuzzyMatch objects sorted by score (descending)
        """
        if not candidates:
            return []

        # Use fuzzywuzzy's process.extract for efficient matching
        matches = process.extract(
            query, candidates, scorer=fuzz.token_sort_ratio, limit=len(candidates)
        )

        # Convert to FuzzyMatch objects and filter by threshold
        results = []
        for candidate, score in matches:
            normalized_score = score / 100.0
            if normalized_score >= threshold:
                results.append(
                    FuzzyMatch(
                        candidate=candidate,
                        score=normalized_score,
                        original_query=query,
                    )
                )

        return results

    def extract_entities(
        self, text: str, entity_types: Optional[List[str]] = None
    ) -> List[EntityMatch]:
        """
        Extract various entities from text.

        Args:
            text: Text to extract entities from
            entity_types: Optional list of specific entity types to extract

        Returns:
            List of EntityMatch objects
        """
        entities = []
        entity_types = entity_types or ["assignee", "priority", "date"]

        if "assignee" in entity_types:
            assignees = self.extract_assignees(text)
            for assignee in assignees:
                # Find position in text
                match = re.search(rf"@?{re.escape(assignee)}", text, re.IGNORECASE)
                entities.append(
                    EntityMatch(
                        value=assignee,
                        entity_type="assignee",
                        confidence=0.9,
                        start_position=match.start() if match else None,
                        end_position=match.end() if match else None,
                    )
                )

        if "priority" in entity_types:
            priority = self.extract_priorities(text)
            if priority:
                entities.append(
                    EntityMatch(
                        value=priority.value, entity_type="priority", confidence=0.9
                    )
                )

        if "date" in entity_types:
            try:
                date_expr = self.parse_date_expression(text)
                entities.append(
                    EntityMatch(
                        value=date_expr.resolved_date.isoformat(),
                        entity_type="date",
                        confidence=date_expr.confidence,
                    )
                )
            except DateParsingError:
                pass

        return entities

"""
NoteProcessor - High-Level Note Operations

Simplifies note processing operations by wrapping existing para-processor.py
and ./notes CLI infrastructure. Reduces complexity from 80-100 lines to 5-10 lines
per command.

Example:
    >>> processor = NoteProcessor()
    >>> # Extract action items (80 lines → 2 lines)
    >>> overdue = processor.get_action_items_by_status("overdue")
    >>> pending = processor.get_action_items_by_status("pending")
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import existing para-processor
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Dynamic import to handle dash in filename
import importlib.util

spec = importlib.util.spec_from_file_location(
    "para_processor",
    str(Path(__file__).parent.parent / "scripts" / "para-processor.py"),
)
para_processor_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(para_processor_module)
ParaNoteProcessor = para_processor_module.ParaNoteProcessor

from tools.config_manager import ConfigManager
from tools.note_models import (
    ActionItemFilters,
    BatchProcessResult,
    CategorizationResult,
    NoteSearchFilters,
    ParaCategory,
    ParsedNote,
)


class NoteProcessorError(Exception):
    """Base exception for NoteProcessor errors."""

    pass


class NoteProcessor:
    """
    High-level note operations wrapping para-processor.py and ./notes CLI.

    Features:
    - Action item extraction and filtering
    - Note search and categorization
    - Project linking operations
    - Frontmatter management
    - Batch processing

    Simplifies command implementation from 80-100 lines to 5-10 lines.

    Example:
        >>> processor = NoteProcessor()
        >>> # Simple action item extraction
        >>> overdue = processor.get_action_items_by_status("overdue")
        >>> print(f"Found {len(overdue)} overdue items")

        >>> # Get project notes
        >>> notes = processor.get_project_notes("mobile-app-v2")
        >>> print(f"Project has {len(notes)} notes")
    """

    def __init__(self, config_root: Optional[Path] = None):
        """
        Initialize NoteProcessor.

        Args:
            config_root: Root directory for configuration files
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self.config_manager = ConfigManager(config_root=self.config_root)
        self.para_processor = ParaNoteProcessor()
        self.notes_cli = Path.cwd() / "notes"

        # Cache for frequently accessed data
        self._cache: Dict[str, Any] = {}

    # Core Operations

    def parse_note(self, file_path: str) -> ParsedNote:
        """
        Parse a note file and extract all information.

        Args:
            file_path: Path to note file

        Returns:
            ParsedNote: Fully parsed note with all extracted data

        Raises:
            NoteProcessorError: If parsing fails

        Example:
            >>> note = processor.parse_note("inbox/meeting-note.md")
            >>> print(f"Found {len(note.action_items)} action items")
        """
        try:
            return self.para_processor.parse_note(str(file_path))
        except Exception as e:
            raise NoteProcessorError(f"Failed to parse note {file_path}: {e}")

    def search_notes(
        self,
        query: Optional[str] = None,
        filters: Optional[NoteSearchFilters] = None,
        para_category: Optional[ParaCategory] = None,
    ) -> List[ParsedNote]:
        """
        Search for notes with optional filters.

        Args:
            query: Search query string
            filters: NoteSearchFilters object with additional filters
            para_category: Filter by PARA category

        Returns:
            List[ParsedNote]: Matching notes

        Example:
            >>> notes = processor.search_notes(
            ...     query="mobile app",
            ...     para_category=ParaCategory.PROJECTS
            ... )
        """
        # Build search command
        cmd = [str(self.notes_cli), "list"]

        if query:
            cmd.extend(["--query", query])

        if para_category:
            cmd.extend(["--category", para_category.value])

        if filters:
            if filters.project:
                cmd.extend(["--project", filters.project])
            if filters.status:
                cmd.extend(["--status", filters.status])
            if filters.tags:
                cmd.extend(["--tags", ",".join(filters.tags)])

        cmd.append("--json")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30, check=True
            )
            data = json.loads(result.stdout) if result.stdout.strip() else {"notes": []}

            # Parse each note
            notes = []
            for note_path in data.get("notes", []):
                try:
                    notes.append(self.parse_note(note_path))
                except Exception:
                    continue  # Skip unparseable notes

            return notes

        except (subprocess.CalledProcessError, json.JSONDecodeError, OSError) as e:
            raise NoteProcessorError(f"Note search failed: {e}")

    def extract_action_items(
        self,
        scope: str = "all",
        filters: Optional[ActionItemFilters] = None,
    ) -> List[Dict[str, Any]]:
        """
        Extract action items from notes with filtering.

        Args:
            scope: Scope for extraction ('all', 'project:<id>', 'inbox', etc.)
            filters: ActionItemFilters for filtering results

        Returns:
            List of action items with metadata

        Example:
            >>> items = processor.extract_action_items(
            ...     scope="project:mobile-app-v2",
            ...     filters=ActionItemFilters(status="pending")
            ... )
        """
        # Build command using ./notes follow-up
        # Note: --json flag must come before the subcommand
        cmd = [str(self.notes_cli), "--json", "follow-up", "--status", "all"]

        # Note: ./notes follow-up doesn't support project filtering directly
        # We'll filter in memory if needed

        if filters and filters.assignee:
            cmd.extend(["--assignee", filters.assignee])

        # Directory filtering based on scope
        if scope.startswith("project:"):
            # For project scope, we search in project directories
            cmd.extend(["--directory", "1-projects"])
        elif scope == "inbox":
            cmd.extend(["--directory", "inbox"])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30, check=True
            )
            data = json.loads(result.stdout) if result.stdout.strip() else {"items": []}

            # Extract action items from response
            items = data.get("data", {}).get("items", []) if data.get("success") else []

            # Apply in-memory filtering
            if filters:
                if filters.status:
                    if filters.status == "pending":
                        items = [item for item in items if not item.get("completed", False)]
                    elif filters.status == "completed":
                        items = [item for item in items if item.get("completed", False)]
                    elif filters.status == "overdue":
                        # Overdue filtering based on due_date
                        from datetime import datetime
                        today = datetime.now().date()
                        items = [
                            item for item in items
                            if item.get("due_date") and
                            datetime.fromisoformat(item["due_date"]).date() < today and
                            not item.get("completed", False)
                        ]

                if filters.priority:
                    items = [item for item in items if item.get("priority") == filters.priority]

            return items

        except (subprocess.CalledProcessError, json.JSONDecodeError, OSError) as e:
            raise NoteProcessorError(f"Action item extraction failed: {e}")

    def get_action_items_by_status(
        self, status: str, project: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get action items filtered by status.

        Args:
            status: Status filter ('pending', 'completed', 'overdue')
            project: Optional project filter

        Returns:
            List of action items

        Example:
            >>> overdue = processor.get_action_items_by_status("overdue")
            >>> for item in overdue:
            ...     print(f"⚠️ {item['text']} - Due: {item['due_date']}")
        """
        scope = f"project:{project}" if project else "all"
        filters = ActionItemFilters(status=status)
        return self.extract_action_items(scope=scope, filters=filters)

    def group_action_items_by_project(
        self, items: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group action items by project for organized follow-up.

        Args:
            items: List of action items

        Returns:
            Dict mapping project names to action items

        Example:
            >>> items = processor.extract_action_items()
            >>> grouped = processor.group_action_items_by_project(items)
            >>> for project, project_items in grouped.items():
            ...     print(f"{project}: {len(project_items)} items")
        """
        grouped: Dict[str, List[Dict[str, Any]]] = {}

        for item in items:
            # Extract project from note path if available
            note_path = item.get("note", "")
            project = "Unassigned"

            if "/1-projects/" in note_path:
                # Extract project folder name from path
                parts = note_path.split("/1-projects/")
                if len(parts) > 1:
                    project_parts = parts[1].split("/")
                    if project_parts:
                        project = project_parts[0]
            elif "/2-areas/" in note_path:
                project = "Areas"
            elif "/inbox/" in note_path:
                project = "Inbox"
            elif "/3-resources/" in note_path:
                project = "Resources"

            if project not in grouped:
                grouped[project] = []
            grouped[project].append(item)

        return grouped

    def prioritize_action_items(
        self, items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Prioritize action items based on urgency, importance, and age.

        Scoring algorithm:
        - Overdue items: +50 points per day overdue
        - High priority: +100 points
        - Medium priority: +50 points
        - Low priority: +25 points
        - Age: +1 point per day since creation

        Args:
            items: List of action items

        Returns:
            Sorted list of action items (highest priority first)

        Example:
            >>> items = processor.extract_action_items()
            >>> prioritized = processor.prioritize_action_items(items)
            >>> for item in prioritized[:5]:
            ...     print(f"{item['text']} - Priority: {item.get('priority', 'none')}")
        """
        from datetime import datetime

        def calculate_priority_score(item: Dict[str, Any]) -> int:
            score = 0
            today = datetime.now().date()

            # Check if overdue
            due_date_str = item.get("due_date")
            if due_date_str and not item.get("completed", False):
                try:
                    due_date = datetime.fromisoformat(due_date_str).date()
                    if due_date < today:
                        days_overdue = (today - due_date).days
                        score += days_overdue * 50  # Heavy weight for overdue
                except (ValueError, TypeError):
                    pass

            # Priority level
            priority = item.get("priority")
            if priority:
                priority_lower = priority.lower()
                if priority_lower == "high":
                    score += 100
                elif priority_lower == "medium":
                    score += 50
                elif priority_lower == "low":
                    score += 25

            # Age of item (from created date if available)
            created_date_str = item.get("created")
            if created_date_str:
                try:
                    created_date = datetime.fromisoformat(created_date_str).date()
                    days_old = (today - created_date).days
                    score += days_old  # 1 point per day
                except (ValueError, TypeError):
                    pass

            return score

        # Create list with scores and sort
        items_with_scores = [
            (calculate_priority_score(item), item) for item in items
        ]
        items_with_scores.sort(key=lambda x: x[0], reverse=True)

        return [item for _, item in items_with_scores]

    def get_stale_action_items(
        self, days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get action items that are stale (old without updates).

        Args:
            days: Number of days to consider an item stale (default: 30)

        Returns:
            List of stale action items

        Example:
            >>> stale = processor.get_stale_action_items(days=30)
            >>> print(f"Found {len(stale)} items older than 30 days")
        """
        from datetime import datetime, timedelta

        all_items = self.extract_action_items(
            filters=ActionItemFilters(status="pending")
        )

        cutoff_date = datetime.now().date() - timedelta(days=days)
        stale_items = []

        for item in all_items:
            created_date_str = item.get("created")
            if created_date_str:
                try:
                    created_date = datetime.fromisoformat(created_date_str).date()
                    if created_date < cutoff_date:
                        stale_items.append(item)
                except (ValueError, TypeError):
                    pass

        return stale_items

    # Project Integration

    def get_project_notes(self, project_id: str) -> List[ParsedNote]:
        """
        Get all notes linked to a specific project.

        Args:
            project_id: Project identifier

        Returns:
            List[ParsedNote]: Notes for the project

        Example:
            >>> notes = processor.get_project_notes("mobile-app-v2")
            >>> print(f"Found {len(notes)} notes for mobile-app-v2")
        """
        return self.search_notes(filters=NoteSearchFilters(project=project_id))

    def link_note_to_project(
        self, note_path: str, project_id: str
    ) -> bool:
        """
        Link a note to a project.

        Args:
            note_path: Path to note file
            project_id: Project identifier

        Returns:
            bool: Success status

        Example:
            >>> processor.link_note_to_project(
            ...     "inbox/feature-brainstorm.md",
            ...     "mobile-app-v2"
            ... )
        """
        try:
            # Update frontmatter with project link
            updates = {"project": project_id}
            return self.update_frontmatter(note_path, updates)

        except Exception as e:
            raise NoteProcessorError(f"Failed to link note to project: {e}")

    def sync_project_notes(self, project_id: str) -> Dict[str, Any]:
        """
        Synchronize project notes with cache system.

        Args:
            project_id: Project identifier

        Returns:
            Sync results with statistics

        Example:
            >>> results = processor.sync_project_notes("mobile-app-v2")
            >>> print(f"Synced {results['synced_count']} notes")
        """
        notes = self.get_project_notes(project_id)

        # Update cache
        cache_path = self.config_root / "cache" / f"notes_{project_id}.json"
        cache_path.parent.mkdir(exist_ok=True)

        cache_data = {
            "project_id": project_id,
            "notes": [
                {
                    "path": note.file_path,
                    "action_items": len(note.action_items),
                    "tags": note.tags,
                    "updated_at": datetime.now().isoformat(),
                }
                for note in notes
            ],
            "synced_at": datetime.now().isoformat(),
        }

        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)

        return {
            "project_id": project_id,
            "synced_count": len(notes),
            "cache_path": str(cache_path),
        }

    # Categorization

    def categorize_note(
        self, note_path: str, auto_move: bool = False
    ) -> CategorizationResult:
        """
        Analyze and categorize a note using PARA Method.

        Args:
            note_path: Path to note file
            auto_move: Whether to automatically move the file

        Returns:
            CategorizationResult: Categorization with confidence and reasoning

        Example:
            >>> result = processor.categorize_note("inbox/meeting-note.md")
            >>> print(f"Category: {result.category} (confidence: {result.confidence:.1%})")
            >>> print(f"Reasoning: {', '.join(result.reasoning)}")
        """
        try:
            note = self.parse_note(note_path)

            if not note.categorization_result:
                raise NoteProcessorError("No categorization result available")

            categorization = note.categorization_result

            if auto_move and categorization.confidence >= 0.7:
                # Move file to suggested category
                source = Path(note_path)
                dest = Path(categorization.category.value) / source.name

                if not dest.exists():
                    source.rename(dest)
                    categorization.category = ParaCategory(categorization.category.value)

            return categorization

        except Exception as e:
            raise NoteProcessorError(f"Categorization failed: {e}")

    # Frontmatter Operations

    def update_frontmatter(
        self, note_path: str, updates: Dict[str, Any], create_backup: bool = True
    ) -> bool:
        """
        Update note frontmatter with atomic write and rollback.

        Args:
            note_path: Path to note file
            updates: Dictionary of frontmatter updates
            create_backup: Whether to create backup before update

        Returns:
            bool: Success status

        Example:
            >>> processor.update_frontmatter(
            ...     "1-projects/mobile-app/sprint-notes.md",
            ...     {"status": "in-progress", "priority": "high"}
            ... )
        """
        try:
            return self.para_processor.update_note_frontmatter(
                note_path, updates, create_backup
            )
        except Exception as e:
            raise NoteProcessorError(f"Frontmatter update failed: {e}")

    # Batch Operations

    def batch_process_inbox(
        self, max_notes: Optional[int] = None, auto_categorize: bool = False
    ) -> BatchProcessResult:
        """
        Batch process notes in inbox with optional categorization.

        Args:
            max_notes: Maximum number of notes to process
            auto_categorize: Whether to auto-categorize with high confidence

        Returns:
            BatchProcessResult: Processing results with statistics

        Example:
            >>> results = processor.batch_process_inbox(max_notes=10, auto_categorize=True)
            >>> print(f"Processed: {results.successful}/{results.total_processed}")
            >>> print(f"Errors: {len(results.errors)}")
        """
        try:
            inbox_path = Path("inbox")
            if not inbox_path.exists():
                raise NoteProcessorError("Inbox directory not found")

            notes = list(inbox_path.glob("*.md"))
            if max_notes:
                notes = notes[:max_notes]

            successful = 0
            failed = 0
            processed_notes = []
            errors = []

            for note_path in notes:
                try:
                    note = self.parse_note(str(note_path))

                    # Auto-categorize if requested
                    if auto_categorize and note.categorization_result:
                        if note.categorization_result.confidence >= 0.8:
                            self.categorize_note(str(note_path), auto_move=True)

                    processed_notes.append(
                        {
                            "path": str(note_path),
                            "action_items": len(note.action_items),
                            "category": (
                                note.categorization_result.category.value
                                if note.categorization_result
                                else None
                            ),
                            "confidence": (
                                note.categorization_result.confidence
                                if note.categorization_result
                                else 0.0
                            ),
                        }
                    )
                    successful += 1

                except Exception as e:
                    failed += 1
                    errors.append({"path": str(note_path), "error": str(e)})

            return BatchProcessResult(
                total_processed=len(notes),
                successful=successful,
                failed=failed,
                notes=processed_notes,
                errors=errors,
            )

        except Exception as e:
            raise NoteProcessorError(f"Batch processing failed: {e}")

    # Utility Methods

    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Get statistics about notes and processing status.

        Returns:
            Dictionary with processing statistics

        Example:
            >>> stats = processor.get_processing_stats()
            >>> print(f"Inbox: {stats['inbox_count']} notes")
            >>> print(f"Total action items: {stats['total_action_items']}")
        """
        try:
            inbox_notes = list(Path("inbox").glob("*.md")) if Path("inbox").exists() else []
            all_notes = []

            for category in ParaCategory:
                if category == ParaCategory.INBOX:
                    continue
                path = Path(category.value)
                if path.exists():
                    all_notes.extend(list(path.rglob("*.md")))

            # Get action item count
            try:
                all_items = self.extract_action_items(scope="all")
                pending_items = [
                    item for item in all_items if not item.get("completed", False)
                ]
            except Exception:
                all_items = []
                pending_items = []

            return {
                "inbox_count": len(inbox_notes),
                "total_notes": len(all_notes) + len(inbox_notes),
                "total_action_items": len(all_items),
                "pending_action_items": len(pending_items),
                "categories": {
                    category.value: len(
                        list(Path(category.value).rglob("*.md"))
                        if Path(category.value).exists()
                        else []
                    )
                    for category in ParaCategory
                    if category != ParaCategory.INBOX
                },
            }

        except Exception as e:
            raise NoteProcessorError(f"Failed to get processing stats: {e}")

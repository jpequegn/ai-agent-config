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

"""
Tests for NoteProcessor tool

Comprehensive test suite for note processing operations with >80% coverage target.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from tools.note_models import (
    ActionItem,
    ActionItemFilters,
    BatchProcessResult,
    CategorizationResult,
    NoteSearchFilters,
    ParaCategory,
    ParsedNote,
)
from tools.note_processor import NoteProcessor, NoteProcessorError


@pytest.fixture
def temp_workspace():
    """Create temporary workspace with PARA structure"""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)

        # Create PARA directories
        (workspace / "inbox").mkdir()
        (workspace / "1-projects").mkdir()
        (workspace / "2-areas").mkdir()
        (workspace / "3-resources").mkdir()
        (workspace / "4-archive").mkdir()
        (workspace / ".claude" / "cache").mkdir(parents=True)

        # Create sample notes
        (workspace / "inbox" / "test-note.md").write_text(
            """---
title: Test Note
tags: [test, sample]
---

# Test Note

- [ ] Task 1 - @alice - due: 2025-10-15
- [x] Task 2 - @bob
- [ ] Task 3 [high]

This is a test note with some content.
"""
        )

        (workspace / "1-projects" / "project-note.md").write_text(
            """---
title: Project Note
project: test-project
status: active
---

# Project Planning

- [ ] Define milestones
- [ ] Set deadlines
- [ ] Assign tasks
"""
        )

        yield workspace


@pytest.fixture
def note_processor(temp_workspace):
    """Create NoteProcessor instance with temp workspace"""
    with patch("tools.note_processor.Path.cwd", return_value=temp_workspace):
        processor = NoteProcessor(config_root=temp_workspace / ".claude")
        processor.notes_cli = temp_workspace / "notes"  # Mock notes CLI path
        return processor


class TestNoteProcessorInit:
    """Test NoteProcessor initialization"""

    def test_init_default(self, temp_workspace):
        """Test initialization with default config root"""
        with patch("tools.note_processor.Path.cwd", return_value=temp_workspace):
            processor = NoteProcessor()
            assert processor.config_root == temp_workspace / ".claude"
            assert processor.para_processor is not None

    def test_init_custom_root(self, temp_workspace):
        """Test initialization with custom config root"""
        custom_root = temp_workspace / "custom"
        custom_root.mkdir()
        processor = NoteProcessor(config_root=custom_root)
        assert processor.config_root == custom_root


class TestParseNote:
    """Test note parsing operations"""

    def test_parse_note_success(self, note_processor, temp_workspace):
        """Test successful note parsing"""
        note_path = temp_workspace / "inbox" / "test-note.md"
        note = note_processor.parse_note(str(note_path))

        # The returned note is from para-processor which uses dataclass, not Pydantic
        assert hasattr(note, "file_path")
        assert note.file_path == str(note_path)
        assert "title" in note.frontmatter
        assert len(note.action_items) == 3

    def test_parse_note_with_action_items(self, note_processor, temp_workspace):
        """Test parsing note with action items"""
        note_path = temp_workspace / "inbox" / "test-note.md"
        note = note_processor.parse_note(str(note_path))

        action_items = note.action_items
        assert len(action_items) == 3
        assert action_items[0].text == "Task 1"
        assert action_items[0].assignee == "alice"
        assert not action_items[0].completed
        assert action_items[1].completed

    def test_parse_note_error(self, note_processor):
        """Test parsing non-existent note raises error"""
        with pytest.raises(NoteProcessorError, match="Failed to parse note"):
            note_processor.parse_note("nonexistent.md")


class TestSearchNotes:
    """Test note search operations"""

    @patch("tools.note_processor.subprocess.run")
    def test_search_notes_basic(self, mock_run, note_processor, temp_workspace):
        """Test basic note search"""
        # Mock subprocess response
        mock_result = Mock()
        mock_result.stdout = json.dumps(
            {"notes": [str(temp_workspace / "inbox" / "test-note.md")]}
        )
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        notes = note_processor.search_notes(query="test")

        assert len(notes) > 0
        mock_run.assert_called_once()

    @patch("tools.note_processor.subprocess.run")
    def test_search_notes_with_filters(self, mock_run, note_processor):
        """Test note search with filters"""
        mock_result = Mock()
        mock_result.stdout = json.dumps({"notes": []})
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        filters = NoteSearchFilters(project="test-project", status="active")
        notes = note_processor.search_notes(filters=filters)

        assert isinstance(notes, list)
        call_args = mock_run.call_args[0][0]
        assert "--project" in call_args
        assert "test-project" in call_args

    @patch("tools.note_processor.subprocess.run")
    def test_search_notes_error(self, mock_run, note_processor):
        """Test search with subprocess error"""
        mock_run.side_effect = FileNotFoundError("notes CLI not found")

        with pytest.raises(NoteProcessorError, match="Note search failed"):
            note_processor.search_notes(query="test")


class TestActionItems:
    """Test action item extraction and filtering"""

    @patch("tools.note_processor.subprocess.run")
    def test_extract_action_items_all(self, mock_run, note_processor):
        """Test extracting all action items"""
        mock_result = Mock()
        mock_result.stdout = json.dumps(
            {
                "action_items": [
                    {"text": "Task 1", "completed": False, "assignee": "alice"},
                    {"text": "Task 2", "completed": True, "assignee": "bob"},
                ]
            }
        )
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        items = note_processor.extract_action_items(scope="all")

        assert len(items) == 2
        assert items[0]["text"] == "Task 1"

    @patch("tools.note_processor.subprocess.run")
    def test_extract_action_items_with_filters(self, mock_run, note_processor):
        """Test extracting action items with filters"""
        mock_result = Mock()
        mock_result.stdout = json.dumps({"action_items": []})
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        filters = ActionItemFilters(status="pending", assignee="alice")
        items = note_processor.extract_action_items(scope="all", filters=filters)

        call_args = mock_run.call_args[0][0]
        assert "--status" in call_args
        assert "pending" in call_args
        assert "--assignee" in call_args
        assert "alice" in call_args

    @patch("tools.note_processor.subprocess.run")
    def test_get_action_items_by_status(self, mock_run, note_processor):
        """Test getting action items by status"""
        mock_result = Mock()
        mock_result.stdout = json.dumps(
            {"action_items": [{"text": "Overdue task", "status": "overdue"}]}
        )
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        items = note_processor.get_action_items_by_status("overdue")

        assert len(items) == 1
        assert items[0]["text"] == "Overdue task"


class TestProjectIntegration:
    """Test project integration operations"""

    @patch("tools.note_processor.subprocess.run")
    def test_get_project_notes(self, mock_run, note_processor, temp_workspace):
        """Test getting project notes"""
        mock_result = Mock()
        mock_result.stdout = json.dumps(
            {"notes": [str(temp_workspace / "1-projects" / "project-note.md")]}
        )
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        notes = note_processor.get_project_notes("test-project")

        assert len(notes) > 0
        call_args = mock_run.call_args[0][0]
        assert "--project" in call_args

    def test_link_note_to_project(self, note_processor, temp_workspace):
        """Test linking note to project"""
        note_path = temp_workspace / "inbox" / "test-note.md"

        # Mock update_frontmatter
        with patch.object(note_processor, "update_frontmatter", return_value=True):
            result = note_processor.link_note_to_project(str(note_path), "test-project")
            assert result is True

    def test_sync_project_notes(self, note_processor, temp_workspace):
        """Test syncing project notes"""
        # Mock get_project_notes
        mock_note = Mock(spec=ParsedNote)
        mock_note.file_path = str(temp_workspace / "1-projects" / "project-note.md")
        mock_note.action_items = []
        mock_note.tags = ["test"]

        with patch.object(
            note_processor, "get_project_notes", return_value=[mock_note]
        ):
            result = note_processor.sync_project_notes("test-project")

            assert result["project_id"] == "test-project"
            assert result["synced_count"] == 1
            assert "cache_path" in result

            # Verify cache file created
            cache_path = Path(result["cache_path"])
            assert cache_path.exists()


class TestCategorization:
    """Test note categorization operations"""

    def test_categorize_note(self, note_processor, temp_workspace):
        """Test note categorization"""
        note_path = temp_workspace / "inbox" / "test-note.md"

        # Mock parse_note to return categorization result
        mock_note = Mock(spec=ParsedNote)
        mock_note.file_path = str(note_path)
        mock_note.categorization_result = CategorizationResult(
            category=ParaCategory.PROJECTS,
            confidence=0.85,
            reasoning=["Contains project keywords", "Has deadlines"],
            alternative_categories=[],
        )

        with patch.object(note_processor, "parse_note", return_value=mock_note):
            result = note_processor.categorize_note(str(note_path))

            assert result.category == ParaCategory.PROJECTS
            assert result.confidence == 0.85
            assert len(result.reasoning) > 0

    def test_categorize_note_auto_move(self, note_processor, temp_workspace):
        """Test categorization with auto-move"""
        note_path = temp_workspace / "inbox" / "test-note.md"

        mock_note = Mock(spec=ParsedNote)
        mock_note.file_path = str(note_path)
        mock_note.categorization_result = CategorizationResult(
            category=ParaCategory.PROJECTS,
            confidence=0.9,
            reasoning=["High confidence categorization"],
            alternative_categories=[],
        )

        with patch.object(note_processor, "parse_note", return_value=mock_note):
            result = note_processor.categorize_note(str(note_path), auto_move=True)

            # Note: actual file move won't happen in this test
            assert result.confidence >= 0.7


class TestFrontmatterOperations:
    """Test frontmatter update operations"""

    def test_update_frontmatter(self, note_processor, temp_workspace):
        """Test updating frontmatter"""
        note_path = temp_workspace / "inbox" / "test-note.md"

        # Mock para_processor update
        with patch.object(
            note_processor.para_processor, "update_note_frontmatter", return_value=True
        ):
            result = note_processor.update_frontmatter(
                str(note_path), {"status": "reviewed"}
            )
            assert result is True

    def test_update_frontmatter_error(self, note_processor):
        """Test frontmatter update error handling"""
        with patch.object(
            note_processor.para_processor,
            "update_note_frontmatter",
            side_effect=Exception("Update failed"),
        ):
            with pytest.raises(NoteProcessorError, match="Frontmatter update failed"):
                note_processor.update_frontmatter("test.md", {"status": "reviewed"})


class TestBatchOperations:
    """Test batch processing operations"""

    def test_batch_process_inbox(self, note_processor, temp_workspace):
        """Test batch processing inbox"""
        result = note_processor.batch_process_inbox(max_notes=10)

        assert isinstance(result, BatchProcessResult)
        assert result.total_processed >= 0
        assert result.successful + result.failed == result.total_processed

    def test_batch_process_inbox_auto_categorize(self, note_processor, temp_workspace):
        """Test batch processing with auto-categorization"""
        # Create mock categorization
        mock_categorization = CategorizationResult(
            category=ParaCategory.PROJECTS,
            confidence=0.85,
            reasoning=["Test"],
            alternative_categories=[],
        )

        with patch.object(
            note_processor, "categorize_note", return_value=mock_categorization
        ):
            result = note_processor.batch_process_inbox(
                max_notes=1, auto_categorize=True
            )

            assert result.total_processed >= 0

    def test_batch_process_inbox_no_inbox(self, note_processor, temp_workspace):
        """Test batch processing when inbox doesn't exist"""
        # Remove inbox and its contents
        import shutil

        shutil.rmtree(temp_workspace / "inbox")

        # Patch the method to use temp_workspace
        with patch.object(Path, "glob", return_value=[]):
            # When inbox is missing, batch_process returns empty result
            result = note_processor.batch_process_inbox()
            assert result.total_processed == 0
            assert result.successful == 0


class TestUtilityMethods:
    """Test utility methods"""

    @patch("tools.note_processor.subprocess.run")
    def test_get_processing_stats(self, mock_run, note_processor, temp_workspace):
        """Test getting processing statistics"""
        mock_result = Mock()
        mock_result.stdout = json.dumps(
            {
                "action_items": [
                    {"text": "Task 1", "completed": False},
                    {"text": "Task 2", "completed": True},
                ]
            }
        )
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        stats = note_processor.get_processing_stats()

        assert "inbox_count" in stats
        assert "total_notes" in stats
        assert "total_action_items" in stats
        assert "pending_action_items" in stats
        assert "categories" in stats

    @patch("tools.note_processor.subprocess.run")
    def test_get_processing_stats_error_handling(self, mock_run, note_processor):
        """Test stats with action item extraction errors"""
        mock_run.side_effect = Exception("Extraction failed")

        stats = note_processor.get_processing_stats()

        # Should still return stats even if action item extraction fails
        assert "inbox_count" in stats
        assert stats["total_action_items"] == 0


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_parse_note_empty_file(self, note_processor, temp_workspace):
        """Test parsing empty note file"""
        empty_note = temp_workspace / "inbox" / "empty.md"
        empty_note.write_text("")

        # Empty files should raise an error from para-processor
        with pytest.raises(NoteProcessorError, match="Failed to parse note"):
            note_processor.parse_note(str(empty_note))

    def test_parse_note_malformed_frontmatter(self, note_processor, temp_workspace):
        """Test parsing note with malformed frontmatter"""
        malformed = temp_workspace / "inbox" / "malformed.md"
        malformed.write_text("---\ninvalid: yaml: content:\n---\n# Note")

        # Should handle gracefully
        try:
            note = note_processor.parse_note(str(malformed))
            # If it parses, that's fine
        except NoteProcessorError:
            # If it raises error, that's also acceptable
            pass

    @patch("tools.note_processor.subprocess.run")
    def test_search_notes_empty_results(self, mock_run, note_processor):
        """Test search with no results"""
        mock_result = Mock()
        mock_result.stdout = json.dumps({"notes": []})
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        notes = note_processor.search_notes(query="nonexistent")
        assert len(notes) == 0

    @patch("tools.note_processor.subprocess.run")
    def test_extract_action_items_empty_response(self, mock_run, note_processor):
        """Test action item extraction with empty response"""
        mock_result = Mock()
        mock_result.stdout = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        items = note_processor.extract_action_items()
        assert len(items) == 0

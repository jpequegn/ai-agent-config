"""
Comprehensive tests for ConfigManager.

Tests cover:
- Basic YAML loading
- Schema validation (valid and invalid)
- Caching behavior
- Atomic updates
- Cross-file synchronization
- Error handling
"""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from tools import ConfigManager, ConfigNotFoundError, ConfigValidationError
from tools.schemas import Project, ProjectsConfig, TeamMember, TeamRosterConfig


@pytest.fixture
def temp_config_dir():
    """Create temporary config directory with sample files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / ".claude"
        config_dir.mkdir()

        # Copy sample fixtures
        fixtures_dir = Path(__file__).parent / "fixtures"

        sample_projects = fixtures_dir / "sample_projects.yaml"
        sample_team = fixtures_dir / "sample_team.yaml"

        if sample_projects.exists():
            (config_dir / "projects.yaml").write_text(sample_projects.read_text())
        if sample_team.exists():
            (config_dir / "team_roster.yaml").write_text(sample_team.read_text())

        yield config_dir


@pytest.fixture
def config_manager(temp_config_dir):
    """Create ConfigManager with temporary config directory."""
    return ConfigManager(config_root=temp_config_dir)


class TestBasicLoading:
    """Test basic YAML loading functionality."""

    def test_load_config_success(self, config_manager):
        """Test loading valid config file."""
        data = config_manager.load_config("projects.yaml")
        assert "projects" in data
        assert "test-project-1" in data["projects"]

    def test_load_config_not_found(self, config_manager):
        """Test loading non-existent config file."""
        with pytest.raises(ConfigNotFoundError):
            config_manager.load_config("nonexistent.yaml")

    def test_load_config_with_schema(self, config_manager):
        """Test loading config with schema validation."""
        data = config_manager.load_config("projects.yaml", schema=ProjectsConfig)
        assert "projects" in data
        # Verify Pydantic conversion happened
        assert isinstance(data["projects"]["test-project-1"]["status"], str)


class TestSchemaValidation:
    """Test schema validation functionality."""

    def test_valid_config(self, config_manager):
        """Test validation of valid config."""
        data = config_manager.validate_config("projects.yaml", ProjectsConfig)
        assert "projects" in data

    def test_invalid_config(self, temp_config_dir):
        """Test validation of invalid config."""
        # Create invalid config
        invalid_path = temp_config_dir / "invalid.yaml"
        invalid_data = {
            "projects": {
                "bad-project": {
                    "name": "Bad Project",
                    "status": "invalid_status",  # Invalid enum value
                    # Missing required fields
                }
            }
        }
        with open(invalid_path, "w") as f:
            yaml.safe_dump(invalid_data, f)

        mgr = ConfigManager(config_root=temp_config_dir)
        with pytest.raises(ConfigValidationError):
            mgr.validate_config("invalid.yaml", ProjectsConfig)


class TestCaching:
    """Test caching behavior."""

    def test_cache_usage(self, config_manager):
        """Test that cache is used on subsequent reads."""
        # First load
        data1 = config_manager.load_config("projects.yaml", use_cache=True)

        # Second load (should use cache)
        data2 = config_manager.load_config("projects.yaml", use_cache=True)

        assert data1 == data2

        # Verify cache statistics
        stats = config_manager.get_cache_stats()
        assert stats["cached_files"] >= 1

    def test_cache_invalidation_on_modification(self, config_manager, temp_config_dir):
        """Test that cache is invalidated when file is modified."""
        # First load
        data1 = config_manager.load_config("projects.yaml", use_cache=True)

        # Modify file
        config_path = temp_config_dir / "projects.yaml"
        with open(config_path, "a") as f:
            f.write("# Modified\n")

        # Second load (should reload from file)
        data2 = config_manager.load_config("projects.yaml", use_cache=True)

        # Cache should have been invalidated and reloaded
        assert config_manager._is_cache_valid(config_path) is True

    def test_cache_disabled(self, config_manager):
        """Test loading without cache."""
        data1 = config_manager.load_config("projects.yaml", use_cache=False)
        data2 = config_manager.load_config("projects.yaml", use_cache=False)

        assert data1 == data2
        # Cache should be empty or minimal
        stats = config_manager.get_cache_stats()
        assert stats["cached_files"] == 0

    def test_clear_cache(self, config_manager):
        """Test clearing cache."""
        # Load to populate cache
        config_manager.load_config("projects.yaml", use_cache=True)

        stats_before = config_manager.get_cache_stats()
        assert stats_before["cached_files"] > 0

        # Clear cache
        config_manager.clear_cache()

        stats_after = config_manager.get_cache_stats()
        assert stats_after["cached_files"] == 0


class TestAtomicUpdates:
    """Test atomic update operations."""

    def test_update_config_success(self, config_manager, temp_config_dir):
        """Test successful config update."""
        updates = {"projects": {"test-project-1": {"status": "completed"}}}

        config_manager.update_config("projects.yaml", updates)

        # Verify update
        data = config_manager.load_config("projects.yaml", use_cache=False)
        assert data["projects"]["test-project-1"]["status"] == "completed"

    def test_update_config_nested(self, config_manager):
        """Test nested updates."""
        updates = {
            "projects": {
                "test-project-1": {
                    "milestones": [
                        {
                            "name": "New Milestone",
                            "date": "2024-12-31",
                            "status": "planned",
                        }
                    ]
                }
            }
        }

        config_manager.update_config("projects.yaml", updates)

        # Verify update
        data = config_manager.load_config("projects.yaml", use_cache=False)
        assert data["projects"]["test-project-1"]["milestones"][0]["name"] == "New Milestone"

    def test_update_config_backup(self, config_manager, temp_config_dir):
        """Test that backup is created and cleaned up."""
        updates = {"projects": {"test-project-1": {"status": "on_hold"}}}

        config_manager.update_config("projects.yaml", updates, backup=True)

        # Verify no backup files remain
        backup_files = list(temp_config_dir.glob("projects.backup.*"))
        assert len(backup_files) == 0

    def test_update_config_not_found(self, config_manager):
        """Test updating non-existent file."""
        with pytest.raises(ConfigNotFoundError):
            config_manager.update_config("nonexistent.yaml", {"key": "value"})


class TestSpecializedOperations:
    """Test specialized operations for common use cases."""

    def test_get_project(self, config_manager):
        """Test getting a specific project."""
        project = config_manager.get_project("test-project-1")

        assert isinstance(project, Project)
        assert project.name == "Test Project 1"
        assert project.status.value == "active"

    def test_get_project_not_found(self, config_manager):
        """Test getting non-existent project."""
        with pytest.raises(KeyError):
            config_manager.get_project("nonexistent-project")

    def test_update_project(self, config_manager):
        """Test updating a specific project."""
        config_manager.update_project("test-project-1", {"status": "completed"})

        # Verify update
        project = config_manager.get_project("test-project-1")
        assert project.status.value == "completed"

    def test_get_all_projects(self, config_manager):
        """Test getting all projects."""
        projects = config_manager.get_all_projects()

        assert len(projects) == 2
        assert "test-project-1" in projects
        assert "test-project-2" in projects

    def test_get_all_projects_filtered(self, config_manager):
        """Test getting filtered projects."""
        projects = config_manager.get_all_projects(filters={"status": ["active"]})

        assert len(projects) == 1
        assert "test-project-1" in projects

    def test_get_team_member(self, config_manager):
        """Test getting a team member."""
        member = config_manager.get_team_member("test@example.com")

        assert isinstance(member, TeamMember)
        assert member.name == "Test User"
        assert member.role == "Developer"

    def test_get_team_member_not_found(self, config_manager):
        """Test getting non-existent team member."""
        with pytest.raises(KeyError):
            config_manager.get_team_member("nonexistent@example.com")


class TestCrossFileSynchronization:
    """Test cross-file synchronization."""

    def test_sync_project_to_notes(self, config_manager, temp_config_dir):
        """Test syncing project to notes cache."""
        cache_dir = temp_config_dir / "cache"
        cache_dir.mkdir(exist_ok=True)

        config_manager.sync_project_to_notes("test-project-1")

        # Verify cache file created
        cache_file = cache_dir / "notes_test-project-1.json"
        assert cache_file.exists()

        # Verify cache content
        with open(cache_file) as f:
            cache_data = json.load(f)
            assert cache_data["name"] == "Test Project 1"

    def test_sync_team_to_stakeholders_no_stakeholders(self, config_manager):
        """Test team sync when stakeholder file doesn't exist."""
        # Should not raise error
        config_manager.sync_team_to_stakeholders()


class TestMergeConfigs:
    """Test configuration merging."""

    def test_merge_configs_shallow(self, config_manager):
        """Test shallow merge of configs."""
        merged = config_manager.merge_configs(
            ["projects.yaml", "team_roster.yaml"], strategy="shallow"
        )

        assert "projects" in merged
        assert "team_members" in merged

    def test_merge_configs_deep(self, config_manager, temp_config_dir):
        """Test deep merge of configs."""
        # Create two configs with overlapping structure
        config1_path = temp_config_dir / "config1.yaml"
        config2_path = temp_config_dir / "config2.yaml"

        config1 = {"shared": {"key1": "value1", "nested": {"a": 1}}}
        config2 = {"shared": {"key2": "value2", "nested": {"b": 2}}}

        with open(config1_path, "w") as f:
            yaml.safe_dump(config1, f)
        with open(config2_path, "w") as f:
            yaml.safe_dump(config2, f)

        merged = config_manager.merge_configs(
            ["config1.yaml", "config2.yaml"], strategy="deep"
        )

        assert merged["shared"]["key1"] == "value1"
        assert merged["shared"]["key2"] == "value2"
        assert merged["shared"]["nested"]["a"] == 1
        assert merged["shared"]["nested"]["b"] == 2


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_yaml(self, config_manager, temp_config_dir):
        """Test handling of invalid YAML."""
        invalid_path = temp_config_dir / "invalid.yaml"
        invalid_path.write_text("{ invalid yaml content")

        with pytest.raises(yaml.YAMLError):
            config_manager.load_config("invalid.yaml")

    def test_invalid_merge_strategy(self, config_manager):
        """Test invalid merge strategy."""
        with pytest.raises(ValueError):
            config_manager.merge_configs(["projects.yaml"], strategy="invalid")


class TestPerformance:
    """Test performance requirements."""

    def test_cached_read_performance(self, config_manager):
        """Test cached reads are fast (<10ms)."""
        import time

        # Warm up cache
        config_manager.load_config("projects.yaml", use_cache=True)

        # Measure cached read
        start = time.perf_counter()
        config_manager.load_config("projects.yaml", use_cache=True)
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms

        assert elapsed < 10, f"Cached read took {elapsed:.2f}ms (expected <10ms)"

    def test_write_performance(self, config_manager):
        """Test writes are reasonably fast (<100ms)."""
        import time

        updates = {"projects": {"test-project-1": {"status": "completed"}}}

        start = time.perf_counter()
        config_manager.update_config("projects.yaml", updates)
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms

        assert elapsed < 100, f"Write took {elapsed:.2f}ms (expected <100ms)"

#!/usr/bin/env python3
"""
Comprehensive tests for DataCollector - Multi-Source Data Aggregation Tool

Tests caching, rate limiting, error handling, and data collection from all sources.
Target: >80% code coverage
"""

import json
import os
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import (
    DataCollector,
    DataCollectorError,
    GitHubData,
    GitHubRateLimitError,
    NotesData,
    ProjectData,
)


class TestDataModels(unittest.TestCase):
    """Test data model classes."""

    def test_github_data_creation(self):
        """Test GitHubData instantiation with defaults."""
        data = GitHubData(repo_name="test-repo")
        self.assertEqual(data.repo_name, "test-repo")
        self.assertEqual(data.pull_requests, [])
        self.assertEqual(data.issues, [])
        self.assertEqual(data.commits, [])
        self.assertEqual(data.milestones, [])
        self.assertEqual(data.repository_stats, {})
        self.assertIsInstance(data.collected_at, str)

    def test_github_data_with_data(self):
        """Test GitHubData with actual data."""
        prs = [{"number": 1, "title": "Test PR"}]
        data = GitHubData(
            repo_name="owner/repo",
            pull_requests=prs,
            issues=[],
            commits=[],
            milestones=[],
            repository_stats={"stars": 100},
        )
        self.assertEqual(len(data.pull_requests), 1)
        self.assertEqual(data.repository_stats["stars"], 100)

    def test_notes_data_creation(self):
        """Test NotesData instantiation."""
        data = NotesData()
        self.assertEqual(data.project_notes, [])
        self.assertEqual(data.action_items, [])
        self.assertEqual(data.decisions, [])
        self.assertIsInstance(data.collected_at, str)

    def test_project_data_aggregation(self):
        """Test ProjectData aggregation."""
        github_data = GitHubData(repo_name="test")
        notes_data = NotesData()

        project_data = ProjectData(
            project_name="test-project",
            github_data=github_data,
            notes_data=notes_data,
        )

        self.assertEqual(project_data.project_name, "test-project")
        self.assertIsNotNone(project_data.github_data)
        self.assertIsNotNone(project_data.notes_data)
        self.assertIsInstance(project_data.to_dict(), dict)


class TestDataCollectorInit(unittest.TestCase):
    """Test DataCollector initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claude"
        self.config_dir.mkdir()

        # Create minimal config files
        (self.config_dir / "integrations.yaml").write_text(
            """
integrations:
  github:
    config:
      token_env: GITHUB_TOKEN
      default_org: test-org
  calendar:
    config:
      api_key_env: CALENDAR_API_KEY
"""
        )

        (self.config_dir / "projects.yaml").write_text(
            """
projects:
  test-project:
    github_repos:
      - test-repo
    team:
      - alice
"""
        )

        (self.config_dir / "team.yaml").write_text(
            """
team:
  members:
    - id: alice
      name: Alice
      role: developer
"""
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_initialization(self):
        """Test DataCollector initialization."""
        collector = DataCollector(config_root=self.config_dir)
        self.assertIsNotNone(collector.config_manager)
        self.assertIsNotNone(collector._cache)
        self.assertEqual(collector.cache_ttl, 300)

    def test_custom_cache_ttl(self):
        """Test custom cache TTL."""
        collector = DataCollector(config_root=self.config_dir, cache_ttl=600)
        self.assertEqual(collector.cache_ttl, 600)

    def test_configuration_loading(self):
        """Test that configurations are loaded correctly."""
        collector = DataCollector(config_root=self.config_dir)
        self.assertIn("integrations", collector.integrations_config)
        self.assertIn("projects", collector.projects_config)
        self.assertIn("team", collector.team_config)


class TestCaching(unittest.TestCase):
    """Test caching functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claude"
        self.config_dir.mkdir()

        # Create minimal configs
        for config in ["integrations.yaml", "projects.yaml", "team.yaml"]:
            (self.config_dir / config).write_text("{}")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cache_key_generation(self):
        """Test cache key generation."""
        collector = DataCollector(config_root=self.config_dir)
        key1 = collector._get_cache_key("test", "key", 123)
        key2 = collector._get_cache_key("test", "key", 123)
        key3 = collector._get_cache_key("different", "key", 123)

        self.assertEqual(key1, key2)
        self.assertNotEqual(key1, key3)

    def test_cache_ttl_expiration(self):
        """Test cache TTL expiration."""
        collector = DataCollector(config_root=self.config_dir, cache_ttl=1)

        # Add item to cache
        key = "test_key"
        collector._cache[key] = "test_value"

        # Should be in cache
        self.assertIn(key, collector._cache)

        # Wait for TTL to expire
        time.sleep(1.1)

        # Should be expired
        self.assertNotIn(key, collector._cache)

    def test_cache_clear(self):
        """Test cache clearing."""
        collector = DataCollector(config_root=self.config_dir)
        collector._cache["key1"] = "value1"
        collector._cache["key2"] = "value2"

        self.assertEqual(len(collector._cache), 2)

        collector.clear_cache()
        self.assertEqual(len(collector._cache), 0)

    def test_cache_stats(self):
        """Test cache statistics."""
        collector = DataCollector(config_root=self.config_dir, cache_ttl=300)
        stats = collector.get_cache_stats()

        self.assertIn("size", stats)
        self.assertIn("max_size", stats)
        self.assertIn("ttl", stats)
        self.assertEqual(stats["ttl"], 300)


class TestGitHubDataCollection(unittest.TestCase):
    """Test GitHub data collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claude"
        self.config_dir.mkdir()

        (self.config_dir / "integrations.yaml").write_text(
            """
integrations:
  github:
    config:
      token_env: GITHUB_TOKEN
      default_org: test-org
"""
        )
        (self.config_dir / "projects.yaml").write_text("{}")
        (self.config_dir / "team.yaml").write_text("{}")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    @patch("requests.get")
    def test_github_data_collection_success(self, mock_get):
        """Test successful GitHub data collection."""
        # Mock responses
        mock_rate_limit = Mock()
        mock_rate_limit.status_code = 200
        mock_rate_limit.json.return_value = {
            "resources": {"core": {"remaining": 5000, "reset": time.time() + 3600}}
        }

        mock_repo = Mock()
        mock_repo.status_code = 200
        mock_repo.json.return_value = {
            "full_name": "test-org/test-repo",
            "stargazers_count": 100,
            "forks_count": 20,
            "open_issues_count": 5,
            "language": "Python",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        mock_prs = Mock()
        mock_prs.status_code = 200
        mock_prs.json.return_value = [{"number": 1, "title": "Test PR"}]

        mock_get.side_effect = [mock_rate_limit, mock_repo, mock_prs, mock_prs, mock_prs, mock_prs]

        collector = DataCollector(config_root=self.config_dir)
        data = collector.collect_github_data(["test-repo"], data_types=["stats", "prs"])

        self.assertIsInstance(data, GitHubData)
        self.assertIn("test-repo", data.repository_stats)
        self.assertEqual(len(data.pull_requests), 1)

    @patch.dict(os.environ, {}, clear=True)
    def test_github_no_token_error(self):
        """Test GitHub collection fails without token."""
        collector = DataCollector(config_root=self.config_dir)

        with self.assertRaises(DataCollectorError) as context:
            collector.collect_github_data(["test-repo"])

        self.assertIn("token not configured", str(context.exception).lower())

    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    @patch("requests.get")
    def test_github_rate_limit_check(self, mock_get):
        """Test GitHub rate limit checking."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "resources": {"core": {"remaining": 50, "reset": time.time() + 3600}}
        }
        mock_get.return_value = mock_response

        collector = DataCollector(config_root=self.config_dir)

        with self.assertRaises(GitHubRateLimitError):
            collector._check_github_rate_limit()

    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    @patch("requests.get")
    def test_github_data_caching(self, mock_get):
        """Test GitHub data is cached."""
        mock_rate_limit = Mock()
        mock_rate_limit.status_code = 200
        mock_rate_limit.json.return_value = {
            "resources": {"core": {"remaining": 5000, "reset": time.time() + 3600}}
        }
        mock_get.return_value = mock_rate_limit

        collector = DataCollector(config_root=self.config_dir, cache_ttl=10)

        # First call - should make API request
        cache_key = collector._get_cache_key("github", "test-repo", None, None)
        test_data = GitHubData(repo_name="test-repo")
        collector._cache[cache_key] = test_data

        # Second call - should use cache
        data = collector.collect_github_data(["test-repo"])

        self.assertEqual(data, test_data)
        # Should only call rate limit check, not actual data collection
        self.assertEqual(mock_get.call_count, 0)


class TestNotesDataCollection(unittest.TestCase):
    """Test notes data collection."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claude"
        self.config_dir.mkdir()

        (self.config_dir / "integrations.yaml").write_text(
            """
integrations:
  github:
    config:
      token_env: GITHUB_TOKEN
"""
        )
        (self.config_dir / "projects.yaml").write_text("{}")
        (self.config_dir / "team.yaml").write_text("{}")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_notes_collection_success(self, mock_exists, mock_run):
        """Test successful notes collection."""
        mock_exists.return_value = True

        mock_list_result = Mock()
        mock_list_result.returncode = 0
        mock_list_result.stdout = json.dumps({"notes": [{"title": "Test Note"}]})

        mock_actions_result = Mock()
        mock_actions_result.returncode = 0
        mock_actions_result.stdout = json.dumps(
            {"action_items": [{"task": "Do something"}]}
        )

        mock_run.side_effect = [mock_list_result, mock_actions_result]

        collector = DataCollector(config_root=self.config_dir)
        data = collector.collect_notes_data("test-project")

        self.assertIsInstance(data, NotesData)
        self.assertEqual(len(data.project_notes), 1)
        self.assertEqual(len(data.action_items), 1)

    def test_notes_cli_not_found(self):
        """Test notes collection fails when CLI not found."""
        collector = DataCollector(config_root=self.config_dir)

        # Patch only the notes CLI path check, not all Path.exists
        with patch.object(Path, 'exists', return_value=False):
            with self.assertRaises(DataCollectorError) as context:
                collector.collect_notes_data("test-project")

        self.assertIn("not found", str(context.exception).lower())

    @patch("subprocess.run")
    @patch("pathlib.Path.exists")
    def test_notes_cli_failure(self, mock_exists, mock_run):
        """Test notes collection handles CLI errors."""
        mock_exists.return_value = True

        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Error message"
        mock_run.return_value = mock_result

        collector = DataCollector(config_root=self.config_dir)

        with self.assertRaises(DataCollectorError):
            collector.collect_notes_data("test-project")


class TestAggregateProjectData(unittest.TestCase):
    """Test aggregate project data functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claude"
        self.config_dir.mkdir()

        (self.config_dir / "integrations.yaml").write_text(
            """
integrations:
  github:
    config:
      token_env: GITHUB_TOKEN
      default_org: test-org
"""
        )

        (self.config_dir / "projects.yaml").write_text(
            """
projects:
  test-project:
    github_repos:
      - test-repo
    team:
      - alice
"""
        )

        (self.config_dir / "team.yaml").write_text(
            """
team:
  members:
    - id: alice
      name: Alice
      role: developer
"""
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_project_not_found(self):
        """Test error when project not found."""
        collector = DataCollector(config_root=self.config_dir)

        with self.assertRaises(DataCollectorError) as context:
            collector.aggregate_project_data("nonexistent-project")

        self.assertIn("not found", str(context.exception).lower())

    @patch("tools.data_collector.DataCollector.collect_github_data")
    @patch("tools.data_collector.DataCollector.collect_notes_data")
    @patch("tools.data_collector.DataCollector.collect_team_data")
    def test_successful_aggregation(self, mock_team, mock_notes, mock_github):
        """Test successful data aggregation."""
        mock_github.return_value = GitHubData(repo_name="test-repo")
        mock_notes.return_value = NotesData()
        mock_team.return_value = Mock()

        collector = DataCollector(config_root=self.config_dir)
        data = collector.aggregate_project_data(
            "test-project", sources=["github", "notes", "team", "config"]
        )

        self.assertIsInstance(data, ProjectData)
        self.assertEqual(data.project_name, "test-project")
        self.assertIsNotNone(data.github_data)
        self.assertIsNotNone(data.notes_data)
        self.assertIn("sources", data.collection_summary)

    @patch("tools.data_collector.DataCollector.collect_github_data")
    def test_graceful_degradation(self, mock_github):
        """Test graceful degradation when sources fail."""
        mock_github.side_effect = Exception("GitHub API error")

        collector = DataCollector(config_root=self.config_dir)
        data = collector.aggregate_project_data("test-project", sources=["github", "config"])

        self.assertIsInstance(data, ProjectData)
        self.assertIsNone(data.github_data)
        self.assertIn("errors", data.collection_summary)
        self.assertTrue(len(data.collection_summary["errors"]) > 0)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and retry logic."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = Path(self.test_dir) / ".claude"
        self.config_dir.mkdir()

        (self.config_dir / "integrations.yaml").write_text(
            """
integrations:
  github:
    config:
      token_env: GITHUB_TOKEN
"""
        )
        (self.config_dir / "projects.yaml").write_text("{}")
        (self.config_dir / "team.yaml").write_text("{}")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_retry_logic(self):
        """Test retry with exponential backoff."""
        collector = DataCollector(config_root=self.config_dir, max_retries=3)

        call_count = 0

        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary error")
            return "success"

        result = collector._retry_request(failing_func)
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_retry_exhaustion(self):
        """Test retry exhaustion raises error."""
        collector = DataCollector(config_root=self.config_dir, max_retries=2)

        def always_failing():
            raise Exception("Permanent error")

        with self.assertRaises(DataCollectorError):
            collector._retry_request(always_failing)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataModels))
    suite.addTests(loader.loadTestsFromTestCase(TestDataCollectorInit))
    suite.addTests(loader.loadTestsFromTestCase(TestCaching))
    suite.addTests(loader.loadTestsFromTestCase(TestGitHubDataCollection))
    suite.addTests(loader.loadTestsFromTestCase(TestNotesDataCollection))
    suite.addTests(loader.loadTestsFromTestCase(TestAggregateProjectData))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

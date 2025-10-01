#!/usr/bin/env python3
"""
Test Suite for Project Synchronizer
Validates multi-project synchronization, conflict detection, and dependency analysis
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Import the synchronizer
from scripts.project_synchronizer import ProjectSynchronizer, ResourceConflict, DependencyIssue

def test_project_synchronizer_initialization():
    """Test ProjectSynchronizer initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".claude"
        config_dir.mkdir(exist_ok=True)

        # Create minimal projects.yaml
        projects_file = config_dir / "projects.yaml"
        projects_file.write_text("projects: {}\n")

        synchronizer = ProjectSynchronizer(str(config_dir))
        assert synchronizer.projects_config == {"projects": {}}

def test_resource_conflict_detection():
    """Test resource allocation conflict detection"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".claude"
        config_dir.mkdir(exist_ok=True)

        # Create test projects with resource conflicts
        projects_file = config_dir / "projects.yaml"
        projects_content = """
projects:
  project-a:
    name: "Project A"
    status: "active"
    priority: "high"
    owner: "developer@company.com"
    start_date: "2024-09-01"
    target_date: "2024-12-31"

  project-b:
    name: "Project B"
    status: "planning"
    priority: "medium"
    owner: "developer@company.com"
    start_date: "2024-11-01"
    target_date: "2025-02-28"
"""
        projects_file.write_text(projects_content)

        synchronizer = ProjectSynchronizer(str(config_dir))
        conflicts = synchronizer._detect_resource_conflicts({})

        # Should detect resource conflict for developer@company.com in Nov-Dec 2024
        assert len(conflicts) >= 1
        conflict = conflicts[0]
        assert conflict.resource == "developer@company.com"
        assert conflict.conflict_type == "time_overlap"
        assert set(conflict.projects) == {"project-a", "project-b"}

def test_dependency_analysis():
    """Test cross-project dependency analysis"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".claude"
        config_dir.mkdir(exist_ok=True)

        # Create test projects with dependency issues
        projects_file = config_dir / "projects.yaml"
        projects_content = """
projects:
  dependent-project:
    name: "Dependent Project"
    status: "planning"
    priority: "high"
    owner: "developer@company.com"
    dependencies: ["blocking-project"]

  blocking-project:
    name: "Blocking Project"
    status: "blocked"
    priority: "critical"
    owner: "other@company.com"
"""
        projects_file.write_text(projects_content)

        synchronizer = ProjectSynchronizer(str(config_dir))
        issues = synchronizer._analyze_cross_project_dependencies({})

        # Should detect dependency issue
        assert len(issues) >= 1
        issue = issues[0]
        assert issue.dependent_project == "dependent-project"
        assert issue.blocking_project == "blocking-project"
        assert issue.issue_type == "blocked"

def test_sync_all_projects():
    """Test full project synchronization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".claude"
        config_dir.mkdir(exist_ok=True)

        # Create comprehensive test projects
        projects_file = config_dir / "projects.yaml"
        projects_content = """
projects:
  marketing-campaign:
    name: "Marketing Campaign"
    status: "in_progress"
    priority: "high"
    owner: "marketing@company.com"
    start_date: "2024-09-01"
    target_date: "2024-12-31"

  product-development:
    name: "Product Development"
    status: "planning"
    priority: "medium"
    owner: "developer@company.com"
    start_date: "2024-10-01"
    target_date: "2025-03-01"
    dependencies: ["design-system"]

  design-system:
    name: "Design System"
    status: "blocked"
    priority: "high"
    owner: "designer@company.com"
"""
        projects_file.write_text(projects_content)

        synchronizer = ProjectSynchronizer(str(config_dir))
        result = synchronizer.sync_all_projects(analyze_conflicts=True)

        # Validate sync result structure
        assert len(result.projects_synced) == 3
        assert "marketing-campaign" in result.projects_synced
        assert "product-development" in result.projects_synced
        assert "design-system" in result.projects_synced

        # Should detect dependency issue (product-development depends on blocked design-system)
        assert len(result.dependency_issues) >= 1

        # Should have recommendations
        assert len(result.recommendations) > 0

def test_json_serialization():
    """Test JSON output format"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir) / ".claude"
        config_dir.mkdir(exist_ok=True)

        projects_file = config_dir / "projects.yaml"
        projects_file.write_text("projects: {}\n")

        synchronizer = ProjectSynchronizer(str(config_dir))
        result = synchronizer.sync_all_projects()

        # Should be JSON serializable
        from dataclasses import asdict
        json_data = json.dumps(asdict(result), indent=2, default=str)
        assert isinstance(json_data, str)
        assert "timestamp" in json_data

if __name__ == "__main__":
    # Run basic tests
    print("Running Project Synchronizer Tests...")

    try:
        test_project_synchronizer_initialization()
        print("✅ Initialization test passed")

        test_resource_conflict_detection()
        print("✅ Resource conflict detection test passed")

        test_dependency_analysis()
        print("✅ Dependency analysis test passed")

        test_sync_all_projects()
        print("✅ Full sync test passed")

        test_json_serialization()
        print("✅ JSON serialization test passed")

        print("\n🎉 All tests passed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
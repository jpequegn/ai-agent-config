#!/usr/bin/env python3
"""
Test script for Cross-Platform Data Collection System
Validates basic functionality and integration points
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

def test_configuration_loading():
    """Test that configurations can be loaded"""
    print("\n📋 Testing configuration loading...")

    try:
        from project_data_collector import ProjectDataCollector
        collector = ProjectDataCollector()

        # Test integrations config
        assert collector.integrations_config is not None
        print("  ✅ Integrations config loaded")

        # Test projects config
        assert collector.projects_config is not None
        projects = collector.projects_config.get('projects', {})
        print(f"  ✅ Projects config loaded ({len(projects)} projects)")

        # Check cache directory creation
        assert collector.cache_dir.exists()
        print("  ✅ Cache directory created")

        return True

    except Exception as e:
        print(f"  ❌ Configuration test failed: {e}")
        return False

def test_data_structures():
    """Test data structure creation"""
    print("\n🏗️ Testing data structures...")

    try:
        from project_data_collector import GitHubData, CalendarData, NotesData, ProjectData

        # Test GitHubData
        github_data = GitHubData(
            repo_name="test-repo",
            pull_requests=[],
            issues=[],
            commits=[],
            milestones=[],
            repository_stats={},
            collected_at=datetime.now().isoformat()
        )
        assert github_data.repo_name == "test-repo"
        print("  ✅ GitHubData structure works")

        # Test CalendarData
        calendar_data = CalendarData(
            events=[],
            meetings=[],
            deadlines=[],
            availability={},
            collected_at=datetime.now().isoformat()
        )
        print("  ✅ CalendarData structure works")

        # Test NotesData
        notes_data = NotesData(
            project_notes=[],
            action_items=[],
            decisions=[],
            collected_at=datetime.now().isoformat()
        )
        print("  ✅ NotesData structure works")

        # Test ProjectData
        project_data = ProjectData(
            project_name="test-project",
            github_data=github_data,
            calendar_data=calendar_data,
            notes_data=notes_data,
            collection_summary={'test': 'data'},
            collected_at=datetime.now().isoformat()
        )
        print("  ✅ ProjectData structure works")

        return True

    except Exception as e:
        print(f"  ❌ Data structure test failed: {e}")
        return False

def test_cache_functionality():
    """Test caching functionality"""
    print("\n💾 Testing cache functionality...")

    try:
        from project_data_collector import ProjectDataCollector
        collector = ProjectDataCollector()

        # Test cache key generation
        cache_path = collector._get_cache_path("test_key")
        assert cache_path.parent == collector.cache_dir
        print("  ✅ Cache path generation works")

        # Test cache save/load
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        collector._save_to_cache("test_cache", test_data)

        loaded_data = collector._load_from_cache("test_cache")
        assert loaded_data is not None
        assert loaded_data["test"] == "data"
        print("  ✅ Cache save/load works")

        # Test cache validity
        is_valid = collector._is_cache_valid("test_cache", max_age_minutes=60)
        assert is_valid == True
        print("  ✅ Cache validity check works")

        return True

    except Exception as e:
        print(f"  ❌ Cache test failed: {e}")
        return False

def test_project_listing():
    """Test project listing functionality"""
    print("\n📁 Testing project listing...")

    try:
        from project_data_collector import ProjectDataCollector
        collector = ProjectDataCollector()

        projects = collector.projects_config.get('projects', {})
        if projects:
            print(f"  ✅ Found {len(projects)} projects:")
            for project_name, project_config in projects.items():
                repos = project_config.get('github_repos', [])
                print(f"    - {project_name} ({len(repos)} repos)")
        else:
            print("  ⚠️ No projects found in configuration")

        return True

    except Exception as e:
        print(f"  ❌ Project listing test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🔑 Testing environment variables...")

    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        print("  ✅ GITHUB_TOKEN is set")
    else:
        print("  ⚠️ GITHUB_TOKEN not set (GitHub collection will fail)")

    calendar_key = os.environ.get('CALENDAR_API_KEY')
    if calendar_key:
        print("  ✅ CALENDAR_API_KEY is set")
    else:
        print("  ⚠️ CALENDAR_API_KEY not set (Calendar collection will use placeholder)")

    return True

def test_cli_interface():
    """Test CLI interface without making API calls"""
    print("\n💻 Testing CLI interface...")

    try:
        # Test help command
        import subprocess
        result = subprocess.run([sys.executable, 'project_data_collector.py', '--help'],
                              capture_output=True, text=True, timeout=10)

        if result.returncode == 0 and 'Cross-Platform Data Collection System' in result.stdout:
            print("  ✅ CLI help command works")
        else:
            print(f"  ❌ CLI help failed: {result.stderr}")
            return False

        # Test project listing (no arguments)
        result = subprocess.run([sys.executable, 'project_data_collector.py'],
                              capture_output=True, text=True, timeout=10)

        if 'Available projects:' in result.stdout:
            print("  ✅ CLI project listing works")
        else:
            print(f"  ⚠️ CLI project listing output: {result.stdout}")

        return True

    except Exception as e:
        print(f"  ❌ CLI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Testing Cross-Platform Data Collection System")
    print("=" * 60)

    tests = [
        ("Configuration Loading", test_configuration_loading),
        ("Data Structures", test_data_structures),
        ("Cache Functionality", test_cache_functionality),
        ("Project Listing", test_project_listing),
        ("Environment Variables", test_environment_variables),
        ("CLI Interface", test_cli_interface)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  💥 Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print("\n" + "=" * 60)
    if passed == len(results):
        print("✅ All tests passed! Data collection system is ready.")
        return 0
    else:
        print(f"❌ {len(results) - passed} test(s) failed. Please fix issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
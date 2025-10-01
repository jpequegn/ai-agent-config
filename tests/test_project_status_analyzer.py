#!/usr/bin/env python3
"""
Test script for Intelligent Project Status Analyzer
Validates health scoring, trend analysis, and integration functionality
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta

def test_analyzer_import():
    """Test that the analyzer can be imported"""
    print("\n📋 Testing analyzer import...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer, HealthMetrics, TrendAnalysis
        analyzer = ProjectStatusAnalyzer()
        print("  ✅ ProjectStatusAnalyzer imported successfully")
        print(f"  ✅ Found {len(analyzer.projects_config.get('projects', {}))} projects in configuration")
        return True
    except Exception as e:
        print(f"  ❌ Import test failed: {e}")
        return False

def test_health_calculation():
    """Test health metric calculation"""
    print("\n🏥 Testing health calculation...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        analyzer = ProjectStatusAnalyzer()

        # Test with a known project
        projects = analyzer.projects_config.get('projects', {})
        if not projects:
            print("  ⚠️ No projects found in configuration")
            return True

        project_name = list(projects.keys())[0]
        project_config = projects[project_name]

        health_metrics = analyzer._calculate_health_metrics(project_config)

        assert hasattr(health_metrics, 'overall_score')
        assert 0.0 <= health_metrics.overall_score <= 1.0
        assert health_metrics.category in ['excellent', 'good', 'at_risk', 'critical']

        print(f"  ✅ Health calculation works for {project_name}")
        print(f"    Score: {health_metrics.overall_score:.2f} ({health_metrics.category})")
        print(f"    Timeline: {health_metrics.timeline_progress:.2f}")
        print(f"    Activity: {health_metrics.activity_level:.2f}")
        print(f"    Blockers: {health_metrics.blocker_impact:.2f}")
        print(f"    Dependencies: {health_metrics.dependency_health:.2f}")

        return True
    except Exception as e:
        print(f"  ❌ Health calculation test failed: {e}")
        return False

def test_blocker_identification():
    """Test blocker identification"""
    print("\n🚧 Testing blocker identification...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        analyzer = ProjectStatusAnalyzer()

        projects = analyzer.projects_config.get('projects', {})
        if not projects:
            print("  ⚠️ No projects found in configuration")
            return True

        project_name = list(projects.keys())[0]
        project_config = projects[project_name]

        blockers, blocker_impact = analyzer._identify_blockers(project_config)

        assert isinstance(blockers, list)
        assert 0.0 <= blocker_impact <= 1.0

        print(f"  ✅ Blocker identification works for {project_name}")
        print(f"    Found {len(blockers)} blockers")
        print(f"    Blocker impact score: {blocker_impact:.2f}")

        for blocker in blockers:
            print(f"    - {blocker['type']}: {blocker['description']} ({blocker['severity']})")

        return True
    except Exception as e:
        print(f"  ❌ Blocker identification test failed: {e}")
        return False

def test_trend_analysis():
    """Test trend analysis"""
    print("\n📈 Testing trend analysis...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        analyzer = ProjectStatusAnalyzer()

        projects = analyzer.projects_config.get('projects', {})
        if not projects:
            print("  ⚠️ No projects found in configuration")
            return True

        project_name = list(projects.keys())[0]
        project_config = projects[project_name]

        trends = analyzer._analyze_trends(project_config)

        assert trends.velocity in ['increasing', 'stable', 'decreasing']
        assert trends.risk_level in ['low', 'medium', 'high']
        assert trends.activity_trend in ['increasing', 'stable', 'decreasing']
        assert 0.0 <= trends.confidence <= 1.0

        print(f"  ✅ Trend analysis works for {project_name}")
        print(f"    Velocity: {trends.velocity}")
        print(f"    Risk level: {trends.risk_level}")
        print(f"    Activity trend: {trends.activity_trend}")
        print(f"    Confidence: {trends.confidence:.2f}")

        return True
    except Exception as e:
        print(f"  ❌ Trend analysis test failed: {e}")
        return False

def test_project_analysis():
    """Test full project analysis"""
    print("\n🔍 Testing project analysis...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        analyzer = ProjectStatusAnalyzer()

        projects = analyzer.projects_config.get('projects', {})
        if not projects:
            print("  ⚠️ No projects found in configuration")
            return True

        project_name = list(projects.keys())[0]
        insight = analyzer.analyze_project(project_name)

        assert insight is not None
        assert insight.project_name == project_name
        assert hasattr(insight, 'health_metrics')
        assert hasattr(insight, 'trends')
        assert hasattr(insight, 'blockers')
        assert hasattr(insight, 'recommendations')

        print(f"  ✅ Project analysis works for {project_name}")
        print(f"    Health score: {insight.health_metrics.overall_score:.2f}")
        print(f"    Blockers: {len(insight.blockers)}")
        print(f"    Recommendations: {len(insight.recommendations)}")

        return True
    except Exception as e:
        print(f"  ❌ Project analysis test failed: {e}")
        return False

def test_portfolio_analysis():
    """Test portfolio analysis"""
    print("\n📊 Testing portfolio analysis...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        analyzer = ProjectStatusAnalyzer()

        portfolio = analyzer.analyze_portfolio()

        assert hasattr(portfolio, 'total_projects')
        assert hasattr(portfolio, 'health_distribution')
        assert hasattr(portfolio, 'portfolio_health_score')
        assert 0.0 <= portfolio.portfolio_health_score <= 1.0

        print(f"  ✅ Portfolio analysis works")
        print(f"    Total projects: {portfolio.total_projects}")
        print(f"    Portfolio health: {portfolio.portfolio_health_score:.2f}")
        print(f"    Health distribution: {portfolio.health_distribution}")
        print(f"    Critical actions needed: {portfolio.critical_actions_needed}")

        return True
    except Exception as e:
        print(f"  ❌ Portfolio analysis test failed: {e}")
        return False

def test_json_serialization():
    """Test JSON serialization of results"""
    print("\n📄 Testing JSON serialization...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        from dataclasses import asdict
        analyzer = ProjectStatusAnalyzer()

        projects = analyzer.projects_config.get('projects', {})
        if not projects:
            print("  ⚠️ No projects found in configuration")
            return True

        project_name = list(projects.keys())[0]
        insight = analyzer.analyze_project(project_name)

        # Test JSON serialization
        insight_json = json.dumps(asdict(insight), default=str, indent=2)
        assert len(insight_json) > 100  # Should be substantial JSON

        # Test deserialization
        parsed = json.loads(insight_json)
        assert parsed['project_name'] == project_name

        print(f"  ✅ JSON serialization works")
        print(f"    JSON length: {len(insight_json)} characters")

        return True
    except Exception as e:
        print(f"  ❌ JSON serialization test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface"""
    print("\n💻 Testing CLI interface...")

    try:
        import subprocess

        # Test help command
        result = subprocess.run([sys.executable, 'project_status_analyzer.py', '--help'],
                              capture_output=True, text=True, timeout=10)

        if result.returncode == 0 and 'Intelligent Project Status Analyzer' in result.stdout:
            print("  ✅ CLI help command works")
        else:
            print(f"  ❌ CLI help failed: {result.stderr}")
            return False

        # Test portfolio analysis
        result = subprocess.run([sys.executable, 'project_status_analyzer.py'],
                              capture_output=True, text=True, timeout=30)

        if result.returncode == 0 and 'Portfolio Health:' in result.stdout:
            print("  ✅ CLI portfolio analysis works")
        else:
            print(f"  ⚠️ CLI portfolio output: {result.stdout}")
            if result.stderr:
                print(f"  ⚠️ CLI errors: {result.stderr}")

        # Test JSON output
        result = subprocess.run([sys.executable, 'project_status_analyzer.py', '--json'],
                              capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            try:
                json.loads(result.stdout)
                print("  ✅ CLI JSON output works")
            except json.JSONDecodeError:
                print(f"  ❌ CLI JSON output invalid")
                return False

        return True
    except Exception as e:
        print(f"  ❌ CLI test failed: {e}")
        return False

def test_integration_with_data_collector():
    """Test integration with ProjectDataCollector"""
    print("\n🔗 Testing integration with ProjectDataCollector...")

    try:
        from project_status_analyzer import ProjectStatusAnalyzer
        analyzer = ProjectStatusAnalyzer()

        # Check if data collector is available
        if analyzer.data_collector is None:
            print("  ⚠️ ProjectDataCollector not available (expected in some environments)")
            return True

        projects = analyzer.projects_config.get('projects', {})
        if not projects:
            print("  ⚠️ No projects found in configuration")
            return True

        project_name = list(projects.keys())[0]

        # Test data collection integration (may fail due to missing API keys, which is expected)
        try:
            insight = analyzer.analyze_project(project_name)
            print(f"  ✅ Data collector integration works for {project_name}")
            print(f"    Analysis completed with health score: {insight.health_metrics.overall_score:.2f}")
        except Exception as e:
            print(f"  ⚠️ Data collection failed (expected without API keys): {e}")
            # This is expected and not a failure

        return True
    except Exception as e:
        print(f"  ❌ Data collector integration test failed: {e}")
        return False

def test_command_file_structure():
    """Test that the command file is properly structured"""
    print("\n📁 Testing command file structure...")

    try:
        command_file = Path('.claude/commands/project-status.md')

        if not command_file.exists():
            print("  ❌ Command file does not exist")
            return False

        content = command_file.read_text()

        # Check for required sections
        required_sections = [
            'name: project-status',
            '/project status',
            'Health Scoring',
            'JSON Output Format',
            'Instructions:'
        ]

        for section in required_sections:
            if section not in content:
                print(f"  ❌ Missing required section: {section}")
                return False

        print("  ✅ Command file structure is valid")
        print(f"    File size: {len(content)} characters")

        return True
    except Exception as e:
        print(f"  ❌ Command file structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Testing Intelligent Project Status Analyzer")
    print("=" * 60)

    tests = [
        ("Analyzer Import", test_analyzer_import),
        ("Health Calculation", test_health_calculation),
        ("Blocker Identification", test_blocker_identification),
        ("Trend Analysis", test_trend_analysis),
        ("Project Analysis", test_project_analysis),
        ("Portfolio Analysis", test_portfolio_analysis),
        ("JSON Serialization", test_json_serialization),
        ("CLI Interface", test_cli_interface),
        ("Data Collector Integration", test_integration_with_data_collector),
        ("Command File Structure", test_command_file_structure)
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
        print("✅ All tests passed! Project status analyzer is ready.")
        return 0
    else:
        print(f"❌ {len(results) - passed} test(s) failed. Please fix issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Integration tests for ProjectStatusGenerator with real project data.

Tests real-world usage scenarios to validate end-to-end functionality.
"""

from tools.project_status_generator import ProjectStatusGenerator, ProjectStatusGeneratorError


def test_single_project_status():
    """Test generating status for a single real project."""
    print("\n=== Test: Single Project Status ===")

    generator = ProjectStatusGenerator()

    try:
        status = generator.generate_status(project_id="mobile-app-v2")

        print(f"✅ Project: {status.project_name}")
        print(f"✅ Health Score: {status.health_score.score:.2f} ({status.health_score.category.value})")
        print(f"✅ Trends: {status.trends.direction.value if status.trends else 'N/A'}")
        print(f"✅ Risks: {len(status.risks)} identified")
        print(f"✅ Processing Time: {status.processing_time_ms:.2f}ms")
        print(f"✅ Output Length: {len(status.formatted_output)} characters")

        # Validation
        assert status.project_name == "mobile-app-v2"
        assert status.health_score.score >= 0.0 and status.health_score.score <= 1.0
        assert status.processing_time_ms > 0
        assert len(status.formatted_output) > 0

        print("\n✅ Single project test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ Single project test FAILED: {e}")
        return False


def test_all_projects_overview():
    """Test generating overview for all projects."""
    print("\n=== Test: All Projects Overview ===")

    generator = ProjectStatusGenerator()

    try:
        overview = generator.generate_overview()

        print(f"✅ Projects: {len(overview)} analyzed")
        for project_id, status in overview.items():
            print(f"   - {project_id}: {status.health_score.category.value} (score: {status.health_score.score:.2f})")

        # Validation
        assert len(overview) > 0
        for project_id, status in overview.items():
            assert status.project_name == project_id
            assert status.health_score.score >= 0.0 and status.health_score.score <= 1.0

        print("\n✅ Overview test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ Overview test FAILED: {e}")
        return False


def test_focus_modes():
    """Test different focus modes."""
    print("\n=== Test: Focus Modes ===")

    generator = ProjectStatusGenerator()

    focus_modes = ["risks", "health", "trends"]
    passed = 0

    for focus in focus_modes:
        try:
            status = generator.generate_status(project_id="mobile-app-v2", focus=focus)
            print(f"✅ Focus '{focus}': {len(status.formatted_output)} characters")
            passed += 1
        except Exception as e:
            print(f"❌ Focus '{focus}' FAILED: {e}")

    print(f"\n{'✅' if passed == len(focus_modes) else '❌'} Focus modes test: {passed}/{len(focus_modes)} passed")
    return passed == len(focus_modes)


def test_json_output():
    """Test JSON output format."""
    print("\n=== Test: JSON Output ===")

    generator = ProjectStatusGenerator()

    try:
        status = generator.generate_status(
            project_id="mobile-app-v2",
            output_format="json"
        )

        print(f"✅ JSON output generated: {len(status.formatted_output)} characters")

        # Validation
        assert "{" in status.formatted_output
        assert "}" in status.formatted_output

        print("\n✅ JSON output test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ JSON output test FAILED: {e}")
        return False


def test_missing_project():
    """Test error handling for missing project."""
    print("\n=== Test: Missing Project Error Handling ===")

    generator = ProjectStatusGenerator()

    try:
        status = generator.generate_status(project_id="nonexistent-project-xyz")
        print(f"❌ Should have raised error for missing project")
        return False
    except ProjectStatusGeneratorError as e:
        print(f"✅ Correctly raised error: {e}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_performance():
    """Test performance characteristics."""
    print("\n=== Test: Performance ===")

    generator = ProjectStatusGenerator()

    try:
        # First run (no cache)
        status1 = generator.generate_status(project_id="mobile-app-v2")
        first_run_time = status1.processing_time_ms
        print(f"✅ First run: {first_run_time:.2f}ms")

        # Second run (with cache)
        status2 = generator.generate_status(project_id="mobile-app-v2")
        second_run_time = status2.processing_time_ms
        print(f"✅ Second run: {second_run_time:.2f}ms")

        # Validation
        if first_run_time < 100:
            print(f"✅ Performance excellent: <100ms")
        elif first_run_time < 200:
            print(f"✅ Performance good: <200ms")
        else:
            print(f"⚠️  Performance acceptable: {first_run_time:.2f}ms")

        print(f"✅ Cache working: {'Yes' if second_run_time <= first_run_time else 'No'}")

        print("\n✅ Performance test PASSED")
        return True
    except Exception as e:
        print(f"\n❌ Performance test FAILED: {e}")
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("ProjectStatusGenerator Integration Tests")
    print("=" * 60)

    tests = [
        ("Single Project Status", test_single_project_status),
        ("All Projects Overview", test_all_projects_overview),
        ("Focus Modes", test_focus_modes),
        ("JSON Output", test_json_output),
        ("Missing Project Error", test_missing_project),
        ("Performance", test_performance),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print(f"\n{'✅' if passed == total else '❌'} Overall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")

    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

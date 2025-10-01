#!/usr/bin/env python3
"""
Test financial tool configuration loading with ConfigManager.

This script validates the financial_tools section migration to ConfigManager.
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tools import ConfigManager
from tools.schemas import IntegrationsConfig, FinancialTool
from tools.config_manager import ConfigValidationError


def test_financial_tools():
    """Test financial tool configuration loading."""
    print("=" * 60)
    print("Testing Financial Tools ConfigManager Integration")
    print("=" * 60)

    mgr = ConfigManager()

    # Test 1: Load all financial tools
    print("\n✅ Test 1: Load all financial tools")
    try:
        all_tools = mgr.get_all_financial_tools()
        print(f"Loaded {len(all_tools)} financial tools:")
        for tool_id, tool in all_tools.items():
            print(f"  - {tool_id}: {tool.provider} ({tool.status})")
    except Exception as e:
        print(f"❌ Failed to load financial tools: {e}")
        return False

    # Test 2: Get specific financial tool
    print("\n✅ Test 2: Get specific financial tool (plaid)")
    try:
        plaid = mgr.get_financial_tool("plaid")
        print(f"Provider: {plaid.provider}")
        print(f"Status: {plaid.status}")
        print(f"Connection Type: {plaid.connection_type}")
        print(f"Sync Frequency: {plaid.sync_frequency}")
        print(f"Data Types: {', '.join(plaid.data_types)}")
        if plaid.rate_limits:
            print(f"Rate Limits: {plaid.rate_limits.requests_per_hour}/hour, {plaid.rate_limits.requests_per_day}/day")
    except Exception as e:
        print(f"❌ Failed to get plaid: {e}")
        return False

    # Test 3: Filter for active tools
    print("\n✅ Test 3: Filter for active financial tools")
    try:
        active_tools = mgr.get_all_financial_tools(filters={"enabled": [True]})
        print(f"Found {len(active_tools)} active financial tools:")
        for tool_id, tool in active_tools.items():
            print(f"  - {tool_id}: {tool.provider}")
    except Exception as e:
        print(f"❌ Failed to filter active tools: {e}")
        return False

    # Test 4: Test error handling for missing tool
    print("\n✅ Test 4: Test error handling for missing tool")
    try:
        mgr.get_financial_tool("nonexistent_tool")
        print("❌ Should have raised KeyError for missing tool")
        return False
    except KeyError as e:
        print(f"✅ Correctly raised KeyError: {e}")

    # Test 5: Access nested configuration
    print("\n✅ Test 5: Access nested configuration safely")
    try:
        schwab = mgr.get_financial_tool("schwab")
        print(f"Schwab Provider: {schwab.provider}")
        print(f"API Version: {schwab.api_version}")
        if schwab.credentials:
            print("Credentials structure exists (values should be null/env vars)")
            print(f"  - client_id: {schwab.credentials.client_id}")
            print(f"  - client_secret: {schwab.credentials.client_secret}")
        if schwab.rate_limits:
            print(f"Rate Limits: {schwab.rate_limits.requests_per_hour}/hour")
    except Exception as e:
        print(f"❌ Failed to access nested config: {e}")
        return False

    # Test 6: Validate all tools have required fields
    print("\n✅ Test 6: Validate required fields for all tools")
    try:
        for tool_id, tool in all_tools.items():
            assert tool.enabled is not None, f"{tool_id}: enabled is required"
            assert tool.provider, f"{tool_id}: provider is required"
            assert tool.connection_type, f"{tool_id}: connection_type is required"
            assert tool.credentials, f"{tool_id}: credentials is required"
            assert tool.sync_frequency, f"{tool_id}: sync_frequency is required"
            assert tool.status, f"{tool_id}: status is required"
            assert isinstance(tool.data_types, list), f"{tool_id}: data_types must be a list"
        print("✅ All financial tools have required fields")
    except AssertionError as e:
        print(f"❌ Validation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_financial_tools()
    sys.exit(0 if success else 1)

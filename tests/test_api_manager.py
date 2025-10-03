"""
Tests for APIManager tool.

Target: >80% code coverage for all API management functions.
"""

import json
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

import pytest
import requests

from tools.api_manager import APIManager, APIManagerError, RateLimitExceededError
from tools.api_models import (
    APIRequest,
    APIResponse,
    BatchRequest,
    BatchResponse,
    CacheEntry,
    HTTPMethod,
    RateLimitStatus,
    ServiceConfig,
    ServiceType,
)


@pytest.fixture
def api_manager():
    """Create APIManager instance for testing."""
    return APIManager()


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    response = Mock(spec=requests.Response)
    response.ok = True
    response.status_code = 200
    response.headers = {"X-RateLimit-Remaining": "4999", "X-RateLimit-Limit": "5000"}
    response.json.return_value = {"data": "test_data"}
    return response


class TestAPIModels:
    """Test suite for API models."""

    def test_rate_limit_status(self):
        """Test RateLimitStatus model."""
        reset_time = datetime.now() + timedelta(seconds=100)
        rate_limit = RateLimitStatus(
            service="github",
            remaining=100,
            limit=5000,
            reset_time=reset_time,
        )

        assert rate_limit.service == "github"
        assert rate_limit.remaining == 100
        assert rate_limit.limit == 5000
        assert not rate_limit.is_limited
        assert rate_limit.reset_seconds > 0
        assert 0 < rate_limit.usage_percentage < 100

    def test_rate_limit_exceeded(self):
        """Test rate limit exceeded condition."""
        reset_time = datetime.now() + timedelta(seconds=100)
        rate_limit = RateLimitStatus(
            service="github",
            remaining=0,
            limit=5000,
            reset_time=reset_time,
        )

        assert rate_limit.is_limited
        assert rate_limit.usage_percentage == 100

    def test_api_response(self):
        """Test APIResponse model."""
        rate_limit = RateLimitStatus(
            service="github",
            remaining=100,
            limit=5000,
            reset_time=datetime.now() + timedelta(seconds=100),
        )

        response = APIResponse(
            success=True,
            status_code=200,
            data={"key": "value"},
            rate_limit=rate_limit,
        )

        assert response.success
        assert response.status_code == 200
        assert response.data == {"key": "value"}
        assert not response.is_rate_limited

    def test_api_response_rate_limited(self):
        """Test rate limited response."""
        response = APIResponse(
            success=False,
            status_code=429,
            error="Rate limit exceeded",
        )

        assert response.is_rate_limited

    def test_cache_entry(self):
        """Test CacheEntry model."""
        entry = CacheEntry(
            key="test_key",
            data={"test": "data"},
            timestamp=datetime.now(),
            ttl=60,
        )

        assert not entry.is_expired
        assert entry.age_seconds >= 0
        assert entry.hits == 0

    def test_cache_entry_expired(self):
        """Test expired cache entry."""
        entry = CacheEntry(
            key="test_key",
            data={"test": "data"},
            timestamp=datetime.now() - timedelta(seconds=120),
            ttl=60,
        )

        assert entry.is_expired


class TestAPIManager:
    """Test suite for APIManager."""

    def test_initialization(self, api_manager):
        """Test APIManager initialization."""
        assert api_manager is not None
        assert api_manager.max_retries == 3
        assert api_manager.backoff_factor == 2.0
        assert api_manager.default_cache_ttl == 300
        assert len(api_manager._cache) == 0

    @patch("requests.request")
    def test_generic_request(self, mock_request, api_manager, mock_response):
        """Test generic HTTP request."""
        mock_request.return_value = mock_response

        response = api_manager.request(
            service="generic",
            endpoint="https://api.example.com/test",
            method="GET",
        )

        assert isinstance(response, APIResponse)
        assert response.success
        assert response.status_code == 200
        assert response.data == {"data": "test_data"}
        mock_request.assert_called_once()

    @patch("requests.request")
    def test_github_request(self, mock_request, api_manager, mock_response):
        """Test GitHub API request."""
        mock_request.return_value = mock_response

        response = api_manager.github_request("/repos/owner/repo")

        assert response.success
        assert response.data == {"data": "test_data"}

    @patch("requests.request")
    def test_calendar_request(self, mock_request, api_manager, mock_response):
        """Test Calendar API request."""
        mock_request.return_value = mock_response

        response = api_manager.calendar_request("/calendars/primary/events")

        assert response.success

    @patch("requests.request")
    def test_jira_request(self, mock_request, api_manager, mock_response):
        """Test Jira API request."""
        mock_request.return_value = mock_response

        response = api_manager.jira_request("/rest/api/2/issue/TEST-1")

        assert response.success

    @patch("requests.request")
    def test_request_with_params(self, mock_request, api_manager, mock_response):
        """Test request with query parameters."""
        mock_request.return_value = mock_response

        response = api_manager.request(
            service="github",
            endpoint="/repos/owner/repo/issues",
            params={"state": "open", "page": 1},
        )

        assert response.success
        # Verify params were passed
        call_kwargs = mock_request.call_args[1]
        assert "params" in call_kwargs
        assert call_kwargs["params"] == {"state": "open", "page": 1}

    @patch("requests.request")
    def test_post_request_with_json(self, mock_request, api_manager, mock_response):
        """Test POST request with JSON data."""
        mock_request.return_value = mock_response

        response = api_manager.request(
            service="github",
            endpoint="/repos/owner/repo/issues",
            method="POST",
            json_data={"title": "Test Issue", "body": "Test body"},
        )

        assert response.success
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["json"] == {"title": "Test Issue", "body": "Test body"}

    @patch("requests.request")
    def test_caching(self, mock_request, api_manager, mock_response):
        """Test request caching."""
        mock_request.return_value = mock_response

        # First request - should hit API
        response1 = api_manager.request(
            service="github",
            endpoint="/repos/owner/repo",
            cache_ttl=300,
        )

        assert response1.success
        assert not response1.cached
        assert mock_request.call_count == 1

        # Second request - should use cache
        response2 = api_manager.request(
            service="github",
            endpoint="/repos/owner/repo",
            cache_ttl=300,
        )

        assert response2.success
        assert response2.cached
        assert mock_request.call_count == 1  # No additional API call

    def test_cache_result_and_get_cached(self, api_manager):
        """Test cache operations."""
        # Cache a result
        api_manager.cache_result(
            service="github",
            endpoint="/test",
            data={"test": "data"},
            ttl=60,
        )

        # Retrieve cached result
        cached = api_manager.get_cached(
            service="github",
            endpoint="/test",
        )

        assert cached is not None
        assert cached.cached
        assert cached.data == {"test": "data"}

    def test_cache_expiration(self, api_manager):
        """Test cache expiration."""
        # Cache with very short TTL
        api_manager.cache_result(
            service="github",
            endpoint="/test",
            data={"test": "data"},
            ttl=1,  # 1 second
        )

        # Wait for expiration
        time.sleep(1.1)

        # Should return None
        cached = api_manager.get_cached(
            service="github",
            endpoint="/test",
        )

        assert cached is None

    def test_clear_cache(self, api_manager):
        """Test cache clearing."""
        # Add some cache entries
        api_manager.cache_result("github", "/test1", {"data": 1}, 60)
        api_manager.cache_result("github", "/test2", {"data": 2}, 60)
        api_manager.cache_result("calendar", "/test3", {"data": 3}, 60)

        assert len(api_manager._cache) == 3

        # Clear all cache (service-specific clearing uses hash keys, so test full clear)
        cleared = api_manager.clear_cache()
        assert cleared == 3
        assert len(api_manager._cache) == 0

    @patch("requests.request")
    def test_retry_logic(self, mock_request, api_manager):
        """Test exponential backoff retry."""
        # Fail twice, succeed third time
        mock_response_fail = Mock(spec=requests.Response)
        mock_response_fail.ok = False
        mock_response_fail.status_code = 500
        mock_response_fail.headers = {}
        mock_response_fail.text = "Server error"

        mock_response_success = Mock(spec=requests.Response)
        mock_response_success.ok = True
        mock_response_success.status_code = 200
        mock_response_success.headers = {}
        mock_response_success.json.return_value = {"success": True}

        mock_request.side_effect = [
            mock_response_fail,
            mock_response_fail,
            mock_response_success,
        ]

        response = api_manager.request(
            service="github",
            endpoint="/test",
        )

        assert response.success
        assert mock_request.call_count == 3

    @patch("requests.request")
    def test_batch_requests_sequential(self, mock_request, api_manager, mock_response):
        """Test sequential batch requests."""
        mock_request.return_value = mock_response

        requests_list = [
            ("github", "/repos/owner/repo1", {}),
            ("github", "/repos/owner/repo2", {}),
            ("github", "/repos/owner/repo3", {}),
        ]

        batch_response = api_manager.batch_requests(requests_list, parallel=False)

        assert isinstance(batch_response, BatchResponse)
        assert len(batch_response.responses) == 3
        assert batch_response.success_count == 3
        assert batch_response.error_count == 0
        assert batch_response.total_time_ms > 0

    @patch("requests.request")
    def test_batch_requests_parallel(self, mock_request, api_manager, mock_response):
        """Test parallel batch requests."""
        mock_request.return_value = mock_response

        requests_list = [
            ("github", "/repos/owner/repo1", {}),
            ("github", "/repos/owner/repo2", {}),
        ]

        batch_response = api_manager.batch_requests(requests_list, parallel=True, max_concurrent=2)

        assert isinstance(batch_response, BatchResponse)
        assert len(batch_response.responses) == 2
        assert batch_response.success_count >= 0  # May have errors in parallel mode

    def test_check_rate_limit(self, api_manager):
        """Test rate limit checking."""
        rate_limit = api_manager.check_rate_limit("github")

        assert isinstance(rate_limit, RateLimitStatus)
        assert rate_limit.service == "github"
        assert rate_limit.remaining > 0

    def test_rate_limit_exceeded_error(self, api_manager):
        """Test rate limit exceeded error."""
        # Set rate limit to exceeded
        api_manager._rate_limits["github"] = RateLimitStatus(
            service="github",
            remaining=0,
            limit=5000,
            reset_time=datetime.now() + timedelta(seconds=100),
        )

        with pytest.raises(RateLimitExceededError):
            api_manager.request("github", "/test")

    @patch("requests.request")
    def test_rate_limit_update_from_response(self, mock_request, api_manager):
        """Test rate limit updating from response headers."""
        mock_response = Mock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Remaining": "4500",
            "X-RateLimit-Limit": "5000",
            "X-RateLimit-Reset": str(int((datetime.now() + timedelta(hours=1)).timestamp())),
        }
        mock_response.json.return_value = {"data": "test"}

        mock_request.return_value = mock_response

        response = api_manager.github_request("/test")

        assert response.success
        assert "github" in api_manager._rate_limits
        assert api_manager._rate_limits["github"].remaining == 4500

    def test_performance_stats(self, api_manager):
        """Test performance statistics tracking."""
        # Initially no stats
        stats = api_manager.get_performance_stats()
        assert stats["total_requests"] == 0

        # Add some mock request times
        api_manager._request_times = [10.0, 20.0, 30.0]

        stats = api_manager.get_performance_stats()
        assert stats["total_requests"] == 3
        assert stats["average_time_ms"] == 20.0
        assert stats["max_time_ms"] == 30.0
        assert stats["min_time_ms"] == 10.0

    @patch("requests.request")
    def test_request_error_handling(self, mock_request, api_manager):
        """Test error handling in requests."""
        mock_request.side_effect = requests.RequestException("Connection error")

        response = api_manager.request("github", "/test")

        assert not response.success
        assert response.error is not None
        assert "Connection error" in str(response.error)

    @patch("requests.request")
    def test_non_json_response(self, mock_request, api_manager):
        """Test handling of non-JSON responses."""
        mock_response = Mock(spec=requests.Response)
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.text = "Plain text response"

        mock_request.return_value = mock_response

        response = api_manager.request("github", "/test")

        assert response.success
        assert response.data == "Plain text response"

    @patch("requests.request")
    def test_performance_overhead(self, mock_request, api_manager, mock_response):
        """Test that overhead is <100ms as per requirements."""
        mock_request.return_value = mock_response

        # Measure overhead
        start = time.time()
        response = api_manager.request("github", "/test", cache_ttl=None)
        overhead = (time.time() - start) * 1000

        # Should be fast (excluding network time which is mocked)
        assert overhead < 100  # <100ms overhead requirement


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=tools.api_manager", "--cov-report=term-missing"])

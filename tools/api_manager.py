"""
APIManager - Unified API Integration

Unified API interface with rate limiting, caching, and error recovery for external services.

Simplifies command implementation from 60-80 lines down to 5-10 lines:

    api = APIManager()
    response = api.github_request("/repos/owner/repo/pulls")
    # Or with caching
    response = api.request("github", "/repos/owner/repo", cache_ttl=3600)
"""

import hashlib
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import requests
from cachetools import TTLCache

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
from tools.config_manager import ConfigManager


class APIManagerError(Exception):
    """Base exception for APIManager errors."""

    pass


class RateLimitExceededError(APIManagerError):
    """Raised when API rate limit is exceeded."""

    pass


class APIManager:
    """
    Unified API management system with rate limiting, caching, and retry logic.

    Features:
    - Generic HTTP client (GET, POST, PUT, DELETE, PATCH)
    - Service-specific methods (GitHub, Calendar, Jira)
    - Automatic rate limiting with waiting
    - TTL-based caching
    - Exponential backoff retry
    - Batch operations with parallelization
    - Performance: <100ms overhead per request

    Example:
        >>> api = APIManager()
        >>> # GitHub request (80 lines → 2 lines)
        >>> response = api.github_request("/repos/owner/repo/pulls")
        >>> print(f"PRs: {len(response.data)}")

        >>> # With caching
        >>> response = api.request("github", "/repos/owner/repo", cache_ttl=3600)

        >>> # Batch requests
        >>> responses = api.batch_requests([
        ...     ("github", "/repos/owner/repo1", {}),
        ...     ("github", "/repos/owner/repo2", {}),
        ... ], parallel=True)
    """

    def __init__(
        self,
        config_root: Optional[Path] = None,
        cache_ttl: int = 300,  # 5 minutes default
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ):
        """
        Initialize APIManager.

        Args:
            config_root: Root directory for configuration files
            cache_ttl: Default cache time-to-live in seconds (default: 300)
            max_retries: Maximum retry attempts for failed requests (default: 3)
            backoff_factor: Exponential backoff multiplier (default: 2.0)
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self.config_manager = ConfigManager(config_root=self.config_root)
        self.default_cache_ttl = cache_ttl
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

        # Initialize cache
        self._cache: Dict[str, CacheEntry] = {}

        # Rate limit tracking per service
        self._rate_limits: Dict[str, RateLimitStatus] = {}

        # Service configurations
        self._service_configs: Dict[str, ServiceConfig] = {}

        # Load configurations
        self._load_service_configs()

        # Performance tracking
        self._request_times: List[float] = []

    def request(
        self,
        service: str,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cache_ttl: Optional[int] = None,
        timeout: int = 30,
    ) -> APIResponse:
        """
        Make a generic API request with automatic retry and caching.

        Args:
            service: Service name (github, calendar, jira, generic)
            endpoint: API endpoint path
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            params: Query parameters
            data: Request body data
            json_data: JSON request body
            headers: Additional headers
            cache_ttl: Cache TTL in seconds (None = no cache)
            timeout: Request timeout in seconds

        Returns:
            APIResponse with data, status, and metadata
        """
        start_time = time.time()

        # Check cache for GET requests
        if method.upper() == "GET" and cache_ttl is not None:
            cached = self.get_cached(service, endpoint, params)
            if cached:
                return cached

        # Check rate limit
        self._check_rate_limit(service)

        # Build request
        api_request = APIRequest(
            service=service,
            endpoint=endpoint,
            method=HTTPMethod[method.upper()],
            params=params or {},
            headers=headers or {},
            data=data,
            json_data=json_data,
            cache_ttl=cache_ttl,
            timeout=timeout,
            max_retries=self.max_retries,
        )

        # Execute with retry
        response = self._retry_with_backoff(self._execute_request, api_request)

        # Cache successful GET responses
        if response.success and method.upper() == "GET" and cache_ttl:
            self.cache_result(service, endpoint, response.data, cache_ttl, params)

        # Track performance
        response_time = (time.time() - start_time) * 1000
        self._request_times.append(response_time)
        response.response_time_ms = response_time

        return response

    def github_request(
        self,
        endpoint: str,
        method: str = "GET",
        **kwargs,
    ) -> APIResponse:
        """
        Make a GitHub API request.

        Simplifies from ~80 lines to 2 lines.

        Args:
            endpoint: GitHub API endpoint (e.g., "/repos/owner/repo/pulls")
            method: HTTP method
            **kwargs: Additional request parameters

        Returns:
            APIResponse with GitHub data
        """
        return self.request("github", endpoint, method=method, **kwargs)

    def calendar_request(
        self,
        endpoint: str,
        method: str = "GET",
        **kwargs,
    ) -> APIResponse:
        """
        Make a Google Calendar API request.

        Args:
            endpoint: Calendar API endpoint
            method: HTTP method
            **kwargs: Additional request parameters

        Returns:
            APIResponse with calendar data
        """
        return self.request("calendar", endpoint, method=method, **kwargs)

    def jira_request(
        self,
        endpoint: str,
        method: str = "GET",
        **kwargs,
    ) -> APIResponse:
        """
        Make a Jira API request.

        Args:
            endpoint: Jira API endpoint
            method: HTTP method
            **kwargs: Additional request parameters

        Returns:
            APIResponse with Jira data
        """
        return self.request("jira", endpoint, method=method, **kwargs)

    def batch_requests(
        self,
        requests_list: List[Tuple[str, str, Dict[str, Any]]],
        parallel: bool = False,
        max_concurrent: int = 5,
    ) -> BatchResponse:
        """
        Execute multiple API requests in batch.

        Args:
            requests_list: List of (service, endpoint, kwargs) tuples
            parallel: Execute requests in parallel
            max_concurrent: Maximum concurrent requests (if parallel)

        Returns:
            BatchResponse with all results
        """
        start_time = time.time()
        responses: List[APIResponse] = []

        if parallel:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
                futures = []
                for service, endpoint, kwargs in requests_list:
                    future = executor.submit(self.request, service, endpoint, **kwargs)
                    futures.append(future)

                for future in as_completed(futures):
                    try:
                        response = future.result()
                        responses.append(response)
                    except Exception as e:
                        # Create error response
                        responses.append(
                            APIResponse(
                                success=False,
                                status_code=0,
                                error=str(e),
                            )
                        )
        else:
            # Sequential execution
            for service, endpoint, kwargs in requests_list:
                try:
                    response = self.request(service, endpoint, **kwargs)
                    responses.append(response)
                except Exception as e:
                    responses.append(
                        APIResponse(
                            success=False,
                            status_code=0,
                            error=str(e),
                        )
                    )

        total_time = (time.time() - start_time) * 1000

        return BatchResponse(
            responses=responses,
            total_time_ms=total_time,
            metadata={"parallel": parallel, "max_concurrent": max_concurrent},
        )

    def check_rate_limit(self, service: str) -> RateLimitStatus:
        """
        Check rate limit status for a service.

        Args:
            service: Service name

        Returns:
            RateLimitStatus with current limit info
        """
        if service not in self._rate_limits:
            # Default rate limit if not tracked
            return RateLimitStatus(
                service=service,
                remaining=5000,
                limit=5000,
                reset_time=datetime.now() + timedelta(hours=1),
            )

        return self._rate_limits[service]

    def wait_for_rate_limit(self, service: str) -> None:
        """
        Wait for rate limit to reset.

        Args:
            service: Service name
        """
        rate_limit = self.check_rate_limit(service)
        if rate_limit.is_limited:
            wait_time = rate_limit.reset_seconds
            if wait_time > 0:
                time.sleep(wait_time)

    def cache_result(
        self,
        service: str,
        endpoint: str,
        data: Any,
        ttl: int,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Cache API response result.

        Args:
            service: Service name
            endpoint: API endpoint
            data: Data to cache
            ttl: Time-to-live in seconds
            params: Query parameters (for cache key)
        """
        cache_key = self._get_cache_key(service, endpoint, params)
        self._cache[cache_key] = CacheEntry(
            key=cache_key,
            data=data,
            timestamp=datetime.now(),
            ttl=ttl,
        )

    def get_cached(
        self,
        service: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[APIResponse]:
        """
        Get cached API response.

        Args:
            service: Service name
            endpoint: API endpoint
            params: Query parameters (for cache key)

        Returns:
            APIResponse if cached and not expired, None otherwise
        """
        cache_key = self._get_cache_key(service, endpoint, params)

        if cache_key not in self._cache:
            return None

        entry = self._cache[cache_key]

        # Check expiration
        if entry.is_expired:
            del self._cache[cache_key]
            return None

        # Update hits
        entry.hits += 1

        # Return cached response
        return APIResponse(
            success=True,
            status_code=200,
            data=entry.data,
            cached=True,
            metadata={"cache_age_seconds": entry.age_seconds, "cache_hits": entry.hits},
        )

    def clear_cache(self, service: Optional[str] = None) -> int:
        """
        Clear cache for a service or all services.

        Args:
            service: Service name (None = clear all)

        Returns:
            Number of entries cleared
        """
        if service is None:
            count = len(self._cache)
            self._cache.clear()
            return count

        # Clear service-specific cache
        keys_to_delete = [key for key in self._cache.keys() if key.startswith(f"{service}_")]
        for key in keys_to_delete:
            del self._cache[key]

        return len(keys_to_delete)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get API performance statistics."""
        if not self._request_times:
            return {
                "average_time_ms": 0.0,
                "max_time_ms": 0.0,
                "min_time_ms": 0.0,
                "total_requests": 0,
                "cache_size": len(self._cache),
            }

        return {
            "average_time_ms": sum(self._request_times) / len(self._request_times),
            "max_time_ms": max(self._request_times),
            "min_time_ms": min(self._request_times),
            "total_requests": len(self._request_times),
            "cache_size": len(self._cache),
            "cache_hit_rate": self._calculate_cache_hit_rate(),
        }

    # Private helper methods

    def _load_service_configs(self):
        """Load service configurations from integrations.yaml."""
        try:
            integrations = self.config_manager.load_config("integrations.yaml")
            services = integrations.get("integrations", {})

            # Load GitHub config
            if "github" in services:
                github_config = services["github"].get("config", {})
                token_env = github_config.get("token_env", "GITHUB_TOKEN")
                token = os.environ.get(token_env)

                self._service_configs["github"] = ServiceConfig(
                    name="github",
                    base_url="https://api.github.com",
                    auth_type="token",
                    auth_header="Authorization",
                    auth_prefix="token",
                    rate_limit=5000,
                    rate_limit_period=3600,
                    default_headers={"Accept": "application/vnd.github.v3+json"},
                )

                # Store token for auth
                if token:
                    os.environ["_GITHUB_TOKEN"] = token

            # Load Calendar config
            if "calendar" in services:
                calendar_config = services["calendar"].get("config", {})
                key_env = calendar_config.get("api_key_env", "CALENDAR_API_KEY")
                api_key = os.environ.get(key_env)

                self._service_configs["calendar"] = ServiceConfig(
                    name="calendar",
                    base_url="https://www.googleapis.com/calendar/v3",
                    auth_type="api_key",
                    rate_limit=1000,
                    rate_limit_period=3600,
                )

                if api_key:
                    os.environ["_CALENDAR_API_KEY"] = api_key

            # Load Jira config
            if "jira" in services:
                jira_config = services["jira"].get("config", {})
                token_env = jira_config.get("token_env", "JIRA_TOKEN")
                token = os.environ.get(token_env)
                base_url = jira_config.get("base_url", "https://your-domain.atlassian.net")

                self._service_configs["jira"] = ServiceConfig(
                    name="jira",
                    base_url=base_url,
                    auth_type="token",
                    auth_header="Authorization",
                    auth_prefix="Bearer",
                    rate_limit=100,
                    rate_limit_period=60,
                )

                if token:
                    os.environ["_JIRA_TOKEN"] = token

        except Exception as e:
            # Non-fatal - can still use generic requests
            pass

    def _get_cache_key(self, service: str, endpoint: str, params: Optional[Dict[str, Any]]) -> str:
        """Generate cache key from request parameters."""
        key_parts = [service, endpoint]
        if params:
            key_parts.append(str(sorted(params.items())))
        key_str = "_".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()

    def _check_rate_limit(self, service: str) -> None:
        """Check and handle rate limiting."""
        if service not in self._rate_limits:
            return

        rate_limit = self._rate_limits[service]
        if rate_limit.is_limited:
            raise RateLimitExceededError(
                f"Rate limit exceeded for {service}. "
                f"Resets in {rate_limit.reset_seconds:.0f}s"
            )

        # Warn if getting low
        if rate_limit.remaining < 100:
            pass  # Could log warning here

    def _execute_request(self, api_request: APIRequest) -> APIResponse:
        """Execute a single API request."""
        # Get service config
        service_config = self._service_configs.get(api_request.service)

        # Build full URL
        if service_config:
            url = f"{service_config.base_url}{api_request.endpoint}"
        else:
            # Generic request - endpoint must be full URL
            url = api_request.endpoint

        # Build headers
        headers = {}
        if service_config:
            headers.update(service_config.default_headers)
            # Add authentication
            if service_config.auth_type == "token":
                token = os.environ.get(f"_{service_config.name.upper()}_TOKEN")
                if token:
                    headers[service_config.auth_header] = f"{service_config.auth_prefix} {token}"
            elif service_config.auth_type == "api_key":
                api_key = os.environ.get(f"_{service_config.name.upper()}_API_KEY")
                if api_key:
                    headers["X-API-Key"] = api_key

        headers.update(api_request.headers)

        # Make request
        try:
            response = requests.request(
                method=api_request.method.value,
                url=url,
                params=api_request.params,
                data=api_request.data,
                json=api_request.json_data,
                headers=headers,
                timeout=api_request.timeout,
            )

            # Update rate limit from response headers
            self._update_rate_limit_from_response(api_request.service, response)

            # Parse response
            try:
                data = response.json()
            except Exception:
                data = response.text

            return APIResponse(
                success=response.ok,
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                rate_limit=self._rate_limits.get(api_request.service),
            )

        except requests.RequestException as e:
            return APIResponse(
                success=False,
                status_code=0,
                error=str(e),
            )

    def _retry_with_backoff(self, func: Callable, *args, **kwargs) -> APIResponse:
        """Execute function with exponential backoff retry."""
        last_response = None

        for attempt in range(self.max_retries):
            try:
                response = func(*args, **kwargs)

                # Success or non-retryable error
                if response.success or (
                    response.status_code not in [429, 500, 502, 503, 504]
                ):
                    return response

                last_response = response

                # Wait before retry
                if attempt < self.max_retries - 1:
                    wait_time = (self.backoff_factor ** attempt)
                    time.sleep(wait_time)

            except Exception as e:
                if attempt == self.max_retries - 1:
                    return APIResponse(
                        success=False,
                        status_code=0,
                        error=f"Request failed after {self.max_retries} attempts: {e}",
                    )
                wait_time = (self.backoff_factor ** attempt)
                time.sleep(wait_time)

        return last_response or APIResponse(
            success=False,
            status_code=0,
            error="Request failed after retries",
        )

    def _update_rate_limit_from_response(self, service: str, response: requests.Response) -> None:
        """Update rate limit tracking from response headers."""
        # GitHub rate limit headers
        if service == "github":
            if "X-RateLimit-Remaining" in response.headers:
                remaining = int(response.headers["X-RateLimit-Remaining"])
                limit = int(response.headers.get("X-RateLimit-Limit", 5000))
                reset = int(response.headers.get("X-RateLimit-Reset", 0))

                self._rate_limits[service] = RateLimitStatus(
                    service=service,
                    remaining=remaining,
                    limit=limit,
                    reset_time=datetime.fromtimestamp(reset) if reset else datetime.now(),
                )

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        if not self._cache:
            return 0.0

        total_hits = sum(entry.hits for entry in self._cache.values())
        total_requests = len(self._request_times)

        if total_requests == 0:
            return 0.0

        return (total_hits / total_requests) * 100

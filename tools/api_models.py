"""
APIManager Data Models

Data classes for API management system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class HTTPMethod(Enum):
    """HTTP request methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ServiceType(Enum):
    """Supported API service types."""

    GITHUB = "github"
    CALENDAR = "calendar"
    JIRA = "jira"
    GENERIC = "generic"


@dataclass
class RateLimitStatus:
    """Rate limit status for an API service."""

    service: str
    remaining: int
    limit: int
    reset_time: datetime
    reset_seconds: float = 0.0

    def __post_init__(self):
        """Calculate seconds until reset."""
        if isinstance(self.reset_time, datetime):
            self.reset_seconds = max(0, (self.reset_time - datetime.now()).total_seconds())

    @property
    def is_limited(self) -> bool:
        """Check if rate limit is currently exceeded."""
        return self.remaining <= 0 and self.reset_seconds > 0

    @property
    def usage_percentage(self) -> float:
        """Calculate percentage of rate limit used."""
        if self.limit == 0:
            return 0.0
        return ((self.limit - self.remaining) / self.limit) * 100


@dataclass
class APIResponse:
    """Response from an API request."""

    success: bool
    status_code: int
    data: Any = None
    error: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    cached: bool = False
    response_time_ms: float = 0.0
    rate_limit: Optional[RateLimitStatus] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_rate_limited(self) -> bool:
        """Check if response indicates rate limiting."""
        return self.status_code in (429, 403) or (self.rate_limit and self.rate_limit.is_limited)


@dataclass
class APIRequest:
    """Configuration for an API request."""

    service: str
    endpoint: str
    method: HTTPMethod = HTTPMethod.GET
    params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    data: Optional[Any] = None
    json_data: Optional[Dict[str, Any]] = None
    cache_ttl: Optional[int] = None
    timeout: int = 30
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class BatchRequest:
    """Batch request configuration."""

    requests: List[APIRequest]
    parallel: bool = False
    max_concurrent: int = 5
    stop_on_error: bool = False


@dataclass
class BatchResponse:
    """Response from a batch request."""

    responses: List[APIResponse]
    success_count: int = 0
    error_count: int = 0
    total_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Calculate success/error counts."""
        self.success_count = sum(1 for r in self.responses if r.success)
        self.error_count = len(self.responses) - self.success_count


@dataclass
class CacheEntry:
    """Cache entry with TTL."""

    key: str
    data: Any
    timestamp: datetime
    ttl: int  # seconds
    hits: int = 0

    @property
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        age = (datetime.now() - self.timestamp).total_seconds()
        return age >= self.ttl

    @property
    def age_seconds(self) -> float:
        """Get age of cache entry in seconds."""
        return (datetime.now() - self.timestamp).total_seconds()


@dataclass
class ServiceConfig:
    """Configuration for an API service."""

    name: str
    base_url: str
    auth_type: str  # token, api_key, oauth, basic, none
    auth_header: str = "Authorization"
    auth_prefix: str = "Bearer"
    rate_limit: Optional[int] = None  # requests per period
    rate_limit_period: int = 3600  # seconds (default: 1 hour)
    default_timeout: int = 30
    default_headers: Dict[str, str] = field(default_factory=dict)
    retry_on_status: List[int] = field(default_factory=lambda: [429, 500, 502, 503, 504])

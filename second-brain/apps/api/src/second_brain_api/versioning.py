"""Central API URL-versioning rules.

Routers should build public paths with :func:`versioned_path` instead of
repeating ``/api/v1`` throughout the application.
"""
from __future__ import annotations

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"


def versioned_path(path: str = "") -> str:
    """Return a normalized public API path under the current API version."""
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if path and not path.startswith("/"):
        raise ValueError("path must start with '/'")
    if path == API_PREFIX or path.startswith(f"{API_PREFIX}/"):
        raise ValueError("path is already versioned")
    return API_PREFIX if not path else f"{API_PREFIX}{path}"


def assert_versioned_path(path: str) -> None:
    """Raise when a public route is outside the current API version."""
    if not (path == API_PREFIX or path.startswith(f"{API_PREFIX}/")):
        raise ValueError(f"public route must start with {API_PREFIX}: {path}")

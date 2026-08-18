"""Small adapter for turning domain errors into HTTP-framework responses."""
from __future__ import annotations

from typing import Any

from .errors import ApiError, internal_failure


def error_response(error: ApiError, trace_id: str) -> tuple[int, dict[str, str], dict[str, Any]]:
    """Return status, headers, and JSON-ready body for an intentional API error."""
    headers = {"Content-Type": "application/json", "X-Trace-ID": trace_id, **error.headers}
    return error.status_code, headers, error.envelope(trace_id).to_dict()


def unexpected_error_response(trace_id: str) -> tuple[int, dict[str, str], dict[str, Any]]:
    """Hide unexpected exception details behind the stable internal-error shape."""
    return error_response(internal_failure(), trace_id)

"""Trace-ID handling shared by HTTP middleware and error handlers."""
from __future__ import annotations

import re
import uuid

TRACE_HEADER = "X-Trace-ID"
_SAFE_TRACE_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


def new_trace_id() -> str:
    return str(uuid.uuid4())


def trace_id_from_header(value: str | None) -> str:
    """Reuse a safe caller trace ID or create one; reject header injection."""
    if value and _SAFE_TRACE_ID.fullmatch(value):
        return value
    return new_trace_id()

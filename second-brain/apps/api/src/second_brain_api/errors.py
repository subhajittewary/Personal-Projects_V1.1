"""Framework-neutral API errors and the stable error response envelope."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class FieldError:
    field: str
    code: str
    message: str | None = None

    def to_dict(self) -> dict[str, str]:
        result = {"field": self.field, "code": self.code}
        if self.message is not None:
            result["message"] = self.message
        return result


@dataclass(frozen=True, slots=True)
class ErrorEnvelope:
    code: str
    message: str
    trace_id: str
    field_errors: tuple[FieldError, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "trace_id": self.trace_id,
        }
        if self.field_errors:
            result["field_errors"] = [error.to_dict() for error in self.field_errors]
        return result


class ApiError(Exception):
    """An intentional client-safe error returned by an API boundary."""

    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        field_errors: tuple[FieldError, ...] = (),
        headers: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.field_errors = field_errors
        self.headers = dict(headers or {})

    def envelope(self, trace_id: str) -> ErrorEnvelope:
        return ErrorEnvelope(
            code=self.code,
            message=self.message,
            trace_id=trace_id,
            field_errors=self.field_errors,
        )


def validation_error(
    message: str = "The request could not be validated.",
    *,
    field_errors: tuple[FieldError, ...] = (),
) -> ApiError:
    return ApiError(status_code=422, code="VALIDATION_ERROR", message=message, field_errors=field_errors)


def authentication_required(message: str = "Authentication is required.") -> ApiError:
    return ApiError(status_code=401, code="AUTHENTICATION_REQUIRED", message=message, headers={"WWW-Authenticate": "Bearer"})


def authorization_denied(message: str = "You are not authorized to perform this action.") -> ApiError:
    return ApiError(status_code=403, code="AUTHORIZATION_DENIED", message=message)


def resource_conflict(message: str = "The request conflicts with the current resource state.") -> ApiError:
    return ApiError(status_code=409, code="RESOURCE_CONFLICT", message=message)


def upstream_failure(message: str = "A dependent service is temporarily unavailable.") -> ApiError:
    """Return a safe message; provider exception details must not reach clients."""
    return ApiError(status_code=502, code="UPSTREAM_FAILURE", message=message)


def not_found(message: str = "The requested resource was not found.") -> ApiError:
    return ApiError(status_code=404, code="RESOURCE_NOT_FOUND", message=message)


def internal_failure(message: str = "The request could not be completed.") -> ApiError:
    return ApiError(status_code=500, code="INTERNAL_ERROR", message=message)

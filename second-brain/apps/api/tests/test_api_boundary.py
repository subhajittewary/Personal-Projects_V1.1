import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from second_brain_api.errors import (  # noqa: E402
    FieldError,
    authentication_required,
    authorization_denied,
    resource_conflict,
    upstream_failure,
    validation_error,
)
from second_brain_api.response import error_response, unexpected_error_response  # noqa: E402
from second_brain_api.trace import TRACE_HEADER, new_trace_id, trace_id_from_header  # noqa: E402
from second_brain_api.versioning import API_PREFIX, assert_versioned_path, versioned_path  # noqa: E402


class VersioningTests(unittest.TestCase):
    def test_versioned_path(self):
        self.assertEqual(versioned_path("/documents"), "/api/v1/documents")
        self.assertEqual(versioned_path(), "/api/v1")

    def test_rejects_double_versioning(self):
        with self.assertRaises(ValueError):
            versioned_path("/api/v1/documents")

    def test_asserts_public_prefix(self):
        assert_versioned_path(f"{API_PREFIX}/health")
        with self.assertRaises(ValueError):
            assert_versioned_path("/health")


class ErrorTests(unittest.TestCase):
    def test_validation_envelope(self):
        error = validation_error(
            field_errors=(FieldError("email", "INVALID_FORMAT", "Enter a valid email."),)
        )
        status, headers, body = error_response(error, "trace-123")
        self.assertEqual(status, 422)
        self.assertEqual(headers[TRACE_HEADER], "trace-123")
        self.assertEqual(body["code"], "VALIDATION_ERROR")
        self.assertEqual(body["field_errors"][0]["field"], "email")

    def test_standard_error_mappings(self):
        self.assertEqual(authentication_required().status_code, 401)
        self.assertEqual(authorization_denied().status_code, 403)
        self.assertEqual(resource_conflict().status_code, 409)
        self.assertEqual(upstream_failure().status_code, 502)

    def test_unexpected_errors_are_safe(self):
        status, _, body = unexpected_error_response("trace-456")
        self.assertEqual(status, 500)
        self.assertNotIn("database", body["message"].lower())


class TraceTests(unittest.TestCase):
    def test_valid_trace_id_is_reused(self):
        self.assertEqual(trace_id_from_header("trace_123"), "trace_123")

    def test_invalid_trace_id_is_replaced(self):
        generated = trace_id_from_header("bad value\r\nX-Leak: true")
        self.assertNotIn("\n", generated)
        self.assertNotEqual(generated, "bad value\r\nX-Leak: true")
        self.assertTrue(new_trace_id())


if __name__ == "__main__":
    unittest.main()

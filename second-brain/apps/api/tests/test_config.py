import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from second_brain_api.config import SettingsError, load_settings  # noqa: E402


BASE_ENV = {
    "APP_ENV": "test",
    "POSTGRES_DB": "second_brain",
    "POSTGRES_USER": "second_brain",
    "POSTGRES_PASSWORD": "postgres-secret",
    "NEO4J_AUTH": "neo4j/neo4j-secret",
    "APP_SECRET_KEY": "a" * 32,
}


class ConfigTests(unittest.TestCase):
    def test_loads_valid_settings(self):
        settings = load_settings(BASE_ENV)
        self.assertEqual(settings.api_port, 8000)
        self.assertEqual(settings.qdrant_url, "http://qdrant:6333")
        self.assertEqual(settings.cors_origins, ("http://localhost:5173",))

    def test_requires_secrets(self):
        for key in ("POSTGRES_PASSWORD", "NEO4J_AUTH", "APP_SECRET_KEY"):
            env = dict(BASE_ENV)
            env.pop(key)
            with self.subTest(key=key), self.assertRaises(SettingsError):
                load_settings(env)

    def test_rejects_invalid_values(self):
        env = dict(BASE_ENV, API_PORT="not-a-port")
        with self.assertRaises(SettingsError):
            load_settings(env)

        env = dict(BASE_ENV, QDRANT_URL="qdrant:6333")
        with self.assertRaises(SettingsError):
            load_settings(env)

    def test_redacted_summary_contains_no_secret_values(self):
        settings = load_settings(BASE_ENV)
        summary = settings.redacted()
        serialized = repr(summary)
        self.assertNotIn("postgres-secret", serialized)
        self.assertNotIn("neo4j-secret", serialized)
        self.assertNotIn("a" * 32, serialized)
        self.assertEqual(summary["app_secret_key"], "***")


if __name__ == "__main__":
    unittest.main()

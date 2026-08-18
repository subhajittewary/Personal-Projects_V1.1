"""Validated, redacted application configuration for every runtime environment."""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Mapping
from urllib.parse import urlparse


class SettingsError(ValueError):
    """Raised when startup configuration is missing or unsafe."""


def _required(env: Mapping[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    if not value:
        raise SettingsError(f"Missing required configuration: {name}")
    return value


def _int(env: Mapping[str, str], name: str, default: int, *, minimum: int, maximum: int) -> int:
    raw = env.get(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise SettingsError(f"{name} must be an integer") from exc
    if not minimum <= value <= maximum:
        raise SettingsError(f"{name} must be between {minimum} and {maximum}")
    return value


def _url(env: Mapping[str, str], name: str, default: str, schemes: set[str]) -> str:
    value = env.get(name, default).strip()
    parsed = urlparse(value)
    if parsed.scheme not in schemes or not parsed.netloc:
        expected = ", ".join(sorted(schemes))
        raise SettingsError(f"{name} must be a URL with scheme {expected}")
    return value


def _auth_pair(env: Mapping[str, str]) -> tuple[str, str]:
    raw = _required(env, "NEO4J_AUTH")
    username, separator, password = raw.partition("/")
    if not separator or not username or not password:
        raise SettingsError("NEO4J_AUTH must use the format username/password")
    return username, password


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str
    log_level: str
    api_host: str
    api_port: int
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str = field(default="", repr=False)
    redis_host: str = "redis"
    redis_port: int = 6379
    qdrant_url: str = "http://qdrant:6333"
    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = field(default="", repr=False)
    app_secret_key: str = field(default="", repr=False)
    cors_origins: tuple[str, ...] = ()

    def redacted(self) -> dict[str, object]:
        """Return a safe diagnostic summary; never include secret values."""
        return {
            "app_env": self.app_env,
            "log_level": self.log_level,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "postgres_host": self.postgres_host,
            "postgres_port": self.postgres_port,
            "postgres_db": self.postgres_db,
            "postgres_user": self.postgres_user,
            "postgres_password": "***",
            "redis_host": self.redis_host,
            "redis_port": self.redis_port,
            "qdrant_url": self.qdrant_url,
            "neo4j_uri": self.neo4j_uri,
            "neo4j_user": self.neo4j_user,
            "neo4j_password": "***",
            "app_secret_key": "***",
            "cors_origins": list(self.cors_origins),
        }


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """Load and validate configuration; fail before serving traffic."""
    env = os.environ if environ is None else environ
    app_env = env.get("APP_ENV", "local").strip().lower()
    if app_env not in {"local", "test", "staging", "production"}:
        raise SettingsError("APP_ENV must be local, test, staging, or production")

    log_level = env.get("LOG_LEVEL", "INFO").strip().upper()
    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise SettingsError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")

    postgres_password = _required(env, "POSTGRES_PASSWORD")
    neo4j_user, neo4j_password = _auth_pair(env)
    app_secret_key = _required(env, "APP_SECRET_KEY")
    if len(app_secret_key) < 32:
        raise SettingsError("APP_SECRET_KEY must contain at least 32 characters")

    origins = tuple(item.strip() for item in env.get("CORS_ORIGINS", "http://localhost:5173").split(",") if item.strip())
    if not origins:
        raise SettingsError("CORS_ORIGINS must contain at least one origin")

    return Settings(
        app_env=app_env,
        log_level=log_level,
        api_host=env.get("API_HOST", "0.0.0.0").strip(),
        api_port=_int(env, "API_PORT", 8000, minimum=1, maximum=65535),
        postgres_host=env.get("POSTGRES_HOST", "postgres").strip(),
        postgres_port=_int(env, "POSTGRES_PORT", 5432, minimum=1, maximum=65535),
        postgres_db=_required(env, "POSTGRES_DB"),
        postgres_user=_required(env, "POSTGRES_USER"),
        postgres_password=postgres_password,
        redis_host=env.get("REDIS_HOST", "redis").strip(),
        redis_port=_int(env, "REDIS_PORT", 6379, minimum=1, maximum=65535),
        qdrant_url=_url(env, "QDRANT_URL", "http://qdrant:6333", {"http", "https"}),
        neo4j_uri=_url(env, "NEO4J_URI", "bolt://neo4j:7687", {"bolt", "neo4j", "neo4j+s"}),
        neo4j_user=neo4j_user,
        neo4j_password=neo4j_password,
        app_secret_key=app_secret_key,
        cors_origins=origins,
    )

"""Application configuration loaded from environment variables."""

from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

load_dotenv()


class Settings(BaseModel):
    """Typed, validated configuration for the application."""

    app_name: str = Field(default_factory=lambda: getenv("APP_NAME", "AI Chat API"))
    app_version: str = Field(default_factory=lambda: getenv("APP_VERSION", "1.0.0"))
    environment: str = Field(default_factory=lambda: getenv("ENVIRONMENT", "development"))
    debug: bool = Field(default_factory=lambda: getenv("DEBUG", "false").lower() == "true")
    host: str = Field(default_factory=lambda: getenv("HOST", "0.0.0.0"))
    port: int = Field(default_factory=lambda: int(getenv("PORT", "8000")))
    allowed_origins: list[str] = Field(
        default_factory=lambda: getenv("ALLOWED_ORIGINS", "").split(",")
    )
    ai_api_key: str | None = Field(default_factory=lambda: getenv("AI_API_KEY") or None)
    ai_model: str = Field(default_factory=lambda: getenv("AI_MODEL", "example-chat-model"))

    @field_validator("allowed_origins")
    @classmethod
    def clean_origins(cls, value: list[str]) -> list[str]:
        return [origin.strip() for origin in value if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the singleton settings object used by the application."""
    return Settings()


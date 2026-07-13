"""Operational health endpoints."""

from fastapi import APIRouter

from config import get_settings
from models.chat import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Check API health")
async def health_check() -> HealthResponse:
    """Return a lightweight liveness response for load balancers."""
    settings = get_settings()
    return HealthResponse(status="healthy", version=settings.app_version)

"""Chat-completion endpoints."""

from fastapi import APIRouter, Depends, status

from models.chat import ChatRequest, ChatResponse
from services.chat_service import ChatService, get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completions", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def create_completion(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Generate an assistant response from the supplied conversation."""
    return await chat_service.complete(request)


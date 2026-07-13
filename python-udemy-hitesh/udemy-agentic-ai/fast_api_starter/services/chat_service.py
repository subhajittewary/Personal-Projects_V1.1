"""Provider-independent chat orchestration."""

from functools import lru_cache

from config import Settings, get_settings
from models.chat import ChatMessage, ChatRequest, ChatResponse


class ChatService:
    """Coordinates chat completions; replace the placeholder with an AI SDK call."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def complete(self, request: ChatRequest) -> ChatResponse:
        """Create a completion response.

        This deterministic placeholder keeps the API runnable before an AI provider
        is selected. Add the provider client here; routers and schemas stay stable.
        """
        latest_user_message = next(
            (message.content for message in reversed(request.messages) if message.role == "user"),
            request.messages[-1].content,
        )
        return ChatResponse(
            model=self._settings.ai_model,
            message=ChatMessage(
                role="assistant",
                content=f"AI provider not configured. Received: {latest_user_message}",
            ),
        )


@lru_cache
def get_chat_service() -> ChatService:
    """Provide a shared service instance for FastAPI dependency injection."""
    return ChatService(get_settings())


from typing import Dict, Any, Optional
from app.storage import cache_manager
from app.log_utils import Logger
from .intents import ConversationIntent


class ConversationManager:
    """Manages conversation state and handles different conversation intents."""

    def __init__(self):
        self.cache = cache_manager
        self.default_ttl = 3600  # 1 hour default TTL

    def get_conversation_state(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation state for a call."""
        if not self.cache.exists(call_id):
            self.cache.set(
                call_id, {"ConversationIntent": ConversationIntent.WELCOME.value}
            )

        state_data = self.cache.get(call_id)
        return state_data

    def update_conversation_state(
        self, call_id: str, new_state: ConversationIntent
    ) -> bool:
        """Update specific fields in conversation state."""
        try:
            return self.cache.set(call_id, {"ConversationIntent": new_state.value})

        except Exception as e:
            Logger.log_session(
                session_id=call_id,
                message=f"Update_conversation_state error: str(e), operation: set_state",
                level="ERROR",
            )
            return False

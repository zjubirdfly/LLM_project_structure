from .conversation_manager import ConversationManager
from .intents import ConversationIntent

# Global conversation manager instance
conversation_manager = ConversationManager()

__all__ = [
    "conversation_manager",
    "ConversationManager",
    "ConversationIntent"
] 
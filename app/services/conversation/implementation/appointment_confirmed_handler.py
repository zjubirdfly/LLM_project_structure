from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from typing import List, Dict, Any
from app.llm_agents import GPTLLM, GeminiLLM
from app.services.conversation import ConversationIntent


class AppointmentConfirmedHandler(ConversationStateHandlerBase):
    """
    Handler for the 'other' intent of the conversation.
    """

    intent = ConversationIntent.APPOINTMENT_CONFIRMED

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
    ):
        super().__init__(model_id)

    def get_state_transfer_prompt(self, context: Dict) -> str:
        pass

    def get_response_prompt(self, context: Dict) -> str:
        pass

    @property
    def potential_next_state(self) -> List[str]:
        pass

    @property
    def is_terminal_state(self) -> bool:
        return False

    @property
    def is_init_state(self) -> bool:
        return False

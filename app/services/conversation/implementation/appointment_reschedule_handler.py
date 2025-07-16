from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)

from typing import List, Dict, Any
from app.llm_agents import GPTLLM, GeminiLLM
from app.services.conversation import ConversationIntent


@ConversationStateHandlerBase.register(ConversationIntent.APPOINTMENT_RESCHEDULE)
class AppointmentRescheduleHandler(ConversationStateHandlerBase):
    """
    Handler for the 'other' intent of the conversation.
    """

    intent = ConversationIntent.APPOINTMENT_RESCHEDULE

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
    ):
        super().__init__(model_id)

    def get_next_state(self, request: Dict[str, Any]) -> str:
        # TODO: Implement logic to determine the next state for this intent
        pass

    def generate_response(self, request: Dict[str, Any]) -> str:
        # TODO: Implement logic to generate a response for this intent
        pass

    def is_terminal_state(self) -> bool:
        # TODO: Implement logic to check if this is a terminal state for this intent
        return False

    def is_init_state(self) -> bool:
        # TODO: Implement logic to check if this is the initial state for this intent
        return False

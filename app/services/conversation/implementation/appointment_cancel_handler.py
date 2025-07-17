from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from typing import List, Dict, Any
from app.llm_agents import GPTLLM, GeminiLLM
from app.services.conversation import ConversationIntent


class AppointmentCancelHandler(ConversationStateHandlerBase):
    """
    Handler for the 'other' intent of the conversation.
    """

    intent = ConversationIntent.APPOINTMENT_CANCEL

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
    ):
        super().__init__(model_id)

    @property
    def state_transfer_prompt_template(self) -> str:
        pass

    @property
    def response_prompt_template(self) -> str:
        pass

    @property
    def potential_next_state(self) -> List[str]:
        pass

    def is_terminal_state(self) -> bool:
        return False

    def is_init_state(self) -> bool:
        return False

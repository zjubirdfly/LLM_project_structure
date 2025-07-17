from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)

from typing import List, Dict, Any
from app.llm_agents import GPTLLM, GeminiLLM
from app.services.conversation import ConversationIntent


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

    @property
    def state_transfer_prompt_template(self) -> str:
        return """
            You are a helpful and polite virtual assistant specialized in managing appointments. Your goal is to guide the user through their request regarding their appointment.

            Here is the user's information:
            User Name: <USER_NAME>
            Latest Appointment: <LATEST_APPOINTMENT_DETAILS>

            Here is the complete conversation history so far:
            <CONVERSATION_HISTORY>

            Based on the conversation history and the user's latest statement, determine the user's intent:
            1.  **Confirm Appointment:** The user wants to ensure their existing appointment is still valid.
            2.  **Cancel Appointment:** The user wishes to remove their existing appointment.
            3.  **Reschedule Appointment:** The user wants to change the date or time of their existing appointment.
            4.  **General Inquiry/Other:** The user's request is not directly related to confirming, canceling, or rescheduling, or is a greeting.

            Craft your *single, next response* as the assistant. Your response should be:
            * **Contextual:** Directly addresses the user's latest input within the full conversation history.
            * **Helpful:** Provides relevant information or asks clarifying questions.
            * **Polite and Professional:** Maintains a friendly and respectful tone.
            * **Action-oriented (if applicable):** If the intent is clear (e.g., reschedule), guide them to the next step. If unclear, ask clarifying questions.
            * **Concise:** Do not ramble. Get straight to the point.

            ---
            Assistant:
            """

    @property
    def response_prompt_template(self) -> str:
        return """
                You are an expert conversational AI designed to determine the user's current intent based on the ongoing dialogue. Your goal is to select the most accurate and specific conversational state from a predefined list.

                Here is the conversation history:
                <CONVERSATION_HISTORY>

                Analyze the full conversation history. Identify the single best conversational state that most accurately reflects the user's current intent.

                If the user's intent is unclear, ambiguous, or not enough information is available to determine the next step, you should default to the 'welcome' state.
            """

    @property
    def potential_next_state(self) -> List[str]:
        return [
            "welcome",
            "appointment_confirmed",
            "appointment_cancel",
            "appointment_reschedule",
        ]

    def is_terminal_state(self) -> bool:
        return False

    def is_init_state(self) -> bool:
        return False

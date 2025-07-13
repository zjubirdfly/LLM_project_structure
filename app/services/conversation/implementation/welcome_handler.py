from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from app.services.conversation.intents import ConversationIntent
import re
from typing import List, Dict, Any
from app.services.conversation import ConversationIntent
from app.entities.vapi import ChatRequest
from app.llm_agents import gemini


class WelcomeHandler(ConversationStateHandlerBase):
    """
    Handler for the welcome state of the conversation.
    """

    intent = ConversationIntent.WELCOME

    _WELCOME_STATE_TRANSFER_PROMPT = """
        You are an expert conversational AI designed to determine the user's current intent based on the ongoing dialogue. Your goal is to select the most accurate and specific conversational state from a predefined list.

        Here is the conversation history:
        <CONVERSATION_HISTORY>

        Analyze the full conversation history. Identify the single best conversational state that most accurately reflects the user's current intent.

        If the user's intent is unclear, ambiguous, or not enough information is available to determine the next step, you should default to the 'welcome' state.
       """

    _POSSIBLE_NEXT_STATES = [
        "welcome",
        "appointment_confirmed",
        "appointment_cancel",
        "appointment_reschedule",
    ]

    _CONVERSATIONAL_STATE_SCHEMA = {
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "The determined conversational state based on user intent.",
                "enum": _POSSIBLE_NEXT_STATES,
            }
        },
        "required": ["state"],
    }

    _WELCOME_CONVERSATION_PROMPT = """
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

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
    ):
        super().__init__(model_id)

    def get_next_state(self, request: Dict[str, Any]) -> ConversationIntent:
        chat_request: ChatRequest = request["request"]
        has_user_message = any(m.role == "user" for m in chat_request.messages)
        if not has_user_message:
            return ConversationIntent.WELCOME
        conversation_history = self._get_conversation_from_messages(
            chat_request.messages
        )
        prompt = self._WELCOME_STATE_TRANSFER_PROMPT.replace(
            "<CONVERSATION_HISTORY>", conversation_history
        )
        return gemini.generate_next_state(
            model_id=self.model_id,
            prompt=prompt,
            output_schema=self._CONVERSATIONAL_STATE_SCHEMA,
        )

    async def generate_response(self, request: Dict[str, Any]):
        chat_request: ChatRequest = request["request"]
        conversation_history = self._get_conversation_from_messages(
            chat_request.messages
        )
        user_latest_appointment = request["user_appointments"]
        user_name = request["user_info"].first_name
        prompt = (
            self._WELCOME_CONVERSATION_PROMPT.replace(
                "<CONVERSATION_HISTORY>", conversation_history
            )
            .replace("<USER_NAME>", user_name)
            .replace(
                "<LATEST_APPOINTMENT_DETAILS>",
                self._appointment_to_string(user_latest_appointment),
            )
        )
        result = gemini.generate_response(model_id=self.model_id, prompt=prompt)
        print(f"DEBUG: result: {result}")

        return result

    def is_terminal_state(self) -> bool:
        return False

    def is_init_state(self) -> bool:
        return True

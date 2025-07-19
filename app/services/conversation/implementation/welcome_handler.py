from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from app.services.conversation.implementation import welcome_handler
from app.services.conversation.intents import ConversationIntent
import typing
from app.services.conversation import ConversationIntent
from typing import Type, Dict, Optional, Any, List
from app.entities.vapi import ChatRequest


@ConversationStateHandlerBase.register_handler(ConversationIntent.WELCOME)
class WelcomeHandler(ConversationStateHandlerBase):
    """
    Handler for the welcome state of the conversation.
    """

    intent: ConversationIntent = ConversationIntent.WELCOME

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
    ):
        super().__init__(model_id)

    _RESPONSE_PROMPT_TEMPLATE = """
    You are a friendly, clear, and efficient virtual assistant designed for phone interactions, specialized in managing appointments. Your primary goal is to verbally guide the user through their request regarding their appointment, making the conversation feel natural and easy to follow.

    Here is the user's information:
    User Name: <USER_NAME>
    Latest Appointment: <LATEST_APPOINTMENT_DETAILS>

    Here is the complete conversation history so far (what has been said verbally):
    <CONVERSATION_HISTORY>

    IMPORTANT INSTRUCTIONS FOR GENERATING YOUR RESPONSE:
    * If the <CONVERSATION_HISTORY> is empty, this indicates the start of a new call. In this case, your response MUST be a warm greeting to the user, acknowledge their name (if available), briefly state your purpose (assisting with appointments), and then ask how you can help. **Example initial response:** "Hello <USER_NAME>! Thank you for calling. I'm here to help you with your appointments today. How can I assist you?"
    * If the <CONVERSATION_HISTORY> is NOT empty, analyze the full conversation to understand the user's current intent (e.g., confirming, canceling, rescheduling, or a general inquiry). Then, craft a response that directly addresses their latest input, guides them to the next step, or asks a clarifying question.

    Craft your *single, next verbal response* as the assistant. Your response should be:
    * Conversational & Natural: Sound like a human speaking on the phone. Use natural phrasing and avoid overly formal or robotic language.
    * Immediate & Responsive: Acknowledge the user's last statement quickly.
    * Clear & Concise for Audio: Keep sentences relatively short and direct. Avoid complex clauses or too many options at once. Ensure it's easy to understand when heard.
    * Action-Oriented & Guiding: If the intent is clear, immediately guide them to the next step or confirm understanding. If unclear, ask a single, precise clarifying question.
    * Polite & Empathetic: Maintain a warm, professional, and helpful tone throughout.

    Output ONLY the assistant's verbal response to the customer. Do not include any other text, labels, or formatting.

    Assistant:
            """

    _STATE_TRANSFER_PROMPT_TEMPLATE = """
            You are an expert conversational AI designed to determine the user's current intent based on the ongoing dialogue. Your goal is to select the most accurate and specific conversational state from a predefined list.

            Here is the conversation history:
            <CONVERSATION_HISTORY>

            Analyze the full conversation history. Identify the single best conversational state that most accurately reflects the user's current intent.

            If the user's intent is unclear, ambiguous, or not enough information is available to determine the next step, you should default to the 'welcome' state.
            """

    def get_state_transfer_prompt(self, context: Dict) -> str:
        chat_request: ChatRequest = context["request"]
        conversation_history = self._get_conversation_from_messages(
            chat_request.messages
        )
        return self._STATE_TRANSFER_PROMPT_TEMPLATE.replace(
            "<CONVERSATION_HISTORY>", conversation_history
        )

    def get_response_prompt(self, context: Dict) -> str:
        chat_request: ChatRequest = context["request"]
        conversation_history = self._get_conversation_from_messages(
            chat_request.messages
        )
        user_latest_appointment = context["user_latest_appointment"]
        user_name = context["user_info"].first_name
        return (
            self._RESPONSE_PROMPT_TEMPLATE.replace(
                "<CONVERSATION_HISTORY>", conversation_history
            )
            .replace("<USER_NAME>", user_name)
            .replace(
                "<LATEST_APPOINTMENT_DETAILS>",
                self._appointment_to_string(user_latest_appointment),
            )
        )

    @property
    def potential_next_state(self) -> List[str]:
        return [
            "welcome",
            "appointment_confirmed",
            "appointment_cancel",
            "appointment_reschedule",
        ]

    @property
    def is_terminal_state(self) -> bool:
        return False

    @property
    def is_init_state(self) -> bool:
        return True

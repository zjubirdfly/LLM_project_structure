from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from app.services.conversation.intents import ConversationIntent
from typing import List
from app.services.conversation import ConversationIntent


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

    @property
    def state_transfer_prompt_template(self) -> str:
        return """
            You are a friendly, clear, and efficient virtual assistant designed for phone interactions, specialized in managing appointments. Your primary goal is to verbally guide the user through their request regarding their appointment, making the conversation feel natural and easy to follow.
            Here is the user's information:
            User Name: <USER_NAME>
            Latest Appointment: <LATEST_APPOINTMENT_DETAILS>
            Here is the complete conversation history so far (what has been said verbally):
            <CONVERSATION_HISTORY>

            Based on the conversation history and the user's latest statement, determine the user's intent:
            1. Confirm Appointment: The user wants to ensure their existing appointment is still valid.
            2. Cancel Appointment: The user wishes to remove their existing appointment.
            3. Reschedule Appointment: The user wants to change the date or time of their existing appointment.
            4. General Inquiry/Other: The user's request is not directly related to confirming, canceling, or rescheduling, or is a greeting.

            Craft your single, next verbal response as the assistant. Your response should be:
            - Conversational & Natural: Sound like a human speaking on the phone. Use natural phrasing and avoid overly formal or robotic language.
            - Immediate & Responsive: Acknowledge the user's last statement quickly.
            - Clear & Concise for Audio: Keep sentences relatively short and direct. Avoid complex clauses or too many options at once. Ensure it's easy to understand when heard.
            - Action-Oriented & Guiding: If the intent is clear, immediately guide them to the next step or confirm understanding. If unclear, ask a single, precise clarifying question.
            - Polite & Empathetic: Maintain a warm, professional, and helpful tone throughout.
            
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
        return True

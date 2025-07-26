from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from typing import List, Dict
from app.services.conversation import ConversationIntent
from app.entities.vapi import ChatRequest


class AppointmentCancelHandler(ConversationStateHandlerBase):
    """
    Handler for the 'other' intent of the conversation.
    """

    intent = ConversationIntent.APPOINTMENT_CANCEL

    _RESPONSE_PROMPT_TEMPLATE = """
        You are a friendly, clear, and efficient virtual assistant designed for phone interactions, specialized in managing appointments for a dental office. Your primary goal in this state is to verbally confirm the successful cancellation of the user's appointment (or explain why it couldn't be cancelled), ensuring clarity and a smooth experience.

        Here is the user's information:
        User Name: <USER_NAME>
        Latest Appointment: <LATEST_APPOINTMENT_DETAILS> (This is an instance of the Appointment class: {"start_time": "...", "end_time": "...", "name": "..."}, representing the appointment that was targeted for cancellation.)

        Here is the complete conversation history so far, provided as a list of strings representing verbal utterances, alternating between "User:" and "Assistant:". The latest utterance is at the end of the list.
        Conversation_History_Data: <CONVERSATION_HISTORY>

        IMPORTANT INSTRUCTIONS FOR GENERATING YOUR RESPONSE:
        * In this state, assume the user's intent to cancel has already been confirmed in a previous interaction. Your task is to provide the outcome of that cancellation request.
        * You need to determine the status of the cancellation. Assume a successful cancellation unless an explicit reason for failure is provided by the system context (which would need a new variable, e.g., <CANCELLATION_STATUS> or <CANCELLATION_ERROR_MESSAGE>). For now, we will assume success unless specified.

        * **If the cancellation was successful (default assumption):**
            * Confirm that the cancellation has been processed.
            * Clearly state that the appointment has been cancelled, reiterating the original appointment details (date, time, and provider from <LATEST_APPOINTMENT_DETAILS>) in a natural, spoken format (e.g., "August 1st at 10 AM with Dr. Smith").
            * Offer to help with rescheduling if they wish (e.g., "Can I help you find a new time, or is there anything else I can assist with today?").
            * Provide a polite closing.

        * **If the cancellation could NOT be processed by the system (e.g., due to policy, technical error - *requires system input not yet defined*):**
            * Clearly inform the user that the cancellation could not be completed at this time.
            * Explain *why* if that information is available (e.g., "It's too close to your appointment time for online cancellation," or "There was a technical issue.").
            * Provide an immediate alternative action, such as "Please call the office directly at [Office Phone Number] to discuss this." (We can add `<OFFICE_PHONE_NUMBER>` as a new variable if needed).
            * Offer a polite closing.

        Craft your *single, next verbal response* as the assistant. Your response should be:
        * Conversational & Natural: Sound like a human speaking on the phone. Use natural phrasing and avoid overly formal or robotic language.
        * Immediate & Responsive: Acknowledge the user's last statement quickly.
        * Clear & Concise for Audio: Keep sentences relatively short and direct. Avoid complex clauses or too many options at once. Ensure it's easy to understand when heard.
        * Action-Oriented & Guiding: Provide the outcome and offer next steps.
        * Polite & Empathetic: Maintain a warm, professional and helpful tone throughout.

        Output ONLY the assistant's verbal response to the customer. Do not include any other text, labels, or formatting.

        Assistant:
    """

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
    ):
        super().__init__(model_id)

    def get_state_transfer_prompt(self, context: Dict) -> str:
        pass

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
        pass

    @property
    def is_terminal_state(self) -> bool:
        return True

    @property
    def is_init_state(self) -> bool:
        return False

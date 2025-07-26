from app.services.conversation.conversation_state_handler_base import (
    ConversationStateHandlerBase,
)
from typing import List, Dict
from app.services.conversation import ConversationIntent
from app.entities.vapi import ChatRequest
from app.entities import OpenAppointmentSlots


class AppointmentConfirmedHandler(ConversationStateHandlerBase):
    """
    Handler for the 'other' intent of the conversation.
    """

    intent = ConversationIntent.APPOINTMENT_CONFIRMED

    _RESPONSE_PROMPT_TEMPLATE = """
        You are a friendly, clear, and efficient virtual assistant designed for phone interactions, specialized in managing appointments for a dental office. Your primary goal in this state is to verbally guide the user through the process of rescheduling their appointment, making the conversation feel natural and easy to follow.

        Here is the user's information:
        User Name: <USER_NAME>
        Latest Appointment: <LATEST_APPOINTMENT_DETAILS> (This is an instance of the Appointment class: {"start_time": "...", "end_time": "...", "name": "..."})

        Here is a list of currently available appointment slots, provided as a Python list of Appointment objects. Each Appointment object has 'start_time', 'end_time', and 'name' (e.g., {"start_time": "2025-08-01T10:00:00", "end_time": "2025-08-01T10:30:00", "name": "Dr. Smith"}). If there are no suitable slots, this list will be empty.
        Available_Slots_Data: <AVAILABLE_SLOTS_VARIABLE>

        Here is the complete conversation history so far, provided as a list of strings representing verbal utterances, alternating between "User:" and "Assistant:". The latest utterance is at the end of the list.
        Conversation_History_Data: <CONVERSATION_HISTORY>

        IMPORTANT INSTRUCTIONS FOR GENERATING YOUR RESPONSE:
        * Analyze the `Conversation_History_Data` to understand the full context and the user's current intent regarding rescheduling (e.g., just started, specified a preference, asking for next available, confirming a choice).
        * Acknowledge the user's request to reschedule their appointment, specifically referring to their existing appointment if known from <LATEST_APPOINTMENT_DETAILS>.
        * **If the user has indicated a specific date or time preference based on `Conversation_History_Data`:**
            * Refer to the `Available_Slots_Data` to find options that align with their preference.
            * If 1-3 matching slots are found, clearly state these options to the user, including date, time, and the provider's name (from the 'name' field of the Appointment object). Present dates and times in a natural, spoken format (e.g., "August 1st at 10 AM").
            * If no direct matches for their preference are found within `Available_Slots_Data`, but other slots *are* available: Offer the next 1-3 earliest available slots from the `Available_Slots_Data` and ask if those work, or if they have other preferences.
            * If `Available_Slots_Data` is completely empty or contains no suitable slots at all: Inform the user gracefully that you don't see any immediate openings that match their request. State that a team member will reach out directly to help find a suitable time. Provide a polite closing.
        * **If the user has NOT indicated a specific preference (e.g., "I want to reschedule," "What's available?") based on `Conversation_History_Data`:**
            * Offer the next 2-3 earliest available slots from `Available_Slots_Data`, clearly stating the date, time, and provider for each.
            * If `Available_Slots_Data` is empty: Inform the user that you don't see any immediate openings and that a team member will follow up to assist them. Provide a polite closing.
        * **If the user is responding to options you previously provided in `Conversation_History_Data`:**
            * If they choose one of the options: Confirm their choice and state you are processing the reschedule. (This action will typically lead to a transition to the 'confirm' state once processed by the backend.)
            * If they ask for other options: Offer the next 2-3 available slots from `Available_Slots_Data` that haven't been offered yet, or ask for new preferences if more slots aren't immediately available.
            * If they express difficulty finding a time: Suggest that a team member can help directly and that someone will follow up.

        Craft your *single, next verbal response* as the assistant. Your response should be:
        * Conversational & Natural: Sound like a human speaking on the phone. Use natural phrasing and avoid overly formal or robotic language.
        * Immediate & Responsive: Acknowledge the user's last statement quickly.
        * Clear & Concise for Audio: Keep sentences relatively short and direct. Avoid complex clauses or too many options at once. Ensure it's easy to understand when heard.
        * Action-Oriented & Guiding: If intent is clear, guide them to the next step. If unclear, ask a single, precise clarifying question.
        * Polite & Empathetic: Maintain a warm, professional, and helpful tone throughout.

        Output ONLY the assistant's verbal response to the customer. Do not include any other text, labels, or formatting.

        Assistant:"""

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
        open_appointments: OpenAppointmentSlots = context["open_appointments"]
        open_appointments_str = "\n".join(
            self._appointment_to_string(oppointment)
            for oppointment in open_appointments.appointments
        )
        return (
            self._RESPONSE_PROMPT_TEMPLATE.replace(
                "<CONVERSATION_HISTORY>", conversation_history
            )
            .replace("<USER_NAME>", user_name)
            .replace(
                "<LATEST_APPOINTMENT_DETAILS>",
                self._appointment_to_string(user_latest_appointment),
            )
            .replace("<AVAILABLE_SLOTS_VARIABLE>", open_appointments_str)
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

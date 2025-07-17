from .conversation_manager import ConversationManager
from .conversation_state_handler_base import ConversationStateHandlerBase
from .intents import ConversationIntent
from .implementation import *

# Global conversation manager instance
conversation_manager = ConversationManager()
welcome_handler = WelcomeHandler()
appointment_cancel_handler = AppointmentCancelHandler()
appointment_confirmed_handler = AppointmentConfirmedHandler()
appointment_reschedule_handler = AppointmentRescheduleHandler()

__all__ = [
    "conversation_manager",
    "ConversationIntent",
    "conversation_state_handler",
    "welcome_handler",
    "appointment_cancel_handler",
    "appointment_confirmed_handler",
    "appointment_reschedule_handler",
]

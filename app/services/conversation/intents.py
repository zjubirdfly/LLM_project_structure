from enum import Enum


class ConversationIntent(Enum):
    """Defines different conversation intents/states."""

    WELCOME = "welcome"
    APPOINTMENT_CONFIRMED = "appointment_confirmed"
    APPOINTMENT_CANCEL = "appointment_cancel"
    APPOINTMENT_RESCHEDULE = "appointment_reschedule"

    @classmethod
    def from_string(cls, intent_str: str):
        """Convert string to ConversationIntent enum."""
        try:
            return cls(intent_str)
        except ValueError:
            return None

    def __str__(self):
        return self.value

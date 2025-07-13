from abc import ABC, abstractmethod
from typing import Type, Dict, Optional, Any, List
from app.entities.appointment import Appointment
from .intents import ConversationIntent
from starlette.responses import StreamingResponse
from app.entities.vapi import Message


class ConversationStateHandlerBase(ABC):
    _registry: Dict[ConversationIntent, Type["ConversationStateHandlerBase"]] = {}

    intent: ConversationIntent = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "intent") and cls.intent:
            ConversationStateHandlerBase._registry[cls.intent] = cls

    def __init__(
        self,
        model_id: str = "gemini-2.5-flash-preview-05-20",
    ):
        self.model_id = model_id

    def _get_conversation_from_messages(self, messages: List[Message]) -> str:
        formatted_messages = []
        for msg in messages:
            if msg.role == "assistant":
                formatted_messages.append(f"Assistant: {msg.content}")
            elif msg.role == "user":
                formatted_messages.append(f"User: {msg.content}")

        return "\n".join(formatted_messages)

    def _appointment_to_string(self, appointment: Appointment) -> str:
        return f"Appointment {appointment.name} from {appointment.start_time} to {appointment.end_time}\n"

    @classmethod
    def get_handler(
        cls, intent: ConversationIntent, **kwargs
    ) -> Optional["ConversationStateHandlerBase"]:
        handler_cls = cls._registry.get(intent)
        print(f"Handler class for intent {intent}: {handler_cls}")
        return handler_cls(**kwargs) if handler_cls else None

    @abstractmethod
    def get_next_state(self, request: Dict[str, Any]) -> ConversationIntent:
        raise NotImplementedError

    @abstractmethod
    def generate_response(self, request: Dict[str, Any]) -> StreamingResponse:
        raise NotImplementedError

    @abstractmethod
    def is_init_state(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_terminal_state(self) -> bool:
        raise NotImplementedError

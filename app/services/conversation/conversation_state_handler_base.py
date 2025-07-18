from abc import ABC, abstractmethod
from typing import Type, Dict, Optional, Any, List
from app.entities.appointment import Appointment
from .intents import ConversationIntent
from starlette.responses import StreamingResponse
from app.entities.vapi import Message
from app.entities.vapi import ChatRequest
from app.llm_agents import gemini


class ConversationStateHandlerBase(ABC):
    _registry: Dict[ConversationIntent, Type["ConversationStateHandlerBase"]] = {}

    _CONVERSATIONAL_STATE_SCHEMA = """{
        "type": "object",
        "properties": {
            "state": {
                "type": "string",
                "description": "The determined conversational state based on user intent.",
                "enum": <NEXT_POTENTIAL_STATES> 
            }
        },
        "required": ["state"],
    }"""

    intent: ConversationIntent = None
    model_id: str = "gemini-2.5-flash-preview-05-20"

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
    def get_state_transfer_prompt(self, context: Dict) -> str:
        pass

    @abstractmethod
    def get_response_prompt(self, context: Dict) -> str:
        pass

    @property
    @abstractmethod
    def potential_next_state(self) -> List[str]:
        pass

    async def get_next_state(self, context: Dict[str, Any]) -> ConversationIntent:
        chat_request: ChatRequest = context["request"]
        has_user_message = any(m.role == "user" for m in chat_request.messages)
        if not has_user_message:
            return ConversationIntent.WELCOME
        return await gemini.generate_next_state(
            model_id=self.model_id,
            prompt=self.get_state_transfer_prompt(context),
            output_schema=self._CONVERSATIONAL_STATE_SCHEMA.replace(
                "<NEXT_POTENTIAL_STATES>", str(self.potential_next_state)
            ),
        )

    async def generate_response(self, context: Dict[str, Any]) -> StreamingResponse:
        result = await gemini.generate_response(
            model_id=self.model_id, prompt=self.get_response_prompt(context)
        )
        print(f"DEBUG: result: {result}")
        return result

    @property
    @abstractmethod
    def is_init_state(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_terminal_state(self) -> bool:
        raise NotImplementedError

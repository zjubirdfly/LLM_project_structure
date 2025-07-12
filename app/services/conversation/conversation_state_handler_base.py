from abc import ABC, abstractmethod
from typing import Type, Dict, Optional, Any, List
from .intents import ConversationIntent
from starlette.responses import StreamingResponse
from app.llm_agents import BaseLLM, GPTLLM, GeminiLLM


class ConversationStateHandlerBase(ABC):
    _registry: Dict[ConversationIntent, Type["ConversationStateHandlerBase"]] = {}

    intent: ConversationIntent 

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "intent") and cls.intent:
            ConversationStateHandlerBase._registry[cls.intent] = cls 

    def __init__(self, llm_model:BaseLLM):
        self.llm_model = llm_model

    @classmethod
    def get_handler(cls, intent: ConversationIntent, **kwargs) -> Optional["ConversationStateHandlerBase"]:
        handler_cls = cls._registry.get(intent)
        return handler_cls(**kwargs) if handler_cls else None
    
    @abstractmethod
    def get_next_state(self, request: Dict[str, Any]) -> ConversationIntent:
        raise NotImplementedError

    @abstractmethod
    def generate_response(self,
                          chat_request: Dict[str, Any]) -> StreamingResponse:
        raise NotImplementedError
    
    @abstractmethod
    def is_init_state(self) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def is_terminal_state(self) -> bool:
        raise NotImplementedError 
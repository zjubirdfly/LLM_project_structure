from app.services.conversation.conversation_state_handler_base import ConversationStateHandler
from typing import List, Dict, Any
from app.llm_agents import BaseLLM, GPTLLM, GeminiLLM
from app.services.conversation import ConversationIntent

class WelcomeHandler(ConversationStateHandler):
    """
    Handler for the welcome state of the conversation.
    """
    intent = ConversationIntent.WELCOME

    WELCOME_STATE_TRANSFER_PROMPT = """
    You are an expert conversational AI designed to determine the current state of a user's intent based on the ongoing dialogue. Your goal is to identify the most accurate and specific conversational state from a predefined list.

Here is the conversation history:
<CONVERSATION_HISTORY>

Here is the list of possible conversational states:
<POSSIBLE_STATES>

Analyze the entire conversation history. Identify the single best conversational state that most accurately reflects the user's current intent and the overall topic of discussion.

Provide only the name of the identified state. Do not include any other text, explanations, or reasoning.
"""

    def __init__(self, llm_model:BaseLLM):
        super().__init__(llm_model)

    def get_next_state(self, request: Dict[str, Any]) -> str:
        pass

    def generate_response(self, request: Dict[str, Any]) -> str:
        pass

    def is_terminal_state(self) -> bool:
        return False
    
    def is_init_state(self) -> bool:
        return True
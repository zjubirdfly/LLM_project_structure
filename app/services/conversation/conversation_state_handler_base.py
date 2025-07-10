from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ConversationStateHandler(ABC):
    """
    Base class for conversation state handlers.
    
    This abstract base class defines the interface that all conversation state handlers
    must implement. Each handler is responsible for managing a specific conversation state
    and determining state transitions based on user input.
    """
    
    @abstractmethod
    def get_next_state(self, conversation_history: List[Dict[str, Any]], latest_user_input: str) -> str:
        """
        Analyze conversation so far and determine if state should transition.
        
        Args:
            conversation_history: List of previous conversation messages with metadata
            latest_user_input: The most recent user input to analyze
            
        Returns:
            str: The next state to transition to, or current state if no transition
        """
        raise NotImplementedError

    @abstractmethod
    def generate_response(self, conversation_state: str, conversation_history: List[Dict[str, Any]]) -> str:
        """
        Generate assistant reply for the current state and context.
        
        Args:
            conversation_state: The current conversation state
            conversation_history: List of previous conversation messages with metadata
            
        Returns:
            str: The generated response to speak to the user
        """
        raise NotImplementedError

    def is_terminal_state(self, state: str) -> bool:
        """
        Optional helper for clean-up or call termination logic.
        
        Args:
            state: The state to check
            
        Returns:
            bool: True if the state is terminal (should end the call)
        """
        return state in ["call_end"] 
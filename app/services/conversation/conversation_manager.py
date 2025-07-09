from typing import Dict, Any, Optional
from datetime import datetime
from app.storage import cache_manager
from app.logging.logger import Logger
from .intents import ConversationIntent

class ConversationManager:
    """Manages conversation state and handles different conversation intents."""
    
    def __init__(self):
        self.cache = cache_manager
        self.default_ttl = 3600  # 1 hour default TTL
    
    def get_conversation_state(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation state for a call."""
        try:
            cache_key = f"conversation:{call_id}"
            state_data = self.cache.get(cache_key)
            
            if state_data:
                Logger.log_json("conversation", "get_state", {
                    "call_id": call_id,
                    "found": True
                })
                return state_data
            
            Logger.log_json("conversation", "get_state", {
                "call_id": call_id,
                "found": False
            })
            return None
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "call_id": call_id,
                "error": str(e),
                "operation": "get_state"
            })
            return None
    
    def set_conversation_state(self, call_id: str, state: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set conversation state for a call."""
        try:
            # Add metadata to state
            state["last_updated"] = datetime.utcnow().isoformat()
            state["call_id"] = call_id
            
            cache_key = f"conversation:{call_id}"
            ttl = ttl or self.default_ttl
            
            success = self.cache.set(cache_key, state, ttl)
            
            Logger.log_json("conversation", "set_state", {
                "call_id": call_id,
                "success": success,
                "ttl": ttl
            })
            
            return success
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "call_id": call_id,
                "error": str(e),
                "operation": "set_state"
            })
            return False
    
    def update_conversation_state(self, call_id: str, updates: Dict[str, Any]) -> bool:
        """Update specific fields in conversation state."""
        current_state = self.get_conversation_state(call_id) or {}
        current_state.update(updates)
        return self.set_conversation_state(call_id, current_state)
    
    def delete_conversation_state(self, call_id: str) -> bool:
        """Delete conversation state for a call."""
        try:
            cache_key = f"conversation:{call_id}"
            success = self.cache.delete(cache_key)
            
            Logger.log_json("conversation", "delete_state", {
                "call_id": call_id,
                "success": success
            })
            
            return success
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "call_id": call_id,
                "error": str(e),
                "operation": "delete_state"
            })
            return False
    
    def handle_appointment_confirmed(self, call_id: str, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle appointment confirmation intent."""
        try:
            # TODO: Call your LLM here for appointment confirmation
            # Example: response = your_llm_service.generate_response(user_message, context)
            pass
            
            # Update conversation state
            current_state = self.get_conversation_state(call_id) or self._initialize_state(call_id)
            current_state.update({
                "current_intent": ConversationIntent.APPOINTMENT_CONFIRMED.value,
                "last_user_message": user_message,
                "message_count": current_state.get("message_count", 0) + 1,
                "context": context or {}
            })
            
            self.set_conversation_state(call_id, current_state)
            
            Logger.log_json("conversation", "appointment_confirmed", {
                "call_id": call_id,
                "user_message": user_message,
                "context": context
            })
            
            return {
                "intent": ConversationIntent.APPOINTMENT_CONFIRMED.value,
                "status": "handled",
                "call_id": call_id
            }
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "call_id": call_id,
                "error": str(e),
                "operation": "appointment_confirmed"
            })
            return {"error": str(e)}
    
    def handle_appointment_cancel(self, call_id: str, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle appointment cancellation intent."""
        try:
            # TODO: Call your LLM here for appointment cancellation
            # Example: response = your_llm_service.generate_response(user_message, context)
            pass
            
            # Update conversation state
            current_state = self.get_conversation_state(call_id) or self._initialize_state(call_id)
            current_state.update({
                "current_intent": ConversationIntent.APPOINTMENT_CANCEL.value,
                "last_user_message": user_message,
                "message_count": current_state.get("message_count", 0) + 1,
                "context": context or {}
            })
            
            self.set_conversation_state(call_id, current_state)
            
            Logger.log_json("conversation", "appointment_cancel", {
                "call_id": call_id,
                "user_message": user_message,
                "context": context
            })
            
            return {
                "intent": ConversationIntent.APPOINTMENT_CANCEL.value,
                "status": "handled",
                "call_id": call_id
            }
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "call_id": call_id,
                "error": str(e),
                "operation": "appointment_cancel"
            })
            return {"error": str(e)}
    
    def handle_appointment_reschedule(self, call_id: str, user_message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle appointment reschedule intent."""
        try:
            # TODO: Call your LLM here for appointment rescheduling
            # Example: response = your_llm_service.generate_response(user_message, context)
            pass
            
            # Update conversation state
            current_state = self.get_conversation_state(call_id) or self._initialize_state(call_id)
            current_state.update({
                "current_intent": ConversationIntent.APPOINTMENT_RESCHEDULE.value,
                "last_user_message": user_message,
                "message_count": current_state.get("message_count", 0) + 1,
                "context": context or {}
            })
            
            self.set_conversation_state(call_id, current_state)
            
            Logger.log_json("conversation", "appointment_reschedule", {
                "call_id": call_id,
                "user_message": user_message,
                "context": context
            })
            
            return {
                "intent": ConversationIntent.APPOINTMENT_RESCHEDULE.value,
                "status": "handled",
                "call_id": call_id
            }
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "call_id": call_id,
                "error": str(e),
                "operation": "appointment_reschedule"
            })
            return {"error": str(e)}
    
    def _initialize_state(self, call_id: str) -> Dict[str, Any]:
        """Initialize a new conversation state."""
        return {
            "call_id": call_id,
            "current_intent": None,
            "conversation_history": [],
            "message_count": 0,
            "context": {},
            "created_at": datetime.utcnow().isoformat()
        }
    
    def get_all_active_conversations(self) -> list:
        """Get all active call IDs."""
        try:
            all_keys = self.cache.get_all_keys()
            # Extract call IDs from conversation keys
            call_ids = []
            for key in all_keys:
                if key.startswith("conversation:"):
                    call_id = key.replace("conversation:", "")
                    call_ids.append(call_id)
            
            Logger.log_json("conversation", "get_all_active", {
                "count": len(call_ids),
                "call_ids": call_ids
            })
            
            return call_ids
            
        except Exception as e:
            Logger.log_json("conversation", "error", {
                "error": str(e),
                "operation": "get_all_active"
            })
            return [] 
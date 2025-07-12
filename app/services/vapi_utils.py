from typing import Optional, Dict, Any, List

def extract_customer_number(data: Dict[str, Any]) -> Optional[str]:
    """Extract customer number from a VAPI webhook message."""
    try:
        return (
            data.get("message", {})
                .get("call", {})
                .get("customer", {})
                .get("number")
        )
    except Exception as e:
        print(f"Error extracting customer number: {str(e)}")
        return None
    
def extract_call_id(data: Dict[str, Any]) -> Optional[str]:
    """Extract call id from a VAPI webhook message."""
    try:
        return (
            data.get("message", {})
                .get("call", {})
                .get("id")
        )
    except Exception as e:
        print(f"Error extracting call id: {str(e)}")
        return None

def extract_conversation_messages(request_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Extract conversation messages from VAPI request data if it's a conversation-update type."""
    try:
        message = request_data.get("message", {})
        if message.get("type") == "conversation-update":
            return message.get("conversation", [])
        return None
    except Exception as e:
        print(f"Error extracting conversation messages: {str(e)}")
        return None

from typing import Optional, Dict, Any, List
from vapi import Vapi
from app.core.config import settings

vapi_client = Vapi(token=settings.vapi_api_key)

def get_call_info_from_call_id(call_id: str) -> Optional[Dict[str, Any]]:
    """
    Get call info from a VAPI call id.
    """
    try:
        call = vapi_client.calls.get(id=call_id)
        return call
    except Exception as e:
        print(f"Error getting call info: {str(e)}")
        return None
    
def get_call_monitor_info_from_call_id(call_id: str) -> Optional[Dict[str, Any]]:
    """
    Get call monitor info from a VAPI call id.
    """
    try:
        call = get_call_info_from_call_id(call_id)
        if not call:
            return None
        call_monitor = call["monitor"]
        if not call_monitor:
            return None
        return call_monitor
    except Exception as e:
        print(f"Error getting call monitor info: {str(e)}")
        return None

def extract_customer_number(data: Dict[str, Any]) -> Optional[str]:
    """
    Extract customer number from a VAPI message.
    
    Args:
        message (Dict[str, Any]): The VAPI message dictionary
        
    Returns:
        Optional[str]: The customer number if found, None otherwise
    """
    try:
        # Check if message has customer information
        if not data:
            return None
        message = data["message"]
        if not message:
            return None
        call = message["call"]   
        if not call:
            return None
        customer = call["customer"]
        if not customer or "number" not in customer:
            print("No customer number found in message")
            return None
            
        return customer["number"]
        
    except Exception as e:
        print(f"Error extracting customer number: {str(e)}")
        return None
    
def extract_call_id(data: Dict[str, Any]) -> Optional[str]:
    """
    Extract customer number from a VAPI message.
    
    Args:
        message (Dict[str, Any]): The VAPI message dictionary
        
    Returns:
        Optional[str]: The customer number if found, None otherwise
    """
    try:
        # Check if message has customer information
        if not data:
            return None
        message = data["message"]
        if not message:
            return None
        call = message["call"]   
        if not call:
            return None
        call_id = call["id"]
        if not call_id:
            print("No call id found in message")
            return None
            
        return call_id
        
    except Exception as e:
        print(f"Error extracting call id: {str(e)}")
        return None

def extract_conversation_messages(request_data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """
    Extract conversation messages from VAPI request data if it's a conversation-update type.
    
    Args:
        request_data (Dict[str, Any]): The request data from VAPI
        
    Returns:
        Optional[List[Dict[str, Any]]]: List of conversation messages if found, None otherwise
    """
    try:
        message = request_data.get("message", {})
        if message.get("type") == "conversation-update":
            return message.get("conversation", [])
        return None
    except (KeyError, AttributeError):
        return None

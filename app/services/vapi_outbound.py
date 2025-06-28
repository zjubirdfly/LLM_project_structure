"""
VAPI outbound call service.
"""

import httpx
from typing import Dict, Any, Tuple
from app.core.config import settings

async def initiate_call(
        *,
        phoneNumberId: str, 
        assistantId: str, 
        customerNumber: str) -> Tuple[str, str]:
    """
    Initiate an outbound call using VAPI.
    
    Args:
        phoneNumberId: The phone id to call
        assistantId: The VAPI assistant ID to use
        customerNumber: the customer phonenumber that you want to call
        
    Returns:
        Tuple of (call_id, web_call_url)
        
    Raises:
        httpx.HTTPStatusError: If the VAPI request fails
    """
    url = f"{settings.vapi_base_url}/call"
    headers = {
        'Authorization': f'Bearer {settings.vapi_api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
            "phoneNumberId": phoneNumberId,
            "assistantId": assistantId,
            "customer": {
                "number": customerNumber,
            }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        call_id = data.get('id')
        
        return call_id
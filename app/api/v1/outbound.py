"""
Outbound call API routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.vapi_outbound import initiate_call

router = APIRouter()

class OutboundCallRequest(BaseModel):
    phoneNumberId: str
    assistantId: str
    customerNumber: str

@router.post("/outbound", tags=["Outbound"])
async def create_outbound_call(request: OutboundCallRequest):
    """
    Create an outbound call using VAPI.
    """
    try:
        call_id = await initiate_call(
            phoneNumberId=request.phoneNumberId,
            assistantId=request.assistantId,
            customerNumber=request.customerNumber
        )
        
        return {
            "status": "success",
            "call_id": call_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to place outbound call",
                "error": str(e)
            }
        ) 
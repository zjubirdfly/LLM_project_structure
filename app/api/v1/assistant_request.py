from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json as jsonfile
from app.core.config import settings
import os
from app.logging.logger import Logger
from app.services.vapi_utils import extract_call_id, extract_conversation_messages, extract_customer_number
from app.services.vapi_assistant_generator import VapiAssistantGenerator as AssistantGenerator
from app.entities import UserInfo

router = APIRouter()
assistant_generator = AssistantGenerator()

@router.post("assistant", tags=["Assistant"])
async def assistant_request(request: Request):
    data = await request.json()
    customer_phone_number = extract_customer_number(data)
    call_id = extract_call_id(data)

    # Log the incoming request with call ID for tracking
    Logger.log_json("vapi/assistant", "request", {
        "call_id": call_id,
        "customer_phone_number": customer_phone_number,
        "request_data": data
    })

    assistant_config = assistant_generator.generate_assistant_by_customer_phone_number(
        customer_phone_number, 
        call_id
    )
    Logger.log_json("vapi/assistant", "response", assistant_config)
        return assistant_config
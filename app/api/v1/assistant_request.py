from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json as jsonfile
from app.core.config import settings
import os
from app.logging.logger import Logger
from app.services.vapi_utils import extract_call_id, extract_conversation_messages, extract_customer_number
from app.services.vapi_assistant_generator import VapiAssistantGenerator as AssistantGenerator
from app.services.user.user_info import UserInfo

router = APIRouter()
assistant_generator = AssistantGenerator()

@router.post("assistant", tags=["Assistant"])
async def assistant_request(request: Request):
    data = await request.json()
    customer_phone_number = extract_customer_number(data)
    
    # Get user information
    user_info = user_records.get_user_by_phone(customer_phone_number)
    if not user_info:
        # If user doesn't exist, create a minimal response with just the phone number
        print(f"Warning: No user information found for {customer_phone_number}")
        user_info = UserInfo(
            phone=customer_phone_number,
            first_name="",
            last_name="",
            nickname="",
            email=""
        )

    assistant_config = assistant_generator.generate_assistant_by_customer_phone_number(customer_phone_number)
    Logger.log_json("vapi/assistant", assistant_config)
    return assistant_config
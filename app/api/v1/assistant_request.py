from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json as jsonfile
from app.core.config import settings
import os
from service.user.records import UserRecords
from service.request.vapi.assistant_generator import AssistantGenerator
from service.util.vapi import extract_customer_number
from service.user.types import UserInfo
from app.logging.logger import Logger

router = APIRouter()
user_records = UserRecords()  # Initialize once at module level
assistant_generator = AssistantGenerator()  # Initialize once at module level

@router.post("")
async def assistant_request(request: Request):
    data = await request.json()
    customer_number = extract_customer_number(data)
    # print(f"Processing request for customer: {customer_number}")
    
    # Get user information
    user_info = user_records.get_user_by_phone(customer_number)
    if not user_info:
        # If user doesn't exist, create a minimal response with just the phone number
        print(f"Warning: No user information found for {customer_number}")
        user_info = UserInfo(
            phone=customer_number,
            first_name="",
            last_name="",
            nickname="",
            email=""
        )
    Logger.log_json("request/vapi/assistant", str(user_info.phone), data)
    # Check if phone is the only non-empty field
    is_new_user = (
        user_info.phone and 
        not user_info.first_name and 
        not user_info.last_name and 
        not user_info.nickname and 
        not user_info.email
    )

    try:
        if is_new_user or user_info.phone == "+12174199131":
            # print("Generating onboarding assistant config for new user or Chen")
            assistant_config = assistant_generator.generate_onboarding_assistant_with_custom_llm(user_info)
            # print(assistant_config)
        else:
            print("Generating english tutor config for existing user")
            assistant_config = assistant_generator.generate_english_tutor(user_info)
        Logger.log_json("response/vapi/assistant", str(user_info.phone), assistant_config)
        return assistant_config

    except Exception as error:
        raise HTTPException(status_code=500, detail={
            "message": "Failed to generate assistant configuration",
            "error": str(error),
        })
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import json as jsonfile
from app.core.config import settings
from app.logging.logger import Logger
from app.services.vapi_utils import extract_call_id, extract_conversation_messages, extract_customer_number
from app.services.vapi_assistant_generator import VapiAssistantGenerator

router = APIRouter()
assistant_generator = VapiAssistantGenerator()

@router.post("assistant", tags=["Assistant"])
async def assistant_request(request: Request):
    data = await request.json()
    customer_number = extract_customer_number(data)
    assistant_config = assistant_generator.generate_assistant_by_customer_number(customer_number)
    Logger.log_json("response/vapi/assistant", assistant_config)
    return assistant_config
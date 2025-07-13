import datetime
import json
import time
from fastapi import APIRouter, Request
from openai import AsyncOpenAI
import os
from starlette.responses import StreamingResponse
from app.entities.vapi import ChatRequest
from app.core.config import settings
from dotenv import load_dotenv
from app.services import llm_response_generator

router = APIRouter()


@router.post("/chat/completions", tags=["Custom LLM"])
async def chat_completion_stream(vapi_payload: ChatRequest):
    print(f"vapi_payload: {vapi_payload}")
    response = await llm_response_generator.generate_custom_llm_response(vapi_payload)
    print(f"DEBUG: Type of response from generate_custom_llm_response: {response}")
    # This should print <class 'fastapi.responses.StreamingResponse'>
    return response

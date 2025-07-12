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

router = APIRouter()

@router.post("/chat/completions", tags=["Custom LLM"])
async def chat_completion_stream(vapi_payload: ChatRequest) -> StreamingResponse:
    print(f"vapi_payload: {vapi_payload}")  
    return StreamingResponse(content="", media_type="text/event-stream")
from fastapi import APIRouter
from app.entities.vapi import ChatRequest
from app.services import llm_response_generator
from app.log_utils import Logger

router = APIRouter()


@router.post("/chat/completions", tags=["Custom LLM"])
async def chat_completion_stream(vapi_payload: ChatRequest):
    print(f"vapi_payload: {vapi_payload}")
    call_id = vapi_payload.call.id
    Logger.log_session(
        session_id=call_id,
        message=f"Received ChatRequest Request from Vapi : {vapi_payload}",
        level="INFO",
    )
    response = await llm_response_generator.generate_custom_llm_response(vapi_payload)
    print(f"DEBUG: Type of response from generate_custom_llm_response: {response}")
    # This should print <class 'fastapi.responses.StreamingResponse'>
    return response

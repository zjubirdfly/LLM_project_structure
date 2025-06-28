import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json as jsonfile

from src.config import settings

router = APIRouter()

# Pydantic model for request body
class OutboundRequest(BaseModel):
    phoneNumberId: str
    assistantId: str
    customerNumber: str

@router.post("/outbound", tags="OutBound")
async def outbound(request: OutboundRequest):
    try:
        url = f"{settings.vapi_base_url}/call"
        headers = {
            'Authorization': f'Bearer {settings.vapi_api_key}',
            'Content-Type': 'application/json'
        }
        json = {
                "phoneNumberId": request.phoneNumberId,
                "assistantId": request.assistantId,
                "customer": {
                    "number": request.customerNumber,
                }
        }

        response = requests.post(url=url, headers=headers, json=json)
        data = response.json()
        if response.status_code == 201:
            call_id = data.get('id')
            web_call_url = data.get('webCallUrl')
            return call_id, web_call_url
        else:
            raise Exception(f"Error: {data}")

    except requests.exceptions.RequestException as error:
        raise HTTPException(status_code=500, detail={
            "message": "Failed to place outbound call",
            "error": str(error),
        })
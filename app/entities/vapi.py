from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class Parameters(BaseModel):
    type: str
    properties: Dict[str, Any]


class Function(BaseModel):
    name: str
    description: str
    parameters: Optional[Parameters] = None


class Tool(BaseModel):
    type: str
    function: Function


class Customer(BaseModel):
    number: str


class Monitor(BaseModel):
    listenUrl: str = Field(..., alias="listenUrl")
    controlUrl: str = Field(..., alias="controlUrl")

    class Config:
        allow_population_by_field_name = True


class Call(BaseModel):
    id: str
    orgId: str
    createdAt: str
    updatedAt: str
    type: str
    status: str
    assistantId: Optional[str] = None
    customer: Optional[Customer] = None
    phoneNumberId: Optional[str] = None
    phoneCallProvider: Optional[str] = None
    phoneCallProviderId: Optional[str] = None
    phoneCallTransport: Optional[str] = None


class PhoneNumber(BaseModel):
    id: str
    orgId: str
    number: str
    createdAt: str
    updatedAt: str
    twilioAccountSid: Optional[str] = None
    twilioAuthToken: Optional[str] = None
    name: str
    provider: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float
    tools: Optional[List[Tool]] = None
    stream: bool
    max_tokens: int
    call: Call
    phoneNumber: Optional[PhoneNumber] = None
    customer: Optional[Customer] = None
    metadata: Dict[str, Any]


class CallControlResponse(BaseModel):
    id: str
    assistantId: str
    phoneNumberId: str
    type: str
    createdAt: str
    updatedAt: str
    orgId: str
    cost: int
    customer: Optional[Customer] = None
    status: str
    phoneCallProvider: str
    phoneCallProviderId: str
    phoneCallTransport: str
    monitor: Optional[Monitor] = None

    class Config:
        allow_population_by_field_name = True
        extra = "allow"  # ignore unexpected fields

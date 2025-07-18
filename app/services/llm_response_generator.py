from app.entities import (
    UserInfo,
    UserScheduleHistory,
    OpenAppointmentSlots,
    Appointment,
)
from typing import Optional, List, Dict, Any
import json
from starlette.responses import StreamingResponse
from datetime import datetime, timedelta
import random
import app.entities.vapi
from .conversation import conversation_manager
from .conversation import ConversationStateHandlerBase
from app.llm_agents import gemini
from app.services.conversation.implementation import *
from google.genai.types import GenerateContentResponse
from app.entities.vapi import ChatRequest
import time


class LlmResponseGenerator:
    def __init__(self):
        """Initialize the generator without loading templates."""
        self.conversation_manager = conversation_manager

    async def generate_custom_llm_response(
        self, chat_request: ChatRequest
    ) -> StreamingResponse:
        phone_number = chat_request.phoneNumber
        call_id = chat_request.call.id
        user_info = self._load_user_info_from_phone_number(phone_number)
        user_appointments = self._load_current_appointment_from_user_id(
            user_info.user_id
        )
        open_appointments = self._load_open_appointment()
        user_latest_appointment = user_appointments.appointments[-1]

        context = {}
        context["request"] = chat_request
        context["user_info"] = user_info
        context["user_latest_appointment"] = user_latest_appointment
        context["open_appointments"] = open_appointments
        current_state = self.conversation_manager.get_conversation_state(call_id)[
            "ConversationIntent"
        ]

        handler = ConversationStateHandlerBase.get_handler(current_state)
        latest_state = await handler.get_next_state(context)
        print(f"Current state: {current_state}, Latest state: {latest_state}")
        self.conversation_manager.update_conversation_state(call_id, latest_state)

        try:

            async def event_stream():
                result_response = await handler.generate_response(context)
                print(f"DEBUG: result_response: {result_response}")
                check_data = self._build_streaming_chunk(result_response)
                streaming = f"data: {check_data}\n\n"
                print(f"DEBUG: Streaming chunk: {streaming}")
                yield streaming

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
            )

        except Exception as e:
            print(f"Error during overall response generation: {e}")
            return StreamingResponse(
                f"data: {json.dumps({'error': str(e)})}\n\n",
                media_type="text/event-stream",
            )

    def _build_streaming_chunk(self, content_text: str) -> str:
        data = {
            "id": "chatcmpl-abc123",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "gpt-4o-2024-05-13",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": content_text},
                    "finish_reason": "stop",
                }
            ],
        }
        return json.dumps(data)

    def _load_user_info_from_phone_number(
        self, phone_number: str
    ) -> Optional[UserInfo]:
        # TODO: Implement actual fetching from a database or storage
        # For now, returning a placeholder UserInfo object
        # user_info = self.user_records.get_user_by_phone(phone_number)
        # if user_info:
        #     return UserInfo(**user_info) # Assuming get_user_by_phone returns a dict
        return UserInfo(
            user_id="test_123",
            phone="+1234567890",
            first_name="Robert",
            last_name="Benea",
            nickname="Robert",
            email="Robert@gmail.com",
        )

    def _load_current_appointment_from_user_id(
        self, user_id: str
    ) -> Optional[UserScheduleHistory]:
        # TODO: Implement fetching user's current appointment from a database or storage
        # For now, returning a placeholder
        fake_appintments = [
            Appointment(
                start_time="2024-04-11T09:00",
                end_time="2024-04-11T09:30",
                name="Teeth cleaning",
            ),
            Appointment(
                start_time="2025-01-11T10:00",
                end_time="2025-01-11T11:00",
                name="Teeth cleaning",
            ),
            Appointment(
                start_time="2025-08-11T13:00",
                end_time="2025-08-11T13:30",
                name="Teeth cleaning",
            ),
        ]
        return UserScheduleHistory(user_id=user_id, appointments=fake_appintments)

    def _load_open_appointment(self) -> OpenAppointmentSlots:
        # TODO: Implement loading available appointment windows from a database or storage
        # For now, returning a placeholder
        start_date = datetime(2025, 8, 11)
        end_date = datetime(2025, 8, 25)

        appointments = []
        for _ in range(10):
            # Pick a random date between 8/11 and 8/25
            random_days = random.randint(0, (end_date - start_date).days)
            slot_date = start_date + timedelta(days=random_days)

            # Random start hour between 8 AM and 4 PM
            start_hour = random.randint(8, 15)
            start_minute = random.choice([0, 30])
            start_time = slot_date.replace(hour=start_hour, minute=start_minute)

            # Slot duration: 30 minutes
            end_time = start_time + timedelta(minutes=30)

            appointments.append(
                Appointment(
                    start_time=start_time.isoformat(),
                    end_time=end_time.isoformat(),
                    name="Available Slot",
                )
            )

        return OpenAppointmentSlots(appointments=appointments)

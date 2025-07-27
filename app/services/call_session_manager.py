from app.core import settings
from app.entities.vapi import Monitor
import httpx
from app.entities import CallControlResponse
from app.log_utils import Logger


class CallSessionManager:
    _instance = None

    def __init__(self):
        self.vapi_base_url = settings.vapi_base_url
        self.vapi_api_key = settings.vapi_api_key

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def _get_vapi_phone_monitor(self, call_id: str) -> Monitor | None:
        url = f"{settings.vapi_base_url}/call/{call_id}"
        headers = {
            "Authorization": f"Bearer {self.vapi_api_key}",
            # "content-type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                Logger.log_session(
                    session_id=call_id,
                    message=f"Call ended successfully. Response: {response}",
                    level="INFO",
                )
                data = CallControlResponse.model_validate(response.json())
                return data.monitor
            except httpx.HTTPStatusError as e:
                Logger.log_session(
                    session_id=call_id,
                    message=f"Error getting monitor url: {e.response.status_code} - {e.response.text}",
                    level="ERROR",
                )

    async def end_call(
        self, call_id: str, assistant_id: str, number: str, phone_number_id: str
    ):
        monitor: Monitor | None = await self._get_vapi_phone_monitor(
            call_id=call_id,
            assistant_id=assistant_id,
            number=number,
            phone_number_id=phone_number_id,
        )

        if monitor is None:
            Logger.log_session(
                session_id=call_id,
                message=f"Monitor object is None, cannot end call. assistant_id: {assistant_id}, number: {number}, phone_number_id: {phone_number_id}",
                level="ERROR",
            )
            return

        control_url = monitor.controlUrl.strip("<>")
        headers = {"Content-Type": "application/json"}
        payload = {"type": "end-call"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(control_url, headers=headers, json=payload)
                response.raise_for_status()
                Logger.log_session(
                    session_id=assistant_id,
                    message=f"Call ended successfully. Response: {response.text}",
                    level="INFO",
                )
            except httpx.HTTPStatusError as e:
                Logger.log_session(
                    session_id=assistant_id,
                    message=f"Error ending call: {e.response.status_code} - {e.response.text}",
                    level="ERROR",
                )

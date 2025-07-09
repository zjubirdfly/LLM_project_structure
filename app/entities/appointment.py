from pydantic import BaseModel
from typing import List, Dict, Any

class UserScheduleHistory(BaseModel):
    user_id: str
    appointments: List[Dict[str, Any]] = []

class OpenAppointmentSlot(BaseModel):
    start_time: str
    end_time: str
    is_available: bool = True 
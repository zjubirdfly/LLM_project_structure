from pydantic import BaseModel
from typing import List, Dict, Any

class Appointment(BaseModel):
    start_time: str
    end_time: str
    name: str

class UserScheduleHistory(BaseModel):
    user_id: str
    appointments: List[Appointment] = []

class OpenAppointmentSlots(BaseModel):
    appointments: List[Appointment]
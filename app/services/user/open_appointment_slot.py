from pydantic import BaseModel
from typing import List, Dict, Any

class OpenAppointmentSlot(BaseModel):
    start_time: str
    end_time: str
    is_available: bool = True 
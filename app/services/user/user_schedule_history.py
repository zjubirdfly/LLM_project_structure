from pydantic import BaseModel
from typing import List, Dict, Any

class UserScheduleHistory(BaseModel):
    user_id: str
    appointments: List[Dict[str, Any]] = [] 
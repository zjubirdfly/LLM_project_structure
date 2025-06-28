from pydantic import BaseModel

class UserInfo(BaseModel):
    phone: str
    first_name: str
    last_name: str
    nickname: str
    email: str 
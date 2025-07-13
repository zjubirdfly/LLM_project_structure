from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    phone: str
    first_name: str
    last_name: str
    nickname: str
    email: str

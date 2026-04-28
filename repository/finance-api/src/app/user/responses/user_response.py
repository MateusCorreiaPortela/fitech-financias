from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

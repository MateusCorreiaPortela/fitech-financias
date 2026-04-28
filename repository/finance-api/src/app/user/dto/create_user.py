from pydantic import BaseModel, EmailStr


class CreateUserDto(BaseModel):
    name: str
    email: EmailStr
    password: str

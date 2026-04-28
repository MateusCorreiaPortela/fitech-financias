from pydantic import BaseModel, EmailStr


class UpdateProfileDto(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class ChangePasswordDto(BaseModel):
    current_password: str
    new_password: str

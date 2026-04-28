from fastapi import HTTPException
from src.app.core.security import hash_password, verify_password
from src.app.user.dto import CreateUserDto, UpdateProfileDto, ChangePasswordDto
from src.app.core.models import User
from src.app.user.repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create(self, dto: CreateUserDto) -> User:
        if await self.repository.exists(email=dto.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        data = dto.model_dump()
        data["password"] = hash_password(data["password"])
        return await self.repository.create(**data)

    async def update_profile(self, user: User, dto: UpdateProfileDto) -> User:
        data = dto.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=400, detail="No fields to update")
        if "email" in data and data["email"] != user.email:
            if await self.repository.exists(email=data["email"]):
                raise HTTPException(status_code=409, detail="Email already registered")
        await user.update_from_dict(data).save()
        return user

    async def change_password(self, user: User, dto: ChangePasswordDto) -> None:
        if not verify_password(dto.current_password, user.password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        user.password = hash_password(dto.new_password)
        await user.save()

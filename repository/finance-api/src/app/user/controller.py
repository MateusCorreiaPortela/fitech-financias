from fastapi import APIRouter, Depends
from src.app.core.dependencies import get_current_user
from src.app.core.models import User
from src.app.user.dto import CreateUserDto, UpdateProfileDto, ChangePasswordDto
from src.app.user.responses import UserResponse
from src.app.user.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])
service = UserService()


@router.post("/", response_model=UserResponse, status_code=201)
async def register(dto: CreateUserDto):
    return await service.create(dto)


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
async def update_profile(dto: UpdateProfileDto, user: User = Depends(get_current_user)):
    return await service.update_profile(user, dto)


@router.patch("/me/password", status_code=204)
async def change_password(dto: ChangePasswordDto, user: User = Depends(get_current_user)):
    await service.change_password(user, dto)

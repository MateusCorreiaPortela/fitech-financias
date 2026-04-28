from fastapi import APIRouter
from src.app.auth.dto import LoginDto
from src.app.auth.responses import TokenResponse
from src.app.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@router.post("/login", response_model=TokenResponse)
async def login(dto: LoginDto):
    token = await service.login(dto.email, dto.password)
    return TokenResponse(access_token=token)

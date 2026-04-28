from fastapi import HTTPException
from src.app.core.models import User
from src.app.core.security import verify_password, create_access_token


class AuthService:
    async def login(self, email: str, password: str) -> str:
        user = await User.filter(email=email).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return create_access_token(user.id)

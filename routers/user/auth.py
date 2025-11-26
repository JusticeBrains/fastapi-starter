from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from config.auth import get_current_user
from config.session import get_session
from models.user.user import User
from schemas.base import Token
from schemas.user.user import UserLogin
from services.user.user import UserService

router = APIRouter(prefix="/auth", tags=["/auth"])


@router.post("/login", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    return await UserService.login(data=data, session=session)


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str, session: AsyncSession = Depends(get_session)
):
    return await UserService.refresh_access_token(
        refresh_token=refresh_token, session=session
    )


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
    }

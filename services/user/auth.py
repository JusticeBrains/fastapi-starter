from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.user.user import RevokedToken, User
from schemas.base import Token
from schemas.user.user import UserLogin

from datetime import datetime
from fastapi import HTTPException, status

from config.auth import Auth

auth = Auth()


class AuthService:
    @staticmethod
    async def login(data: UserLogin, session: AsyncSession) -> Token:
        query = select(User).where(User.username == data.username)
        result = await session.exec(query)
        user = result.one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is inactive",
            )

        if not await auth.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )

        access_token = await auth.create_access_token(data={"sub": str(user.id)})
        refresh_token = await auth.create_refresh_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def logout(token: str, session: AsyncSession):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        revoked = RevokedToken(token=token, revoked_at=datetime.now())
        session.add(revoked)
        await session.commit()
        return {"detail": "Logged out successfully"}

    @staticmethod
    async def refresh_access_token(refresh_token: str, session: AsyncSession) -> Token:
        user_id = await auth.verify_token(token=refresh_token, session=session)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await session.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or inactive",
            )

        access_token = await auth.create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, refresh_token=refresh_token)

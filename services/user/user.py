from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from config.auth import Auth
from models.user.user import RevokedToken, User
from schemas.base import Token
from schemas.user.user import UserCreate, UserLogin

auth = Auth()


class UserService:
    @staticmethod
    async def create_user(data: UserCreate, session: AsyncSession):
        hashed_password = await auth.get_password_hash(data.password)
        username = User.get_username(data=data)
        fullname = User.get_fullname(data=data)

        user = User.model_validate(
            data.model_dump(exclude_unset=True),
            update={
                "username": username,
                "fullname": fullname,
                "password": hashed_password,
                "is_active": data.is_active,
                "is_password_changed": False,
                "is_password_reset": False,
            },
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

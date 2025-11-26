from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from config.session import get_session
from schemas.user.user import UserCreate, UserRead
from services.user.user import UserService

router = APIRouter(prefix="/users", tags=["/users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    return await UserService.create_user(data=data, session=session)

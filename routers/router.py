from fastapi import APIRouter

from routers.user.user import router as user_router
from routers.user.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/v1")
api_router.include_router(auth_router, prefix="/v1")

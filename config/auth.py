from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from config.rate_limiter import RateLimiter
from config.user_identifier import UserIdentifer
from config.env import REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from config.session import get_session
from models.user.user import User

rate_limiter = RateLimiter()
user_identifier = UserIdentifer()


class Auth:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def verify_token(self, token: str, session: AsyncSession):
        try:
            payload = jwt.decode(token, self.secret_key, self.algorithm)
            user_id: str = payload.get("sub")
            if not user_id:
                return None
            return user_id
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            print(f"Token verification error: {e}")
            return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    session: AsyncSession = Depends(get_session),
    auth: Auth = Depends(Auth),
    request: Request = None,
):
    token = credentials.credentials
    if rate_limiter.is_rate_limited(token):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests"
        )

    user_id = await auth.verify_token(token, session=session)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = await session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    ip_address = user_identifier.get_client_ip(request=request)
    device_info = user_identifier.get_user_device(request=request)
    user_identifier.user_activity(user.username, ip_address, device_info)

    return user

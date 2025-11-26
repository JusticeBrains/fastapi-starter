from environs import Env
from uuid import uuid4

env = Env()
env.read_env()

DEFAULT_SECRET_KEY = str(uuid4())

DATABASE_URL = env.str("DATABASE_URL", default="sqlite+aiosqlite:///./test.db")
SECRET_KEY = env.str("SECRET_KEY", default=DEFAULT_SECRET_KEY)
ALGORITHM = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
REFRESH_TOKEN_EXPIRE_DAYS = env.int("REFRESH_TOKEN_EXPIRE_DAYS", default=7)
REQUESTS_PER_MINUTE = env.int("REQUESTS_PER_MINUTE", default=60)

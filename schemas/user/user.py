from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel


class UserBase(SQLModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    password: str
    is_active: bool = True
    is_password_changed: bool = False
    is_password_reset: bool = False


class UserRead(UserBase):
    id: UUID
    username: str
    fullname: str
    is_active: bool
    is_password_changed: bool
    is_password_reset: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserBase):
    password: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    is_active: bool | None = None
    is_password_changed: bool | None = None
    is_password_reset: bool | None = None


class UserLogin(SQLModel):
    username: str
    password: str
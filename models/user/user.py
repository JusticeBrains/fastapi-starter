from random import random
from uuid import uuid4, UUID
from sqlmodel import Boolean, SQLModel, Column, Field, String


from datetime import datetime


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    username: str = Field(sa_column=Column(String(20), nullable=False, unique=True))
    firstname: str = Field(sa_column=Column(String(50), nullable=False))
    lastname: str = Field(sa_column=Column(String(50), nullable=False))
    fullname: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    password: str = Field(sa_column=Column(String(255), nullable=False))
    is_active: bool = Field(sa_column=Column(Boolean, default=True, nullable=False))
    is_password_changed: bool = Field(sa_column=Column(Boolean, default=False, nullable=False))
    is_password_reset: bool = Field(sa_column=Column(Boolean, default=False, nullable=False))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )

    @staticmethod
    def get_fullname(data):
        return f"{data.lastname} {data.firstname}"

    @staticmethod
    def get_username(data):
        ext = str(random())[2:5]
        return f"{data.firstname[:3].lower()}{data.lastname[1:3].lower()}{ext}"

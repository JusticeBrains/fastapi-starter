from sqlmodel import SQLModel
from typing import Generic, List, TypeVar

T = TypeVar("T")


class ResponseModel(SQLModel, Generic[T]):
    count: int
    next: str | None = None
    previous: str | None = None
    results: List[T]


class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

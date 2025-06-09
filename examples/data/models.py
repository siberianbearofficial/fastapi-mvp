from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str


class User(BaseModel):
    id: UUID
    login: str
    password: str

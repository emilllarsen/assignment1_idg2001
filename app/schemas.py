"""Pydantic schemas for request/response validation."""
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    tokens: int

    model_config = {"from_attributes": True}


class TokenAdd(BaseModel):
    user_id: str
    amount: int


class TokenResponse(BaseModel):
    user_id: str
    tokens: int
    message: str

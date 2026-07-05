from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=6, example="secret123")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    avatar_url: Optional[str] = None
    storage_used: int
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    auth_code: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int  # in seconds
    user_id: int

class UserProfile(BaseModel):
    user_id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime


class UserInDB(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime





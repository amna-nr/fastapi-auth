from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class RegisterRequest(BaseModel):
    email: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class UserOut(BaseModel):
    id: UUID
    email: str
    role: str
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
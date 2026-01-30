from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
  access_token: str
  token_type: str
  refresh_token: Optional[str] = None

class TokenData(BaseModel):
  email: Optional[str] = None

class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class GoogleAuthRequest(BaseModel):
  token: str  # Google OAuth token

class RefreshTokenRequest(BaseModel):
  refresh_token: str
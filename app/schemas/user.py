from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
  email: EmailStr
  full_name = Optional[str] = None

class UserCreate(UserBase):
  password: str

class UserOAuthCreate(BaseModel):
  email: EmailStr
  full_name: Optional[str] = None
  oauth_provider: str
  oauth_id: str

class UserResponse(UserBase):
  id: int
  oauth_provider: Optional[str] = None
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
  full_name: Optional[str] = None
  email: Optional[EmailStr] = None
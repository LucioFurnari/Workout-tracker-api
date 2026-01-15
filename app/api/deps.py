from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import verify_token
from app.models.user import User

# OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_db() -> Generator:
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

async def get_current_user(
  token: str = Depends(oauth2_scheme),
  db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = verify_token(token)
    if email is None:
      return credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
      return credentials_exception
    
    return user

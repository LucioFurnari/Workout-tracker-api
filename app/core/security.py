import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
# from passlib.context import CryptContext
from app.config import settings

# Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Verify a password against a hash"""
  password_bytes = plain_password[:72].encode('utf-8')
  hashed_bytes = hashed_password.encode('utf-8')
  return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
  """Hash a password using bcrypt"""
  # Truncate to 72 bytes as bcrypt requires
  password_bytes = password[:72].encode('utf-8')
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(password_bytes, salt)
  return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
  to_encode = data.copy()
  if expires_delta:
      expire = datetime.utcnow() + expires_delta
  else:
      expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def verify_token(token: str) -> Optional[str]:
  try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email: str = payload.get("sub")
      if email is None:
          return None
      return email
  except JWTError:
      return None
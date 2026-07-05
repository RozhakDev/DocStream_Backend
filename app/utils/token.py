from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import jwt, JWTError

from app.core.config import settings

def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
import time
import jwt
from typing import Optional, Dict
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(subject: str, expires_minutes: int | None = None, extra: dict | None = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    now = int(time.time())
    payload: Dict[str, object] = {"sub": subject, "iat": now, "exp": now + expires_minutes * 60}
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def decode_access_token(token: str) -> Optional[dict]:
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded
    except Exception:
        return None

def create_verify_token(email: str, ttl_minutes: int = 60*24) -> str:
    return create_access_token(email, expires_minutes=ttl_minutes, extra={"purpose": "verify"})

def decode_verify_token(token: str) -> Optional[dict]:
    return decode_access_token(token)
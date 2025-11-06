from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ScoreReq(BaseModel):
    src: str
    mt: str

class BatchReq(BaseModel):
    pairs: List[ScoreReq]

class ScoreResp(BaseModel):
    score: float

class BatchResp(BaseModel):
    scores: List[float]
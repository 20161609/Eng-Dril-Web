from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserLogin, UserOut, Token
from app import models
from app.db import SessionLocal
from app.deps import get_db, get_current_user
from app.utils import hash_password, verify_password, create_access_token, create_verify_token, decode_verify_token
from app.emailer import send_email
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)

def register(data: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    # send verify email
    token = create_verify_token(user.email)
    link = f"{settings.PUBLIC_API_BASE}auth/verify?token={token}" if settings.PUBLIC_API_BASE else f"/auth/verify?token={token}"
    print('Link', link)
    subject = f"[{settings.APP_NAME}] Verify your email"
    body = f"Hello,\n\nClick to verify your email:\n{link}\n\nIf you didn't request this, ignore."
    err = send_email(user.email, subject, body)
    if err:
        # not fatal for API demo; in prod, handle differently
        pass

    return user

@router.get("/verify")
def verify(token: str = Query(...), db: Session = Depends(get_db)):
    payload = decode_verify_token(token)
    if not payload or payload.get("purpose") != "verify":
        raise HTTPException(status_code=400, detail="Invalid token")
    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.add(user)
    db.commit()
    return {"ok": True}

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return current
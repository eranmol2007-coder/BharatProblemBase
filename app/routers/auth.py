from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, OTPVerify, TokenResponse, UserResponse, ForgotPassword, ResetPassword
from app.utils.security import (
    hash_password, verify_password, create_access_token,
    decode_access_token, generate_otp, get_otp_expiry,
)
from app.utils.email import send_reset_email, send_otp_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/signup", response_model=TokenResponse)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    if not data.email and not data.phone:
        raise HTTPException(status_code=400, detail="Email or phone required")

    if data.email:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

    if data.phone:
        existing = db.query(User).filter(User.phone == data.phone).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone already registered")

    otp = generate_otp()
    user = User(
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        otp=otp,
        otp_expiry=get_otp_expiry(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Send OTP via email/SMS
    if data.email:
        send_otp_email(data.email, otp)
    else:
        print(f"OTP for {data.phone}: {otp}")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = None
    if data.email:
        user = db.query(User).filter(User.email == data.email).first()
    elif data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    user = None
    if data.email:
        user = db.query(User).filter(User.email == data.email).first()
    elif data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if user.otp_expiry and user.otp_expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP expired")

    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    db.commit()

    return {"message": "Account verified successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    user = None
    if data.email:
        user = db.query(User).filter(User.email == data.email).first()
    elif data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()

    if not user:
        return {"message": "If an account exists, a reset link has been sent."}

    token = generate_otp(32)
    user.reset_token = token
    user.reset_token_expiry = get_otp_expiry()
    db.commit()

    # Send reset email
    if data.email:
        send_reset_email(data.email, token)
    else:
        print(f"Reset link for {data.phone}: token={token}")

    return {"message": "If an account exists, a reset link has been sent."}


@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    user = None
    if data.email:
        user = db.query(User).filter(User.email == data.email).first()
    elif data.phone:
        user = db.query(User).filter(User.phone == data.phone).first()

    if not user or user.reset_token != data.token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    if user.reset_token_expiry and user.reset_token_expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token expired")

    user.password_hash = hash_password(data.new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()

    return {"message": "Password reset successfully"}

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserOut
from app.schemas.verification import VerifyEmailRequest, ResendVerificationRequest
from app.services.auth_service import (
    register_user,
    verify_email,
    authenticate_user,
    create_access_token,
    resend_verification,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = register_user(db, data.username, data.email, data.password)
    logger.info(f"User registered: {user.email}")
    return {"message": "Verification code sent", "email": user.email}


@router.post("/verify-email")
def verify(data: VerifyEmailRequest, db: Session = Depends(get_db)):
    print(f"Verifying email {data.email} with code {data.code}")
    logger.info(f"Verifying email {data.email} with code {data.code}")
    with open("auth_log.txt", "a") as f:
        f.write(f"Verifying email {data.email} with code {data.code}\n")

    if not verify_email(db, data.email, data.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired code")
    return {"message": "Email verified"}


@router.post("/resend-verification")
def resend(data: ResendVerificationRequest, db: Session = Depends(get_db)):
    if not resend_verification(db, data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to resend code")
    return {"message": "Verification code sent", "email": data.email}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.login, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")
    if not user.is_email_verified:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Email not verified", "email": user.email},
        )

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))

import random
import string
import logging
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS, VERIFICATION_CODE_EXPIRE_MINUTES
from app.models.user import User
from app.models.verification import EmailVerification
from app.services.email_service import send_verification_email

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def generate_verification_code() -> str:
    return "".join(random.choices(string.digits, k=6))


def register_user(db: Session, username: str, email: str, password: str) -> User:
    logger.info(f"Registering user {username} with email {email}")
    with open("auth_log.txt", "a") as f:
        f.write(f"Registering user {username} with email {email}\n")

    user = User(
        username=username,
        email=email.lower(),
        password_hash=hash_password(password),
    )
    db.add(user)
    db.flush()

    code = generate_verification_code()
    verification = EmailVerification(
        user_id=user.id,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_CODE_EXPIRE_MINUTES),
    )
    db.add(verification)
    db.commit()
    db.refresh(user)

    send_verification_email(email, code)
    return user


def resend_verification(db: Session, email: str) -> bool:
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user or user.is_email_verified:
        return False

    code = generate_verification_code()
    verification = EmailVerification(
        user_id=user.id,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=VERIFICATION_CODE_EXPIRE_MINUTES),
    )
    db.add(verification)
    db.commit()

    send_verification_email(email, code)
    return True


def verify_email(db: Session, email: str, code: str) -> bool:
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user:
        return False

    verification = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.user_id == user.id,
            EmailVerification.code == code,
            EmailVerification.is_used == False,
            EmailVerification.expires_at > datetime.now(timezone.utc),
        )
        .order_by(EmailVerification.created_at.desc())
        .first()
    )
    if not verification:
        return False

    verification.is_used = True
    user.is_email_verified = True
    db.commit()
    return True


def authenticate_user(db: Session, login: str, password: str) -> User | None:
    user = db.query(User).filter(
        (User.email == login.lower()) | (User.username == login)
    ).first()
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        return None
    return user

import re

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_must_be_latin(cls, v: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", v):
            raise ValueError("Username must contain only latin letters, digits, hyphens, or underscores")
        return v


class UserLogin(BaseModel):
    login: str  # email or username
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    auth_provider: str
    display_name: str | None = None
    avatar_url: str | None = None
    is_active: bool
    is_email_verified: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

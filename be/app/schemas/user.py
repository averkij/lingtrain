from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


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

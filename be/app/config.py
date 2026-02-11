import os

SECRET_KEY = os.environ.get(
    "LINGTRAIN_SECRET_KEY",
    "dev-secret-key-change-in-production",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

DATABASE_URL = os.environ.get("LINGTRAIN_DATABASE_URL", "sqlite:///./lingtrain.db")

VERIFICATION_CODE_EXPIRE_MINUTES = 15

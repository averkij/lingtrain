import os

SECRET_KEY = os.environ.get(
    "LINGTRAIN_SECRET_KEY",
    "dev-secret-key-change-in-production",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

DATABASE_URL = os.environ.get("LINGTRAIN_DATABASE_URL", "sqlite:///./lingtrain2.db")

VERIFICATION_CODE_EXPIRE_MINUTES = 15

LOG_DIR = os.environ.get("LINGTRAIN_LOG_DIR", "log")
LOG_ARCHIVE_DIR = os.environ.get("LINGTRAIN_LOG_ARCHIVE_DIR", "log_archive")
LOG_RETENTION_DAYS = int(os.environ.get("LINGTRAIN_LOG_RETENTION_DAYS", "7"))
LOG_LEVEL = os.environ.get("LINGTRAIN_LOG_LEVEL", "INFO")

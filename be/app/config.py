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

DATA_DIR = os.environ.get("LINGTRAIN_DATA_DIR", "data")
STATIC_DIR = os.environ.get("LINGTRAIN_STATIC_DIR", "static")
ALIGNER_MODEL = os.environ.get(
    "LINGTRAIN_ALIGNER_MODEL", "sentence_transformer_multilingual_labse"
)
ALIGNER_BATCH_SIZE = int(os.environ.get("LINGTRAIN_ALIGNER_BATCH_SIZE", "200"))
ALIGNER_WINDOW = int(os.environ.get("LINGTRAIN_ALIGNER_WINDOW", "50"))
ALIGNER_PROCESSORS = int(os.environ.get("LINGTRAIN_ALIGNER_PROCESSORS", "1"))
ALIGNER_EMBED_BATCH_SIZE = int(
    os.environ.get("LINGTRAIN_ALIGNER_EMBED_BATCH_SIZE", "5")
)
ALIGNER_NORMALIZE_EMBEDDINGS = (
    os.environ.get("LINGTRAIN_ALIGNER_NORMALIZE_EMBEDDINGS", "true").lower() == "true"
)
ALIGNER_MAX_BATCHES = int(os.environ.get("LINGTRAIN_ALIGNER_MAX_BATCHES", "2000"))

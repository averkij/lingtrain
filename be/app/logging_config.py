import glob
import logging
import logging.config
import os
import zipfile
from datetime import datetime

from app.config import LOG_ARCHIVE_DIR, LOG_DIR, LOG_LEVEL, LOG_RETENTION_DAYS

LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LOG_FORMAT,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                },
                "file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "standard",
                    "filename": LOG_FILE,
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 0,
                    "encoding": "utf-8",
                    "suffix": "%Y-%m-%d",
                },
            },
            "loggers": {
                "uvicorn": {
                    "level": LOG_LEVEL,
                    "propagate": True,
                },
                "uvicorn.access": {
                    "level": LOG_LEVEL,
                    "propagate": True,
                },
            },
            "root": {
                "level": LOG_LEVEL,
                "handlers": ["console", "file"],
            },
        }
    )


def archive_old_logs():
    logger = logging.getLogger(__name__)
    rotated = glob.glob(os.path.join(LOG_DIR, "app.log.*"))
    if not rotated:
        return

    now = datetime.now()
    archived_count = 0

    for path in rotated:
        age_days = (now - datetime.fromtimestamp(os.path.getmtime(path))).days
        if age_days < LOG_RETENTION_DAYS:
            continue

        os.makedirs(LOG_ARCHIVE_DIR, exist_ok=True)
        basename = os.path.basename(path)
        zip_path = os.path.join(LOG_ARCHIVE_DIR, basename + ".zip")

        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(path, basename)
            os.remove(path)
            archived_count += 1
        except Exception:
            logger.exception("Failed to archive %s", path)

    if archived_count:
        logger.info("Archived %d old log file(s) to %s", archived_count, LOG_ARCHIVE_DIR)

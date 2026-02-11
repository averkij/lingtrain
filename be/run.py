import uvicorn
import logging

from app.logging_config import setup_logging, archive_old_logs

setup_logging()
archive_old_logs()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True, log_level="debug")

import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True, log_level="debug")

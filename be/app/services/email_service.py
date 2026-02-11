import logging

logger = logging.getLogger(__name__)

def send_verification_email(email: str, code: str) -> None:
    logger.info(f"Verification code sent to {email}: {code}")
    with open("email_log.txt", "a") as f:
        f.write(f"Verification code sent to {email}: {code}\n")

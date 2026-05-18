import logging

logger = logging.getLogger(__name__)

MAX_LENGTH = 500
BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "you are now",
    "forget everything",
    "act as",
    "jailbreak",
    "prompt injection",
]

def sanitize(text: str) -> tuple[bool, str]:
    # strip whitespace
    text = text.strip()

    # empty check
    if not text:
        return False, "question can't be empty."

    # too long
    if len(text) > MAX_LENGTH:
        return False, f"question too long. max {MAX_LENGTH} characters."

    # prompt injection attempts
    lower = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lower:
            logger.warning("blocked prompt injection attempt: %s", text[:50])
            return False, "that question can't be processed."

    return True, text
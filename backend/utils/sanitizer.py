import logging

logger = logging.getLogger(__name__)

MAX_LENGTH = 500
BLOCKED_PATTERNS = [
    # direct injection
    "ignore previous instructions",
    "ignore all instructions",
    "ignore your instructions",
    "disregard previous",
    "disregard all",
    # role switching
    "you are now",
    "pretend you are",
    "act as",
    "act like",
    "roleplay as",
    "simulate being",
    "you are a different",
    "forget you are",
    "forget your role",
    # jailbreak
    "jailbreak",
    "dan mode",
    "developer mode",
    "no restrictions",
    "without restrictions",
    "bypass your",
    "override your",
    # memory wipes
    "forget everything",
    "forget all",
    "start fresh",
    "new instructions",
    "your new role",
    # prompt leaking
    "show me your prompt",
    "reveal your instructions",
    "what are your instructions",
    "print your system prompt",
    "prompt injection",
]

def sanitize(text: str) -> tuple[bool, str]:
    text = text.strip()

    if not text:
        return False, "question can't be empty."

    if len(text) > MAX_LENGTH:
        return False, f"question too long. max {MAX_LENGTH} characters."

    lower = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lower:
            logger.warning("blocked injection attempt: %s", text[:50])
            return False, "that question can't be processed."

    return True, text
import logging
import httpx
from config.settings import GROQ_API_KEY, GROQ_URL, GROQ_MODEL, MAX_TOKENS

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

    def complete(self, prompt: str) -> str | None:
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7,
        }
        try:
            r = httpx.post(GROQ_URL, headers=self.headers, json=payload, timeout=30)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            logger.error("groq api error: %s", str(e))
            return None
        except Exception as e:
            logger.error("unexpected error: %s", str(e))
            return None
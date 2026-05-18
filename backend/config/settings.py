import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX   = os.getenv("PINECONE_INDEX", "")
PINECONE_HOST    = os.getenv("PINECONE_HOST", "")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.3-70b-versatile"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K       = 3
NAMESPACE   = "ns1"
MAX_TOKENS  = 2048

RATE_LIMIT  = "10/minute"
DAILY_LIMIT = 100

if not all([PINECONE_API_KEY, PINECONE_INDEX, PINECONE_HOST, GROQ_API_KEY]):
    logger.warning("missing env vars — check your .env file")
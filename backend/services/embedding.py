import logging
from sentence_transformers import SentenceTransformer
from config.settings import EMBED_MODEL

logger = logging.getLogger(__name__)

# load at import time so first request isn't slow
logger.info("loading embedding model...")
_model = SentenceTransformer(EMBED_MODEL)
logger.info("embedding model ready")

def encode(text: str) -> list[float]:
    vector = _model.encode(text, convert_to_numpy=True)
    return vector.flatten().tolist()
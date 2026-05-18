import logging
from sentence_transformers import SentenceTransformer
from config.settings import EMBED_MODEL

logger = logging.getLogger(__name__)

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("loading embedding model...")
        _model = SentenceTransformer(EMBED_MODEL)
    return _model

def encode(text: str) -> list[float]:
    vector = get_model().encode(text, convert_to_numpy=True)
    return vector.flatten().tolist()
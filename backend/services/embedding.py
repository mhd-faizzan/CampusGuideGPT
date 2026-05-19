import logging
from fastembed import TextEmbedding
from config.settings import EMBED_MODEL

logger = logging.getLogger(__name__)

logger.info("loading embedding model...")
_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
logger.info("embedding model ready")

def encode(text: str) -> list[float]:
    vectors = list(_model.embed([text]))
    return vectors[0].tolist()
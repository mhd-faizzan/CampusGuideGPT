import logging
from pinecone import Pinecone
from config.settings import PINECONE_API_KEY, PINECONE_INDEX, PINECONE_HOST, TOP_K, NAMESPACE

logger = logging.getLogger(__name__)

MIN_SCORE = 0.55  # filter out irrelevant matches

class VectorService:
    def __init__(self):
        try:
            pc = Pinecone(api_key=PINECONE_API_KEY)
            self.index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
            logger.info("pinecone connected")
        except Exception as e:
            logger.error("pinecone connection failed: %s", str(e))
            raise RuntimeError(f"pinecone failed to connect: {str(e)}")

    def search(self, vector: list[float]) -> list[dict]:
        try:
            results = self.index.query(
                vector=vector,
                top_k=TOP_K,
                include_metadata=True,
                namespace=NAMESPACE,
            )

            # only keep matches we're actually confident about
            confident_matches = [m for m in results.matches if m.score > MIN_SCORE]

            if not confident_matches:
                logger.info("no matches above confidence threshold (%.2f)", MIN_SCORE)

            return [
                {
                    "question": m.metadata.get("question", ""),
                    "answer":   m.metadata.get("answer", ""),
                    "score":    m.score,
                }
                for m in confident_matches
            ]
        except Exception as e:
            logger.error("pinecone search failed: %s", str(e))
            return []
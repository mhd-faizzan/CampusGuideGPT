import logging
from pinecone import Pinecone
from config.settings import PINECONE_API_KEY, PINECONE_INDEX, PINECONE_HOST, TOP_K, NAMESPACE

logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
        logger.info("pinecone connected")

    def search(self, vector: list[float]) -> list[dict]:
        results = self.index.query(
            vector=vector,
            top_k=TOP_K,
            include_metadata=True,
            namespace=NAMESPACE,
        )
        return [
            {
                "question": m.metadata.get("question", ""),
                "answer":   m.metadata.get("answer", ""),
                "score":    m.score,
            }
            for m in results.matches
        ]
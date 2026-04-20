from pinecone import Pinecone

TOP_K     = 3
NAMESPACE = "ns1"

class VectorService:
    def __init__(self, api_key: str, index_name: str, host: str):
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name, host=host)

    def search(self, vector: list[float]) -> list[dict]:
        results = self.index.query(
            vector=vector,
            top_k=TOP_K,
            include_metadata=True,
            namespace=NAMESPACE,
        )
        return [
            {
                "question": m.get("metadata", {}).get("question", ""),
                "answer":   m.get("metadata", {}).get("answer", ""),
                "score":    m.get("score", 0.0),
            }
            for m in results.matches
        ]

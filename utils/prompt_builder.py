def build_prompt(question: str, hits: list[dict]) -> str:
    # no results — fall back to general knowledge
    if not hits:
        return (
            f"Answer this question about Hochschule Harz based on general knowledge.\n\n"
            f"Question: {question}\nAnswer:"
        )

    # build context from retrieved chunks
    context = ""
    for i, hit in enumerate(hits, 1):
        context += f"Source {i}:\nQ: {hit['question']}\nA: {hit['answer']}\n\n"

    return (
        f"Context:\n{context}\n"
        f"Question: {question}\n\n"
        f"Answer concisely based on the context:\n"
    )

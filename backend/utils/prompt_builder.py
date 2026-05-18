def build_prompt(question: str, hits: list[dict]) -> str:
    if not hits:
        return (
            f"You are CampusGuideGPT, a helpful assistant for Hochschule Harz students.\n\n"
            f"Answer this question using your general knowledge.\n"
            f"If unsure, tell the user to contact bwehlend@hs-harz.de\n\n"
            f"Question: {question}\nAnswer:"
        )

    context = ""
    for i, hit in enumerate(hits, 1):
        context += f"Source {i}:\nQ: {hit['question']}\nA: {hit['answer']}\n\n"

    return (
        f"You are CampusGuideGPT, a helpful assistant for Hochschule Harz students.\n\n"
        f"Use the context below to answer the question.\n"
        f"Never mention 'Source 1/2/3' — answer naturally.\n"
        f"If unsure, suggest contacting bwehlend@hs-harz.de\n\n"
        f"Context:\n{context}\n"
        f"Question: {question}\nAnswer:"
    )
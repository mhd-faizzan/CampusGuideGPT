def build_prompt(question: str, hits: list[dict]) -> str:
    # no results — fall back to general knowledge
    if not hits:
        return (
            f"You are CampusGuideGPT, a friendly assistant for Hochschule Harz and German universities.\n\n"
            f"Answer the following question helpfully. Start with a warm opening, give a thorough answer, "
            f"and end by offering further help.\n\n"
            f"Question: {question}\nAnswer:"
        )

    # build context from retrieved chunks
    context = ""
    for i, hit in enumerate(hits, 1):
        context += f"Source {i}:\nQ: {hit['question']}\nA: {hit['answer']}\n\n"

    return (
        f"You are CampusGuideGPT, a friendly and knowledgeable assistant for Hochschule Harz.\n\n"
        f"Use the context below to answer the user's question in a warm, conversational way.\n\n"
        f"Context:\n{context}\n"
        f"Question: {question}\n\n"
        f"Instructions:\n"
        f"- Start with a friendly opening sentence acknowledging the question\n"
        f"- Give a clear, thorough explanation based on the context\n"
        f"- End with a helpful closing sentence offering further assistance\n"
        f"- Use a warm, helpful tone like a knowledgeable senior student\n\n"
        f"Answer:"
    )

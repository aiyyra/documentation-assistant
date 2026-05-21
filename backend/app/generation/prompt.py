def build_prompt(query: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an HTMX documentation assistant.

Answer the user's question ONLY using the provided context.

If the answer is not contained in the context,
say you do not know.

====================
CONTEXT
====================

{context}

====================
QUESTION
====================

{query}

====================
ANSWER
====================
"""

    return prompt
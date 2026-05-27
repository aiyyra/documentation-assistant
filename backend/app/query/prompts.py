def build_rewrite_prompt(query: str) -> str:
    return f"""
You are a query rewriting system for an HTMX documentation retrieval engine.

Your task is to rewrite the user's query into a concise technical retrieval query.

Focus on:
- HTMX terminology
- HTMX attribute names
- technical concepts
- concise retrieval phrasing

IMPORTANT:
- Do NOT answer the question
- Do NOT explain anything
- Return ONLY the rewritten query

Some example:
1. User Query: `How do I update part of the page automatically?` -> Rewritten Query: `htmx partial page updates using hx-swap and hx-target`
2. User Query: `How do I trigger requests from events?` -> Rewritten Query: `htmx triggering requests with hx-trigger events`
3. User Query: `Help me dynamically insert data into htmx container` -> Rewritten Query: `htmx triggering requests with hx-trigger eventshtmx dynamic DOM updates using hx-swap and hx-target`

User Query:
{query}

Rewritten Query:
"""


def build_contextual_rewrite_prompt(
    query: str,
    history: str,
) -> str:
    return f"""
You are a query rewriting system for an HTMX documentation retrieval engine.

Your task is to rewrite the user's query into a concise technical retrieval query.

Use the conversation context to resolve references and follow-ups.

Focus on:
- HTMX terminology
- HTMX attribute names
- technical concepts
- concise retrieval phrasing

IMPORTANT:
- Do NOT answer the question
- Do NOT explain anything
- Return ONLY the rewritten query

Conversation Context:
{history}

User Query:
{query}

Rewritten Query:
"""
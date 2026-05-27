from openai import OpenAI

from langchain_core.messages import BaseMessage

from app.agent.utils import format_history

import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a routing system for an HTMX RAG assistant.

Classify the user query into ONE category:

- rag
- conversational

Use:
- rag → HTMX/documentation/technical questions
- conversational → greetings, thanks, casual chat, follow ups or anything not necesserily HTMX-related

Return ONLY one word:
- rag
- conversational
"""


def route_query(query: str) -> str:
    return _route_query_internal(query, None)


def route_query_with_history(
    query: str,
    chat_history: list[BaseMessage] | None,
) -> str:
    history_text = format_history(chat_history)

    return _route_query_internal(query, history_text)


def _route_query_internal(
    query: str,
    history: str | None,
) -> str:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if history:
        messages.append(
            {
                "role": "system",
                "content": (
                    "Conversation context:\n" + history
                ),
            }
        )

    messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0,
    )

    route = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .lower()
    )

    if route not in [
        "rag",
        "conversational",
    ]:
        route = "rag"

    return route


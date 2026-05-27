import os

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

from app.agent.memory import (
    append_ai_message,
    append_user_message,
)


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are a strict evaluator for an HTMX assistant.

Check whether the answer:
1) Addresses the user's question.
2) Is grounded in the provided context (if context is provided).

Return ONLY one of the following formats:
- PASS
- RETRY: <short reason>
"""


def evaluate_node(state):
    query = state["query"]
    answer = state.get("answer", "")
    context_block = state.get("context_block", "")

    evaluation_input = (
        "QUESTION:\n"
        f"{query}\n\n"
        "ANSWER:\n"
        f"{answer}\n\n"
    )

    if context_block:
        evaluation_input += (
            "CONTEXT:\n"
            f"{context_block}\n\n"
        )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": evaluation_input,
            },
        ],
        temperature=0,
    )

    verdict_raw = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    verdict_lower = verdict_raw.lower()

    needs_retry = verdict_lower.startswith("retry")
    retry_reason = ""

    if needs_retry:
        parts = verdict_raw.split(":", 1)
        if len(parts) > 1:
            retry_reason = parts[1].strip()

    loop_count = state.get("loop_count", 0)
    max_loops = state.get("max_loops", 1)

    if needs_retry and loop_count < max_loops:
        loop_count += 1
    else:
        needs_retry = False
        retry_reason = ""

    next_state = {
        **state,
        "needs_retry": needs_retry,
        "retry_reason": retry_reason,
        "loop_count": loop_count,
        "max_loops": max_loops,
    }

    if not needs_retry:
        chat_history = state.get("chat_history", [])

        chat_history = append_user_message(
            chat_history,
            query,
        )

        metadata = {
            "citations": state.get(
                "citations",
                [],
            ),
            "used_rag": state.get(
                "used_rag",
                False,
            ),
            "rewritten_query": state.get(
                "rewritten_query",
                None,
            ),
            "retry_reason": retry_reason,
        }

        chat_history = append_ai_message(
            chat_history,
            answer,
            metadata=metadata,
        )

        next_state["chat_history"] = chat_history

    return next_state

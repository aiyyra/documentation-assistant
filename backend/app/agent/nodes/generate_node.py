from app.generation.agent_prompt import (
    build_agent_prompt,
)
from app.generation.generator import generate_response


def generate_node(state):
    query = state["query"]
    chat_history = state.get(
        "chat_history",
        [],
    )

    context_block = state.get(
        "context_block",
        "",
    )

    prompt = build_agent_prompt(
        query=query,
        chat_history=chat_history,
        context_block=context_block,
    )

    answer = generate_response(prompt)

    route = state.get(
        "route",
        "conversational",
    )

    return {
        **state,
        "route": route,
        "answer": answer,
    }

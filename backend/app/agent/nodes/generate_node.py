from app.agent.memory import (
    append_ai_message,
    append_user_message,
)
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
    }

    chat_history = append_ai_message(
        chat_history,
        answer,
        metadata=metadata,
    )

    route = state.get(
        "route",
        "conversational",
    )

    return {
        **state,
        "route": route,
        "answer": answer,
        "chat_history": chat_history,
    }

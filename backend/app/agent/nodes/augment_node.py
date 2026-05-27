from app.generation.agent_prompt import (
    build_context_block,
)


def augment_node(state):
    chunks = state.get(
        "retrieved_chunks",
        [],
    )

    context_block = (
        build_context_block(chunks)
        if chunks
        else ""
    )

    return {
        **state,
        "context_block": context_block,
    }

from langgraph.graph import (
    StateGraph,
    END,
)

from app.agent.state import AgentState
from app.agent.router import (
    route_query_with_history,
)

from app.agent.nodes.retrieve_node import (
    retrieve_node,
)
from app.agent.nodes.augment_node import (
    augment_node,
)
from app.agent.nodes.generate_node import (
    generate_node,
)


workflow = StateGraph(AgentState)


workflow.add_node("retrieve", retrieve_node)
workflow.add_node("augment", augment_node)
workflow.add_node("generate", generate_node)


# Router function

def router(state: AgentState):
    route = route_query_with_history(
        state["query"],
        state.get("chat_history"),
    )

    return route


workflow.set_conditional_entry_point(
    router,
    {
        "rag": "retrieve",
        "conversational": "generate",
    },
)


workflow.add_edge("retrieve", "augment")
workflow.add_edge("augment", "generate")
workflow.add_edge("generate", END)


graph = workflow.compile()


if __name__ == "__main__":
    chat_history = []
    while True:
        query = input("\nQuery > ")

        if query.lower() in [
            "exit",
            "quit",
        ]:
            break

        result = graph.invoke(
            {
                "query": query,
                "chat_history": chat_history,
            }
        )

        chat_history = result.get(
            "chat_history",
            chat_history,
        )

        print("\nROUTE:")
        print(result.get("route"))

        print("\nANSWER:\n")
        print(result["answer"])
from app.agent.nodes.augment_node import (
    augment_node,
)


# Reason:
# Context block should be assembled from chunks.
def test_augment_node_builds_context_block():
    state = {
        "retrieved_chunks": [
            "chunk a",
            "chunk b",
        ]
    }

    result = augment_node(state)

    assert result["context_block"] == (
        "chunk a\n\nchunk b"
    )


# Reason:
# Empty chunks should yield empty context.
def test_augment_node_empty_context():
    result = augment_node({})

    assert result["context_block"] == ""

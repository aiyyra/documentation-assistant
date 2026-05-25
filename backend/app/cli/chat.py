from app.rag.pipeline import ask


def main():
    print("HTMX RAG Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Query > ")

        if query.lower() in ["exit", "quit"]:
            break

        result = ask(query)

        print("\n" + "=" * 80)
        print("ANSWER\n")
        print(result["answer"])

        print("\n" + "=" * 80)
        print("SOURCES\n")

        for metadata in result["metadata"]:
            print(
                f"- {metadata['source']} "
                f"(chunk {metadata['chunk_index']})"
            )

        print("\n")

        print("\nCITATIONS\n")

        for citation in result["citations"]:
            print(
                f"- {citation['source']} "
                f"(chunk {citation['chunk_index']})"
            )


if __name__ == "__main__":
    main()
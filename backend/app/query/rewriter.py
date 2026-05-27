from openai import OpenAI

from app.query.prompts import (
    build_rewrite_prompt,
    build_contextual_rewrite_prompt,
)

import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

client = OpenAI()


def rewrite_query(query: str) -> str:
    prompt = build_rewrite_prompt(query)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        # to ensure the output is static and stable: temperature must be 0
        temperature=0, 
    )

    rewritten_query = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return rewritten_query


def rewrite_query_with_history(
    query: str,
    history: str,
) -> str:
    prompt = build_contextual_rewrite_prompt(
        query,
        history,
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    rewritten_query = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return rewritten_query


if __name__ == "__main__":
    while True:
        query = input("\nOriginal Query > ")

        if query.lower() in ["exit", "quit"]:
            break

        rewritten = rewrite_query(query)

        print("\nREWRITTEN QUERY:\n")

        print(rewritten)
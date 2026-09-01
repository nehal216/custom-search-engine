import os

from dotenv import load_dotenv
from groq import Groq

MAX_CONTENT_LENGTH = 3000

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


def generate_answer(query, search_results):
    context_parts = []

    for number, result in enumerate(search_results, start=1):
        content = result.get("content", "")

        # Limit each result to avoid sending excessive text
        content = content[:MAX_CONTENT_LENGTH]

        context_parts.append(
            f"""
Source {number}
Title: {result.get('title', 'Unknown')}
URL: {result.get('url', 'Unknown')}
Content:
{content}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
    You are an AI search assistant.

    Answer the user's question using the web search results provided below.

    USER QUESTION:
    {query}

    WEB SEARCH RESULTS:
    {context}

    RULES:
    1. Give a clear and useful answer.
    2. Base your answer on the provided search results.
    3. Do not invent information.
    4. If the sources disagree, mention the disagreement.
    5. If there is not enough information to answer confidently, say so.
    6. Keep the answer reasonably concise.
    """

    try:
        response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful and reliable AI search assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"Unable to generate an AI answer: {error}"
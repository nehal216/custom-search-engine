import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)


def generate_answer(query, search_results):
    context = ""

    for number, result in enumerate(search_results, start=1):
        context += (
            f"Source {number}:\n"
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Content: {result.get('content', '')}\n\n"
        )

    prompt = f"""
You are an AI search assistant.

Answer the user's question using the provided web search results.

User question:
{query}

Web search results:
{context}

Instructions:
- Give a clear and concise answer.
- Use the search results as your primary source of information.
- Do not invent facts that are not supported by the results.
- If the search results do not contain enough information, say so.
- Do not include a separate sources list. The Python program will display the sources.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI search assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
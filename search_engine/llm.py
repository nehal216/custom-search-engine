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
            SOURCE [{number}]
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
    2. Base your answer only on the provided search results.
    3. Do not invent information.
    4. Add a citation like [1], [2], or [3] after claims that are supported by a source.
    5. The citation number must match the source number provided above.
    6. You may use multiple citations such as [1][3] when multiple sources support a claim.
    7. If the sources disagree, mention the disagreement and cite the relevant sources.
    8. If there is not enough information to answer confidently, say so.
    9. Do not create citations that do not exist.
    10. Do not include a separate sources section. The Python program will display the sources.
    11. Keep the answer reasonably concise.
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
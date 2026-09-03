import os

from dotenv import load_dotenv
from groq import Groq


MAX_CONTENT_LENGTH = 3000

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(query, search_results, conversation_history=None):

    if conversation_history is None:
        conversation_history = []

    # Build search-result context
    context_parts = []

    for number, result in enumerate(search_results, start=1):

        title = result.get("title", "Unknown")
        url = result.get("url", "Unknown")
        content = result.get("content", "")

        content = content[:MAX_CONTENT_LENGTH]

        context_parts.append(
            f"""
            SOURCE [{number}]
            Title: {title}
            URL: {url}
            Content: {content}
            """
        )

    context = "\n".join(context_parts)

    # Build conversation history
    history_text = ""

    for message in conversation_history:
        history_text += (
            f"{message['role'].upper()}: "
            f"{message['content']}\n"
        )

    # Build the prompt
    prompt = f"""
    You are an AI search assistant.

    Use the conversation history and web search results
    to answer the user's latest question.

    CONVERSATION HISTORY:
    {history_text}

    LATEST USER QUESTION:
    {query}

    WEB SEARCH RESULTS:
    {context}

    RULES:
    1. Answer the latest question clearly.
    2. Use the conversation history to understand references
    such as "it", "they", "which one", or "that".
    3. Use the web search results as the primary source of facts.
    4. Do not invent information.
    5. Add citations such as [1], [2], or [3] after claims
    supported by the corresponding source.
    6. If multiple sources support a claim, use multiple citations.
    7. If the sources disagree, mention the disagreement.
    8. If there is not enough information, say so.
    9. Do not create citations that do not exist.
    10. Do not include a separate sources section.
    11. Keep the answer reasonably concise.
    """

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content

        if not answer:
            return "Unable to generate an AI answer: empty response."

        return answer

    except Exception as error:
        return f"Unable to generate an AI answer: {error}"
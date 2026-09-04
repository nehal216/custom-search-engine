import re
from search_engine.llm import rewrite_query_with_llm

def clean_query(query):
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def analyze_query(query):
    query = clean_query(query)

    if not query:
        return []

    # Only split when "and" is connecting two separate questions.
    # For example:
    #
    # "Why is the sky blue and does it look different on Mars?"
    #
    # But do NOT split:
    #
    # "What are Python and Java used for?"

    question_words = (
        "what",
        "why",
        "how",
        "when",
        "where",
        "who",
        "which",
        "does",
        "do",
        "did",
        "is",
        "are",
        "can",
        "could",
        "would",
        "should"
    )

    pattern = (
        r"\band\s+(?="
        + "|".join(question_words)
        + r")\b"
    )

    parts = re.split(
        pattern,
        query,
        flags=re.IGNORECASE
    )

    queries = []

    for part in parts:
        part = part.strip(" ,.?")

        if part:
            queries.append(part)

    return queries


def make_contextual_query(query, conversation_history):
    """
    Rewrite a follow-up question into a standalone
    search query using conversation history.
    """

    if not conversation_history:
        return query

    recent_messages = conversation_history[-6:]

    conversation_context = ""

    for message in recent_messages:
        role = message["role"].upper()
        content = message["content"]

        conversation_context += (
            f"{role}: {content}\n"
        )

    return rewrite_query_with_llm(
        query,
        conversation_context
    )
import re


def clean_query(query):
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query


def analyze_query(query):
    query = clean_query(query)

    if not query:
        return []

    parts = re.split(r"\band\b", query, flags=re.IGNORECASE)

    queries = []

    for part in parts:
        part = part.strip(" ,.?")

        if part:
            queries.append(part)

    return queries


def make_contextual_query(query, conversation_history):
    """
    Add recent conversation context to follow-up questions.
    """

    if not conversation_history:
        return query

    # Get the most recent user message.
    previous_user_message = None

    for message in reversed(conversation_history):
        if message["role"] == "user":
            previous_user_message = message["content"]
            break

    if not previous_user_message:
        return query

    # Words that usually indicate a follow-up question.
    follow_up_words = [
        "it",
        "its",
        "they",
        "them",
        "their",
        "this",
        "that",
        "these",
        "those",
        "he",
        "she",
        "which one",
        "what about",
        "how about"
    ]

    query_lower = query.lower()

    is_follow_up = any(
        phrase in query_lower
        for phrase in follow_up_words
    )

    if is_follow_up:
        return f"{query} Context: {previous_user_message}"

    return query
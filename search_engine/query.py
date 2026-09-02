import re


QUESTION_WORDS = {
    "what",
    "why",
    "how",
    "when",
    "where",
    "who",
    "which",
    "can",
    "does",
    "do",
    "is",
    "are"
}


def clean_query(query):
    query = query.strip()

    query = re.sub(r"\s+", " ", query)

    return query


def analyze_query(query):
    query = clean_query(query)

    if not query:
        return []

    # Split questions joined by "and"
    parts = re.split(r"\band\b", query, flags=re.IGNORECASE)

    queries = []

    for part in parts:
        part = part.strip(" ,.?")

        if not part:
            continue

        queries.append(part)

    return queries
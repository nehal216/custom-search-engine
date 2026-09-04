from search_engine.query import clean_query, analyze_query


def test_clean_query_removes_extra_spaces():
    query = "   What    is    Python?   "

    result = clean_query(query)

    assert result == "What is Python?"


def test_analyze_query_keeps_python_and_java_together():
    query = "What are Python and Java used for?"

    result = analyze_query(query)

    assert result == [
        "What are Python and Java used for"
    ]


def test_analyze_query_splits_two_questions():
    query = "Why is the sky blue and does it look different on Mars?"

    result = analyze_query(query)

    assert result == [
        "Why is the sky blue",
        "does it look different on Mars"
    ]


def test_analyze_query_empty_query():
    result = analyze_query("")

    assert result == []
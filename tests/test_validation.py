from search_engine.validation import (
    extract_citations,
    validate_citations,
    remove_invalid_citations
)


def test_extract_citations():

    answer = (
        "Python is a programming language [1]. "
        "It was created by Guido van Rossum [2]."
    )

    result = extract_citations(answer)

    assert result == [1, 2]


def test_validate_valid_citations():

    answer = "Python is a programming language [1]."

    sources = [
        {"title": "Python", "url": "https://python.org"},
        {"title": "Wikipedia", "url": "https://wikipedia.org"}
    ]

    valid, invalid = validate_citations(
        answer,
        sources
    )

    assert valid == [1]
    assert invalid == []


def test_validate_invalid_citations():

    answer = "Python is a programming language [5]."

    sources = [
        {"title": "Python", "url": "https://python.org"},
        {"title": "Wikipedia", "url": "https://wikipedia.org"}
    ]

    valid, invalid = validate_citations(
        answer,
        sources
    )

    assert valid == []
    assert invalid == [5]


def test_remove_invalid_citations():

    answer = (
        "Python is a programming language [1]. "
        "It was created by someone [9]."
    )

    sources = [
        {"title": "Python", "url": "https://python.org"}
    ]

    result = remove_invalid_citations(
        answer,
        sources
    )

    assert result == (
        "Python is a programming language [1]. "
        "It was created by someone ."
    )
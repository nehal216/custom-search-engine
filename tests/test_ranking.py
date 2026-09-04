from search_engine.ranking import (
    is_valid_result,
    get_domain,
    calculate_relevance_score,
    rank_results
)


def create_result(title, url, content, score):
    return {
        "title": title,
        "url": url,
        "content": content,
        "score": score
    }


def test_valid_result():

    result = create_result(
        "Python Programming",
        "https://python.org",
        "Python is a programming language used for many applications.",
        0.9
    )

    assert is_valid_result(result) is True


def test_invalid_result_without_title():

    result = create_result(
        "",
        "https://python.org",
        "Python is a programming language used for many applications.",
        0.9
    )

    assert is_valid_result(result) is False


def test_invalid_result_without_content():

    result = create_result(
        "Python",
        "https://python.org",
        "",
        0.9
    )

    assert is_valid_result(result) is False


def test_get_domain():

    result = get_domain(
        "https://www.python.org/tutorial/"
    )

    assert result == "python.org"


def test_higher_score_ranks_first():

    results = [
        create_result(
            "Python",
            "https://example.com/python",
            "Python is a high-level programming language used for software development, automation, data analysis, and many other applications.",
            0.5
        ),
        create_result(
            "Python Programming",
            "https://python.org",
            "Python is a high-level programming language used for software development, automation, data analysis, and many other applications.",
            0.9
        )
    ]

    ranked = rank_results(
        results,
        "Python programming"
    )

    assert ranked[0]["url"] == "https://python.org"

def test_duplicate_domains_are_removed():

    results = [
        create_result(
            "Python Page 1",
            "https://example.com/page1",
            "Python programming information with useful content.",
            0.9
        ),
        create_result(
            "Python Page 2",
            "https://example.com/page2",
            "More Python programming information with useful content.",
            0.8
        ),
        create_result(
            "Python Page 3",
            "https://python.org",
            "Official Python programming language information.",
            0.7
        )
    ]

    ranked = rank_results(
        results,
        "Python programming"
    )

    domains = [
        get_domain(result["url"])
        for result in ranked
    ]

    assert domains.count("example.com") == 1
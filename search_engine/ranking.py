from urllib.parse import urlparse


def is_valid_result(result):
    """
    Check whether a search result contains enough
    useful information to be included.
    """

    if not result:
        return False

    url = result.get("url", "")
    title = result.get("title", "")
    content = result.get("content", "")

    # Result must have a valid URL
    if not url.startswith(("http://", "https://")):
        return False

    # Result should have a title
    if not title.strip():
        return False

    # Result should contain some actual content
    if len(content.strip()) < 50:
        return False

    return True

def get_domain(url):
    """
    Extract the domain name from a URL.
    """

    try:
        parsed_url = urlparse(url)

        return parsed_url.netloc.lower().replace(
            "www.",
            ""
        )

    except Exception:
        return ""


def rank_results(results, limit=3):

    if not results:
        return []

    try:
        # Step 1: Remove poor-quality results
        valid_results = []

        for result in results:
            if is_valid_result(result):
                valid_results.append(result)

        # Step 2: Sort by Tavily relevance score
        ranked_results = sorted(
            valid_results,
            key=lambda result: result.get("score", 0),
            reverse=True
        )

        # Step 3: Remove duplicate URLs
        selected_results = []
        seen_urls = set()
        seen_domains = set()

        for result in ranked_results:

            url = result.get("url", "").strip()
            domain = get_domain(url)

            if url in seen_urls:
                continue

            if domain in seen_domains:
                continue

            selected_results.append(result)
            seen_urls.add(url)
            seen_domains.add(domain)

            if len(selected_results) >= limit:
                break

        return selected_results

    except Exception as error:
        print(f"Ranking error: {error}")

        # Fall back to the original results
        return results
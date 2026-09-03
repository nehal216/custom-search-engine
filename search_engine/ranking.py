def rank_results(results, limit=3):

    if not results:
        return []

    try: 
        ranked_results = sorted(
            results,
            key=lambda result: result.get("score", 0),
            reverse=True
        )

        selected_results = []
        seen_urls = set()

        for result in ranked_results:
            url = result.get("url")

            if url in seen_urls:
                continue

            selected_results.append(result)
            seen_urls.add(url)

            if len(selected_results) >= limit:
                break

        return selected_results
    
    except Exception as error:
        print(f"Ranking error: {error}")

        # Fall back to the original results
        return results
def rank_results(results, limit=3):
    ranked_results = sorted(
        results,
        key=lambda result: result.get("score", 0),
        reverse=True
    )

    return ranked_results[:limit]
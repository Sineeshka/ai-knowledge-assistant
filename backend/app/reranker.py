def rerank(query: str, results: list, top_k: int = 5):
    if not results:
        return []

    # Keep retrieval lightweight for small hosts. The hybrid RRF score is
    # already calculated by search.py and avoids loading a second ML model.
    return sorted(
        results,
        key=lambda result: result.get("rrf_score", 0),
        reverse=True,
    )[:top_k]
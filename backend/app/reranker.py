from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query: str, results: list, top_k: int = 5):
    if not results:
        return []

    pairs = [
        (query, result["content"])
        for result in results
    ]

    scores = model.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):
        reranked.append({
            **result,
            "reranker_score": float(score)
        })

    reranked.sort(
        key=lambda x: x["reranker_score"],
        reverse=True
    )

    return reranked[:top_k]
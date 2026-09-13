from sqlalchemy import select, text
from .models import DocumentChunk
from .embedding import generate_embedding
from .database import SessionLocal

# Vector search
def search_similar_chunks(query: str, top_k: int = 5):
    query_embedding = generate_embedding(query)

    db = SessionLocal()

    try:
        statement = (
            select(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(query_embedding).label(
                    "distance"
                )
            )
            .where(DocumentChunk.embedding.is_not(None))
            .order_by("distance")
            .limit(top_k)
        )

        results = db.execute(statement).all()

        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "distance": float(distance),
            }
            for chunk, distance in results
        ]

    finally:
        db.close()

#keyword search
def search_keyword_chunks(query: str, top_k: int = 5):
    db = SessionLocal()

    try:
        sql = text("""
            SELECT
                id,
                document_id,
                page_number,
                chunk_index,
                content,
                ts_rank(
                    to_tsvector('english', content),
                    plainto_tsquery('english', :query)
                ) AS rank
            FROM document_chunks
            WHERE to_tsvector('english', content)
                  @@ plainto_tsquery('english', :query)
            ORDER BY rank DESC
            LIMIT :top_k
        """)

        results = db.execute(
            sql,
            {
                "query": query,
                "top_k": top_k
            }
        ).mappings().all()

        return [
            {
                "chunk_id": row["id"],
                "document_id": row["document_id"],
                "page_number": row["page_number"],
                "chunk_index": row["chunk_index"],
                "content": row["content"],
                "rank": float(row["rank"])
            }
            for row in results
        ]

    finally:
        db.close()

#hybrid search

def hybrid_search(query: str, top_k: int = 5):
    vector_results = search_similar_chunks(query, top_k=10)
    keyword_results = search_keyword_chunks(query, top_k=10)

    rrf_scores = {}

    # Add scores from vector search
    for rank, result in enumerate(vector_results, start=1):
        chunk_id = result["chunk_id"]

        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = {
                "score": 0,
                "result": result
            }

        rrf_scores[chunk_id]["score"] += 1 / (60 + rank)

    # Add scores from keyword search
    for rank, result in enumerate(keyword_results, start=1):
        chunk_id = result["chunk_id"]

        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = {
                "score": 0,
                "result": result
            }

        rrf_scores[chunk_id]["score"] += 1 / (60 + rank)

    ranked_results = sorted(
        rrf_scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    final_results = []

    for item in ranked_results[:top_k]:
        result = item["result"]

        final_results.append({
            "chunk_id": result["chunk_id"],
            "document_id": result["document_id"],
            "page_number": result["page_number"],
            "chunk_index": result["chunk_index"],
            "content": result["content"],
            "rrf_score": item["score"]
        })

    return final_results
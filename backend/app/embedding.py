import os

from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")


def generate_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT",
):
    return generate_embeddings([text], task_type=task_type)[0]


def generate_embeddings(
    texts: list[str],
    task_type: str = "RETRIEVAL_DOCUMENT",
):
    if not texts:
        return []

    response = client.models.embed_content(
        model=MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=384,
        ),
    )

    return [embedding.values for embedding in response.embeddings]
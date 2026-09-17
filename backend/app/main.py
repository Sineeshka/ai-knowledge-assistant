import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from pathlib import Path
from sqlalchemy import select, text
from .database import Base, engine, SessionLocal
from . import models
from .pdf_parser import extract_text_from_pdf
from .chunker import chunk_text
from .search import search_similar_chunks, search_keyword_chunks, hybrid_search
from .embedding import generate_embeddings
from .reranker import rerank
from .llm import generate_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Knowledge Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        os.getenv("FRONTEND_URL"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "AI Knowledge Assistant API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": result.scalar()}


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "20")) * 1024 * 1024
MAX_PDF_PAGES = int(os.getenv("MAX_PDF_PAGES", "200"))


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    filename = Path(file.filename or "document.pdf").name
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        total_bytes = 0
        while content := await file.read(1024 * 1024):
            total_bytes += len(content)
            if total_bytes > MAX_UPLOAD_BYTES:
                file_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=413,
                    detail=f"PDF must be smaller than {MAX_UPLOAD_BYTES // (1024 * 1024)} MB",
                )
            buffer.write(content)

    try:
        pages = extract_text_from_pdf(str(file_path), max_pages=MAX_PDF_PAGES)
    except ValueError as error:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=413, detail=str(error)) from error

    all_chunks = []
    for page in pages:
        chunks = chunk_text(page["text"])

        for chunk_index, chunk in enumerate(chunks):
            all_chunks.append({
                "page_number": page["page_number"],
                "chunk_index": chunk_index,
                "content": chunk
            })
      
    db = SessionLocal()
    try:
        document = models.Document(
            filename=filename,
            file_type=file.content_type
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        embedding_batch_size = 50
        for batch_start in range(0, len(all_chunks), embedding_batch_size):
            chunk_batch = all_chunks[
                batch_start:batch_start + embedding_batch_size
            ]
            embeddings = generate_embeddings([
                chunk["content"]
                for chunk in chunk_batch
            ])

            for chunk, embedding in zip(chunk_batch, embeddings):
                document_chunk = models.DocumentChunk(
                    document_id=document.id,
                    page_number=chunk["page_number"],
                    chunk_index=chunk["chunk_index"],
                    content=chunk["content"],
                    embedding=embedding
                )
                db.add(document_chunk)

        db.commit()

        # Read ORM values while the database session is still open.
        return {
            "id": document.id,
            "filename": document.filename,
            "file_type": document.file_type,
            "pages": len(pages),
            "message": "Document uploaded and text extracted successfully"
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.get("/ask")
def ask(q: str):
    # Step 1: Retrieve candidate chunks
    candidates = hybrid_search(q, top_k=10)

    # Step 2: Rerank the candidates
    results = rerank(q, candidates, top_k=5)

    # Step 3: Get document filenames
    db = SessionLocal()

    try:
        document_ids = [result["document_id"] for result in results]

        documents = db.execute(
            select(models.Document).where(
                models.Document.id.in_(document_ids)
            )
        ).scalars().all()

        document_map = {
            document.id: document.filename
            for document in documents
        }

    finally:
        db.close()

    # Step 4: Build context for Gemini
    context_parts = []

    for result in results:
        filename = document_map.get(
            result["document_id"],
            "Unknown document"
        )

        context_parts.append(
            f"Source: {filename}, Page {result['page_number']}\n"
            f"{result['content']}"
        )

    context = "\n\n".join(context_parts)

    # Step 5: Generate answer
    answer = generate_answer(q, context)

    if "I couldn't find the answer in the provided documents." in answer:
        return {
            "question": q,
            "answer": answer,
            "sources": []
        }
    
    # Step 6: Return answer + useful citations
    return {
        "question": q,
        "answer": answer,
        "sources": [
            {
                "filename": document_map.get(
                    result["document_id"],
                    "Unknown document"
                ),
                "page_number": result["page_number"],
                "chunk_id": result["chunk_id"]
            }
            for result in results
        ]
    }
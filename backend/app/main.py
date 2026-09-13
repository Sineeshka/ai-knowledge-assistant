from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from sqlalchemy import text
from .database import Base, engine, SessionLocal
from . import models
from .pdf_parser import extract_text_from_pdf
from .chunker import chunk_text
from .search import search_similar_chunks, search_keyword_chunks, hybrid_search

app = FastAPI(title="AI Knowledge Assistant")

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


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    pages = extract_text_from_pdf(str(file_path))

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
            filename=file.filename,
            file_type=file.content_type
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        for chunk in all_chunks:
            document_chunk = models.DocumentChunk(
                document_id=document.id,
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                embedding=generate_embedding(chunk["content"])
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

@app.get("/search")
def search(q: str, top_k: int = 5):
    return search_similar_chunks(q, top_k)

@app.get("/keyword-search")
def keyword_search(q: str, top_k: int = 5):
    return search_keyword_chunks(q, top_k)

@app.get("/hybrid-search")
def hybrid_search_endpoint(q: str, top_k: int = 5):
    return hybrid_search(q, top_k)
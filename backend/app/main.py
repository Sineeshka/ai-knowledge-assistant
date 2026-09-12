from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from sqlalchemy import text
from .database import Base, engine, SessionLocal
from . import models

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

    db = SessionLocal()

    document = models.Document(
        filename=file.filename,
        file_type=file.content_type
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    db.close()

    return {
        "id": document.id,
        "filename": file.filename,
        "file_type": file.content_type,
        "message": "Document uploaded successfully"
    }
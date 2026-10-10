# AI Knowledge Assistant

An AI-powered document question-answering application that allows users to upload PDF documents and ask questions about their content using natural language.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant document content and generate context-aware answers using Google Gemini.

## Features

- Upload and process PDF documents.
- Extract text using PyMuPDF.
- Split document text into manageable chunks.
- Generate embeddings using Gemini.
- Store document data and embeddings in PostgreSQL with pgvector.
- Retrieve relevant document content using vector similarity search.
- Generate answers using Gemini based on retrieved context.
- React frontend with a FastAPI backend.

## Tech Stack

- **Frontend:** React, JavaScript, Vite
- **Backend:** Python, FastAPI
- **AI:** Google Gemini API and embeddings
- **Database:** PostgreSQL, pgvector
- **PDF Processing:** PyMuPDF
- **Tools:** Git, GitHub, Docker
- **Deployment:** Vercel, Render, Supabase

## Architecture

```text
React Frontend
      |
      v
FastAPI Backend
      |
      +------> PostgreSQL + pgvector
      |
      +------> Gemini API
```

## Screenshot

![AI Knowledge Assistant](screenshots)

*Document upload and question-answering interface.*

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL with pgvector
- Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/Sineeshka/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

### 2. Run the backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `backend/.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_connection_string
FRONTEND_URL=http://localhost:5173
```

Start the API:

```bash
uvicorn app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

### 3. Run the frontend

Open a second terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Open the local URL displayed in the terminal, usually `http://localhost:5173`.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/documents/upload` | Upload and process a PDF |
| GET | `/ask?q=your_question` | Ask a question about indexed documents |

## Future Improvements

- OCR support for scanned PDFs.
- Source-page citations in answers.
- Improved document management.
- Retrieval evaluation and answer-quality testing.

## Author

**Sineesh K A**  
B.Tech Computer Science and Engineering, Government Engineering College Thrissur

- [GitHub Profile](https://github.com/Sineeshka)
- [Project Repository](https://github.com/Sineeshka/ai-knowledge-assistant)

---

*Educational and portfolio project. Free-tier hosting and database services may pause or have usage limitations.*

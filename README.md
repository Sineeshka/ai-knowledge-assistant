# AI Knowledge Assistant

An AI-powered document question-answering system that allows users to upload documents and retrieve relevant information using hybrid search and reranking.

## Overview

AI Knowledge Assistant processes uploaded PDF documents, extracts and chunks their content, and retrieves relevant information when a user asks a question.

The system combines keyword-based retrieval and vector similarity search, then uses Reciprocal Rank Fusion (RRF) and reranking to improve the relevance of retrieved results.

## Features

- PDF document upload and processing
- Page-aware text extraction using PyMuPDF
- Document chunking for efficient retrieval
- Keyword-based and vector similarity search
- Hybrid retrieval using Reciprocal Rank Fusion (RRF)
- Result reranking for improved relevance
- PostgreSQL database for document and chunk storage
- pgvector for vector storage and similarity search
- FastAPI backend
- React frontend
- Docker-based PostgreSQL environment

## Deploying the backend on a small host

The backend uses Gemini for both answer generation and embeddings, so it does
not load PyTorch or local transformer models. This keeps the web service small
enough for low-memory hosts such as Render's free web service.

Create a Render Web Service with:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Set these environment variables in the service:

- `GEMINI_API_KEY`
- `DATABASE_URL` (a PostgreSQL database with the `vector` extension enabled)
- `FRONTEND_URL` (the deployed frontend URL)
- `GEMINI_MODEL` (optional, defaults to `gemini-3.6-flash`)
- `GEMINI_EMBEDDING_MODEL` (optional, defaults to `gemini-embedding-001`)

The embedding provider has changed from the local MiniLM model to Gemini. Any
existing chunks must be uploaded again, or their embeddings must be regenerated,
before using vector search. The database column remains 384-dimensional.

## Architecture

                    ┌─────────────────┐
                    │   User uploads  │
                    │    PDF document │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    PyMuPDF      │
                    │  Text Extraction│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Chunking &      │
                    │ Processing      │
                    └────────┬────────┘
                             │
                             ▼
                 ┌─────────────────────────┐
                 │ PostgreSQL + pgvector  │
                 │ Documents & Chunks      │
                 └────────────┬────────────┘
                              │
                     User Question
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Hybrid Retrieval        │
                 │ Keyword + Vector Search │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Reciprocal Rank Fusion  │
                 │          (RRF)           │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │       Reranking         │
                 └────────────┬────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Relevant Results│
                    └─────────────────┘

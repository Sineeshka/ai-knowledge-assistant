# ai-knowledge-assistant# AI Knowledge Assistant

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

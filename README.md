# DocChat — Retrieval-Augmented Document Question Answering System

## Overview

DocChat is a document-grounded question-answering system built with FastAPI, Streamlit, ChromaDB, LangChain, and Ollama.

Users can upload PDF documents, automatically index them into a vector database, and ask natural language questions about their contents.

The system retrieves relevant document chunks, rewrites follow-up questions into standalone queries, and generates grounded answers using local language models.

Unlike a basic chatbot, DocChat is designed around Retrieval-Augmented Generation (RAG) principles to reduce hallucinations and ensure answers remain tied to uploaded documents.

## Screenshot

*Add screenshots here.*

---

## Why this project exists

Most LLM chat applications answer questions using model knowledge alone.

This project was built to practice and understand:

* Document ingestion pipelines
* Vector databases
* Embedding models
* Semantic search
* Retrieval-Augmented Generation (RAG)
* FastAPI backend development
* API-driven frontend architecture
* LangChain orchestration
* Local LLM deployment using Ollama

The goal was to move beyond simple prompting and learn how production-style AI applications retrieve and ground information.

---

## Architecture

### High-Level Flow

1. User uploads a PDF document
2. PDF is stored locally
3. Document is parsed and split into chunks
4. Chunks are embedded using an embedding model
5. Embeddings are stored in ChromaDB
6. User submits a question
7. Follow-up questions are rewritten into standalone queries
8. Relevant chunks are retrieved from the vector database
9. Retrieved context is injected into a prompt
10. LLM generates a grounded answer
11. Sources are returned to the user for inspection

---

## Core Components

### 1) Document Upload Service

Handles:

* PDF validation
* Duplicate detection
* File storage
* Metadata tracking

Documents are registered in a manifest system and assigned a unique document ID.

---

### 2) Indexing Pipeline

Responsible for:

* Loading PDFs
* Extracting pages
* Splitting text into chunks
* Generating chunk metadata
* Storing embeddings in ChromaDB

Each chunk receives:

* Document ID
* Filename
* Chunk index
* Page number

---

### 3) Question Rewriter

Many user questions depend on previous conversation history.

Example:

User: What is DHCP?

User: Why is it useful?

The rewriter transforms follow-up questions into standalone questions before retrieval.

Example:

Why is DHCP useful?

This improves retrieval quality significantly.

---

### 4) Retriever

Performs semantic similarity search against ChromaDB.

Features:

* Document-level filtering
* Configurable top-k retrieval
* Chunk filtering
* Async retrieval pipeline

Only chunks relevant to the selected document are retrieved.

---

### 5) Prompt Builder

Constructs a grounded prompt using:

* Retrieved context
* Source metadata
* User question

The prompt enforces:

* Context-first answering
* No hallucinated information
* Explicit refusal when information is missing

---

### 6) Answer Generator

Uses a local Ollama model to:

* Consume retrieved context
* Generate grounded responses
* Return supporting citations

The model is instructed to answer only using retrieved evidence.

---

### 7) FastAPI Backend

Provides REST endpoints for:

#### Documents

* Upload document
* List documents
* View document details
* Delete document

#### Chat

* Submit questions
* Retrieve grounded answers

The backend is fully separated from the frontend.

---

### 8) Streamlit Frontend

Provides:

* Document library
* PDF upload interface
* Chat interface
* Retrieval debugging tools

The frontend communicates exclusively through the FastAPI API.

---

## Features

* PDF upload and storage
* Automatic document indexing
* Semantic search with embeddings
* ChromaDB vector database
* Follow-up question rewriting
* Retrieval-Augmented Generation (RAG)
* Grounded answer generation
* Source citations
* FastAPI REST backend
* Streamlit frontend
* Document management system
* Retrieval debugging view
* Local LLM execution with Ollama

---

## Tech Stack

### Backend

* FastAPI
* Pydantic
* Python

### RAG Pipeline

* LangChain
* ChromaDB
* Ollama
* EmbeddingGemma

### Frontend

* Streamlit

### Storage

* JSON Manifest Storage
* Local File Storage
* Chroma Vector Database

---

## Project Structure

| Path                  | Purpose                      |
| --------------------- | ---------------------------- |
| `app/api/`            | FastAPI endpoints            |
| `app/services/`       | Business logic               |
| `app/schema/`         | Request and response models  |
| `app/rag/`            | RAG pipeline components      |
| `app/storage/`        | File and vector storage      |
| `app/core/`           | Configuration and exceptions |
| `streamlit/pages/`    | User interface pages         |
| `streamlit/services/` | API communication layer      |
| `data/uploads/`       | Uploaded PDFs                |
| `data/chroma/`        | Vector database              |

---

## How To Run

### Prerequisites

* Python 3.10+
* Ollama
* ChromaDB

Required Ollama models:

* `embeddinggemma`
* `llama3.2:3b`
* `llama2:13b`

---

### 1) Clone Repository

```bash
git clone <your-repository-url>
cd docchat
```

### 2) Install Dependencies

```bash
pip install -r requirements.txt
```

### 3) Start Ollama

```bash
ollama serve

ollama pull embeddinggemma
ollama pull llama3.2:3b
ollama pull llama2:13b
```

### 4) Run FastAPI

```bash
uvicorn app.main:app --reload
```

### 5) Run Streamlit

```bash
streamlit run App.py
```

---

## Future Improvements

Planned improvements include:

* Hybrid Search (BM25 + Vector Search)
* Reranking
* PostgreSQL Metadata Storage
* User Authentication
* Multi-document Chat
* Streaming Responses
* Conversation Persistence
* Evaluation Pipeline
* Production Deployment

---

## What This Project Demonstrates

* Retrieval-Augmented Generation (RAG)
* FastAPI API Design
* Vector Database Integration
* LangChain Pipelines
* Semantic Search
* Local LLM Deployment
* Prompt Engineering
* Frontend / Backend Separation
* AI Application Architecture

This project was built as a learning-focused RAG system to explore the core concepts behind modern document-grounded AI applications.

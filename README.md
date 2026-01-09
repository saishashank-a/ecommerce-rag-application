# E-commerce RAG Application (Phase 1)

This project is a local implementation of a **Retrieval-Augmented Generation (RAG)** system for E-commerce product reviews.

It builds a searchable Vector Database from raw CSV data using:

* **ChromaDB**: For vector storage and retrieval.
* **Sentence-Transformers**: For generating semantic embeddings (`all-MiniLM-L6-v2`).
* **Pandas**: For data processing.

## Prerequisites

* Python 3.10+
* Amazon Reviews CSV file (e.g., `Reviews.csv`)

## Installation

1. Clone this repository.
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Start Support Services

Ensure **Ollama** is running and you have the model:

```bash
ollama serve
# In another terminal if needed:
ollama pull llama3.1:latest
```

### 2. Start Backend API

Open a terminal:

```bash
uvicorn backend.app.main:app --port 8000
```

### 3. Start Frontend UI

Open a **new** terminal:

```bash
streamlit run frontend/app.py
```

### 4. Interact

Open your browser (usually `http://localhost:8501`).

* **Search**: Find products.
* **Chat**: Ask questions about your products.

## Project Structure

* `ingest.py`: Script to load data into the vector database.
* `query.py`: Script to search the vector database.
* `requirements.txt`: Python dependencies.
* `chroma_db/`: (Created after ingestion) The local database folder.

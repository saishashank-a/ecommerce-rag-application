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

### 1. Ingest Data

Reads the CSV, converts text to vectors, and saves them locally in `./chroma_db`.

1. Open `ingest.py` and verify `CSV_PATH` points to your `Reviews.csv`.
2. Run the script:

    ```bash
    python3 ingest.py
    ```

### 2. Search Products

Search the database using natural language (e.g., "dog food" or "yummy candy").

```bash
python3 query.py
```

Type `exit` to quit the search loop.

## Project Structure

* `ingest.py`: Script to load data into the vector database.
* `query.py`: Script to search the vector database.
* `requirements.txt`: Python dependencies.
* `chroma_db/`: (Created after ingestion) The local database folder.

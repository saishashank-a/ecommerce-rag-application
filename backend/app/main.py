from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import os

app = FastAPI(title="Ecommerce RAG API")

# Configuration
# We assume this app is run from the project root
DB_PATH = "./chroma_db"
COLLECTION_NAME = "amazon_reviews"

# Initialize ChromaDB Client
# We do this globally so we don't reconnect on every request
print(f"Connecting to ChromaDB at {DB_PATH}...")
client = chromadb.PersistentClient(path=DB_PATH)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)

class SearchRequest(BaseModel):
    query: str
    k: int = 3

@app.get("/")
def read_root():
    return {"status": "ok", "message": "E-commerce RAG API is running"}

import ollama

@app.post("/search")
def search_products(request: SearchRequest):
    """
    Semantic search for products based on user query.
    """
    try:
        results = collection.query(
            query_texts=[request.query],
            n_results=request.k
        )
        
        # Format results for cleaner JSON response
        formatted_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                formatted_results.append({
                    "product_id": meta['ProductId'],
                    "score": meta['Score'],
                    "summary": meta['Summary'],
                    "review_snippet": doc[:500]  # Increased snippet size for context
                })
        
        return {"query": request.query, "results": formatted_results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_with_products(request: ChatRequest):
    """
    RAG Endpoint: Search + Generate Answer using Ollama.
    """
    try:
        # 1. Retrieval
        search_res = search_products(SearchRequest(query=request.query, k=3))
        results = search_res["results"]
        
        if not results:
            return {"answer": "I couldn't find any relevant products in the database.", "context": []}

        # 2. Augmented Prompt Construction
        context_str = "\n\n".join([
            f"Product: {r['summary']}\nReview: {r['review_snippet']}" 
            for r in results
        ])
        
        messages = [
            {"role": "system", "content": "You are a helpful E-commerce assistant. Answer the user's question using ONLY the context provided below. If you don't know, say so."},
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {request.query}"}
        ]
        
        # 3. Generation (Ollama)
        # Using llama3.1:latest as verified
        # Use env var for K8s support (host.docker.internal), default to localhost
        ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        client = ollama.Client(host=ollama_host)
        response = client.chat(model='llama3.1:latest', messages=messages)
        answer = response['message']['content']
        
        return {
            "query": request.query,
            "answer": answer,
            "context": results
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

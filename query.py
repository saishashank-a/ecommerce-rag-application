import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "./chroma_db"
COLLECTION_NAME = "amazon_reviews"

def query_db():
    print(f"Connecting to ChromaDB at {DB_PATH}...")
    client = chromadb.PersistentClient(path=DB_PATH)
    
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)
    
    print("\n--- Product Search (Type 'exit' to quit) ---")
    
    while True:
        query_text = input("\nEnter search query (e.g., 'dog food quality'): ")
        if query_text.lower() == 'exit':
            break
            
        print(f"Searching for: '{query_text}'...")
        
        results = collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        print(f"\nFound {len(results['documents'][0])} matches:\n")
        
        for i, doc in enumerate(results['documents'][0]):
            meta = results['metadatas'][0][i]
            print(f"[Match {i+1}] Score: {meta['Score']}/5 - ProductID: {meta['ProductId']}")
            print(f"Summary: {meta['Summary']}")
            print(f"Content Preview: {doc[:150]}...") # Show first 150 chars
            print("-" * 50)

if __name__ == "__main__":
    query_db()

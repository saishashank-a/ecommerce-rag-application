import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os

# Configuration
CSV_PATH = "/Users/saishashankanchuri/Downloads/Reviews.csv"
DB_PATH = "./chroma_db"
COLLECTION_NAME = "amazon_reviews"
SAMPLE_SIZE = 1000  # Process first 1000 rows for speed

def ingest_data():
    print(f"Loading data from {CSV_PATH}...")
    # Load limited rows
    df = pd.read_csv(CSV_PATH, nrows=SAMPLE_SIZE)
    
    # Fill NaN values to avoid errors
    df['Summary'] = df['Summary'].fillna("")
    df['Text'] = df['Text'].fillna("")
    
    print("Preparing documents...")
    documents = []
    metadatas = []
    ids = []
    
    for index, row in df.iterrows():
        # Create a rich representation for the vector search
        # We combine Summary and Text to catch matches in both
        doc_text = f"Subject: {row['Summary']}\nReview: {row['Text']}"
        documents.append(doc_text)
        
        # Store useful metadata for filtering/display
        metadatas.append({
            "ProductId": row['ProductId'],
            "Score": row['Score'],
            "Summary": row['Summary'],
            "UserId": row['UserId']
        })
        
        ids.append(f"rev_{index}")

    print(f"Initializing ChromaDB at {DB_PATH}...")
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Use default embedding function (all-MiniLM-L6-v2)
    # This automatically downloads the model if needed
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )
    
    print(f"Adding {len(documents)} documents to collection '{COLLECTION_NAME}'...")
    # Upsert helps avoid duplicates if run multiple times
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("Ingestion complete!")
    print(f"Count in collection: {collection.count()}")

if __name__ == "__main__":
    ingest_data()

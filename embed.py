import chromadb
from sentence_transformers import SentenceTransformer
from chunk import chunk_documents
from ingest import load_documents

COLLECTION_NAME = "professor_reviews"

def build_vector_store():
    # Load and chunk documents
    docs = load_documents()
    chunks = chunk_documents(docs)
    
    # Initialize embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it already exists (fresh rebuild)
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing collection.")
    except:
        pass
    
    collection = client.create_collection(COLLECTION_NAME)
    
    # Embed and store chunks
    print(f"Embedding {len(chunks)} chunks...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks]
    )
    
    print(f"\nStored {collection.count()} chunks in ChromaDB.")
    return collection, model

def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    return results

if __name__ == "__main__":
    collection, model = build_vector_store()
    
    # Test retrieval
    test_query = "What do students say about exams?"
    print(f"\nTest query: '{test_query}'")
    results = retrieve(test_query, collection, model)
    
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"\nResult {i+1} | Source: {meta['source']} | Distance: {dist:.3f}")
        print(doc[:200])
        print("-" * 40)
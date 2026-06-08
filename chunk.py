from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingest import load_documents

def chunk_documents(documents, chunk_size=600, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            # Filter out chunks that are pure metadata with no review opinion
            if is_meaningful(chunk):
                all_chunks.append({
                    "text": chunk,
                    "source": doc["source"],
                    "chunk_index": i
                })
    
    return all_chunks

def is_meaningful(chunk):
    # Must be at least 100 chars
    if len(chunk.strip()) < 100:
        return False
    # Must contain at least one word longer than 5 chars (filters pure metadata)
    words = chunk.split()
    long_words = [w for w in words if len(w) > 5]
    if len(long_words) < 3:
        return False
    return True

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    
    print(f"\nTotal chunks: {len(chunks)}")
    print("\n--- Sample chunks ---")
    for chunk in chunks[:5]:
        print(f"\nSource: {chunk['source']} | Chunk {chunk['chunk_index']}")
        print(chunk['text'])
        print("-" * 40)
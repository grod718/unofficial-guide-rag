import os
from dotenv import load_dotenv
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

COLLECTION_NAME = "professor_reviews"

def load_retriever():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection(COLLECTION_NAME)
    return collection, model

def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    return results

def build_context(results):
    context_parts = []
    sources = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context_parts.append(f"[Source: {meta['source']}]\n{doc}")
        if meta["source"] not in sources:
            sources.append(meta["source"])
    return "\n\n".join(context_parts), sources

def ask(question):
    collection, model = load_retriever()
    results = retrieve(question, collection, model)
    context, sources = build_context(results)
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""You are a helpful assistant that answers questions about professors 
at New York City College of Technology based only on student reviews.

Answer the question using ONLY the information in the provided reviews below.
If the reviews do not contain enough information to answer the question, 
say exactly: "I don't have enough information on that based on the available reviews."
Do not use any outside knowledge. Always refer to specific details from the reviews.

Student Reviews:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    answer = response.choices[0].message.content
    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    questions = [
        "What do students say about Warren Franklin's exams?",
        "Is Deodat Sharma recommended for CST students?",
    ]
    
    for q in questions:
        print(f"\nQuestion: {q}")
        result = ask(q)
        print(f"\nAnswer: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print("=" * 60)
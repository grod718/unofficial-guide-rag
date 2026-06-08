import os

DOCUMENTS_DIR = "documents"

def load_documents():
    documents = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()
            cleaned = clean_text(raw_text)
            documents.append({
                "source": filename,
                "text": cleaned
            })
            print(f"Loaded: {filename} ({len(cleaned)} chars)")
    return documents

def clean_text(text):
    import re
    # Remove extra whitespace and blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

if __name__ == "__main__":
    docs = load_documents()
    print(f"\nTotal documents loaded: {len(docs)}")
    for doc in docs:
        print(f"\n--- {doc['source']} ---")
        print(doc['text'][:300])
        print("...")
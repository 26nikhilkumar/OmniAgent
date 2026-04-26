from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.rag.ingestion import chunk_documents, load_text_documents


if __name__ == "__main__":
    docs = load_text_documents(["README.md"])
    chunks = chunk_documents(docs)
    print(f"loaded_docs={len(docs)} chunks={len(chunks)}")

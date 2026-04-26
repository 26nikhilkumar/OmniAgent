from pathlib import Path


def load_text_documents(paths: list[str]) -> list[str]:
    docs: list[str] = []
    for p in paths:
        file_path = Path(p)
        if file_path.exists() and file_path.is_file():
            docs.append(file_path.read_text(encoding="utf-8", errors="ignore"))
    return docs


def chunk_documents(docs: list[str], chunk_size: int = 800, overlap: int = 120) -> list[str]:
    chunks: list[str] = []
    for doc in docs:
        start = 0
        while start < len(doc):
            end = start + chunk_size
            chunks.append(doc[start:end])
            start += max(1, chunk_size - overlap)
    return chunks

class InMemoryVectorStore:
    """Simple in-memory vector-ish store using token overlap proxy.

    Intended as a local fallback before swapping to Chroma/pgvector.
    """

    def __init__(self) -> None:
        self._docs: list[str] = []

    def add(self, docs: list[str]) -> None:
        self._docs.extend(docs)

    def query(self, query: str, k: int = 3) -> list[str]:
        q = set(query.lower().split())
        ranked = sorted(
            self._docs,
            key=lambda d: len(set(d.lower().split()).intersection(q)),
            reverse=True,
        )
        return ranked[:k]

from collections import defaultdict

from rank_bm25 import BM25Okapi


class HybridRetriever:
    def __init__(self) -> None:
        self.documents: list[str] = []
        self.bm25: BM25Okapi | None = None

    def add_documents(self, docs: list[str]) -> None:
        self.documents = docs
        tokenized = [d.lower().split() for d in docs]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, k: int = 3, alpha: float = 0.5) -> list[dict[str, float | str]]:
        if not self.bm25:
            return []
        query_tokens = query.lower().split()
        bm25_scores = self.bm25.get_scores(query_tokens)

        dense_scores = [self._dense_overlap_score(doc, query_tokens) for doc in self.documents]

        combined = defaultdict(float)
        for idx, score in enumerate(bm25_scores):
            combined[idx] += (1 - alpha) * float(score)
        for idx, score in enumerate(dense_scores):
            combined[idx] += alpha * float(score)

        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:k]
        return [{"document": self.documents[i], "score": score} for i, score in ranked]

    @staticmethod
    def _dense_overlap_score(doc: str, query_tokens: list[str]) -> float:
        doc_tokens = set(doc.lower().split())
        if not doc_tokens:
            return 0.0
        overlap = len(doc_tokens.intersection(query_tokens))
        return overlap / len(doc_tokens)

from collections import defaultdict

from rank_bm25 import BM25Okapi


class HybridRetriever:
    def __init__(self) -> None:
        self.documents: list[str] = []
        self.bm25: BM25Okapi | None = None
        self.chroma = None
        self.embedder = None
        self.reranker = None

        try:
            import chromadb
            from sentence_transformers import CrossEncoder, SentenceTransformer

            self._chromadb = chromadb
            self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
            self.chroma = chromadb.Client().create_collection(name="omniagent")
        except Exception:
            self._chromadb = None

    def add_documents(self, docs: list[str]) -> None:
        self.documents = docs
        tokenized = [d.lower().split() for d in docs]
        self.bm25 = BM25Okapi(tokenized)

        if self.chroma and self.embedder:
            embeddings = self.embedder.encode(docs).tolist()
            self.chroma.add(
                ids=[str(i) for i in range(len(docs))],
                documents=docs,
                embeddings=embeddings,
            )

    def search(self, query: str, k: int = 5, alpha: float = 0.5) -> list[dict[str, float | str]]:
        if not self.bm25:
            return []
        query_tokens = query.lower().split()
        bm25_scores = self.bm25.get_scores(query_tokens)

        dense_scores = [0.0 for _ in self.documents]
        if self.chroma and self.embedder:
            q_emb = self.embedder.encode([query]).tolist()[0]
            response = self.chroma.query(query_embeddings=[q_emb], n_results=min(k, len(self.documents)))
            for doc, dist in zip(response.get("documents", [[]])[0], response.get("distances", [[]])[0]):
                idx = self.documents.index(doc)
                dense_scores[idx] = max(0.0, 1.0 - float(dist))
        else:
            dense_scores = [self._dense_overlap_score(doc, query_tokens) for doc in self.documents]

        combined = defaultdict(float)
        for idx, score in enumerate(bm25_scores):
            combined[idx] += (1 - alpha) * float(score)
        for idx, score in enumerate(dense_scores):
            combined[idx] += alpha * float(score)

        ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)[: k * 2]
        docs = [self.documents[i] for i, _ in ranked]

        if self.reranker:
            pairs = [(query, d) for d in docs]
            reranked_scores = self.reranker.predict(pairs)
            rescored = sorted(zip(docs, reranked_scores), key=lambda x: x[1], reverse=True)[:k]
            return [{"document": d, "score": float(s)} for d, s in rescored]

        return [{"document": self.documents[i], "score": score} for i, score in ranked[:k]]

    @staticmethod
    def _dense_overlap_score(doc: str, query_tokens: list[str]) -> float:
        doc_tokens = set(doc.lower().split())
        if not doc_tokens:
            return 0.0
        overlap = len(doc_tokens.intersection(query_tokens))
        return overlap / len(doc_tokens)

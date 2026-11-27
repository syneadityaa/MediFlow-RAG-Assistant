"""Step 5 and 8: store vectors in FAISS and search them."""
import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks: list[dict] = []

    def build(self, chunks: list[dict], embeddings: np.ndarray) -> None:
        if not chunks:
            raise ValueError("No chunks to index.")
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must have the same length.")
        vectors = np.ascontiguousarray(embeddings, dtype="float32")
        self.index = faiss.IndexFlatIP(vectors.shape[1])  # exact inner-product search
        self.index.add(vectors)
        self.chunks = list(chunks)

    def search(self, query_vector: np.ndarray, k: int = 4) -> list[dict]:
        """Return the top-k chunks, each with a 'score' (cosine similarity, higher = closer)."""
        if self.index is None or not self.chunks:
            return []
        query = np.ascontiguousarray(query_vector.reshape(1, -1), dtype="float32")
        scores, ids = self.index.search(query, min(k, len(self.chunks)))
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue
            item = dict(self.chunks[idx])
            item["score"] = float(score)
            results.append(item)
        return results
"""Step 4 and 7: turn text into vectors with Sentence Transformers (free, runs locally)."""
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def embed(self, texts) -> np.ndarray:
        """Return a float32 array (n, dim). Vectors are normalized, so inner product = cosine similarity."""
        vectors = self.model.encode(
            list(texts),
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.ascontiguousarray(vectors, dtype="float32")
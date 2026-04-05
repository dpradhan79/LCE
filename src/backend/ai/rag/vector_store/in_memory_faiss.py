from typing import List, Dict, Any

import faiss
from sentence_transformers import SentenceTransformer


class InMemoryFAISS:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.documents = []

    def build_index(self, chunks: List[Dict[str, Any]]):
        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.documents = chunks

    def query(self, query_text: str, top_k: int = 5):
        query_embedding = self.model.encode(
            [query_text],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.documents[idx])

        return results

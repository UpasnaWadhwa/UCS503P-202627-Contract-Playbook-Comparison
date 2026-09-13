import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from common.schemas import Chunk
from common.config import EMBEDDING_MODEL

class EmbeddingIndex:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.chunks = []
        
    def build_index(self, chunks: List[Chunk]):
        self.chunks = chunks
        if not chunks:
            return
            
        texts = [c.text for c in chunks]
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        
        dimension = embeddings.shape[1]
        # IndexFlatIP with normalized embeddings is equivalent to cosine similarity
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(np.array(embeddings).astype("float32"))
        
    def query(self, query_text: str, top_k: int = 3) -> List[tuple[Chunk, float]]:
        if not self.chunks or self.index is None:
            return []
            
        query_emb = self.model.encode([query_text], normalize_embeddings=True)
        distances, indices = self.index.search(np.array(query_emb).astype("float32"), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append((self.chunks[idx], float(distances[0][i])))
                
        return results

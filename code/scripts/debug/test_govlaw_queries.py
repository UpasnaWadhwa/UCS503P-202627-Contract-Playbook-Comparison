from sentence_transformers import SentenceTransformer
import numpy as np
from ingestion.loaders import load_synthetic_dataset
from ingestion.chunking import chunk_text
from ingestion.embedding_index import EmbeddingIndex

contracts, playbook, gt = load_synthetic_dataset()
cid = "contract_06"
chunks = chunk_text(contracts[cid], cid)
index = EmbeddingIndex()
index.build_index(chunks)

queries_to_try = [
    "This agreement shall be governed by the laws of the jurisdiction.",
    "governing law jurisdiction state country applicable law",
    "Governing Law. This Agreement shall be governed by and construed in accordance with the laws of",
]

for q in queries_to_try:
    results = index.query(q, top_k=1)
    print(repr(q))
    print("  ->", round(results[0][1], 3), repr(results[0][0].text[:90]))
    print()

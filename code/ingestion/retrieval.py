from typing import List
from common.schemas import PlaybookClause, RetrievalResult, Chunk
from common.config import RETRIEVAL_TOP_K
from ingestion.chunking import chunk_text
from ingestion.embedding_index import EmbeddingIndex

def retrieve_all_clauses(contract_text: str, contract_id: str, playbook: List[PlaybookClause]) -> List[RetrievalResult]:
    """
    Chunk the contract, build an index, and retrieve top chunks for each playbook clause.
    """
    chunks = chunk_text(contract_text, contract_id)
    
    index = EmbeddingIndex()
    index.build_index(chunks)
    
    results = []
    for clause in playbook:
        top_chunks_with_scores = index.query(clause.query_text, top_k=RETRIEVAL_TOP_K)
        candidates = [chunk for chunk, score in top_chunks_with_scores]
        top_score = top_chunks_with_scores[0][1] if top_chunks_with_scores else 0.0
        
        results.append(RetrievalResult(
            clause_type=clause.clause_type,
            contract_id=contract_id,
            candidates=candidates,
            top_score=top_score
        ))
        
    return results

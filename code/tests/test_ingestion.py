import pytest
from common.schemas import PlaybookClause
from ingestion.chunking import chunk_text
from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses

def test_chunking():
    text = "Hello world. This is a test. We are chunking text."
    chunks = chunk_text(text, "test_1", chunk_size_chars=20, overlap_chars=5)
    assert len(chunks) > 1
    assert chunks[0].contract_id == "test_1"
    assert chunks[0].start_offset == 0
    assert chunks[0].text.startswith("Hello")

def test_retrieval_hit_rate():
    contracts, playbook, ground_truth = load_synthetic_dataset()
    
    # Just test the first contract
    cid = "contract_01"
    text = contracts[cid]
    gt = ground_truth[cid]
    
    results = retrieve_all_clauses(text, cid, playbook)
    
    for result in results:
        clause_type = result.clause_type
        gt_span = gt[clause_type].get("text_span")
        
        if gt_span:
            # Check if gt_span is in any of the retrieved chunks
            found = any(gt_span in candidate.text for candidate in result.candidates)
            assert found, f"Ground truth span for {clause_type} not found in top-k chunks"

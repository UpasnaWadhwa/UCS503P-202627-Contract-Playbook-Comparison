import json
import os
from common.config import SYNTHETIC_DATA_DIR
from common.schemas import PlaybookClause
from comparison.pipeline import run_pipeline

def evaluate():
    try:
        from ingestion.loaders import load_synthetic_dataset
        contracts, playbook, ground_truth = load_synthetic_dataset()
    except ImportError:
        print("Ingestion module not available. Cannot run evaluation.")
        return
        
    total_clauses = 0
    correct_verdicts = 0
    hit_rate_success = 0
    
    print(f"Evaluating on {len(contracts)} synthetic contracts...")
    
    for cid, text in contracts.items():
        report = run_pipeline(text, cid, playbook, use_llm=False)
        gt = ground_truth[cid]
        
        for result in report.results:
            clause_type = result.clause_type
            expected_verdict = gt[clause_type]["verdict"]
            expected_span = gt[clause_type].get("text_span")
            
            total_clauses += 1
            
            # 1. Verdict Agreement
            if result.verdict == expected_verdict:
                correct_verdicts += 1
                
            # 2. Retrieval Hit Rate (only meaningful if expected_span exists)
            if expected_span:
                # Note: Hit rate is slightly approximated here as we check if the citation contains the span or vice versa
                if result.citation_text and (expected_span in result.citation_text or result.citation_text in expected_span):
                    hit_rate_success += 1
            elif not expected_span and not result.citation_text:
                hit_rate_success += 1
                
    verdict_acc = correct_verdicts / total_clauses if total_clauses > 0 else 0
    hit_rate = hit_rate_success / total_clauses if total_clauses > 0 else 0
    
    print("\n--- Evaluation Results ---")
    print(f"Total Clauses Evaluated: {total_clauses}")
    print(f"Verdict Agreement: {verdict_acc:.2%}")
    print(f"Retrieval Hit-Rate: {hit_rate:.2%}")

if __name__ == "__main__":
    evaluate()

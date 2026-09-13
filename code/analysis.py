import os
import json
import numpy as np
from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses

def analyze_scores():
    contracts, playbook, ground_truth = load_synthetic_dataset()
    
    scores = {
        "MATCH/DEVIATION": [],
        "MISSING": []
    }
    
    for cid, text in contracts.items():
        retrieval_results = retrieve_all_clauses(text, cid, playbook)
        gt = ground_truth[cid]
        
        for result in retrieval_results:
            clause_type = result.clause_type
            expected_verdict = gt[clause_type]["verdict"]
            top_score = result.top_score
            
            if expected_verdict in ["MATCH", "DEVIATION"]:
                scores["MATCH/DEVIATION"].append(top_score)
            elif expected_verdict == "MISSING":
                scores["MISSING"].append(top_score)
                if top_score > 0.5:
                    print(f"HIGH MISSING SCORE ({top_score:.3f}): {cid} - {clause_type} matched chunk: '{result.candidates[0].text}'")
                
    print("=== Retrieval Score Distribution ===")
    for group, vals in scores.items():
        if not vals:
            print(f"{group}: No data")
            continue
        print(f"{group}: N={len(vals)}, Min={min(vals):.3f}, Max={max(vals):.3f}, Avg={np.mean(vals):.3f}")

if __name__ == "__main__":
    analyze_scores()

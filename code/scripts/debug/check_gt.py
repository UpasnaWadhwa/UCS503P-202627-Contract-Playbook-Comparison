import sys
from ingestion.loaders import load_synthetic_dataset

def verify_ground_truth():
    contracts, _, ground_truth = load_synthetic_dataset()
    all_ok = True
    print("=== Ground Truth Verbatim Verification ===")
    
    for cid, text in contracts.items():
        gt = ground_truth[cid]
        for clause, data in gt.items():
            span = data.get("text_span")
            if span and span not in text:
                print(f"ERROR: {cid} - {clause} span not found verbatim!")
                print(f"  Expected span: '{span}'")
                all_ok = False
                
    if all_ok:
        print("All ground truth spans found verbatim in contracts.")
    return all_ok

if __name__ == "__main__":
    success = verify_ground_truth()
    sys.exit(0 if success else 1)

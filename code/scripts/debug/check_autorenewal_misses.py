from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses

contracts, playbook, gt = load_synthetic_dataset()

for cid in contracts:
    span = gt[cid]['Auto-Renewal'].get('text_span')
    if span is None:
        continue
    results = retrieve_all_clauses(contracts[cid], cid, playbook)
    r = [x for x in results if x.clause_type == 'Auto-Renewal'][0]
    found = any(span in c.text for c in r.candidates)
    if not found:
        print(f"--- MISS: {cid} ---")
        print("Ground truth span:", repr(span))
        print("Top candidate instead:", repr(r.candidates[0].text[:100]))
        print()

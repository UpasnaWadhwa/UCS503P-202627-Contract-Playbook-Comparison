from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses

contracts, playbook, gt = load_synthetic_dataset()

for cid in contracts:
    span = gt[cid]['Governing Law'].get('text_span')
    if span is None:
        continue
    results = retrieve_all_clauses(contracts[cid], cid, playbook)
    r = [x for x in results if x.clause_type == 'Governing Law'][0]
    found_rank1 = span in r.candidates[0].text
    if not found_rank1:
        print(f"--- {cid}: rank-1 wrong ---")
        print("Ground truth span:", repr(span))
        print("Rank-1 instead:", repr(r.candidates[0].text[:100]))
        print()

from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses

contracts, playbook, gt = load_synthetic_dataset()
gov_query = [p for p in playbook if p.clause_type == 'Governing Law'][0]

for cid in ['contract_06', 'contract_07']:
    results = retrieve_all_clauses(contracts[cid], cid, playbook)
    r = [x for x in results if x.clause_type == 'Governing Law'][0]
    print(f"--- {cid} ---")
    for c in r.candidates:
        print(round(r.top_score, 3) if c is r.candidates[0] else "", repr(c.text[:100]))
    print()

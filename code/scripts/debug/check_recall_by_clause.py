from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses
from collections import defaultdict

contracts, playbook, gt = load_synthetic_dataset()
stats = defaultdict(lambda: {'total': 0, 'rank1': 0, 'top3': 0})

for cid in contracts:
    results = retrieve_all_clauses(contracts[cid], cid, playbook)
    for r in results:
        span = gt[cid][r.clause_type].get('text_span')
        if span is None:
            continue
        s = stats[r.clause_type]
        s['total'] += 1
        cand_texts = [c.text for c in r.candidates]
        if span in cand_texts[0]:
            s['rank1'] += 1
            s['top3'] += 1
        elif any(span in t for t in cand_texts):
            s['top3'] += 1

for clause, s in stats.items():
    r1_pct = s['rank1'] / s['total']
    r3_pct = s['top3'] / s['total']
    print(clause.ljust(20), "Recall@1=", s['rank1'], "/", s['total'], f"({r1_pct:.0%})",
          "  Recall@3=", s['top3'], "/", s['total'], f"({r3_pct:.0%})")
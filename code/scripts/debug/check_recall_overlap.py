from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses
from collections import defaultdict

def overlap_ratio(span, chunk_text):
    span_words = set(span.lower().split())
    chunk_words = set(chunk_text.lower().split())
    if not span_words:
        return 0
    return len(span_words & chunk_words) / len(span_words)

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
        if overlap_ratio(span, cand_texts[0]) >= 0.7:
            s['rank1'] += 1
            s['top3'] += 1
        elif any(overlap_ratio(span, t) >= 0.7 for t in cand_texts):
            s['top3'] += 1

for clause, s in stats.items():
    print(clause.ljust(20), "Recall@1=", s['rank1'], "/", s['total'], f"({s['rank1']/s['total']:.0%})",
          "  Recall@3=", s['top3'], "/", s['total'], f"({s['top3']/s['total']:.0%})")

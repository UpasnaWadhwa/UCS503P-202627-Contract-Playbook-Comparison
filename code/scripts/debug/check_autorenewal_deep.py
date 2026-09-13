from ingestion.loaders import load_synthetic_dataset
from ingestion.retrieval import retrieve_all_clauses

def overlap_ratio(span, chunk_text):
    span_words = set(span.lower().split())
    chunk_words = set(chunk_text.lower().split())
    if not span_words:
        return 0
    return len(span_words & chunk_words) / len(span_words)

contracts, playbook, gt = load_synthetic_dataset()

for cid in contracts:
    span = gt[cid]['Auto-Renewal'].get('text_span')
    if span is None:
        continue
    results = retrieve_all_clauses(contracts[cid], cid, playbook)
    r = [x for x in results if x.clause_type == 'Auto-Renewal'][0]
    ratios = [round(overlap_ratio(span, c.text), 2) for c in r.candidates]
    if max(ratios) < 0.7:
        print(f"--- MISS: {cid} (best overlap={max(ratios)}) ---")
        print("Ground truth:", repr(span))
        for c, ratio in zip(r.candidates, ratios):
            print(f"  [{ratio}]", repr(c.text[:100]))
        print()

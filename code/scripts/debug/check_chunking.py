import sys
import json
import os
from ingestion.loaders import load_synthetic_dataset
from ingestion.chunking import chunk_text

try:
    contracts, playbook, gt = load_synthetic_dataset()
except ValueError:
    print("Failed to unpack load_synthetic_dataset (likely returns 2 instead of 3 values in some places?)")
    # Actually, load_synthetic_dataset returns contracts, playbook, ground_truth as defined earlier.
    import ingestion.loaders
    res = ingestion.loaders.load_synthetic_dataset()
    print("Return length:", len(res))
    contracts, playbook, gt = res

print("Total contracts:", len(contracts))

for cid, text in contracts.items():
    chunks = chunk_text(text, cid)
    offsets_ok = all(text[c.start_offset:c.end_offset] == c.text for c in chunks)
    print(f"{cid} chunks: {len(chunks)} offsets_ok: {offsets_ok}")

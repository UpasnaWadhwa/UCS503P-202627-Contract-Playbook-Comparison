import sys
from ingestion.loaders import load_synthetic_dataset
from ingestion.chunking import chunk_text

def verify_offsets():
    contracts, _, _ = load_synthetic_dataset()
    all_ok = True
    print("=== Chunk Offset Verification ===")
    for cid, text in contracts.items():
        chunks = chunk_text(text, cid)
        offsets_ok = all(text[c.start_offset:c.end_offset] == c.text for c in chunks)
        print(f"{cid}: {len(chunks)} chunks, offsets OK: {offsets_ok}")
        if not offsets_ok:
            all_ok = False
            for c in chunks:
                if text[c.start_offset:c.end_offset] != c.text:
                    print(f"  Mismatch in chunk {c.chunk_id}: '{c.text}' != '{text[c.start_offset:c.end_offset]}'")
    return all_ok

if __name__ == "__main__":
    success = verify_offsets()
    sys.exit(0 if success else 1)

import sys
from sentence_transformers import SentenceTransformer
import torch
import torch.nn.functional as F

def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Contract clause from generate.py
    clause_text = "Either party may terminate this agreement upon 30 days prior written notice."
    
    # Queries
    bad_query = "The contract contains a termination clause"
    good_query = "Either party may terminate this agreement"
    
    # Get embeddings
    embeddings = model.encode([clause_text, bad_query, good_query], convert_to_tensor=True)
    clause_emb = embeddings[0]
    bad_emb = embeddings[1]
    good_emb = embeddings[2]
    
    # Compute similarity
    score_bad = F.cosine_similarity(clause_emb.unsqueeze(0), bad_emb.unsqueeze(0)).item()
    score_good = F.cosine_similarity(clause_emb.unsqueeze(0), good_emb.unsqueeze(0)).item()
    
    print(f"Target Clause: '{clause_text}'")
    print(f"Bad Query: '{bad_query}' -> Score: {score_bad:.4f}")
    print(f"Good Query: '{good_query}' -> Score: {score_good:.4f}")

if __name__ == "__main__":
    main()

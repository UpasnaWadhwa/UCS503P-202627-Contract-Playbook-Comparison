import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNTHETIC_DATA_DIR = os.path.join(BASE_DIR, "data", "synthetic")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Data Source Switch ("synthetic" or "cuad")
DATA_SOURCE = "synthetic"

# Embedding settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE_TOKENS = 50
CHUNK_OVERLAP_RATIO = 0.2
RETRIEVAL_TOP_K = 3
SIMILARITY_THRESHOLD = 0.35  # Set empirically to err on side of MATCH/DEVIATION

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

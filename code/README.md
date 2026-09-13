# Contract Playbook Comparison System

This is the Stage 1 Proof of Concept for a retrieval-augmented pipeline that compares an incoming contract against an internal legal "playbook". It reports whether clauses Match, Deviate, or are Missing, with citations to the exact text.

## Features (Stage 1 PoC)
- **CPU-Only**: Uses `sentence-transformers` and `faiss-cpu` for efficient local execution.
- **Rule-Based Fallback**: Works with zero external API access using keyword/number heuristics.
- **Reporting**: Generates tabular CSV and color-coded PDF reports.
- **Interactive UI**: Includes a Streamlit app for uploading contracts and viewing results interactively.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI
Run the full pipeline on a specific contract:
```bash
python main.py --contract data/synthetic/contracts/contract_01.txt
```
This generates a CSV and PDF report in the `output/` directory.

### Streamlit App
Run the interactive web app:
```bash
streamlit run reporting/app.py
```

### Evaluation
Evaluate the pipeline against the synthetic ground truth:
```bash
python -m comparison.evaluation
```

## Stage 2: Moving off Synthetic Data
To swap from the synthetic dataset to a real dataset like CUAD, only minor changes are needed thanks to the pluggable architecture:
1. In `common/config.py`, change `DATA_SOURCE = "synthetic"` to `"cuad"`.
2. In `ingestion/loaders.py`, implement the `load_cuad_dataset()` function to parse the CUAD schema into our standard `PlaybookClause` and `Chunk` objects.
3. No downstream code in comparison or reporting needs to change.

import os
import json
from typing import List, Tuple, Dict
from common.schemas import PlaybookClause
from common.config import SYNTHETIC_DATA_DIR
from ingestion.pdf_parser import extract_text

def load_synthetic_dataset() -> Tuple[Dict[str, str], List[PlaybookClause], Dict[str, dict]]:
    """
    Loads the synthetic playbook and contracts.
    Returns:
        contracts: dict of contract_id to raw_text
        playbook: list of PlaybookClause objects
        ground_truth: dict mapping contract_id to ground truth annotations
    """
    with open(os.path.join(SYNTHETIC_DATA_DIR, "playbook.json"), "r") as f:
        playbook_data = json.load(f)
        playbook = [PlaybookClause(**c) for c in playbook_data]
        
    contracts = {}
    contracts_dir = os.path.join(SYNTHETIC_DATA_DIR, "contracts")
    for filename in os.listdir(contracts_dir):
        if filename.endswith(".txt"):
            contract_id = filename.replace(".txt", "")
            file_path = os.path.join(contracts_dir, filename)
            contracts[contract_id] = extract_text(file_path)
            
    with open(os.path.join(SYNTHETIC_DATA_DIR, "ground_truth.json"), "r") as f:
        ground_truth = json.load(f)
        
    return contracts, playbook, ground_truth

def load_cuad_dataset():
    """Stub for Stage 2."""
    raise NotImplementedError("Stage 2")

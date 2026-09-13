import argparse
import os
import json
from common.config import OUTPUT_DIR, SYNTHETIC_DATA_DIR
from common.schemas import PlaybookClause
from ingestion.pdf_parser import extract_text
from comparison.pipeline import run_pipeline
from reporting.csv_report import write_csv_report
from reporting.pdf_report import write_pdf_report

def main():
    parser = argparse.ArgumentParser(description="Contract Playbook Comparison System (Stage 1 PoC)")
    parser.add_argument("--contract", type=str, required=True, help="Path to the contract file (.txt or .pdf)")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM for comparison instead of rule fallback")
    args = parser.parse_args()

    contract_path = args.contract
    if not os.path.exists(contract_path):
        print(f"Error: Contract file not found at {contract_path}")
        return

    print(f"Loading contract from {contract_path}...")
    contract_text = extract_text(contract_path)
    contract_id = os.path.basename(contract_path).split('.')[0]

    print("Loading playbook...")
    with open(os.path.join(SYNTHETIC_DATA_DIR, "playbook.json"), "r") as f:
        playbook_data = json.load(f)
        playbook = [PlaybookClause(**c) for c in playbook_data]

    print("Running pipeline...")
    report = run_pipeline(contract_text, contract_id, playbook, use_llm=args.use_llm)

    print("Generating reports...")
    csv_path = os.path.join(OUTPUT_DIR, f"{contract_id}_report.csv")
    pdf_path = os.path.join(OUTPUT_DIR, f"{contract_id}_report.pdf")
    
    write_csv_report(report, csv_path)
    write_pdf_report(report, pdf_path)
    
    print("\n--- Pipeline Complete ---")
    print(f"CSV Report saved to: {csv_path}")
    print(f"PDF Report saved to: {pdf_path}")

if __name__ == "__main__":
    main()

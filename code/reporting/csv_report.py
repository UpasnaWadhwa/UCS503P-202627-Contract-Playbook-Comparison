import csv
from typing import List, Dict
from common.schemas import ContractReport
from reporting.report_builder import build_tabular_report

def write_csv_report(report: ContractReport, output_path: str):
    """
    Writes a ContractReport to a CSV file.
    """
    rows = build_tabular_report(report)
    if not rows:
        return
        
    fieldnames = ["Clause", "Status", "Explanation", "Citation"]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

from typing import List, Dict
from common.schemas import ContractReport

def build_tabular_report(report: ContractReport) -> List[Dict[str, str]]:
    """
    Formats a ContractReport into a simple tabular structure.
    Returns a list of dictionaries with columns: Clause, Status, Explanation, Citation.
    """
    rows = []
    for result in report.results:
        rows.append({
            "Clause": result.clause_type,
            "Status": result.verdict.value,
            "Explanation": result.explanation,
            "Citation": result.citation_text if result.citation_text else "N/A"
        })
    return rows

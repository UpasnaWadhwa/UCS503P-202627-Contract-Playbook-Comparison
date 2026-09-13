import pytest
from common.schemas import ContractReport, ClauseResult, ClauseVerdict
from reporting.report_builder import build_tabular_report

def test_build_tabular_report():
    report = ContractReport(
        contract_id="test",
        results=[
            ClauseResult(
                clause_type="Governing Law",
                contract_id="test",
                verdict=ClauseVerdict.MATCH,
                explanation="Matches.",
                citation_text="Delaware.",
                citation_offset=(0, 10)
            )
        ]
    )
    
    rows = build_tabular_report(report)
    assert len(rows) == 1
    assert rows[0]["Clause"] == "Governing Law"
    assert rows[0]["Status"] == "MATCH"
    assert rows[0]["Explanation"] == "Matches."
    assert rows[0]["Citation"] == "Delaware."

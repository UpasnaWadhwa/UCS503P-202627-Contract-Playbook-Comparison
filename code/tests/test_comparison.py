import pytest
from common.schemas import ClauseVerdict
from comparison.rule_fallback import compare_fallback

def test_rule_fallback_governing_law():
    chunk = "This agreement shall be governed by the laws of the State of Delaware."
    verdict, expl = compare_fallback("Governing Law", "Standard position", chunk)
    assert verdict == ClauseVerdict.MATCH
    
    chunk_dev = "This agreement shall be governed by the laws of California."
    verdict_dev, expl_dev = compare_fallback("Governing Law", "Standard position", chunk_dev)
    assert verdict_dev == ClauseVerdict.DEVIATION

def test_rule_fallback_termination():
    chunk = "Either party may terminate this agreement upon 30 days prior written notice."
    verdict, expl = compare_fallback("Termination Notice", "Standard", chunk)
    assert verdict == ClauseVerdict.MATCH
    
    chunk_dev = "Either party may terminate this agreement upon 90 days prior written notice."
    verdict_dev, expl_dev = compare_fallback("Termination Notice", "Standard", chunk_dev)
    assert verdict_dev == ClauseVerdict.DEVIATION

import re
from typing import Tuple
from common.schemas import ClauseVerdict

def compare_fallback(clause_type: str, standard_position: str, chunk_text: str) -> Tuple[ClauseVerdict, str]:
    """
    Keyword/number-based heuristic comparator for zero API access scenarios.
    """
    text_lower = chunk_text.lower()
    
    if clause_type == "Termination Notice":
        # Look for numbers
        numbers = re.findall(r'\b\d+\b', text_lower)
        if "30" in numbers:
            return ClauseVerdict.MATCH, "Found 30 days notice period matching standard position."
        elif numbers:
            return ClauseVerdict.DEVIATION, f"Found notice period(s) {', '.join(numbers)} which deviates from 30 days."
        else:
            return ClauseVerdict.DEVIATION, "Termination clause found but notice period unclear."
            
    elif clause_type == "Liability Cap":
        if "12 months" in text_lower or "twelve months" in text_lower:
            return ClauseVerdict.MATCH, "Found 12 months fee cap matching standard position."
        else:
            return ClauseVerdict.DEVIATION, "Liability cap found but does not match 12 months fee standard."
            
    elif clause_type == "Auto-Renewal":
        if "60 days" in text_lower and "written notice" in text_lower:
            return ClauseVerdict.MATCH, "Found 60 days notice requirement for non-renewal."
        else:
            return ClauseVerdict.DEVIATION, "Auto-renewal clause deviates from standard 60 days notice."
            
    elif clause_type == "Governing Law":
        if "delaware" in text_lower:
            return ClauseVerdict.MATCH, "Governing law is Delaware as per standard position."
        else:
            return ClauseVerdict.DEVIATION, "Governing law is not Delaware."
            
    # Default fallback
    return ClauseVerdict.DEVIATION, "Manual review required: rule fallback could not definitively classify."

from typing import Tuple
from common.schemas import ClauseVerdict

def compare_llm(clause_type: str, standard_position: str, chunk_text: str) -> Tuple[ClauseVerdict, str]:
    """
    LLM comparison function (stubbed for PoC).
    Receives ONLY the playbook's standard_position and the retrieved chunk text.
    Must return a ClauseVerdict + one-sentence explanation.
    """
    # For Stage 1 PoC without an API key, we will raise NotImplementedError or fallback.
    # In a real implementation, this would call an LLM API.
    raise NotImplementedError("LLM API not configured. Use rule_fallback instead.")

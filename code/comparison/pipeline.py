from typing import List, Optional
from common.schemas import ContractReport, PlaybookClause, ClauseResult, ClauseVerdict, RetrievalResult
from common.config import SIMILARITY_THRESHOLD
from comparison.rule_fallback import compare_fallback
from comparison.llm_comparison import compare_llm

def run_pipeline(contract_text: str, contract_id: str, playbook: List[PlaybookClause], use_llm: bool = False) -> ContractReport:
    """
    Orchestration function.
    Calls ingestion's retrieval, applies SIMILARITY_THRESHOLD, then calls comparator.
    Note: For branch isolation before merging, we dynamically import retrieval here or stub it if not available.
    """
    try:
        from ingestion.retrieval import retrieve_all_clauses
        retrieval_results = retrieve_all_clauses(contract_text, contract_id, playbook)
    except ImportError:
        # Stub for isolated testing if ingestion is not available
        retrieval_results = []
        
    results = []
    
    for clause, retrieval_result in zip(playbook, retrieval_results):
        if retrieval_result.top_score < SIMILARITY_THRESHOLD:
            results.append(ClauseResult(
                clause_type=clause.clause_type,
                contract_id=contract_id,
                verdict=ClauseVerdict.MISSING,
                explanation=f"No relevant text found (top score {retrieval_result.top_score:.2f} < {SIMILARITY_THRESHOLD}).",
                citation_text=None,
                citation_offset=None
            ))
            continue
            
        top_chunk = retrieval_result.candidates[0]
        
        if use_llm:
            try:
                verdict, explanation = compare_llm(clause.clause_type, clause.standard_position, top_chunk.text)
            except NotImplementedError:
                # Fallback if LLM is not implemented
                verdict, explanation = compare_fallback(clause.clause_type, clause.standard_position, top_chunk.text)
        else:
            verdict, explanation = compare_fallback(clause.clause_type, clause.standard_position, top_chunk.text)
            
        results.append(ClauseResult(
            clause_type=clause.clause_type,
            contract_id=contract_id,
            verdict=verdict,
            explanation=explanation,
            citation_text=top_chunk.text,
            citation_offset=(top_chunk.start_offset, top_chunk.end_offset)
        ))
        
    return ContractReport(
        contract_id=contract_id,
        results=results
    )

from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Tuple

class Chunk(BaseModel):
    chunk_id: str
    contract_id: str
    text: str
    start_offset: int
    end_offset: int

class PlaybookClause(BaseModel):
    clause_type: str
    query_text: str
    standard_position: str

class RetrievalResult(BaseModel):
    clause_type: str
    contract_id: str
    candidates: List[Chunk]
    top_score: float

class ClauseVerdict(str, Enum):
    MATCH = "MATCH"
    DEVIATION = "DEVIATION"
    MISSING = "MISSING"

class ClauseResult(BaseModel):
    clause_type: str
    contract_id: str
    verdict: ClauseVerdict
    explanation: str
    citation_text: Optional[str] = None
    citation_offset: Optional[Tuple[int, int]] = None

class ContractReport(BaseModel):
    contract_id: str
    results: List[ClauseResult]

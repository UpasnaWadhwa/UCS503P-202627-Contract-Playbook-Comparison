import uuid
from typing import List
from common.schemas import Chunk
from common.config import CHUNK_SIZE_TOKENS, CHUNK_OVERLAP_RATIO

def chunk_text(text: str, contract_id: str, chunk_size_chars: int = CHUNK_SIZE_TOKENS * 4, overlap_chars: int = int(CHUNK_SIZE_TOKENS * 4 * CHUNK_OVERLAP_RATIO)) -> List[Chunk]:
    """
    Split text into chunks with overlap, retaining character offsets.
    Uses character counts as a proxy for tokens for the PoC.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size_chars, text_length)
        
        # If not at the end, try to find a natural break (newline or period)
        if end < text_length:
            natural_break = max(text.rfind('\n', start, end), text.rfind('. ', start, end))
            if natural_break != -1 and natural_break > start + (chunk_size_chars // 2):
                end = natural_break + 1
                
        raw_chunk = text[start:end]
        leading_whitespaces = len(raw_chunk) - len(raw_chunk.lstrip())
        actual_start = start + leading_whitespaces
        
        chunk_text = raw_chunk.strip()
        if chunk_text:
            chunks.append(Chunk(
                chunk_id=str(uuid.uuid4()),
                contract_id=contract_id,
                text=chunk_text,
                start_offset=actual_start,
                end_offset=actual_start + len(chunk_text)
            ))
            
        start = end - overlap_chars
        if start < 0:
            start = 0
        if end >= text_length:
            break
            
    return chunks

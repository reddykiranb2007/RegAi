from typing import List, Dict, Optional
from rapidfuzz import process, fuzz
# import sentence_transformers # Optional for future use

class EmbeddingService:
    """
    Handles similarity search using Fuzzy Matching (MVP) or Embeddings (Advanced).
    """

    def __init__(self):
        # In a full implementation, load models here
        pass

    def find_best_match(self, query: str, candidates: List[Dict], threshold: int = 60) -> Optional[Dict]:
        """
        Finds the best matching device from the candidate list using fuzzy matching.
        """
        device_names = [d.get('originalName', '') for d in candidates]
        
        # Use simple token set ratio for robustness against word order
        match = process.extractOne(query, device_names, scorer=fuzz.token_set_ratio)
        
        if match:
            best_match_name = match[0]
            score = match[1]
            index = match[2]
            
            if score >= threshold:
                return {
                    "match": candidates[index],
                    "score": score
                }
        
        return None

from pydantic import BaseModel
from typing import List

class FactCheckRequest(BaseModel):
    """Request for fact checking"""
    claim: str
    category: str  # tech, finance, general

class FactCheckResult(BaseModel):
    """Result of fact checking"""
    claim: str
    is_plausible: bool
    confidence: float  # 0-1
    explanation: str
    sources: List[str]

class FactChecker:
    """Checks facts and validates claims"""
    
    # Simple knowledge base for demonstration
    KNOWN_FACTS = {
        "Python is a programming language": True,
        "The earth is flat": False,
        "Machine learning is part of AI": True,
        "Blockchain is only for crypto": False,
    }
    
    def check_fact(self, request: FactCheckRequest) -> FactCheckResult:
        """
        Check if a claim is plausible
        
        Args:
            request: FactCheckRequest with claim and category
            
        Returns:
            FactCheckResult with plausibility assessment
        """
        claim = request.claim.strip()
        
        # Check against known facts
        if claim in self.KNOWN_FACTS:
            is_plausible = self.KNOWN_FACTS[claim]
            confidence = 0.95
            explanation = f"This claim is verified in our database."
            sources = ["Internal Knowledge Base"]
        else:
            # Use simple heuristics for unknown claims
            word_count = len(claim.split())
            is_plausible = 3 <= word_count <= 50
            confidence = 0.6
            explanation = "Claim structure seems reasonable. Manual verification recommended."
            sources = ["Structural Analysis"]
        
        return FactCheckResult(
            claim=claim,
            is_plausible=is_plausible,
            confidence=confidence,
            explanation=explanation,
            sources=sources
        )
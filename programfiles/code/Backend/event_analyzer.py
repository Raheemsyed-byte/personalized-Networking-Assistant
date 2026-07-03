from ..schemas import EventAnalysisRequest
from typing import Dict, Any

class EventAnalyzerService:
    """Analyzes networking events to extract insights"""
    
    EVENT_CATEGORIES = {
        "tech": ["conference", "hackathon", "webinar", "summit", "meetup"],
        "business": ["expo", "trade show", "networking event", "convention"],
        "professional": ["seminar", "workshop", "panel", "course", "symposium"]
    }
    
    @staticmethod
    def categorize_event(event_type: str) -> str:
        """
        Categorize event into standard types
        
        Args:
            event_type: The type of event
            
        Returns:
            Standardized category
        """
        event_type_lower = event_type.lower()
        
        for category, keywords in EventAnalyzerService.EVENT_CATEGORIES.items():
            if any(keyword in event_type_lower for keyword in keywords):
                return category
        
        return "professional"  # Default category
    
    @staticmethod
    def analyze_event(request: EventAnalysisRequest) -> Dict[str, Any]:
        """
        Analyze event data
        
        Args:
            request: Event analysis request
            
        Returns:
            Dictionary with event analysis
        """
        category = EventAnalyzerService.categorize_event(request.event_type)
        
        return {
            "name": request.name,
            "type": request.event_type,
            "category": category,
            "attendees_expected": request.attendees_expected,
            "description": request.description,
            "complexity_level": EventAnalyzerService._calculate_complexity(
                request.attendees_expected
            )
        }
    
    @staticmethod
    def _calculate_complexity(attendees: int) -> str:
        """Calculate event complexity based on attendees"""
        if attendees < 50:
            return "low"
        elif attendees < 200:
            return "medium"
        else:
            return "high"
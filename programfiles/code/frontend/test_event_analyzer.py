import pytest
from backend.services.event_analyzer import EventAnalyzerService
from backend.schemas import EventAnalysisRequest


class TestEventAnalyzerService:
    """Test suite for EventAnalyzerService"""
    
    def test_categorize_event_tech(self):
        """Test categorizing tech events"""
        result = EventAnalyzerService.categorize_event("tech conference")
        assert result == "tech"
    
    def test_categorize_event_business(self):
        """Test categorizing business events"""
        result = EventAnalyzerService.categorize_event("trade show")
        assert result == "business"
    
    def test_categorize_event_professional(self):
        """Test categorizing professional events"""
        result = EventAnalyzerService.categorize_event("workshop")
        assert result == "professional"
    
    def test_categorize_event_default(self):
        """Test default categorization for unknown events"""
        result = EventAnalyzerService.categorize_event("random event")
        assert result == "professional"
    
    def test_analyze_event(self):
        """Test event analysis"""
        request = EventAnalysisRequest(
            name="Tech Summit",
            event_type="conference",
            attendees_expected=200,
            description="A tech summit"
        )
        
        result = EventAnalyzerService.analyze_event(request)
        
        assert result["name"] == "Tech Summit"
        assert result["type"] == "conference"
        assert result["category"] == "tech"
        assert result["attendees_expected"] == 200
    
    def test_calculate_complexity_low(self):
        """Test low complexity calculation"""
        result = EventAnalyzerService._calculate_complexity(30)
        assert result == "low"
    
    def test_calculate_complexity_medium(self):
        """Test medium complexity calculation"""
        result = EventAnalyzerService._calculate_complexity(100)
        assert result == "medium"
    
    def test_calculate_complexity_high(self):
        """Test high complexity calculation"""
        result = EventAnalyzerService._calculate_complexity(300)
        assert result == "high"
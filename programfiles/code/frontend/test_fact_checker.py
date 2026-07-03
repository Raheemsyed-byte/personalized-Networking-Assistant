import pytest
from backend.services.fact_checker import FactCheckerService
from backend.schemas import FactCheckResult


class TestFactCheckerService:
    """Test suite for FactCheckerService"""
    
    def test_check_fact_returns_result(self):
        """Test that fact checking returns a valid result"""
        result = FactCheckerService.check_fact("AI is powerful")
        
        assert isinstance(result, FactCheckResult)
        assert result.statement == "AI is powerful"
        assert isinstance(result.is_accurate, bool)
        assert 0 <= result.confidence_score <= 1
        assert len(result.explanation) > 0
    
    def test_check_fact_with_context(self):
        """Test fact checking with context"""
        result = FactCheckerService.check_fact(
            statement="Python is popular",
            context="Programming languages"
        )
        
        assert result.statement == "Python is popular"
    
    def test_calculate_accuracy_level_very_high(self):
        """Test accuracy level calculation - very high"""
        level = FactCheckerService.calculate_accuracy_level(0.95)
        assert level == "Very High"
    
    def test_calculate_accuracy_level_high(self):
        """Test accuracy level calculation - high"""
        level = FactCheckerService.calculate_accuracy_level(0.75)
        assert level == "High"
    
    def test_calculate_accuracy_level_medium(self):
        """Test accuracy level calculation - medium"""
        level = FactCheckerService.calculate_accuracy_level(0.55)
        assert level == "Medium"
    
    def test_calculate_accuracy_level_low(self):
        """Test accuracy level calculation - low"""
        level = FactCheckerService.calculate_accuracy_level(0.3)
        assert level == "Low"
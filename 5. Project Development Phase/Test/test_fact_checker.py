import pytest
from app.services.fact_checker import FactChecker, FactCheckRequest, FactCheckResult

@pytest.fixture
def checker():
    return FactChecker()

def test_check_fact_returns_result(checker):
    """Test that check_fact returns FactCheckResult"""
    request = FactCheckRequest(
        claim="Python is a programming language",
        category="tech"
    )
    result = checker.check_fact(request)
    assert isinstance(result, FactCheckResult)

def test_known_true_fact(checker):
    """Test checking a known true fact"""
    request = FactCheckRequest(
        claim="Python is a programming language",
        category="tech"
    )
    result = checker.check_fact(request)
    assert result.is_plausible is True
    assert result.confidence == 0.95

def test_known_false_fact(checker):
    """Test checking a known false fact"""
    request = FactCheckRequest(
        claim="The earth is flat",
        category="general"
    )
    result = checker.check_fact(request)
    assert result.is_plausible is False

def test_confidence_score_range(checker):
    """Test that confidence is between 0 and 1"""
    request = FactCheckRequest(
        claim="Something unknown",
        category="general"
    )
    result = checker.check_fact(request)
    assert 0 <= result.confidence <= 1

def test_explanation_provided(checker):
    """Test that explanation is always provided"""
    request = FactCheckRequest(
        claim="Any claim here",
        category="general"
    )
    result = checker.check_fact(request)
    assert len(result.explanation) > 0
    assert isinstance(result.sources, list)
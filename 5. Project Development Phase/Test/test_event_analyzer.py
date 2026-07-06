import pytest
from datetime import datetime
from app.services.event_analyzer import EventAnalyzer, NetworkEvent, EventAnalysis

@pytest.fixture
def analyzer():
    """Fixture providing EventAnalyzer instance"""
    return EventAnalyzer()

@pytest.fixture
def sample_event():
    """Fixture providing a sample network event"""
    return NetworkEvent(
        event_name="Tech Meetup 2024",
        attendees=25,
        duration_minutes=90,
        date=datetime(2024, 1, 15, 18, 0),
        description="A great networking event for tech professionals"
    )

def test_analyze_event_returns_event_analysis(analyzer, sample_event):
    """Test that analyze_event returns EventAnalysis object"""
    result = analyzer.analyze_event(sample_event)
    assert isinstance(result, EventAnalysis)
    assert result.event_name == sample_event.event_name

def test_engagement_score_calculation(analyzer, sample_event):
    """Test engagement score is between 0-100"""
    result = analyzer.analyze_event(sample_event)
    assert 0 <= result.engagement_score <= 100

def test_success_metrics_generated(analyzer, sample_event):
    """Test that success metrics are generated"""
    result = analyzer.analyze_event(sample_event)
    assert len(result.success_metrics) > 0
    assert isinstance(result.success_metrics, list)

def test_recommendations_generated(analyzer):
    """Test that recommendations are generated for small events"""
    small_event = NetworkEvent(
        event_name="Small Meetup",
        attendees=5,
        duration_minutes=30,
        date=datetime(2024, 1, 15),
        description="Small event"
    )
    result = analyzer.analyze_event(small_event)
    assert len(result.recommendations) > 0
    assert "Consider promoting" in result.recommendations[0]

def test_high_quality_event_metrics(analyzer):
    """Test metrics for a high-quality event"""
    great_event = NetworkEvent(
        event_name="Premium Event",
        attendees=50,
        duration_minutes=120,
        date=datetime(2024, 1, 15),
        description="Excellent networking event with great speakers and discussions"
    )
    result = analyzer.analyze_event(great_event)
    assert result.engagement_score > 80
    assert "High attendance" in result.success_metrics
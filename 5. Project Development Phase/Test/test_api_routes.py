import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_analyze_event_endpoint(client):
    """Test analyze event endpoint"""
    event_data = {
        "event_name": "Tech Summit",
        "attendees": 30,
        "duration_minutes": 120,
        "date": "2024-01-15T18:00:00",
        "description": "Great networking event"
    }
    response = client.post("/api/analyze-event", json=event_data)
    assert response.status_code == 200
    result = response.json()
    assert "engagement_score" in result
    assert "success_metrics" in result
    assert "recommendations" in result

def test_generate_topics_endpoint(client):
    """Test generate topics endpoint"""
    request_data = {
        "industry": "tech",
        "experience_level": "mid",
        "interests": ["AI", "Cloud"]
    }
    response = client.post("/api/generate-topics", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "topics" in result
    assert len(result["topics"]) > 0
    assert result["difficulty_level"] == "mid"

def test_check_fact_endpoint(client):
    """Test fact check endpoint"""
    request_data = {
        "claim": "Python is a programming language",
        "category": "tech"
    }
    response = client.post("/api/check-fact", json=request_data)
    assert response.status_code == 200
    result = response.json()
    assert "is_plausible" in result
    assert "confidence" in result
    assert result["is_plausible"] is True

def test_invalid_event_data(client):
    """Test error handling with invalid data"""
    invalid_event = {
        "event_name": "Tech Summit",
        # Missing required fields
    }
    response = client.post("/api/analyze-event", json=invalid_event)
    assert response.status_code == 422  # Validation error

def test_analyze_event_invalid_attendees(client):
    """Test with negative attendees"""
    event_data = {
        "event_name": "Event",
        "attendees": -5,  # Invalid
        "duration_minutes": 60,
        "date": "2024-01-15T18:00:00",
        "description": "Test"
    }
    response = client.post("/api/analyze-event", json=event_data)
    # Should fail validation
    assert response.status_code != 200
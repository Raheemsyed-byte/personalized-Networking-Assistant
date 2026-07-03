import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestTopicRoutes:
    """Test topic routes"""
    
    def test_generate_topics_success(self):
        """Test successful topic generation"""
        payload = {
            "event_name": "Tech Summit",
            "event_type": "conference",
            "user_background": "Software Engineer",
            "industry": "Technology",
            "num_topics": 3
        }
        
        response = client.post("/api/v1/topics/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_generate_topics_missing_field(self):
        """Test topic generation with missing field"""
        payload = {
            "event_name": "Tech Summit",
            # Missing required fields
        }
        
        response = client.post("/api/v1/topics/generate", json=payload)
        assert response.status_code == 422  # Validation error


class TestFactRoutes:
    """Test fact checking routes"""
    
    def test_check_fact_success(self):
        """Test successful fact checking"""
        payload = {
            "statement": "The earth is round"
        }
        
        response = client.post("/api/v1/facts/check", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "is_accurate" in data
        assert "confidence_score" in data
        assert "explanation" in data
    
    def test_check_fact_with_context(self):
        """Test fact checking with context"""
        payload = {
            "statement": "Python is a programming language",
            "context": "Programming languages"
        }
        
        response = client.post("/api/v1/facts/check", json=payload)
        assert response.status_code == 200
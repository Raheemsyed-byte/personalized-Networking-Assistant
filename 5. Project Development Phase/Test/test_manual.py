"""
Manual testing script - run this to verify everything works
"""
import httpx
from datetime import datetime
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_analyze_event():
    """Test event analysis"""
    print("\n=== Testing Event Analysis ===")
    data = {
        "event_name": "Python Meetup",
        "attendees": 25,
        "duration_minutes": 90,
        "date": datetime.now().isoformat(),
        "description": "Networking event for Python developers"
    }
    response = httpx.post(f"{BASE_URL}/api/analyze-event", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_generate_topics():
    """Test topic generation"""
    print("\n=== Testing Topic Generation ===")
    data = {
        "industry": "tech",
        "experience_level": "mid",
        "interests": ["Python", "FastAPI", "DevOps"]
    }
    response = httpx.post(f"{BASE_URL}/api/generate-topics", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_check_fact():
    """Test fact checking"""
    print("\n=== Testing Fact Checking ===")
    data = {
        "claim": "Python is a programming language",
        "category": "tech"
    }
    response = httpx.post(f"{BASE_URL}/api/check-fact", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("Starting manual API tests...")
    test_health()
    test_analyze_event()
    test_generate_topics()
    test_check_fact()
    print("\n✅ All manual tests completed!")
import pytest
from app.services.topic_generator import (
    TopicGenerator, TopicRequest, GeneratedTopics
)

@pytest.fixture
def generator():
    return TopicGenerator()

@pytest.fixture
def tech_request():
    return TopicRequest(
        industry="tech",
        experience_level="mid",
        interests=["cloud computing", "DevOps"]
    )

def test_generate_topics_returns_generated_topics(generator, tech_request):
    """Test that generate_topics returns GeneratedTopics object"""
    result = generator.generate_topics(tech_request)
    assert isinstance(result, GeneratedTopics)

def test_topics_are_list_of_strings(generator, tech_request):
    """Test that topics is a list of strings"""
    result = generator.generate_topics(tech_request)
    assert isinstance(result.topics, list)
    assert all(isinstance(topic, str) for topic in result.topics)
    assert len(result.topics) > 0

def test_difficulty_level_matches_request(generator):
    """Test that difficulty level matches the request"""
    for level in ["junior", "mid", "senior"]:
        request = TopicRequest(
            industry="tech",
            experience_level=level,
            interests=[]
        )
        result = generator.generate_topics(request)
        assert result.difficulty_level == level

def test_interests_included_in_topics(generator):
    """Test that interests are included in generated topics"""
    request = TopicRequest(
        industry="tech",
        experience_level="junior",
        interests=["AI", "Machine Learning"]
    )
    result = generator.generate_topics(request)
    topics_str = " ".join(result.topics)
    assert "AI" in topics_str or "Machine Learning" in topics_str

def test_unsupported_industry_fallback(generator):
    """Test that unsupported industries get default topics"""
    request = TopicRequest(
        industry="underwater_basket_weaving",
        experience_level="junior",
        interests=[]
    )
    result = generator.generate_topics(request)
    assert len(result.topics) > 0
    assert "career journey" in result.topics[0]
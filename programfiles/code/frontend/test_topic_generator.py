import pytest
from backend.services.topic_generator import TopicGeneratorService
from backend.schemas import TopicGenerationRequest, EventAnalysis


class TestTopicGeneratorService:
    """Test suite for TopicGeneratorService"""
    
    def test_generate_topics_tech(self):
        """Test generating tech topics"""
        topics = TopicGeneratorService.generate_topics(
            event_category="tech",
            user_background="Engineer",
            industry="Technology",
            num_topics=3
        )
        
        assert len(topics) == 3
        assert all("topic_name" in topic for topic in topics)
        assert all("conversation_starter" in topic for topic in topics)
        assert all("follow_up_questions" in topic for topic in topics)
        assert all(0 <= topic["relevance_score"] <= 1 for topic in topics)
    
    def test_generate_topics_business(self):
        """Test generating business topics"""
        topics = TopicGeneratorService.generate_topics(
            event_category="business",
            user_background="Founder",
            industry="StartUp",
            num_topics=2
        )
        
        assert len(topics) <= 2
    
    def test_generate_topics_limit(self):
        """Test that generated topics don't exceed template count"""
        topics = TopicGeneratorService.generate_topics(
            event_category="tech",
            user_background="Engineer",
            industry="Tech",
            num_topics=100  # Request more than available
        )
        
        assert len(topics) <= 3  # Template has 3 topics max
    
    def test_personalize_topic(self):
        """Test topic personalization"""
        topic = {
            "topic_name": "Test",
            "conversation_starter": "What do you think?",
            "follow_up_questions": [],
            "relevance_score": 0.8
        }
        
        personalized = TopicGeneratorService.personalize_topic(
            topic,
            "Data Scientist"
        )
        
        assert "Data Scientist" in personalized["conversation_starter"]
        assert personalized["relevance_score"] == 0.8
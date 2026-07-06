from pydantic import BaseModel
from typing import List
import random

class TopicRequest(BaseModel):
    """Request model for topic generation"""
    industry: str
    experience_level: str  # junior, mid, senior
    interests: List[str]

class GeneratedTopics(BaseModel):
    """Generated conversation topics"""
    topics: List[str]
    difficulty_level: str

class TopicGenerator:
    """Generates relevant networking conversation topics"""
    
    # Knowledge base of topics by industry
    TOPICS_DB = {
        "tech": {
            "junior": [
                "What technologies are you learning right now?",
                "How did you start your career in tech?",
                "What's your favorite programming language?"
            ],
            "mid": [
                "What architectural patterns do you prefer?",
                "How do you approach system design?",
                "What's your take on microservices?"
            ],
            "senior": [
                "How do you lead technical strategy?",
                "What's your approach to mentoring junior developers?",
                "How do you balance innovation with stability?"
            ]
        },
        "finance": {
            "junior": [
                "What drew you to finance?",
                "What's the most interesting project you've worked on?",
                "How do you stay updated on market trends?"
            ],
            "mid": [
                "What's your investment strategy?",
                "How do you manage risk in your portfolio?",
                "What emerging markets interest you?"
            ],
            "senior": [
                "How do you guide investment strategy?",
                "What's your vision for the future of fintech?",
                "How do you mentor the next generation?"
            ]
        }
    }
    
    def generate_topics(self, request: TopicRequest) -> GeneratedTopics:
        """
        Generate conversation topics based on industry and experience level
        
        Args:
            request: TopicRequest with industry, experience level, and interests
            
        Returns:
            GeneratedTopics with relevant topics
        """
        industry = request.industry.lower()
        level = request.experience_level.lower()
        
        # Get base topics
        if industry in self.TOPICS_DB and level in self.TOPICS_DB[industry]:
            base_topics = self.TOPICS_DB[industry][level]
        else:
            base_topics = ["Tell me about your career journey"]
        
        # Personalize with interests
        personalized_topics = base_topics.copy()
        for interest in request.interests[:2]:
            personalized_topics.append(f"How do you apply {interest} in your work?")
        
        return GeneratedTopics(
            topics=personalized_topics[:5],
            difficulty_level=level
        )
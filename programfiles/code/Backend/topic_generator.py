from typing import List, Dict, Any
import random

class TopicGeneratorService:
    """Generates personalized networking conversation topics"""
    
    TOPIC_TEMPLATES = {
        "tech": [
            {
                "name": "Emerging Technologies",
                "starter": "What's the most exciting technology you've encountered recently?",
                "follow_ups": [
                    "How are you planning to implement this in your work?",
                    "What challenges do you foresee?",
                    "What's your prediction for this technology in 5 years?"
                ]
            },
            {
                "name": "Industry Trends",
                "starter": "How do you stay updated with the latest industry trends?",
                "follow_ups": [
                    "Which trends do you think are overrated?",
                    "What trend surprises you the most?",
                    "How do you implement these trends?"
                ]
            },
            {
                "name": "Career Growth",
                "starter": "What's been your biggest learning in your career?",
                "follow_ups": [
                    "How do you share knowledge with your team?",
                    "What skills are you developing now?",
                    "What advice would you give to someone starting out?"
                ]
            }
        ],
        "business": [
            {
                "name": "Market Opportunities",
                "starter": "What market opportunities are you currently exploring?",
                "follow_ups": [
                    "What's your go-to-market strategy?",
                    "How do you identify untapped markets?",
                    "What's the biggest challenge you've faced scaling?"
                ]
            },
            {
                "name": "Business Strategies",
                "starter": "How do you approach building customer relationships?",
                "follow_ups": [
                    "What's your customer retention strategy?",
                    "How do you measure success?",
                    "What's your approach to competing?"
                ]
            }
        ],
        "professional": [
            {
                "name": "Leadership",
                "starter": "What's your leadership philosophy?",
                "follow_ups": [
                    "How do you motivate your team?",
                    "What's the biggest challenge you face as a leader?",
                    "How do you handle conflict?"
                ]
            },
            {
                "name": "Professional Development",
                "starter": "How do you invest in your professional development?",
                "follow_ups": [
                    "What's the best advice you've received?",
                    "How do you balance work and learning?",
                    "What's next in your career?"
                ]
            }
        ]
    }
    
    @staticmethod
    def generate_topics(
        event_category: str,
        user_background: str,
        industry: str,
        num_topics: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized networking topics
        
        Args:
            event_category: Category of the event (tech, business, professional)
            user_background: User's professional background
            industry: User's industry
            num_topics: Number of topics to generate
            
        Returns:
            List of generated topics
        """
        # Get templates for this category
        templates = TopicGeneratorService.TOPIC_TEMPLATES.get(
            event_category,
            TopicGeneratorService.TOPIC_TEMPLATES["professional"]
        )
        
        # Select random topics
        selected_templates = random.sample(
            templates,
            min(num_topics, len(templates))
        )
        
        topics = []
        for i, template in enumerate(selected_templates, 1):
            topic = {
                "id": i,
                "topic_name": template["name"],
                "conversation_starter": template["starter"],
                "follow_up_questions": template["follow_ups"],
                "relevance_score": round(0.75 + (random.random() * 0.25), 2)
            }
            topics.append(topic)
        
        return topics
    
    @staticmethod
    def personalize_topic(
        topic: Dict[str, Any],
        user_background: str
    ) -> Dict[str, Any]:
        """
        Personalize a topic based on user background
        
        Args:
            topic: The topic to personalize
            user_background: User's professional background
            
        Returns:
            Personalized topic
        """
        personalized = topic.copy()
        # Could enhance starter with user context
        personalized["conversation_starter"] = (
            f"Based on your {user_background} background, {topic['conversation_starter'].lower()}"
        )
        return personalized
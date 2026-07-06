from pydantic import BaseModel
from datetime import datetime
from typing import List

class NetworkEvent(BaseModel):
    """Model for a networking event"""
    event_name: str
    attendees: int
    duration_minutes: int
    date: datetime
    description: str

class EventAnalysis(BaseModel):
    """Analysis result of a networking event"""
    event_name: str
    engagement_score: float  # 0-100
    success_metrics: List[str]
    recommendations: List[str]

class EventAnalyzer:
    """Analyzes networking events to provide insights"""
    
    def analyze_event(self, event: NetworkEvent) -> EventAnalysis:
        """
        Analyze a networking event and return insights
        
        Args:
            event: NetworkEvent object with event details
            
        Returns:
            EventAnalysis with engagement score and recommendations
        """
        # Calculate engagement score
        base_score = min((event.attendees / 10) * 10, 80)
        duration_bonus = min(event.duration_minutes / 5, 20)
        engagement_score = base_score + duration_bonus
        
        # Generate success metrics
        success_metrics = []
        if event.attendees > 20:
            success_metrics.append("High attendance")
        if event.duration_minutes > 60:
            success_metrics.append("Good duration for networking")
        if len(event.description) > 50:
            success_metrics.append("Well-documented event")
        
        # Generate recommendations
        recommendations = []
        if event.attendees < 15:
            recommendations.append("Consider promoting to more people")
        if event.duration_minutes < 45:
            recommendations.append("Extend duration for better networking")
        if not recommendations:
            recommendations.append("Event looks well-planned!")
        
        return EventAnalysis(
            event_name=event.event_name,
            engagement_score=min(engagement_score, 100),
            success_metrics=success_metrics,
            recommendations=recommendations
        )
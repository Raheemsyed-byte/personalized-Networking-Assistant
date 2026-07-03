from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ============== Request Models ==============

class EventAnalysisRequest(BaseModel):
    """Request model for event data"""
    name: str = Field(..., min_length=1, max_length=200)
    event_type: str = Field(..., description="Type: tech, business, professional")
    attendees_expected: int = Field(..., ge=1, le=10000)
    description: str = Field(..., min_length=1, max_length=1000)


class TopicGenerationRequest(BaseModel):
    """Request model for topic generation"""
    event_name: str
    event_type: str
    user_background: str
    industry: str
    num_topics: int = Field(default=3, ge=1, le=10)


class FactCheckRequest(BaseModel):
    """Request model for fact checking"""
    statement: str = Field(..., min_length=1, max_length=500)
    context: Optional[str] = Field(default=None, max_length=500)


class FeedbackRequest(BaseModel):
    """Request model for feedback"""
    topic_id: int
    rating: int = Field(..., ge=1, le=5)
    comments: str = Field(default="", max_length=500)


# ============== Response Models ==============

class Topic(BaseModel):
    """Generated networking topic"""
    id: Optional[int] = None
    topic_name: str
    conversation_starter: str
    follow_up_questions: List[str]
    relevance_score: float = Field(..., ge=0, le=1)
    
    class Config:
        from_attributes = True


class FactCheckResult(BaseModel):
    """Result of fact checking"""
    statement: str
    is_accurate: bool
    confidence_score: float = Field(..., ge=0, le=1)
    explanation: str


class ConversationLog(BaseModel):
    """Logged conversation"""
    id: Optional[int] = None
    user_id: str
    event_name: str
    topic: str
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackLog(BaseModel):
    """Logged feedback"""
    id: Optional[int] = None
    user_id: str
    topic_id: int
    rating: int
    comments: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    """Response for history endpoint"""
    total_conversations: int
    recent_conversations: List[ConversationLog]


class FeedbackResponse(BaseModel):
    """Response for feedback endpoint"""
    total_feedback: int
    average_rating: float
    recent_feedback: List[FeedbackLog]
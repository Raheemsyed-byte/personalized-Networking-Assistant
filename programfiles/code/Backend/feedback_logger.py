from typing import List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class FeedbackModel(Base):
    """Database model for feedback"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    topic_id = Column(Integer)
    rating = Column(Integer)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class FeedbackLoggerService:
    """Manages user feedback"""
    
    def __init__(self, db_url: str = "sqlite:///networking.db"):
        """Initialize feedback logger with database"""
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def log_feedback(
        self,
        user_id: str,
        topic_id: int,
        rating: int,
        comments: str = ""
    ) -> dict:
        """
        Log user feedback
        
        Args:
            user_id: User identifier
            topic_id: ID of the topic being rated
            rating: Rating from 1-5
            comments: Feedback comments
            
        Returns:
            Logged feedback data
        """
        db: Session = self.SessionLocal()
        try:
            # Validate rating
            rating = max(1, min(5, rating))
            
            feedback = FeedbackModel(
                user_id=user_id,
                topic_id=topic_id,
                rating=rating,
                comments=comments
            )
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            
            return {
                "id": feedback.id,
                "user_id": feedback.user_id,
                "topic_id": feedback.topic_id,
                "rating": feedback.rating,
                "comments": feedback.comments,
                "created_at": feedback.created_at
            }
        finally:
            db.close()
    
    def get_user_feedback(self, user_id: str, limit: int = 10) -> List[dict]:
        """
        Get user's feedback history
        
        Args:
            user_id: User identifier
            limit: Maximum number of records
            
        Returns:
            List of feedback entries
        """
        db: Session = self.SessionLocal()
        try:
            feedbacks = db.query(FeedbackModel)\
                .filter(FeedbackModel.user_id == user_id)\
                .order_by(FeedbackModel.created_at.desc())\
                .limit(limit)\
                .all()
            
            return [
                {
                    "id": f.id,
                    "user_id": f.user_id,
                    "topic_id": f.topic_id,
                    "rating": f.rating,
                    "comments": f.comments,
                    "created_at": f.created_at
                }
                for f in feedbacks
            ]
        finally:
            db.close()
    
    def get_average_rating(self, user_id: str) -> float:
        """
        Calculate average rating for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Average rating
        """
        db: Session = self.SessionLocal()
        try:
            feedbacks = db.query(FeedbackModel)\
                .filter(FeedbackModel.user_id == user_id)\
                .all()
            
            if not feedbacks:
                return 0.0
            
            return sum(f.rating for f in feedbacks) / len(feedbacks)
        finally:
            db.close()
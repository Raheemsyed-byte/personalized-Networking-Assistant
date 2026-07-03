from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class ConversationModel(Base):
    """Database model for conversations"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_name = Column(String)
    topic = Column(String)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class HistoryLoggerService:
    """Manages conversation history"""
    
    def __init__(self, db_url: str = "sqlite:///networking.db"):
        """Initialize history logger with database"""
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def log_conversation(
        self,
        user_id: str,
        event_name: str,
        topic: str,
        notes: str = ""
    ) -> dict:
        """
        Log a conversation
        
        Args:
            user_id: User identifier
            event_name: Name of the networking event
            topic: The topic discussed
            notes: Additional notes
            
        Returns:
            Logged conversation data
        """
        db: Session = self.SessionLocal()
        try:
            conversation = ConversationModel(
                user_id=user_id,
                event_name=event_name,
                topic=topic,
                notes=notes
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            return {
                "id": conversation.id,
                "user_id": conversation.user_id,
                "event_name": conversation.event_name,
                "topic": conversation.topic,
                "notes": conversation.notes,
                "created_at": conversation.created_at
            }
        finally:
            db.close()
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[dict]:
        """
        Get user's conversation history
        
        Args:
            user_id: User identifier
            limit: Maximum number of records to return
            
        Returns:
            List of conversations
        """
        db: Session = self.SessionLocal()
        try:
            conversations = db.query(ConversationModel)\
                .filter(ConversationModel.user_id == user_id)\
                .order_by(ConversationModel.created_at.desc())\
                .limit(limit)\
                .all()
            
            return [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "event_name": c.event_name,
                    "topic": c.topic,
                    "notes": c.notes,
                    "created_at": c.created_at
                }
                for c in conversations
            ]
        finally:
            db.close()
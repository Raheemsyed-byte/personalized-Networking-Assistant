from fastapi import APIRouter, HTTPException
from app.services.event_analyzer import EventAnalyzer, NetworkEvent
from app.services.topic_generator import TopicGenerator, TopicRequest
from app.services.fact_checker import FactChecker, FactCheckRequest

router = APIRouter(prefix="/api", tags=["networking"])

# Initialize services
event_analyzer = EventAnalyzer()
topic_generator = TopicGenerator()
fact_checker = FactChecker()

@router.post("/analyze-event")
async def analyze_event(event: NetworkEvent):
    """Analyze a networking event"""
    try:
        analysis = event_analyzer.analyze_event(event)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-topics")
async def generate_topics(request: TopicRequest):
    """Generate conversation topics"""
    try:
        topics = topic_generator.generate_topics(request)
        return topics
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/check-fact")
async def check_fact(request: FactCheckRequest):
    """Check the plausibility of a fact"""
    try:
        result = fact_checker.check_fact(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Any

# ============== Page Configuration ==============

st.set_page_config(
    page_title="Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== Constants ==============

API_BASE_URL = "http://localhost:8000/api/v1"

# ============== Session State Initialization ==============

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_default"

if "generated_topics" not in st.session_state:
    st.session_state.generated_topics = []

if "selected_topic_for_feedback" not in st.session_state:
    st.session_state.selected_topic_for_feedback = None

# ============== Styling ==============

st.markdown("""
<style>
    .title-main {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============== Main Application ==============

def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🤝 Networking Assistant</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("Your AI-powered guide to mastering networking conversations")
    
    # Sidebar
    st.sidebar.title("⚙️ Navigation")
    page = st.sidebar.radio(
        "Select a page",
        ["🏠 Home", "💬 History", "📊 Feedback", "✅ Fact Checker"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### User Settings")
    st.session_state.user_id = st.sidebar.text_input(
        "User ID",
        value=st.session_state.user_id
    )
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "💬 History":
        show_history_page()
    elif page == "📊 Feedback":
        show_feedback_page()
    elif page == "✅ Fact Checker":
        show_fact_checker_page()


# ============== Page Functions ==============

def show_home_page():
    """Display home page with topic generation"""
    st.header("📌 Generate Networking Topics")
    
    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Event Details")
        event_name = st.text_input(
            "Event Name",
            value="Tech Conference 2024",
            key="event_name"
        )
        
        event_type = st.selectbox(
            "Event Type",
            ["tech", "business", "professional"],
            key="event_type"
        )
        
        attendees = st.slider(
            "Expected Attendees",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
    
    with col2:
        st.subheader("Your Profile")
        user_background = st.text_area(
            "Your Background",
            value="Software Engineer with 5 years of experience",
            height=100
        )
        
        industry = st.text_input(
            "Your Industry",
            value="Technology"
        )
    
    event_description = st.text_area(
        "Event Description",
        value="Annual tech conference focusing on AI and innovation",
        height=80
    )
    
    num_topics = st.slider(
        "Number of Topics to Generate",
        min_value=1,
        max_value=10,
        value=3
    )
    
    # Generate Button
    if st.button("🎯 Generate Topics", use_container_width=True, key="generate_btn"):
        with st.spinner("Generating topics..."):
            try:
                request_payload = {
                    "event_name": event_name,
                    "event_type": event_type,
                    "user_background": user_background,
                    "industry": industry,
                    "num_topics": num_topics
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/topics/generate",
                    json=request_payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    st.session_state.generated_topics = response.json()
                    st.success("✅ Topics generated successfully!")
                else:
                    st.error(f"❌ Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    
    # Display Generated Topics
    if st.session_state.generated_topics:
        st.divider()
        st.subheader("📚 Generated Topics")
        
        for i, topic in enumerate(st.session_state.generated_topics, 1):
            with st.expander(f"**Topic {i}: {topic.get('topic_name', 'Topic')}**"):
                st.markdown("### 💬 Conversation Starter")
                st.info(topic.get('conversation_starter', 'N/A'))
                
                st.markdown("### ❓ Follow-up Questions")
                follow_ups = topic.get('follow_up_questions', [])
                for j, question in enumerate(follow_ups, 1):
                    st.write(f"{j}. {question}")
                
                relevance = topic.get('relevance_score', 0)
                st.markdown(f"### 📈 Relevance Score: **{relevance:.0%}**")
                st.progress(relevance)
                
                # Feedback Buttons
                st.markdown("### 💭 Feedback")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("👍 Useful", key=f"useful_{i}", use_container_width=True):
                        log_feedback(topic.get('id', i), 5, "This topic was very helpful")
                
                with col2:
                    if st.button("😐 Neutral", key=f"neutral_{i}", use_container_width=True):
                        log_feedback(topic.get('id', i), 3, "This topic was okay")
                
                with col3:
                    if st.button("👎 Not Useful", key=f"not_useful_{i}", use_container_width=True):
                        log_feedback(topic.get('id', i), 1, "This topic wasn't helpful")


def show_history_page():
    """Display conversation history"""
    st.header("💬 Conversation History")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/history/user/{st.session_state.user_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Conversations", data.get('total_conversations', 0))
            
            conversations = data.get('recent_conversations', [])
            if conversations:
                st.subheader("Recent Conversations")
                for conv in conversations:
                    with st.expander(f"📅 {conv.get('created_at', 'N/A')} - {conv.get('event_name', 'Event')}"):
                        st.write(f"**Topic:** {conv.get('topic', 'N/A')}")
                        if conv.get('notes'):
                            st.write(f"**Notes:** {conv['notes']}")
            else:
                st.info("No conversations logged yet. Generate some topics first!")
        else:
            st.error("Failed to fetch history")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_feedback_page():
    """Display feedback history"""
    st.header("📊 Feedback History")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/feedback/user/{st.session_state.user_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Feedback Entries", data.get('total_feedback', 0))
            with col2:
                avg_rating = data.get('average_rating', 0)
                st.metric("Average Rating", f"{'⭐' * int(avg_rating)} {avg_rating:.1f}/5.0")
            
            feedback_list = data.get('recent_feedback', [])
            if feedback_list:
                st.subheader("Recent Feedback")
                for feedback in feedback_list:
                    rating = feedback.get('rating', 0)
                    stars = "⭐" * rating + "☆" * (5 - rating)
                    
                    with st.expander(f"{stars} - {feedback.get('created_at', 'N/A')}"):
                        st.write(f"**Rating:** {rating}/5")
                        if feedback.get('comments'):
                            st.write(f"**Comments:** {feedback['comments']}")
            else:
                st.info("No feedback yet. Rate some topics to see your feedback history!")
        else:
            st.error("Failed to fetch feedback")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_fact_checker_page():
    """Display fact checker"""
    st.header("✅ Fact Checker")
    st.write("Verify the accuracy of statements before using them in conversations")
    
    statement = st.text_area(
        "Enter a statement to fact-check",
        value="AI will revolutionize every industry in the next 5 years",
        height=100
    )
    
    context = st.text_input(
        "Additional Context (optional)",
        value=""
    )
    
    if st.button("🔍 Check Fact", use_container_width=True):
        with st.spinner("Checking fact..."):
            try:
                payload = {
                    "statement": statement,
                    "context": context if context else None
                }
                
                response = requests.post(
                    f"{API_BASE_URL}/facts/check",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if result.get('is_accurate'):
                            st.success("✅ Likely Accurate")
                        else:
                            st.warning("⚠️ Needs Verification")
                    
                    with col2:
                        confidence = result.get('confidence_score', 0)
                        st.metric("Confidence Score", f"{confidence:.0%}")
                        st.progress(confidence)
                    
                    st.markdown("### 📝 Explanation")
                    st.info(result.get('explanation', 'No explanation available'))
                else:
                    st.error(f"Error: {response.status_code}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


# ============== Helper Functions ==============

def log_feedback(topic_id: int, rating: int, comments: str = ""):
    """Log feedback to backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/feedback/log",
            params={
                "user_id": st.session_state.user_id,
                "topic_id": topic_id,
                "rating": rating,
                "comments": comments
            },
            timeout=10
        )
        
        if response.status_code == 200:
            st.success("✅ Feedback logged!")
        else:
            st.error("Failed to log feedback")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
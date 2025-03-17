import streamlit as st
from datetime import datetime
import json
import os
from config import STAGES, DEFAULT_LANGUAGE

class SessionManager:
    """Class to manage the session state for the chatbot."""
    
    @staticmethod
    def initialize_session():
        """Initialize or get the session state variables."""
        if "initialized" not in st.session_state:
            # Core conversation state
            st.session_state.messages = []
            st.session_state.current_stage = "greeting"
            st.session_state.conversation_ended = False
            
            # Candidate information
            st.session_state.candidate_info = {
                "name": None,
                "email": None,
                "phone": None,
                "experience": None,
                "position": None,
                "location": None,
                "tech_stack": []
            }
            
            # Technical assessment tracking
            st.session_state.tech_questions_generated = False
            st.session_state.technical_assessment = {
                "questions_asked": [],
                "answers": [],
                "evaluations": [],
                "scores": {},
                "overall_score": 0,
                "completed": False
            }
            
            # Advanced features state
            st.session_state.sentiment_data = []
            st.session_state.language = DEFAULT_LANGUAGE
            st.session_state.selected_language = "English"
            
            # Set initialization flag
            st.session_state.initialized = True
    
    @staticmethod
    def reset_session():
        """Reset the session state to start a new conversation."""
        # Keep API key but reset everything else
        api_key = st.session_state.get("api_key", None)
        client = st.session_state.get("gemini_client", None)
        
        for key in list(st.session_state.keys()):
            if key not in ["api_key", "gemini_client"]:
                del st.session_state[key]
        
        # Restore API key and client
        if api_key:
            st.session_state.api_key = api_key
        if client:
            st.session_state.gemini_client = client
            
        # Re-initialize session
        SessionManager.initialize_session()
    
    @staticmethod
    def save_session(filename=None):
        """Save the current session to a file."""
        if not filename:
            # Generate filename based on candidate name and timestamp
            candidate_name = st.session_state.candidate_info.get("name", "anonymous")
            candidate_name = candidate_name.replace(" ", "_").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{candidate_name}_{timestamp}.json"
        
        # Create sessions directory if it doesn't exist
        os.makedirs("sessions", exist_ok=True)
        
        # Prepare session data
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "candidate_info": st.session_state.candidate_info,
            "messages": st.session_state.messages,
            "current_stage": st.session_state.current_stage,
            "technical_assessment": st.session_state.technical_assessment,
            "sentiment_data": st.session_state.sentiment_data,
            "language": st.session_state.language
        }
        
        # Save to file
        with open(os.path.join("sessions", filename), "w") as f:
            json.dump(session_data, f, indent=4)
        
        return filename
    
    @staticmethod
    def load_session(filename):
        """Load a session from a file."""
        try:
            with open(os.path.join("sessions", filename), "r") as f:
                session_data = json.load(f)
            
            # Restore session state
            st.session_state.messages = session_data.get("messages", [])
            st.session_state.candidate_info = session_data.get("candidate_info", {})
            st.session_state.current_stage = session_data.get("current_stage", "greeting")
            st.session_state.technical_assessment = session_data.get("technical_assessment", {})
            st.session_state.sentiment_data = session_data.get("sentiment_data", [])
            st.session_state.language = session_data.get("language", DEFAULT_LANGUAGE)
            
            # Set appropriate flags
            st.session_state.conversation_ended = st.session_state.current_stage == "conclusion"
            st.session_state.tech_questions_generated = len(st.session_state.technical_assessment.get("questions_asked", [])) > 0
            
            return True
        except Exception as e:
            st.error(f"Error loading session: {str(e)}")
            return False
    
    @staticmethod
    def list_saved_sessions():
        """List all saved session files."""
        try:
            os.makedirs("sessions", exist_ok=True)
            sessions = [f for f in os.listdir("sessions") if f.endswith(".json")]
            return sorted(sessions, reverse=True)
        except Exception as e:
            st.error(f"Error listing sessions: {str(e)}")
            return []

import streamlit as st
import os
import plotly.express as px
from datetime import datetime

from src.prompt_generator import PromptGenerator
from src.gemini_client import GeminiClient
from src.session_manager import SessionManager
from src.conversation_handler import ConversationHandler
from src.visualization import Visualization
from src.language_detector import LanguageDetector
from utils.helpers import load_custom_css
from config import SUPPORTED_LANGUAGES, UI_THEME

# Set page config
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Initialize session state
SessionManager.initialize_session()

# # Sidebar content
# with st.sidebar:
#     st.title("TalentScout Hiring Assistant")
#     st.markdown("---")
    
#     # API key input
#     with st.container():


#             if "gemini_client" not in st.session_state or st.session_state.gemini_client is None:
#                 st.session_state.gemini_client = GeminiClient()
#                 # if st.session_state.gemini_client.is_initialized():
#                 #     st.success("API connected successfully!")
#                 # else:
#                 #     st.error("Failed to initialize API client. Check your API key.")
    
#     # Language selector
#     with st.container():
#         st.subheader("Language Settings")
#         selected_language = st.selectbox(
#             "Preferred Language",
#             list(SUPPORTED_LANGUAGES.keys()),
#             index=0
#         )
#         st.session_state.language = SUPPORTED_LANGUAGES[selected_language]
#         st.session_state.selected_language = selected_language
    
#     # Display candidate information if collected
#     if any(value is not None for value in st.session_state.candidate_info.values()):
#         with st.container():
#             st.subheader("Candidate Information")
            
#             # Format candidate info in a clean panel
#             #st.markdown('<div class="candidate-info">', unsafe_allow_html=True)
            
#             for key, value in st.session_state.candidate_info.items():
#                 if value:
#                     if key == "tech_stack" and len(value) > 0:
#                         st.markdown(f"**{key.replace('_', ' ').title()}:**")
#                         # Display tech stack as tags
#                         tech_tags = ' '.join([f'<span class="tech-tag">{tech}</span>' for tech in value])
#                         st.markdown(tech_tags, unsafe_allow_html=True)
#                     else:
#                         st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     # Visualizations
#     if len(st.session_state.sentiment_data) > 2:
#         with st.container():
            
            
#             # Sentiment trend
#             st.markdown("#### Sentiment Analysis")
#             sentiment_fig = Visualization.create_sentiment_graph(st.session_state.sentiment_data)
#             if sentiment_fig:
#                 st.plotly_chart(sentiment_fig, use_container_width=True)
            
            

            

    
#     # Session management
#     with st.container():
#         st.subheader("Session Management")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             if st.button("Reset Conversation", key="reset_btn"):
#                 SessionManager.reset_session()
#                 st.experimental_rerun()
        
#         with col2:
#             if st.button("Save Session", key="save_btn") and len(st.session_state.messages) > 1:
#                 filename = SessionManager.save_session()
#                 st.success(f"Session saved as: {filename}")
        
#         # Session loading
#         saved_sessions = SessionManager.list_saved_sessions()
#         if saved_sessions:
#             selected_session = st.selectbox("Load Previous Session", ["Select a session..."] + saved_sessions)
            
#             if selected_session != "Select a session..." and st.button("Load Session"):
#                 if SessionManager.load_session(selected_session):
#                     st.success(f"Session '{selected_session}' loaded successfully!")
#                     st.experimental_rerun()

# # Sidebar content
with st.sidebar:
    st.title("TalentScout Hiring Assistant")
    st.markdown("---")
    
    # API key input
    with st.container():
        # st.subheader("API Configuration")
        # api_key = st.text_input("Enter your Gemini API Key", type="password", key="api_key_input")
        
        # if api_key:
            if "gemini_client" not in st.session_state or st.session_state.gemini_client is None:
                st.session_state.gemini_client = GeminiClient()
                # if st.session_state.gemini_client.is_initialized():
                #     st.success("API connected successfully!")
                # else:
                #     st.error("Failed to initialize API client. Check your API key.")
    
    # Language selector
    with st.container():
        st.subheader("Language Settings")
        selected_language = st.selectbox(
            "Preferred Language",
            list(SUPPORTED_LANGUAGES.keys()),
            index=0
        )
        st.session_state.language = SUPPORTED_LANGUAGES[selected_language]
        st.session_state.selected_language = selected_language
    
    # Display candidate information if collected
    if any(value is not None for value in st.session_state.candidate_info.values()):
        with st.container():
            st.subheader("Candidate Information")
            
            # Format candidate info in a clean panel
            st.markdown('<div class="candidate-info">', unsafe_allow_html=True)
            
            for key, value in st.session_state.candidate_info.items():
                if value:
                    if key == "tech_stack" and len(value) > 0:
                        st.markdown(f"**{key.replace('_', ' ').title()}:**")
                        # Display tech stack as tags
                        tech_tags = ' '.join([f'<span class="tech-tag">{tech}</span>' for tech in value])
                        st.markdown(tech_tags, unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualizations
    if len(st.session_state.sentiment_data) > 2:
        with st.container():
            st.subheader("Conversation Analytics")
            
            # Sentiment trend
            st.markdown("#### Sentiment Analysis")
            sentiment_fig = Visualization.create_sentiment_graph(st.session_state.sentiment_data)
            if sentiment_fig:
                st.plotly_chart(sentiment_fig, use_container_width=True)
            
            # Technical assessment score if available
            if st.session_state.technical_assessment.get("scores"):
                st.markdown("#### Technical Assessment")
                tech_fig = Visualization.create_technical_assessment_chart(st.session_state.technical_assessment)
                if tech_fig:
                    st.plotly_chart(tech_fig, use_container_width=True)
    
    # Session management
    with st.container():
        st.subheader("Session Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Reset Conversation", key="reset_btn"):
                SessionManager.reset_session()
                st.experimental_rerunrerun()
        
        with col2:
            if st.button("Save Session", key="save_btn") and len(st.session_state.messages) > 1:
                filename = SessionManager.save_session()
                st.success(f"Session saved as: {filename}")
        
        # Session loading
        saved_sessions = SessionManager.list_saved_sessions()
        if saved_sessions:
            selected_session = st.selectbox("Load Previous Session", ["Select a session..."] + saved_sessions)
            
            if selected_session != "Select a session..." and st.button("Load Session"):
                if SessionManager.load_session(selected_session):
                    st.success(f"Session '{selected_session}' loaded successfully!")
                    st.experimental_rerun()



# Main content area
st.title("TalentScout Hiring Assistant")
st.markdown("An intelligent chatbot for initial candidate screening")

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if "gemini_client" in st.session_state and st.session_state.gemini_client and st.session_state.gemini_client.is_initialized():
        if not st.session_state.conversation_ended:
            # Initialize conversation handler
            conversation_handler = ConversationHandler(st.session_state.gemini_client)
            
            # If this is the first message, initiate the conversation
            if not st.session_state.messages:
                # Generate initial greeting
                prompt = PromptGenerator.create_prompt(
                    "greeting", 
                    st.session_state.candidate_info,
                    st.session_state.language
                )
                
                # Get response from model
                try:
                    response_text = ""
                    for chunk in st.session_state.gemini_client.generate_content(prompt, st.session_state.messages):
                        if chunk.text:
                            response_text += chunk.text
                    
                    # Display the initial greeting
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    # Update session state
                    st.session_state.current_stage = "greeting"
                    
                    st.experimental_rerun()
                
                except Exception as e:
                    st.error(f"Error generating initial greeting: {str(e)}")
  
            
            # Get user input
            user_input = st.chat_input("Type your message here...")
            
            if user_input:
                # Process the message and get the response
                conversation_handler.process_message(user_input)
                st.experimental_rerun()
        else:
            st.info("The conversation has ended. You can start a new conversation using the 'Reset Conversation' button in the sidebar.")
    else:
        st.info("Please enter your Gemini API Key in the sidebar to start the conversation.")



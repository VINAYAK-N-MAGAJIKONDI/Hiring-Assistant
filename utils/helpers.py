import re
import streamlit as st
import os
import json
from datetime import datetime

def format_timestamp(timestamp_str):
    """Format an ISO timestamp string to a readable format."""
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        return timestamp.strftime("%b %d, %Y %I:%M %p")
    except:
        return timestamp_str

def extract_email(text):
    """Extract an email address from text."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    """Extract a phone number from text."""
    # Remove non-numeric characters
    digits = re.sub(r'\D', '', text)
    
    # Check for typical phone number patterns
    if len(digits) >= 10:
        return digits[-10:]  # Return last 10 digits
    
    return None

def sanitize_filename(name):
    """Convert a string to a valid filename."""
    # Replace spaces and special characters
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_').lower()

def load_custom_css():
    """Load custom CSS for the Streamlit app."""
    css_file = "assets/custom.css"
    
    # Create directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Check if file exists, create it if not
    if not os.path.exists(css_file):
        with open(css_file, "w") as f:
            f.write("""
            /* Custom CSS for TalentScout Hiring Assistant */
            .main {
                background-color: #F5F7F9;
            }
            
            .stApp {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            /* Chat message styling */
            .user-message {
                background-color: #E8F4FD;
                border-radius: 15px 15px 3px 15px;
                padding: 10px 15px;
                margin-bottom: 10px;
                position: relative;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            
            .assistant-message {
                background-color: #F0F2F5;
                border-radius: 15px 15px 15px 3px;
                padding: 10px 15px;
                margin-bottom: 10px;
                position: relative;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            
            /* Loading animation */
            .typing-indicator {
                display: inline-block;
                animation: blink 1s infinite;
            }
            
            @keyframes blink {
                0% { opacity: 0.2; }
                20% { opacity: 1; }
                100% { opacity: 0.2; }
            }
            
            /* Sidebar styling */
            .sidebar .block-container {
                padding-top: 2rem;
            }
            
            /* Button styling */
            button {
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
            }
            
            /* Candidate info panel */
            .candidate-info {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                margin-bottom: 20px;
            }
            
            .tech-tag {
                display: inline-block;
                background-color: #E1F5FE;
                color: #0277BD;
                padding: 4px 8px;
                border-radius: 12px;
                margin: 2px;
                font-size: 0.8rem;
            }
            """)
    
    # Load the CSS
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

import os
from google import genai
from google.genai import types
import streamlit as st
from config import GEMINI_API_KEY, GEMINI_MODEL

class GeminiClient:
    """Class to handle communication with the Gemini API."""
    
    def __init__(self, api_key=None):
        """Initialize the Gemini client with API key."""
        self.api_key = api_key or GEMINI_API_KEY
        self.model = GEMINI_MODEL
        self.client = None
        self.initialize()
    
    def initialize(self):
        """Initialize the Gemini client."""
        try:
            if not self.api_key:
                st.error("Gemini API key is missing. Please set it in the .env file or provide it in the UI.")
                return False
            
            self.client = genai.Client(api_key=self.api_key)
            return True
        except Exception as e:
            st.error(f"Failed to initialize Gemini client: {str(e)}")
            return False
    
    def is_initialized(self):
        """Check if the client is initialized."""
        return self.client is not None
    
    def generate_content(self, prompt, messages=None, temperature=0.7, max_tokens=8192):
        """Generate content using the Gemini API with streaming enabled."""
        if not self.is_initialized():
            return "Error: Gemini client is not initialized."
        
        try:
            # Create content from prompt
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ]
            
            # Add conversation history if provided
            if messages:
                for msg in messages:
                    contents.append(
                        types.Content(
                            role="user" if msg["role"] == "user" else "model",
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
            
            # Configure generation parameters
            config = types.GenerateContentConfig(
                temperature=temperature,
                top_p=0.95,
                top_k=40,
                max_output_tokens=max_tokens,
                response_mime_type="text/plain",
            )
            
            # Return a generator for streaming responses
            return self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=config,
            )
        
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            return None

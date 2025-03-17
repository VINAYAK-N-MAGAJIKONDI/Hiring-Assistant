import re
import streamlit as st
from src.prompt_generator import PromptGenerator
from src.tech_analyzer import TechAnalyzer
from src.sentiment_analyzer import SentimentAnalyzer
from src.language_detector import LanguageDetector
from datetime import datetime

class ConversationHandler:
    """Class to handle the chatbot conversation flow."""
    
    def __init__(self, gemini_client):
        """Initialize the conversation handler with the Gemini client."""
        self.gemini_client = gemini_client
        self.tech_analyzer = TechAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.language_detector = LanguageDetector()
    
    def process_message(self, message , display_prompt=True):
        """Process the candidate's message and update the chatbot state."""
        # Skip empty messages
        if not message or message.strip() == "":
            return None
        
        # Check for conversation ending keywords
        if re.search(r'\b(quit|exit|bye|end)\b', message.lower()):
            st.session_state.current_stage = "conclusion"
        

        if display_prompt:
            st.session_state.messages.append({"role": "user", "content": message, "timestamp": datetime.now().isoformat()})
        
        # Process sentiment
        sentiment = self.sentiment_analyzer.analyze_sentiment(message)
        st.session_state.sentiment_data.append({
            "message": message,
            "sentiment": sentiment["label"],
            "score": sentiment["score"],
            "timestamp": datetime.now().isoformat()
        })
        

        
        # Process based on current stage
        self._process_stage_specific_message(message)
        
        # Generate response
        return self._generate_response(message, sentiment)
    
    def _process_stage_specific_message(self, message):
        """Process the message based on the current conversation stage."""
        
        if st.session_state.current_stage == "greeting" and st.session_state.candidate_info["name"] is None:
            # Extract name from greeting
            name_match = re.search(r'\b(?:my name is|i am|i\'m|this is)\s+([A-Za-z\s]+)', message, re.IGNORECASE)
            if name_match:
                st.session_state.candidate_info["name"] = name_match.group(1).strip()
            else:
                st.session_state.candidate_info["name"] = message.strip()
            st.session_state.current_stage = "gather_info"
        
        elif st.session_state.current_stage == "gather_info":
            # Extract missing information
            if not st.session_state.candidate_info["email"] and re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message):
                st.session_state.candidate_info["email"] = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message).group(0)
            elif not st.session_state.candidate_info["phone"] and re.search(r'\b\d{10}\b', message.replace("-", "").replace(" ", "")):
                st.session_state.candidate_info["phone"] = re.search(r'\b\d{10}\b', message.replace("-", "").replace(" ", "")).group(0)
            elif not st.session_state.candidate_info["experience"]:
                # Try to extract years of experience
                if any(word in message.lower() for word in ["year", "years", "yrs", "experience"]):
                    st.session_state.candidate_info["experience"] = re.search(r'\b\d+\s*(?:year|years|yrs|experience)\b', message, re.IGNORECASE).group(0)
            elif not st.session_state.candidate_info["position"]:
                st.session_state.candidate_info["position"] = message
            elif not st.session_state.candidate_info["location"]:
                st.session_state.candidate_info["location"] = message
                
                # Check if we've collected all basic info to move to tech stack
                if all(st.session_state.candidate_info[k] is not None for k in ["name", "email", "phone", "experience", "position", "location"]):
                    st.session_state.current_stage = "tech_stack"
        
        elif st.session_state.current_stage == "tech_stack":
            # Extract tech stack from message
            found_techs = self.tech_analyzer.extract_tech(message)
            if found_techs:
                st.session_state.candidate_info["tech_stack"].extend(found_techs)
                # Remove duplicates
                st.session_state.candidate_info["tech_stack"] = list(set(st.session_state.candidate_info["tech_stack"]))
            
            # Check if we should move to technical questions
            confirmation_keywords = ["confirm", "yes", "that's it", "that is it", "correct", "right", "looks good"]
            if any(keyword in message.lower() for keyword in confirmation_keywords) and st.session_state.candidate_info["tech_stack"]:
                st.session_state.current_stage = "technical_questions"
        
        elif st.session_state.current_stage == "technical_questions":
            # Store the candidate's answer to technical questions
            if st.session_state.tech_questions_generated:
                st.session_state.technical_assessment["answers"].append(message)
            
            # Check if technical assessment is complete
            complete_keywords = [ "end", "thank you"]
            if st.session_state.tech_questions_generated and any(keyword in message.lower() for keyword in complete_keywords):
                st.session_state.current_stage = "conclusion"
                st.session_state.technical_assessment["completed"] = True
    
    def _generate_response(self, message, sentiment):
        """Generate a response using the Gemini model."""
        # If client is not initialized, return error message
        if not self.gemini_client or not self.gemini_client.is_initialized():
            return "I'm currently unavailable. Please check your API key and try again."
        
        # Create the prompt based on current stage and candidate information
        prompt = PromptGenerator.create_prompt(
            st.session_state.current_stage, 
            st.session_state.candidate_info,
            st.session_state.language,
            sentiment
        )
        
        # Get response from model
        try:
            # Show typing indicator in UI
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.text("Thinking...")
                
                full_response = ""
                
                # Stream the response
                for chunk in self.gemini_client.generate_content(prompt, st.session_state.messages):
                    if chunk.text:
                        full_response += chunk.text
                        # Update the response in real-time
                        message_placeholder.markdown(full_response + "▌")
                
                # Display the final response
                message_placeholder.markdown(full_response)
            
            # Add assistant message to the history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Update stage based on bot response
            self._update_stage_from_response(full_response)
            
            return full_response
            
        except Exception as e:
            error_message = f"I'm sorry, there was an error generating a response: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_message,
                "timestamp": datetime.now().isoformat()
            })
            return error_message
    
    def _update_stage_from_response(self, response):
        """Update the conversation stage based on the bot's response."""
        
        # Check if we're transitioning from tech stack to technical questions
        if st.session_state.current_stage == "tech_stack" and any(phrase in response.lower() for phrase in ["technical question", "assess your knowledge", "let's test"]):
            st.session_state.current_stage = "technical_questions"
            st.session_state.tech_questions_generated = True
        
        # Check if we've reached the conclusion
        elif st.session_state.current_stage == "conclusion":
            st.session_state.conversation_ended = True
            
            # Extract technical assessment scores if available
            if "overall score" in response.lower() or "score:" in response.lower():
                score_pattern = r'(\d+(\.\d+)?)\s*\/\s*5'
                scores = re.findall(score_pattern, response)
                if scores:
                    overall_score = float(scores[0][0])
                    st.session_state.technical_assessment["overall_score"] = overall_score

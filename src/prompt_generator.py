from config import STAGES

class PromptGenerator:
    """Class to generate prompts for different conversation stages."""
    
    
    @staticmethod
    def create_prompt(stage, candidate_info, language=None, sentiment=None):
        """Create a prompt based on the current conversation stage and candidate info."""
        base_prompt = """
        You are a professional Hiring Assistant chatbot for TalentScout named "TalentScout HA", a recruitment agency specializing in technology placements. 
        Your task is to conduct an initial screening of candidates by gathering information and asking relevant technical questions.
        
        Follow these guidelines for the conversation:
        1. Maintain a professional, friendly tone throughout the conversation.
        2. Only ask one question at a time and wait for the candidate's response.
        3. Don't make up information about the candidate.
        4. If the candidate mentions "quit", "exit", "bye", or "end", gracefully end the conversation.
        5. Focus on gathering accurate information and asking relevant technical questions.
        
        Current information collected about the candidate:
        """
        
        # Add the current information we have
        for key, value in candidate_info.items():
            if value:
                if key == "tech_stack" and len(value) > 0:
                    base_prompt += f"\n- {key}: {', '.join(value)}"
                else:
                    base_prompt += f"\n- {key}: {value}"
        
        # Add language instruction if provided
        if language and language != "en":
            base_prompt += f"\n\nThe candidate's preferred language is {language}. Please communicate in this language."
        
        # Add sentiment-based instruction if provided
        if sentiment and sentiment.get("label") == "negative" and sentiment.get("score", 0) < -0.3:
            base_prompt += "\n\nThe candidate seems to be expressing negative sentiment. Please be more empathetic and supportive in your response."
        
        # Add stage-specific instructions
        stage_prompts = {
            "greeting": PromptGenerator._greeting_prompt(),
            "gather_info": PromptGenerator._gather_info_prompt(candidate_info),
            "tech_stack": PromptGenerator._tech_stack_prompt(),
            "technical_questions": PromptGenerator._technical_questions_prompt(candidate_info),
            "conclusion": PromptGenerator._conclusion_prompt()
        }
        
        if stage in stage_prompts:
            base_prompt += stage_prompts[stage]
        
        return base_prompt
    
    @staticmethod
    def _greeting_prompt():
        """Generate the greeting stage prompt."""
        return """
        
        You are at the GREETING stage.
        1. Greet the candidate warmly.
        2. Introduce yourself as a Hiring Assistant for TalentScout.
        3. Explain that you'll be asking some questions to understand their background and skills.
        4. Ask for their full name to begin the process.
        Start with "Hello!...."
        """
    
    @staticmethod
    def _gather_info_prompt(candidate_info):
        """Generate the information gathering stage prompt."""
        # Determine what information we still need
        missing_info = []
        if not candidate_info.get("email"):
            missing_info.append("email address")
        if not candidate_info.get("phone"):
            missing_info.append("phone number")
        if not candidate_info.get("experience"):
            missing_info.append("years of experience")
        if not candidate_info.get("position"):
            missing_info.append("desired position(s)")
        if not candidate_info.get("location"):
            missing_info.append("current location")
        
        return f"""
        
        You are at the GATHER_INFO stage.
        Current missing information: {', '.join(missing_info) if missing_info else "None"}
        
        If information is missing:
        1. Ask for ONE piece of missing information at a time, following the order: email, phone, experience, position, location.
        2. After receiving the information, acknowledge it and proceed to the next missing item.
        
        If all basic information is collected:
        1. Thank the candidate for providing their information.
        2. Transition to asking about their tech stack (programming languages, frameworks, databases, tools they're proficient in).
        3. Move to the TECH_STACK stage once you ask about their tech stack.
        """
    
    @staticmethod
    def _tech_stack_prompt():
        """Generate the tech stack stage prompt."""
        return """
        
        You are at the TECH_STACK stage.
        1. If the tech stack is empty, ask the candidate about their technical skills, including programming languages, frameworks, databases, and tools they're proficient in.
        2. Parse their response to identify technologies and add them to the tech stack.
        3. Confirm the tech stack with the candidate and ask if they want to add anything else.
        4. Once the tech stack is confirmed, move to the TECHNICAL_QUESTIONS stage.
        """
    
    @staticmethod
    def _technical_questions_prompt(candidate_info):
        """Generate the technical questions stage prompt."""
        exp_years = 0
        if candidate_info.get("experience"):
            # Try to extract numeric years from experience
            import re
            years_match = re.search(r'(\d+)', candidate_info.get("experience", ""))
            if years_match:
                exp_years = int(years_match.group(1))
        
        difficulty = "intermediate"
        if exp_years < 2:
            difficulty = "beginner"
        elif exp_years > 5:
            difficulty = "advanced"
        
        return f"""
        
        You are at the TECHNICAL_QUESTIONS stage.
        1. Based on the candidate's tech stack, generate 3-5 relevant technical questions to assess their proficiency.
        2. The candidate has approximately {exp_years} years of experience, so questions should be at a {difficulty} level.
        3. Present the questions one by one, waiting for the candidate's response before moving to the next question.
        4. After each response, provide a brief evaluation of the answer (was it correct, partially correct, incorrect) and assign a score from 1-5.
        5. After all questions are answered, provide a summary of the technical assessment.
        6. Move to the CONCLUSION stage after the assessment is complete.
        
        IMPORTANT: Generate specific technical questions for each technology in their stack. Do not ask generic questions.
        For example:
        - For Python: Ask about specific Python features, common patterns, or problem-solving approaches.
        - For React: Ask about component lifecycle, state management, or performance optimization.
        - For databases: Ask about query optimization, normalization, or specific database features.
        """
    
    @staticmethod
    def _conclusion_prompt():
        """Generate the conclusion stage prompt."""
        return """
        
        You are at the CONCLUSION stage.
        1. Thank the candidate for their time and responses.
        2. Summarize the key points from the conversation, including their experience and technical skills.
        3. Inform them that their information and responses will be reviewed by the TalentScout team.
        4. Let them know that they will be contacted if their profile matches current opportunities.
        5. Wish them well and end the conversation professionally.
        """

import re
from config import TECH_KEYWORDS

class TechAnalyzer:
    """Class for analyzing and extracting technical skills from text."""
    
    def __init__(self):
        """Initialize with available tech keywords from config."""
        self.all_keywords = []
        for category in TECH_KEYWORDS.values():
            self.all_keywords.extend(category)
    
    def extract_tech(self, text):
        """Extract technical skills from a text message."""
        text = text.lower()
        
        # Extract known keywords
        found_techs = []
        
        # Direct matching of keywords
        for tech in self.all_keywords:
            # Match whole words only (using word boundaries)
            if re.search(r'\b' + re.escape(tech) + r'\b', text):
                found_techs.append(tech)
        
        # Special case handling for common abbreviations and variations
        special_cases = {
            "javascript": ["js"],
            "typescript": ["ts"],
            "python": ["py"],
            "react.js": ["react", "reactjs"],
            "node.js": ["node", "nodejs"],
            "express.js": ["express", "expressjs"],
            "postgresql": ["postgres"],
            "kubernetes": ["k8s"],
            "continuous integration": ["ci"],
            "continuous deployment": ["cd"],
            "machine learning": ["ml"],
            "artificial intelligence": ["ai"],
            "natural language processing": ["nlp"]
        }
        
        # Check for special cases
        for full_name, abbreviations in special_cases.items():
            for abbr in abbreviations:
                if abbr in found_techs and full_name not in found_techs:
                    found_techs.remove(abbr)
                    found_techs.append(full_name)
        
        return found_techs
    
    def categorize_tech_stack(self, tech_list):
        """Categorize a list of technologies by type."""
        categorized = {}
        
        for category, keywords in TECH_KEYWORDS.items():
            category_name = category.replace("_", " ").title()
            categorized[category_name] = []
            
            for tech in tech_list:
                if tech.lower() in keywords:
                    categorized[category_name].append(tech)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def suggest_related_technologies(self, tech_list):
        """Suggest related technologies based on the current tech stack."""
        suggestions = []
        
        # Common technology relationships
        tech_relationships = {
            "react": ["redux", "typescript", "next.js", "graphql"],
            "python": ["django", "flask", "fastapi", "pandas", "numpy"],
            "javascript": ["typescript", "react", "vue", "node.js"],
            "node.js": ["express.js", "nestjs", "mongodb", "graphql"],
            "java": ["spring", "hibernate", "maven", "junit"],
            "aws": ["ec2", "s3", "lambda", "cloudformation"],
            "docker": ["kubernetes", "docker-compose", "ci/cd"],
            "machine learning": ["tensorflow", "pytorch", "scikit-learn", "pandas"]
        }
        
        # Check for related technologies
        for tech in tech_list:
            if tech.lower() in tech_relationships:
                for related in tech_relationships[tech.lower()]:
                    if related not in tech_list and related not in suggestions:
                        suggestions.append(related)
        
        return suggestions[:5]  # Limit to top 5 suggestions

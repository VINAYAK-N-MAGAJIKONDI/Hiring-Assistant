import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

# App configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Conversation stages
STAGES = [
    "greeting",
    "gather_info",
    "tech_stack",
    "technical_questions",
    "conclusion"
]

# Technical keywords for tech stack detection
TECH_KEYWORDS = {
    "programming_languages": [
        "python", "java", "javascript", "js", "typescript", "ts", "c#", "c++", 
        "ruby", "go", "rust", "swift", "kotlin", "php", "perl", "r", "scala", 
        "dart", "julia", "haskell", "elixir", "clojure"
    ],
    "web_frameworks": [
        "react", "angular", "vue", "svelte", "nextjs", "nuxt", "django", "flask", 
        "spring", "express", "fastapi", "laravel", "rails", "asp.net", "blazor"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "dynamodb", 
        "cassandra", "redis", "neo4j", "couchdb", "firebase", "supabase"
    ],
    "cloud_services": [
        "aws", "azure", "gcp", "google cloud", "firebase", "heroku", "vercel", 
        "netlify", "digitalocean", "cloudflare"
    ],
    "devops_tools": [
        "docker", "kubernetes", "k8s", "jenkins", "gitlab", "github actions", 
        "terraform", "ansible", "puppet", "chef", "prometheus", "grafana"
    ],
    "mobile": [
        "android", "ios", "react native", "flutter", "xamarin", "ionic", "swift", 
        "kotlin", "objective-c"
    ],
    "ai_ml": [
        "tensorflow", "pytorch", "keras", "sklearn", "scikit-learn", "machine learning", 
        "ml", "ai", "deep learning", "nlp", "computer vision", "cv"
    ],
    "other_tools": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence", "slack", 
        "notion", "figma", "adobe", "photoshop", "illustrator"
    ]
}

# Language settings
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Hindi": "hi",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar"
}

# UI settings
UI_THEME = {
    "primary_color": "#1E88E5",
    "background_color": "#F5F7F9",
    "secondary_color": "#FFC107",
    "text_color": "#212121",
    "accent_color": "#FF5722"
}

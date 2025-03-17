from langdetect import detect, LangDetectException
import pycountry

class LanguageDetector:
    """Class for detecting and handling multiple languages."""
    
    def detect_language(self, text):
        """Detect the language of a text."""
        if not text or len(text.strip()) < 10:
            return None
            
        try:
            # Detect language code
            lang_code = detect(text)
            return lang_code
        except LangDetectException:
            return None
    
    def get_language_name(self, lang_code):
        """Convert a language code to its full name."""
        try:
            language = pycountry.languages.get(alpha_2=lang_code)
            return language.name if language else "Unknown"
        except:
            # Fallback for common languages
            language_map = {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "zh": "Chinese",
                "ja": "Japanese",
                "hi": "Hindi",
                "pt": "Portuguese",
                "ru": "Russian",
                "ar": "Arabic"
            }
            return language_map.get(lang_code, "Unknown")
    
    def should_translate(self, text, preferred_language):
        """Determine if translation is needed."""
        detected = self.detect_language(text)
        
        # If detection failed or matches preference, no translation needed
        if not detected or detected == preferred_language:
            return False
            
        return True

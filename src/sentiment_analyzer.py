from textblob import TextBlob

class SentimentAnalyzer:
    """Class for analyzing sentiment in text."""
    
    def analyze_sentiment(self, text):
        """Analyze the sentiment of text and return the polarity score."""
        try:
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            
            # Determine sentiment label
            if sentiment_score > 0.2:
                label = "positive"
            elif sentiment_score < -0.2:
                label = "negative"
            else:
                label = "neutral"
            
            # Also include subjectivity score
            subjectivity = blob.sentiment.subjectivity
            
            return {
                "score": sentiment_score,
                "label": label,
                "subjectivity": subjectivity
            }
        
        except Exception as e:
            # Return neutral sentiment in case of errors
            return {
                "score": 0,
                "label": "neutral",
                "subjectivity": 0,
                "error": str(e)
            }
    
    def get_average_sentiment(self, messages):
        """Calculate average sentiment across multiple messages."""
        if not messages:
            return {"score": 0, "label": "neutral", "subjectivity": 0}
        
        total_score = 0
        total_subjectivity = 0
        
        for message in messages:
            sentiment = self.analyze_sentiment(message)
            total_score += sentiment["score"]
            total_subjectivity += sentiment.get("subjectivity", 0)
        
        avg_score = total_score / len(messages)
        avg_subjectivity = total_subjectivity / len(messages)
        
        # Determine average sentiment label
        if avg_score > 0.2:
            label = "positive"
        elif avg_score < -0.2:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "score": avg_score,
            "label": label,
            "subjectivity": avg_subjectivity
        }

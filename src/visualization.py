import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import plotly.express as px
from datetime import datetime

class Visualization:
    """Class for creating visualizations of conversation data."""
    
    @staticmethod
    def create_sentiment_graph(sentiment_data):
        """Create a sentiment trend graph."""
        if not sentiment_data:
            return None
            
        # Create DataFrame from sentiment data
        df = pd.DataFrame(sentiment_data)
        
        # Add numeric index for x-axis
        df['index'] = range(len(df))
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create interactive plot with Plotly
        fig = px.line(
            df, 
            x='index', 
            y='score', 
            labels={'index': 'Message Number', 'score': 'Sentiment Score'},
            title='Sentiment Trend During Conversation',
            color_discrete_sequence=['#1E88E5'],
            markers=True
        )
        
        # Add horizontal line at zero
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Message Sequence",
            yaxis_title="Sentiment (-1 to +1)",
            hovermode="x unified",
            yaxis=dict(range=[-1.1, 1.1])
        )
        
        return fig
    
    @staticmethod
    def create_wordcloud(messages):
        """Create a word cloud from conversation messages."""
        if not messages:
            return None
            
        # Extract user messages
        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        
        if not user_messages:
            return None
            
        # Combine all messages
        text = " ".join(user_messages)
        
        # Generate wordcloud
        wordcloud = WordCloud(
            width=400, 
            height=200, 
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(text)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        
        return fig
    
    @staticmethod
    def create_technical_assessment_chart(assessment):
        """Create a chart showing technical assessment scores."""
        if not assessment or not assessment.get("scores"):
            return None
            
        # Create DataFrame from scores
        df = pd.DataFrame([
            {"Technology": tech, "Score": score} 
            for tech, score in assessment["scores"].items()
        ])
        
        # Create bar chart
        fig = px.bar(
            df, 
            x='Technology', 
            y='Score',
            labels={'Technology': 'Technology', 'Score': 'Score (1-5)'},
            title='Technical Assessment Scores',
            color='Score',
            color_continuous_scale='Viridis',
            range_y=[0, 5.5]  # Score range from 0 to 5
        )
        
        # Add horizontal lines for score ranges
        for i in range(1, 6):
            fig.add_hline(y=i, line_dash="dot", line_color="gray", opacity=0.5)
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Technology",
            yaxis_title="Score (1-5)",
            coloraxis_showscale=False
        )
        
        return fig

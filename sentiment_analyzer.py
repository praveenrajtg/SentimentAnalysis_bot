from textblob import TextBlob
import random
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self):
        self.responses = {
            'positive': [
                "I'm so glad to hear that! How can I help you further?",
                "That's wonderful! I'm here to assist you with anything else.",
                "Great to hear! What else can I do for you today?",
                "Fantastic! I'm happy to help with your next question."
            ],
            'negative': [
                "I understand you're frustrated. Let me help resolve this for you.",
                "I'm sorry you're experiencing this. I'm here to help make things better.",
                "I hear your concern and I want to help. Let's work through this together.",
                "I apologize for any inconvenience. How can I assist you better?"
            ],
            'neutral': [
                "I'm here to help! What can I assist you with?",
                "How can I help you today?",
                "What would you like to know?",
                "I'm ready to assist you with your questions."
            ]
        }
    
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'positive', polarity
        elif polarity < -0.1:
            return 'negative', polarity
        else:
            return 'neutral', polarity
    
    def get_response(self, sentiment):
        return random.choice(self.responses[sentiment])
    
    def process_message(self, user_message):
        sentiment, score = self.analyze_sentiment(user_message)
        bot_response = self.get_response(sentiment)
        
        return {
            'timestamp': datetime.now(),
            'user_message': user_message,
            'sentiment': sentiment,
            'score': round(score, 3),
            'bot_response': bot_response
        }
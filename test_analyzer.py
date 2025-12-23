from sentiment_analyzer import SentimentAnalyzer

def test_sentiment_analysis():
    analyzer = SentimentAnalyzer()
    
    # Test cases
    test_messages = [
        "I love this service! It's amazing!",
        "This is terrible, nothing works!",
        "What are your business hours?",
        "Thank you so much for your help!",
        "I'm really frustrated with this issue."
    ]
    
    print("Sentiment Analysis Test Results:")
    print("=" * 50)
    
    for message in test_messages:
        result = analyzer.process_message(message)
        print(f"\nMessage: '{message}'")
        print(f"Sentiment: {result['sentiment'].upper()} (Score: {result['score']})")
        print(f"Response: {result['bot_response']}")
        print("-" * 30)

if __name__ == "__main__":
    test_sentiment_analysis()
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
print("sentiment_analyzer at work")

analyzer = SentimentIntensityAnalyzer()

def get_vader_sentiment(text):
    if not isinstance(text, str):
        return "neutral"
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

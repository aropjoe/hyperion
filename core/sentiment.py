import nltk

nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def analyze_sentiment(text):
    # Instantiate the SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
    # Analyze the sentiment of the text
    sentiment = sia.polarity_scores(text)
    # Return the sentiment score
    return sentiment

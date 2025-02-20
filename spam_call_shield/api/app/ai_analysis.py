import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Load NLP models
nlp = spacy.load("en_core_web_sm")
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Suspicious keywords
SUSPICIOUS_KEYWORDS = ["OTP", "CVV", "password", "bank details", "AnyDesk", "TeamViewer", "install app", "remote access"]

# Detect suspicious content
def analyze_text(text):
    doc = nlp(text)
    sentiment = sia.polarity_scores(text)
    suspicious = any(word.lower() in text.lower() for word in SUSPICIOUS_KEYWORDS)
    reason = None

    if suspicious:
        for keyword in SUSPICIOUS_KEYWORDS:
            if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
                reason = f"Mentioned suspicious keyword: {keyword}"
                break

    elif sentiment['neg'] > 0.5:
        reason = "Negative sentiment detected"
        suspicious = True

    return suspicious, reason

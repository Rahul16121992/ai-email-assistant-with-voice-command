from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Better training data
texts = [
    # Important
    "urgent meeting tomorrow",
    "project deadline update",
    "team meeting schedule",
    "important notice regarding work",

    # Spam
    "win money lottery now",
    "claim your prize click link",
    "free cash offer limited time",
    "you won lottery urgent response",

    # Promotional
    "big discount sale offer",
    "buy one get one free",
    "limited time shopping deal",
    "special promotion for you"
]

labels = [
    "important", "important", "important", "important",
    "spam", "spam", "spam", "spam",
    "promotional", "promotional", "promotional", "promotional"
]

# Model training
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

def classify_email(text):
    text = text.lower()
    X_test = vectorizer.transform([text])
    return model.predict(X_test)[0]
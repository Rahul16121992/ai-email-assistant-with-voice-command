import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def summarize(text):
    sentences = sent_tokenize(text)
    return " ".join(sentences[:2])
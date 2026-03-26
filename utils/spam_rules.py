def is_spam(text):
    text = text.lower()

    spam_keywords = [
        "lottery", "win", "prize", "click", "free",
        "money", "offer", "claim", "cash",
        "reward", "bonus"
    ]

    for word in spam_keywords:
        if word in text:
            return True

    return False
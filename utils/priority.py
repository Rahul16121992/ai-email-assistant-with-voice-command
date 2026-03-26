def get_priority(text):
    text = text.lower()
    score = 0

    if "urgent" in text:
        score += 40
    if "meeting" in text:
        score += 30
    if "deadline" in text:
        score += 30

    return min(score, 100)
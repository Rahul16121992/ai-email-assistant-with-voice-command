def generate_reply(text):
    text = text.lower()

    if "meeting" in text:
        return "I will attend the meeting."

    elif "project" in text:
        return "I will review the project."

    elif "deadline" in text:
        return "I will complete it before the deadline."

    else:
        return "Thanks for your email. I will get back to you soon."
def handle_command(text):
    text = text.lower()

    if "spam" in text:
        return "Showing spam emails"

    elif "important" in text:
        return "Showing important emails"

    elif "delete" in text:
        return "Deleting emails"

    elif "summary" in text:
        return "Summarizing email"

    else:
        return "Command not recognized"
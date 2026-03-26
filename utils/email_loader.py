import pandas as pd

def load_emails():
    try:
        df = pd.read_csv("data/emails.csv")
        return df
    except:
        return None
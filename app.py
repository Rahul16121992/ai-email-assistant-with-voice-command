import streamlit as st
from utils.classifier import classify_email
from utils.summarizer import summarize
from utils.priority import get_priority
from utils.reply import generate_reply
from utils.spam_rules import is_spam
from utils.email_loader import load_emails
from utils.voice import speak

# Voice input
try:
    from utils.voice_input import listen
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

st.set_page_config(page_title="AI Email Assistant Pro", layout="wide")

# CSS
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f172a, #1e3a8a, #7f1d1d, #1e40af);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* REMOVE HEADER */
[data-testid="stHeader"] {
    background: transparent;
}

/* GLOBAL WHITE TEXT */
html, body, [class*="css"] {
    color: white !important;
}

/* GLASS CARD */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    color: white;
    margin-bottom: 20px;
}

/* 🔥 TEXTAREA FINAL PERFECT FIX */
textarea {
    border-radius: 12px !important;
    background-color: white !important;  /* white box */
    color: black !important;             /* black text */
    font-weight: 500;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(45deg, #2563eb, #dc2626);
    color: white;
    border-radius: 12px;
    padding: 12px 25px;
    font-weight: bold;
}

.stButton>button:hover {
    transform: scale(1.1);
}

</style>
""", unsafe_allow_html=True)

# HEADER
col_logo, col_title = st.columns([1,5])

with col_logo:
    st.image("email_icon.png", width=80)

with col_title:
    st.markdown('<h1 style="color:white;">AI Email Assistant PRO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:white;">Smart • Offline • Voice Enabled</p>', unsafe_allow_html=True)

emails_df = load_emails()

col1, col2 = st.columns([2, 1])

# LEFT PANEL
with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.markdown('<h3 style="color:white;">✉️ Enter Email</h3>', unsafe_allow_html=True)

    email_text = st.text_area("", height=150)

    c1, c2 = st.columns(2)

    with c1:
        analyze = st.button("🚀 Analyze")

    with c2:
        speak_btn = st.button("🎤 Speak")

    if analyze:
        if email_text.strip() == "":
            st.warning("Enter email content")
        else:
            if is_spam(email_text):
                category = "spam"
            else:
                category = classify_email(email_text)

            summary = summarize(email_text)
            priority = get_priority(email_text)
            reply = generate_reply(email_text)

            st.markdown(f'<div class="glass">📌 Category: {category}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass">📝 {summary}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass">🔥 Priority: {priority}/100</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass">💬 {reply}</div>', unsafe_allow_html=True)

            speak("Email analyzed")

    # VOICE
    if speak_btn:
        if not VOICE_AVAILABLE:
            st.warning("Mic not available")
        else:
            text = listen()
            st.write("You said:", text)

            if emails_df is not None:

                if "important" in text.lower():
                    imp = []
                    for _, row in emails_df.iterrows():
                        mail = row["subject"] + " " + row["body"]
                        if not is_spam(mail) and classify_email(mail) == "important":
                            imp.append(mail)

                    st.markdown('<div class="glass"><h3>📌 Important Emails</h3></div>', unsafe_allow_html=True)
                    for m in imp:
                        st.markdown(f"<p style='color:white;'>• {m}</p>", unsafe_allow_html=True)

                    speak("Showing important emails")

                elif "spam" in text.lower():
                    spam_list = []
                    for _, row in emails_df.iterrows():
                        mail = row["subject"] + " " + row["body"]
                        if is_spam(mail):
                            spam_list.append(mail)

                    st.markdown('<div class="glass"><h3>⚠️ Spam Emails</h3></div>', unsafe_allow_html=True)
                    for m in spam_list:
                        st.markdown(f"<p style='color:white;'>• {m}</p>", unsafe_allow_html=True)

                    speak("Showing spam emails")

    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT PANEL
with col2:
    if emails_df is not None:
        total = len(emails_df)
        spam = 0
        important = 0

        for _, row in emails_df.iterrows():
            text = row["subject"] + " " + row["body"]

            if is_spam(text):
                spam += 1
            elif classify_email(text) == "important":
                important += 1

        st.markdown(f"""
        <div class="glass">
        <h2>📊 Dashboard</h2>
        <h3>📂 Total Emails: {total}</h3>
        <h3>⚠️ Spam Emails: {spam}</h3>
        <h3>📌 Important Emails: {important}</h3>
        </div>
        """, unsafe_allow_html=True)

# DATA
st.markdown('<div class="glass">📁 Email Dataset</div>', unsafe_allow_html=True)

if emails_df is not None:
    st.dataframe(emails_df)
import pyttsx3
import threading

def speak(text):
    def run_speech():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)   # speed control
            engine.setProperty('volume', 1.0) # volume (0.0 to 1.0)

            engine.say(text)
            engine.runAndWait()

        except Exception as e:
            print("Voice Error:", e)

    # Run in separate thread to avoid Streamlit loop error
    thread = threading.Thread(target=run_speech)
    thread.start()
# aceapp_complete.py
import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
import csv
import os
from datetime import datetime

# ---------- CONFIGURATION ----------
AGENT_NAME = "Ace"
AGENT_ROLE = "Customer Support Specialist"
AGENT_MISSION = "Ace assists clients with care, clarity, and consistency—whether they have questions about services, want to check the status of a dispute, or need a little extra motivation."
ADMIN_USERNAME = "admin53"
CSV_LOG_FILE = "ace_convo_log.csv"
UPLOAD_FOLDER = "uploaded_documents"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- VOICE SETUP ----------
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

# ---------- CHAT FUNCTION ----------
def query_ollama(prompt):
    try:
        full_prompt = f"You are Ace, a professional and friendly customer support rep for a credit repair business. You help clients understand credit repair, upload documents, answer questions, and keep them encouraged. If the user asks something outside your role, refer them to Valor the CEO.\n\nQuestion: {prompt}\n\nAnswer:"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": full_prompt, "stream": False},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Oops! Ace ran into a technical issue.\n\n(Error: {e})"

# ---------- LOGGING ----------
def save_convo_log(user_input, ace_response):
    with open(CSV_LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), user_input, ace_response])

# ---------- APP UI ----------
st.set_page_config(page_title="Meet Ace", layout="centered")
st.title(f"🤖 Meet {AGENT_NAME} – Your {AGENT_ROLE}")
st.markdown(f"**Role:** {AGENT_ROLE}")
st.markdown(f"**Mission:** {AGENT_MISSION}")

# Admin Login
admin_mode = False
if st.text_input("🔐 Enter Admin Username:", type="password") == ADMIN_USERNAME:
    st.success("Admin mode activated")
    admin_mode = True

# Voice Input
if st.button("🎙️ Speak to Ace"):
    user_input = listen()
    if user_input:
        st.text_input("Your question:", value=user_input, key="voice_input")

# Text Input
user_input = st.text_input("💬 Ask Ace a question about your credit repair journey:")

# Custom Response as Ace
with st.expander("✍️ Type your own response as Ace"):
    custom_response = st.text_area("Respond as Ace:")
    if st.button("Send as Ace"):
        st.success(f"**Ace's Answer:**\n\n{custom_response}")
        speak(custom_response)
        save_convo_log("[Custom Response]", custom_response)

# Main Bot Response
if user_input:
    with st.spinner("Ace is thinking..."):
        ace_response = query_ollama(user_input)
        st.write(f"**Ace's Answer:**\n\n{ace_response}")
        speak(ace_response)
        save_convo_log(user_input, ace_response)

# ---------- DOCUMENT UPLOAD ----------
st.header("📎 Upload Your Documents")
uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "docx", "txt", "jpg", "png"])
if uploaded_file:
    save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ {uploaded_file.name} uploaded successfully!")

# ---------- FREQUENTLY ASKED QUESTIONS ----------
st.header("📚 Frequently Asked Questions")
st.markdown("""
**Q: How long does credit repair take?**  
A: Most credit repair programs take 3–6 months, depending on your situation.

**Q: How can I track the status of my disputes?**  
A: You can check your portal for updates, or message Ace for a quick update.

**Q: I need help uploading my credit reports. Can you help?**  
A: Absolutely! Just use the uploader in your portal, or message me for a walkthrough.

**Q: What if I miss a billing payment?**  
A: No worries! Let us know and we’ll help you reschedule or update your info.

**Q: How do I contact Valor?**  
A: I’ll escalate your request or provide Valor’s contact form right away.
""")


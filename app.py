import streamlit as st
import requests

st.set_page_config(page_title="Ace – Customer Service Rep", page_icon="🤖")

st.markdown("### 👋 Meet Ace – Your Friendly Customer Service Rep for Your Credit Repair Business")
st.markdown("""
**Role Title:** Customer Support Specialist  
**Name:** Ace  
**Mission:** To assist clients with care, clarity, and consistency—whether they have questions about services, want to check the status of a dispute, or need a little extra motivation along their credit journey.

---

🎯 **Ace’s Top Responsibilities**

**Client Communication**  
- Respond to customer inquiries via chat, email, or portal  
- Help new clients understand the credit repair process  
- Explain steps, timelines, and expectations clearly  

**Account Support**  
- Provide updates on disputes, investigations, and progress  
- Guide clients on how to pull credit reports and upload documents  
- Assist with billing, appointments, or portal access  

**Client Education**  
- Share tips on how to boost credit scores  
- Offer helpful reminders and positive reinforcement  
- Direct clients to free tools and financial resources  

**Problem Solving**  
- Listen to client concerns and offer calm, helpful solutions  
- Escalate complex issues to Valor (the CEO)  
- Keep records of conversations and resolutions  

---

🛠️ **Ace’s Toolbox**  
- CRM or portal system for tracking client interactions  
- Credit education handouts and FAQs  
- Sample scripts for email/text responses  
- Customer feedback forms  
- Quick access to dispute timelines and service updates  

---

💬 **Motto:**  
**Ace is here to keep it smooth, supportive, and stress-free—every step of your credit repair journey!**
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Function to query Ollama (gemma:2b)
def query_ollama(prompt):
    full_prompt = f"You are Ace, a professional and friendly customer service representative for a credit repair business. Answer this like you're a real CSR helping someone interested in our services. If it's a business or leadership question, kindly refer them to Valor.\n\nQuestion: {prompt}\n\nAnswer:"
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": full_prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return "Sorry, I'm having trouble reaching Ace right now."

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    with st.spinner("Ace is typing..."):
        response = query_ollama(user_input)
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})


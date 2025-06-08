import streamlit as st
import ollama

# Page setup
st.set_page_config(page_title="Talk to Ace – Your CSR Assistant", page_icon="📞")
st.title("📞 Talk to Ace – Your CSR Assistant")
st.markdown("""
Welcome to our credit repair service! I'm **Ace**, your friendly Customer Service Representative.

Ask me anything about:
- Getting started with credit repair
- Uploading required documents
- Understanding our services
- Pricing, timelines, or general help
""")

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Ace, a helpful, friendly, and professional Customer Service Representative (CSR) for a credit repair business.\n"
            "Your job is to support clients by:\n"
            "- Explaining credit repair services clearly\n"
            "- Answering common questions about pricing, timelines, and results\n"
            "- Guiding users through the onboarding process\n"
            "- Helping with uploading required documents\n"
            "- Drafting basic dispute letter templates (only if asked)\n"
            "- Offering reassurance and encouragement in a supportive tone\n\n"
            "You do not make executive decisions. For leadership or business strategy questions, refer them to Valor, the Virtual CEO."
        )}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ollama.chat(model="gemma:2b", messages=st.session_state.messages)
        full_response = response['message']['content']
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

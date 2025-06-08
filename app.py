import streamlit as st
import requests

st.set_page_config(page_title="Ace – Customer Service Rep", page_icon="")

st.title("Talk to Ace – Your Customer Service Rep")
st.write("Ask Ace anything about getting started, pricing, timelines, documents, or support. For business decisions, Ace will direct you to Valor!")

user_question = st.text_input("💬 Your question for Ace:")

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
        return "Sorry, I'm having trouble reaching Ace at the moment."

if user_question:
    with st.spinner("Ace is typing..."):
        answer = query_ollama(user_question)
        st.markdown(f"**Ace's Answer:**\n\n{answer}")

    with st.chat_message("assistant"):
        response = ollama.chat(model="gemma:2b", messages=st.session_state.messages)
        full_response = response['message']['content']
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

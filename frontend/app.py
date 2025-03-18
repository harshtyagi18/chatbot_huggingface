import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("💬 AI Support Chatbot with Sentiment Analysis")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    role = "🧑‍💻 You" if msg['role'] == "User" else "🤖 AI"
    st.write(f"{role}: {msg['text']}")

user_input = st.text_input("You: ")

if st.button("Send"):
    if user_input:
        response = requests.post(f"{API_URL}/chat/", params={"user_input": user_input})
        data = response.json()

        bot_response = data.get("response", "No response")
        sentiment = data.get("sentiment", "Unknown")

        st.session_state["messages"].append({"role": "User", "text": user_input})
        st.session_state["messages"].append({"role": "Bot", "text": f"{bot_response} (Sentiment: {sentiment})"})

        st.write(f"🤖 AI: {bot_response} (Sentiment: {sentiment})")

if st.button("Show Chat History"):
    history = requests.get(f"{API_URL}/history/").json()
    for chat in history:
        st.write(f"🧑‍💻 You: {chat['user']}")
        st.write(f"🤖 AI: {chat['bot']} (Sentiment: {chat['sentiment']})")

import streamlit as st
import google.generativeai as genai
import os

def app():
    st.title("🤖 Fitness Chatbot")

    # Securely load Gemini API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❗ GEMINI_API_KEY environment variable not set.")
        return

    # Configure Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("Ask your fitness question (e.g., workout, diet, recovery):", "")

    # Send button
    if st.button("Send"):
        if user_input.strip() != "":
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("Thinking..."):
                try:
                    response = model.generate_content(user_input)
                    bot_reply = response.text.strip()
                except Exception as e:
                    bot_reply = f"❗ Error: {str(e)}"

            st.session_state.chat_history.append({"role": "bot", "content": bot_reply})

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**CoachBot:** {chat['content']}")

    # Option to clear chat
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

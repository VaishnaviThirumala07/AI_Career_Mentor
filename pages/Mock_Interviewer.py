import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the model you found successfully in your test_brain.py
# If this preview model fails, switch to 'gemini-1.5-flash'
MODEL_NAME = 'gemini-2.5-flash-lite-preview-09-2025' 
model = genai.GenerativeModel(MODEL_NAME)

st.title("🤖 AI Mock Interviewer")

# 2. Session State (The AI's Memory)
# This keeps the chat history alive even when you click buttons
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Sidebar Settings
with st.sidebar:
    st.header("Interview Settings")
    role = st.selectbox("Target Role", ["Python Developer", "Data Scientist", "AI Engineer", "Product Manager"])
    topic = st.selectbox("Focus Topic", ["Technical Skills", "Behavioral (HR)", "System Design"])
    difficulty = st.select_slider("Difficulty", options=["Junior", "Mid-Level", "Senior"])
    
    if st.button("Start New Interview"):
        # Reset memory
        st.session_state.messages = []
        # Initial System Prompt to set the persona
        initial_prompt = f"""
        You are an expert Technical Interviewer for a {difficulty} {role} position. 
        Focus heavily on {topic}.
        
        Rules:
        1. Ask only ONE question at a time.
        2. Wait for the user's response.
        3. After the user answers, provide brief feedback (correct/incorrect) and then ask the NEXT question.
        4. Keep the tone professional but encouraging.
        
        Start by introducing yourself and asking the first question.
        """
        # Send first message to AI to kickstart the chat
        response = model.generate_content(initial_prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. User Input Handling
if user_answer := st.chat_input("Type your answer here..."):
    # A. Display User Message
    with st.chat_message("user"):
        st.write(user_answer)
    st.session_state.messages.append({"role": "user", "content": user_answer})

    # B. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Construct the full chat history for context
            # We join previous messages so the AI knows what's going on
            chat_history = [
                {"role": "user" if msg["role"] == "user" else "model", "parts": msg["content"]}
                for msg in st.session_state.messages
            ]
            
            # Start a chat session with history
            chat = model.start_chat(history=chat_history[:-1]) # Load all except last (which is the new input)
            response = chat.send_message(user_answer)
            
            st.write(response.text)
            
    # C. Save AI Response to memory
    st.session_state.messages.append({"role": "assistant", "content": response.text})